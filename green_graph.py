#!/usr/bin/env python3
"""
🟢 GitHub Green Graph — Fill your GitHub contribution graph with backdated commits.

Makes your contribution graph look active by creating empty commits with
backdated timestamps across your repositories. Uses GitHub's official
GIT_AUTHOR_DATE and GIT_COMMITTER_DATE environment variables.

Usage:
    python green_graph.py --token YOUR_GITHUB_TOKEN
    python green_graph.py --token YOUR_GITHUB_TOKEN --start 2025-01-01 --end 2025-12-31
    python green_graph.py --token YOUR_GITHUB_TOKEN --repos user/repo1 user/repo2
    python green_graph.py --token YOUR_GITHUB_TOKEN --coverage 0.9 --dry-run

Author: Yahye Abdirahman (fikrado2)
License: MIT
"""

import subprocess
import os
import sys
import random
import datetime
import json
import argparse
import time


# ─── Default commit messages ────────────────────────────────────────────────
DEFAULT_MESSAGES = [
    "update readme",
    "fix typo",
    "refactor code",
    "add feature",
    "update dependencies",
    "improve docs",
    "bug fix",
    "optimize performance",
    "add tests",
    "clean up imports",
    "update config",
    "add comments",
    "minor fixes",
    "style update",
    "version bump",
    "fix lint",
    "improve error handling",
    "add logging",
    "update changelog",
    "remove dead code",
]


# ─── Helper: run shell commands ─────────────────────────────────────────────
def run(cmd, cwd=None, env_extra=None, timeout=300):
    """Run a shell command and return (stdout, stderr, returncode)."""
    env = os.environ.copy()
    if env_extra:
        env.update(env_extra)
    result = subprocess.run(
        cmd, shell=True, cwd=cwd, env=env,
        capture_output=True, text=True, timeout=timeout
    )
    return result.stdout.strip(), result.stderr.strip(), result.returncode


# ─── Fetch user's repos from GitHub API ─────────────────────────────────────
def fetch_repos(token):
    """Fetch all repos (public + private) for the authenticated user."""
    repos = []
    page = 1
    while True:
        stdout, stderr, rc = run(
            f'curl -s -H "Authorization: token {token}" '
            f'"https://api.github.com/user/repos?per_page=100&page={type}&type=all"'
        )
        if rc != 0:
            print(f"  Failed to fetch repos: {stderr}")
            break
        data = json.loads(stdout) if stdout else []
        if not data or not isinstance(data, list):
            break
        for r in data:
            repos.append({
                "full_name": r["full_name"],
                "default_branch": r["default_branch"],
                "visibility": r["visibility"],
            })
        if len(data) < 100:
            break
        page += 1
    return repos


# ─── Calculate active days ──────────────────────────────────────────────────
def calculate_active_days(start_date, end_date, coverage=0.78, seed=42):
    """Generate the list of days that will get commits."""
    all_days = []
    d = start_date
    while d <= end_date:
        all_days.append(d)
        d += datetime.timedelta(days=1)

    rng = random.Random(seed)
    active_days = [day for day in all_days if rng.random() < coverage]
    return all_days, active_days


# ─── Get existing commit dates from a local repo ────────────────────────────
def get_existing_dates(repo_dir):
    """Read all commit dates from a cloned repo since 2025-06-01."""
    dates = set()
    stdout, _, _ = run(
        "git log --format='%ai' --since='2025-06-01'", cwd=repo_dir, timeout=30
    )
    for line in stdout.splitlines():
        try:
            dt = datetime.datetime.strptime(line[:10], "%Y-%m-%d").date()
            dates.add(dt)
        except ValueError:
            pass
    return dates


