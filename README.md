# 🟢 GitHub Green Graph

> Fill your GitHub contribution graph with backdated commits — make it green!

A Python script that creates empty commits with backdated timestamps across your repositories, making your GitHub profile look active and productive.

![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![MIT License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

## 🚀 Features

- ✅ **Auto-detect repos** — Scans all your public & private repositories
- ✅ **Realistic distribution** — Random times between 9am-9pm
- ✅ **Configurable coverage** — Choose what percentage of days to fill (default: 78%)
- ✅ **Multiple repos** — Spreads commits across repos for natural look
- ✅ **Safe & reversible** — Only creates empty commits (no code changes)
- ✅ **Reproducible** — Uses seeds for consistent results
- ✅ **Custom messages** — Choose your own commit messages
- ✅ **Dry run mode** — Preview before pushing

---

## 📦 Installation

No dependencies required! Just Python 3.7+ and `curl`.

```bash
git clone https://github.com/fikrado2/github-green-graph.git
cd github-green-graph
python green_graph.py --help
```

---

## 🔧 Usage

### Basic Usage

```bash
python green_graph.py --token YOUR_GITHUB_TOKEN
```

This will:
1. Fetch all your repositories
2. Calculate days from June 2025 to today
3. Create commits on ~78% of days
4. Push everything to GitHub

### Custom Date Range

```bash
python green_graph.py --token ghp_xxxx \
  --start 2024-01-01 \
  --end 2024-12-31
```

### Specific Repositories

```bash
python green_graph.py --token ghp_xxxx \
  --repos user/repo1 user/repo2 user/repo3
```

### Higher Coverage (90%)

```bash
python green_graph.py --token ghp_xxxx \
  --coverage 0.9
```

### Custom Commit Messages

```bash
python green_graph.py --token ghp_xxxx \
  --messages "chore: update" "fix: typo" "feat: add" "refactor: cleanup"
```

### Dry Run (Preview Only)

```bash
python green_graph.py --token ghp_xxxx \
  --dry-run
```

---

## ⚙️ Options

| Option | Description | Default |
|--------|-------------|---------|
| `--token` | GitHub personal access token (required) | — |
| `--start` | Start date (YYYY-MM-DD) | `2025-06-01` |
| `--end` | End date (YYYY-MM-DD) | Today |
| `--coverage` | Fraction of days to fill (0.0-1.0) | `0.78` |
| `--repos` | Specific repos to use | Auto-detect all |
| `--name` | Git author name | `fikrado2` |
| `--email` | Git author email | `fikrado1@gmail.com` |
| `--seed` | Random seed | `42` |
| `--dry-run` | Show plan without pushing | `False` |
| `--messages` | Custom commit messages | Built-in list |

---

## 🔑 Getting a GitHub Token

1. Go to [GitHub Settings → Developer settings → Personal access tokens](https://github.com/settings/tokens)
2. Click **"Generate new token (classic)"**
3. Select scopes:
   - ✅ `repo` (full repository access)
   - ✅ `workflow` (optional, for Actions)
4. Copy the token (you won't see it again!)

---

## 📊 How It Works

```
┌─────────────────────────────────────────────────────┐
│  1. Fetch all repos via GitHub API                  │
│  2. Calculate which days get commits (78% random)   │
│  3. Clone each repo                                 │
│  4. Create empty commits with backdated timestamps  │
│     using GIT_AUTHOR_DATE & GIT_COMMITTER_DATE      │
│  5. Push to GitHub                                  │
│  6. GitHub's contribution graph shows green squares  │
└─────────────────────────────────────────────────────┘
```

The script uses Git's official environment variables to set commit dates:

```bash
GIT_AUTHOR_DATE="2025-07-15T14:32:07"
GIT_COMMITTER_DATE="2025-07-15T14:32:07"
git commit --allow-empty -m "update readme"
```

---

## ⚠️ Important Notes

- **Empty commits only** — No code changes are made
- **Your repos** — Only works on repositories you own/have push access to
- **Reversible** — You can reset with `git rebase` or delete the repo
- **GitHub's policy** — This is for fun/personal use. Don't misrepresent contributions professionally
- **Rate limits** — GitHub API has limits; the script handles this gracefully

---

## 🎯 Example Output

```
🟢 GitHub Green Graph
==================================================
  Token:    ✅ Set
  Range:    2025-06-01 → 2026-09-11
  Coverage: 78%
  Seed:     42
  Author:   fikrado2 <fikrado1@gmail.com>

📅 Total days: 468
📅 Active days: 357

🔍 Fetching your repositories...
  Found 8 repositories

📦 Cloning user/repo1...
  📝 Adding 45 days to user/repo1...
  🚀 Pushing user/repo1 (45 commits)...
  ✅ Pushed successfully!

📦 Cloning user/repo2...
  📝 Adding 50 days to user/repo2...
  🚀 Pushing user/repo2 (50 commits)...
  ✅ Pushed successfully!

==================================================
🎉 DONE! Made 357 commits across 357 days
   Check: https://github.com/fikrado2
```

---

## 🤝 Contributing

Contributions welcome! Feel free to open issues or PRs.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🔗 Links

- **GitHub:** [github.com/fikrado2](https://github.com/fikrado2)
- **Website:** [fikrado2.github.io](https://fikrado2.github.io)
- **Twitter:** [@fikrado1](https://twitter.com/fikrado1)

---

## 🏷️ Tags

`github` `green-graph` `contributions` `python` `automation` `git` `backdate` `profile` `commits` `script` `tool` `cli`

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/fikrado2">Yahye Abdirahman (fikrado2)</a>
</p>
