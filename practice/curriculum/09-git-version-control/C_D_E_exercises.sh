#!/bin/bash
# =============================================================================
# Section 9 — Git: Intermediate (C1-C8) + Debug (D1-D5) + Production (E1)
# Guide: docs/curriculum/09-git-version-control.md
# =============================================================================

# --- INTERMEDIATE ---

# Exercise 9.C.1 — Interactive Rebase
# TODO: Make 4 messy commits, then: git rebase -i HEAD~4
# Squash, fixup, reword, reorder

# Exercise 9.C.2 — Git Bisect
# TODO: git bisect start
# TODO: git bisect bad (current) / git bisect good (old)
# TODO: Automate: git bisect run pytest tests/

# Exercise 9.C.3 — Git Hooks
# TODO: Create .git/hooks/pre-commit that runs ruff check
# chmod +x .git/hooks/pre-commit

# Exercise 9.C.4 — Cherry-Pick
# TODO: git cherry-pick <commit-hash>

# Exercise 9.C.5 — Git Worktrees
# TODO: git worktree add ../hotfix-branch hotfix/fix

# Exercise 9.C.6 — Advanced .gitignore
# TODO: Create patterns with negation (!.env.example)

# Exercise 9.C.7 — Rewriting History (filter-repo)
# TODO: pip install git-filter-repo
# TODO: git filter-repo --path secrets.env --invert-paths

# Exercise 9.C.8 — Signed Commits
# TODO: gpg --gen-key
# TODO: git config --global commit.gpgsign true

# --- DEBUG LAB ---

# Exercise 9.D.1 — Debug: Detached HEAD State
# TODO: git checkout <hash>  → create branch to save work

# Exercise 9.D.2 — Debug: Lost Commits After Reset
# TODO: git reflog → git reset --hard HEAD@{n}

# Exercise 9.D.3 — Debug: Merge Went Wrong
# TODO: git revert -m 1 <merge-commit>

# Exercise 9.D.4 — Debug: Diverged Branches
# TODO: git pull --rebase

# Exercise 9.D.5 — Debug: Large File Committed
# TODO: git filter-repo or BFG Repo Cleaner

# --- PRODUCTION ---

# Exercise 9.E.1 — Team Git Workflow
# TODO: Create repo with main+develop
# TODO: Feature branches, PRs, squash-merge, tags, hotfix