# ─── Create backdated commits and push ──────────────────────────────────────
def process_repo(repo_name, token, repo_days, messages, user_name, user_email):
    """Clone a repo, create empty commits with backdated dates, and push."""
    repo_url = f"https://{token}@github.com/{repo_name}.git"
    repo_dir = f"/tmp/green-graph/{repo_name.replace('/', '_')}"
    lock_file = os.path.join(repo_dir, ".git", "index.lock")

    # Clone
    print(f"\n📦 Cloning {repo_name}...")
    if os.path.exists(repo_dir):
        run("git pull --quiet", cwd=repo_dir, timeout=120)
    else:
        os.makedirs(os.path.dirname(repo_dir), exist_ok=True)
        _, err, rc = run(f"git clone --quiet {repo_url} {repo_dir}", timeout=300)
        if rc != 0:
            print(f"  ❌ Clone failed: {err}")
            return 0

    # Remove stale lock files
    if os.path.exists(lock_file):
        os.remove(lock_file)

    # Check existing dates
    existing = get_existing_dates(repo_dir)
    days_to_do = [d for d in repo_days if d not in existing]

    if not days_to_do:
        print(f"  ✅ All days already covered in {repo_name}")
        return 0

    print(f"  📝 Adding {len(days_to_do)} days to {repo_name}...")
    success = 0

    for day in days_to_do:
        # Remove lock file before each commit (paranoid but safe)
        if os.path.exists(lock_file):
            os.remove(lock_file)

        # Random time between 9am and 9pm
        hour = random.randint(9, 21)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        dt_str = f"{day.isoformat()}T{hour:02d}:{minute:02d}:{second:02d}"
        msg = random.choice(messages)

        env = {
            "GIT_AUTHOR_DATE": dt_str,
            "GIT_COMMITTER_DATE": dt_str,
            "GIT_AUTHOR_NAME": user_name,
            "GIT_COMMITTER_NAME": user_name,
            "GIT_AUTHOR_EMAIL": user_email,
            "GIT_COMMITTER_EMAIL": user_email,
        }

        _, stderr, rc = run(
            f'git commit --allow-empty -m "{msg}"',
            cwd=repo_dir, env_extra=env, timeout=30
        )

        if rc != 0:
            print(f"  ⚠️  Commit failed for {day}: {stderr[:80]}")
            continue
        success += 1

    # Push
    print(f"  🚀 Pushing {repo_name} ({success} commits)...")
    _, err, rc = run("git push --quiet origin HEAD", cwd=repo_dir, timeout=300)
    if rc != 0:
        print(f"  ❌ Push failed: {err}")
    else:
        print(f"  ✅ Pushed successfully!")

    return success


# ─── Main ────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="🟢 GitHub Green Graph — Fill your contribution graph!",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python green_graph.py --token ghp_xxxx
  python green_graph.py --token ghp_xxxx --start 2025-01-01 --end 2025-12-31
  python green_graph.py --token ghp_xxxx --coverage 0.9
  python green_graph.py --token ghp_xxxx --repos user/repo1 user/repo2
  python green_graph.py --token ghp_xxxx --dry-run
        """
    )
    parser.add_argument("--token", required=True, help="GitHub personal access token")
    parser.add_argument("--start", default="2025-06-01", help="Start date (default: 2025-06-01)")
    parser.add_argument("--end", default=None, help="End date (default: today)")
    parser.add_argument("--coverage", type=float, default=0.78, help="Fraction of days to fill (0.0-1.0, default: 0.78)")
    parser.add_argument("--repos", nargs="+", help="Specific repos to use (default: auto-detect all)")
    parser.add_argument("--name", default="fikrado2", help="Git author name (default: fikrado2)")
    parser.add_argument("--email", default="fikrado1@gmail.com", help="Git author email")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility (default: 42)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without pushing")
    parser.add_argument("--messages", nargs="+", help="Custom commit messages")

    args = parser.parse_args()

    start_date = datetime.date.fromisoformat(args.start)
    end_date = datetime.date.fromisoformat(args.end) if args.end else datetime.date.today()
    messages = args.messages if args.messages else DEFAULT_MESSAGES

    print("🟢 GitHub Green Graph")
    print("=" * 50)
    print(f"  Token:    {'✅ Set' if args.token else '❌ Missing'}")
    print(f"  Range:    {start_date} → {end_date}")
    print(f"  Coverage: {args.coverage * 100:.0f}%")
    print(f"  Seed:     {args.seed}")
    print(f"  Author:   {args.name} <{args.email}>")
    print()

    # Calculate days
    all_days, active_days = calculate_active_days(start_date, end_date, args.coverage, args.seed)
    print(f"📅 Total days: {len(all_days)}")
    print(f"📅 Active days: {len(active_days)}")
    print()

    # Get repos
    if args.repos:
        repos = [{"full_name": r, "default_branch": "main"} for r in args.repos]
    else:
        print("🔍 Fetching your repositories...")
        repos = fetch_repos(args.token)
        if not repos:
            print("❌ No repositories found!")
            sys.exit(1)
        print(f"  Found {len(repos)} repositories")

    # Distribute days across repos
    repo_weights = [max(1, len(repos) - i) for i in range(len(repos))]
    total_weight = sum(repo_weights)

    total_commits = 0
    covered_days = set()

    for i, repo in enumerate(repos):
        repo_name = repo["full_name"]
        weight = repo_weights[i] / total_weight
        share = max(1, int(len(active_days) * weight))

        # Filter out already-covered days
        repo_days = [d for d in active_days if d not in covered_days][:share]

        if args.dry_run:
            print(f"\n🔍 [DRY RUN] Would add {len(repo_days)} days to {repo_name}")
            covered_days.update(repo_days)
            continue

        commits = process_repo(
            repo_name, args.token, repo_days, messages, args.name, args.email
        )
        total_commits += commits
        covered_days.update(repo_days[:commits])

    # Summary
    print("\n" + "=" * 50)
    if args.dry_run:
        print(f"🔍 [DRY RUN] Would make {len(active_days)} commits across {len(repos)} repos")
    else:
        print(f"🎉 DONE! Made {total_commits} commits across {len(covered_days)} days")
        print(f"   Check: https://github.com/{args.name}")


if __name__ == "__main__":
    main()
