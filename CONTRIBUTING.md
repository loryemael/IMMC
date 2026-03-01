# CONTRIBUTING

This document explains exactly how to contribute to this repository (`IMMC`) if you already have write access.

## Repository Basics

- Remote URL: `https://github.com/loryemael/IMMC.git`
- Default branch: `main`
- Important: this repo currently has both `main` and `master` history; daily work must target `main`.

## 1. One-Time Setup

Configure your Git identity once:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
```

## 2. First Time Joining This Repo

```bash
git clone https://github.com/loryemael/IMMC.git
cd IMMC
git checkout main
git pull origin main
```

Verify:

```bash
git branch -a
git remote -v
```

## 3. Standard Daily Workflow (Required)

Do not develop directly on `main`.

```bash
# sync main first
git checkout main
git pull origin main

# create your feature branch
git checkout -b feat/<topic>-<yourname>
```

After editing files:

```bash
git status
git add <files>
git commit -m "feat: short clear message"
git push -u origin feat/<topic>-<yourname>
```

Then open GitHub and create a Pull Request:

- base branch: `main`
- compare branch: `feat/<topic>-<yourname>`

## 4. Commit Message Format

Use `type: message`.

- `feat`: new feature
- `fix`: bug fix
- `docs`: documentation changes
- `refactor`: code cleanup without behavior change
- `chore`: tooling or maintenance

Examples:

- `docs: expand onboarding notebook`
- `fix: correct branch setup instructions`

## 5. Keep Your Branch Up to Date

If your branch is behind `main`:

```bash
git checkout main
git pull origin main
git checkout feat/<topic>-<yourname>
git rebase main
git push --force-with-lease
```

## 6. Common Problems

### A) `nothing to commit, working tree clean`

No staged changes exist. Check with:

```bash
git status
git diff
```

### B) `rejected (non-fast-forward)`

Remote has new commits:

```bash
git pull --rebase origin main
git push
```

### C) Merge or rebase conflict

1. Open conflicted files and keep correct content.
2. Remove conflict markers.
3. Stage fixed files:

```bash
git add <conflicted-files>
```

4. Continue:

```bash
git rebase --continue   # if rebasing
# or
git commit              # if merging
```

5. Push again.

## 7. After PR Is Merged

Clean local and remote branch:

```bash
git checkout main
git pull origin main
git branch -d feat/<topic>-<yourname>
git push origin --delete feat/<topic>-<yourname>
```

## 8. Collaboration Rules For This Repo

- Always open PR to `main`.
- Keep commits focused and small.
- Do not include unrelated local files in your commit.
- Before pushing, run `git status` and confirm only intended files are staged.

## 9. Quick Copy-Paste Flow

```bash
git checkout main
git pull origin main
git checkout -b feat/<topic>-<yourname>
# edit files
git add .
git commit -m "feat: <what changed>"
git push -u origin feat/<topic>-<yourname>
# open PR to main on GitHub
```
