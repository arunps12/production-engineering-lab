# SECTION 9 — GIT & VERSION CONTROL (DEEP DIVE)

---

## PART A — CONCEPT EXPLANATION

### Why Version Control is a Core DevOps Skill

Every production system relies on version control. It's not just "saving files" — it's the backbone of:
- **Collaboration**: Multiple engineers working on the same codebase without conflicts
- **Auditability**: Every change has a who, what, when, and why
- **Rollback**: Undo any change, any time
- **CI/CD**: Pipelines trigger from git events (push, tag, PR)
- **Infrastructure as Code**: Terraform, Kubernetes manifests — all versioned in git

### Git Internals: How It Actually Works

Git is a **content-addressable filesystem**. Every object (blob, tree, commit) is stored by its SHA-1 hash.

```
Working Directory → git add → Staging Area → git commit → Repository
     (files)                    (index)                   (.git/objects)
```

**Three areas:**
1. **Working directory** — Your actual files
2. **Staging area (index)** — What will go into the next commit
3. **Repository (.git)** — The permanent history

**Object types:**
- **Blob** — File contents (no filename!)
- **Tree** — Directory listing (maps names → blobs/trees)
- **Commit** — Snapshot pointer + metadata (author, message, parent)
- **Tag** — Named pointer to a commit

### Branching Model

A branch is just a pointer to a commit. Creating a branch is O(1) — it writes 41 bytes (SHA + newline).

```
main:     A → B → C
                    \
feature:             D → E
```

**HEAD** points to the current branch, which points to the latest commit.

### Merge vs Rebase

**Merge** creates a new merge commit with two parents:
```
main:     A → B → C --------→ M
                    \        /
feature:             D → E -/
```

**Rebase** replays commits on top of the target:
```
main:     A → B → C
                    \
feature:             D' → E'    (rebased — new commit hashes!)
```

**Rule of thumb**: Rebase for local cleanup, merge for shared branches.

### The Reflog — Your Safety Net

Git never truly deletes commits. The reflog records every HEAD movement:
```bash
git reflog                    # See all HEAD positions
git reset --hard HEAD@{3}    # Go back to 3 moves ago
```

Even after a bad rebase or reset, you can recover via reflog (for ~90 days).

### Branching Strategies

**Git Flow:**
```
main ──────────────────────────────
  └── develop ─────────────────────
       ├── feature/login ──────┘
       ├── feature/payments ───┘
       └── release/1.0 ───────┘
```

**Trunk-Based Development** (preferred for CI/CD):
```
main ──────────────────────────────
  ├── short-feature-1 ─┘ (merged in <1 day)
  ├── short-feature-2 ─┘
  └── short-feature-3 ─┘
```

### Common Beginner Misunderstandings

1. **"git pull is safe"** — `git pull` = `git fetch` + `git merge`. It can create unexpected merge commits. Use `git pull --rebase` or fetch+rebase manually.
2. **"I can't undo a commit"** — You almost always can: `git revert`, `git reset`, `git reflog`.
3. **"Branches are expensive"** — Branches are 41 bytes. Create them liberally.
4. **"Force push is evil"** — Force push to YOUR feature branch is fine. Force push to main/shared branches is destructive.
5. **"Merge conflicts mean something is wrong"** — They're normal. They mean two people changed the same lines. Learn to resolve them calmly.

---

## PART B — BEGINNER PRACTICE

### Exercise 9.B.1 — Initialize and Make First Commits

Create a new repository and practice the basic workflow:
```bash
mkdir git-practice && cd git-practice
git init
echo "# Git Practice" > README.md
git add README.md
git commit -m "Initial commit"
```

Now add more files, see status, diff:
```bash
echo "hello" > file1.txt
echo "world" > file2.txt
git status
git add file1.txt
git status              # file1 staged, file2 untracked
git diff                # Shows unstaged changes
git diff --staged       # Shows staged changes
git commit -m "Add file1"
git add file2.txt && git commit -m "Add file2"
git log --oneline
```

### Exercise 9.B.2 — Understand the Three Areas

Demonstrate working directory vs staging vs repository:
```bash
echo "line 1" > test.txt
git add test.txt                    # Now in staging
echo "line 2" >> test.txt           # Modified in working dir but NOT staged
git diff                            # Shows "line 2" (unstaged)
git diff --staged                   # Shows "line 1" (staged)
git commit -m "Add test"            # Only commits "line 1"!
cat test.txt                        # Still has both lines
git diff                            # Shows "line 2" still unstaged
```

### Exercise 9.B.3 — Branching Basics

```bash
git branch feature-login            # Create branch
git checkout feature-login          # Switch to it
# OR: git checkout -b feature-login  (create + switch)
echo "login code" > login.py
git add login.py && git commit -m "Add login"
git checkout main
ls                                  # login.py is gone!
git merge feature-login             # Bring it back
ls                                  # login.py is here
git branch -d feature-login         # Clean up
```

### Exercise 9.B.4 — Resolve a Merge Conflict

Create a conflict intentionally:
```bash
git checkout -b branch-a
echo "version A" > config.txt
git add config.txt && git commit -m "Branch A config"

git checkout main
echo "version main" > config.txt
git add config.txt && git commit -m "Main config"

git merge branch-a                  # CONFLICT!
cat config.txt                      # See conflict markers
# Edit file to resolve, then:
git add config.txt
git commit -m "Resolve merge conflict"
```

### Exercise 9.B.5 — Git Log and History

Explore log formats:
```bash
git log                             # Full log
git log --oneline                   # Compact
git log --oneline --graph --all     # Visual branch graph
git log --author="Your Name"        # Filter by author
git log --since="2 days ago"        # Time-based filter
git log -- filename.py              # History for one file
git show <commit-hash>              # Show specific commit details
```

### Exercise 9.B.6 — Undoing Things

Practice different undo methods:
```bash
# Unstage a file:
git reset HEAD file.txt

# Discard working directory changes:
git checkout -- file.txt

# Amend the last commit message:
git commit --amend -m "Better message"

# Undo a commit (keeping changes):
git reset --soft HEAD~1

# Undo a commit (discarding changes):
git reset --hard HEAD~1

# Create a reverse commit (safe for shared branches):
git revert HEAD
```

### Exercise 9.B.7 — Git Stash

```bash
# You're working on something, need to switch branches:
echo "work in progress" > wip.txt
git stash                           # Save changes
git stash list                      # See stashes
git checkout other-branch
# ... do other work ...
git checkout main
git stash pop                       # Restore changes
```

### Exercise 9.B.8 — Tagging Releases

```bash
git tag v1.0.0                      # Lightweight tag
git tag -a v1.1.0 -m "Release 1.1" # Annotated tag (preferred)
git tag                             # List tags
git show v1.1.0                     # Show tag details
git push origin v1.1.0              # Push specific tag
git push origin --tags              # Push all tags
```

---

## PART C — INTERMEDIATE PRACTICE

### Exercise 9.C.1 — Interactive Rebase

Clean up messy commit history before merging:
```bash
# Make several messy commits
echo "a" > a.txt && git add . && git commit -m "wip"
echo "b" > b.txt && git add . && git commit -m "more wip"
echo "c" > c.txt && git add . && git commit -m "fix typo"
echo "d" > d.txt && git add . && git commit -m "actually fix it"

# Now clean up last 4 commits:
git rebase -i HEAD~4
# Change 'pick' to 'squash' or 'fixup' to combine
# Change 'pick' to 'reword' to rename
# Reorder lines to reorder commits
```

### Exercise 9.C.2 — Git Bisect (Find Bug-Introducing Commit)

```bash
# Suppose something broke between v1.0 and now
git bisect start
git bisect bad                      # Current commit is broken
git bisect good v1.0                # v1.0 was working
# Git checks out middle commit — test it
git bisect good                     # or: git bisect bad
# Repeat until git finds the exact commit
git bisect reset                    # Done, go back to HEAD
```

Automate with a script:
```bash
git bisect start HEAD v1.0
git bisect run python -m pytest tests/test_feature.py
```

### Exercise 9.C.3 — Git Hooks

Create a pre-commit hook that runs linting:
```bash
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
echo "Running pre-commit checks..."
ruff check . || { echo "Linting failed!"; exit 1; }
ruff format --check . || { echo "Formatting failed!"; exit 1; }
echo "All checks passed!"
EOF
chmod +x .git/hooks/pre-commit
```

Now any `git commit` will run linting first. If it fails, the commit is rejected.

### Exercise 9.C.4 — Cherry-Pick

Apply specific commits from one branch to another:
```bash
git log --oneline feature-branch    # Find the commit hash
git checkout main
git cherry-pick abc1234             # Apply that specific commit
```

### Exercise 9.C.5 — Git Worktrees

Work on multiple branches simultaneously without stashing:
```bash
git worktree add ../hotfix-branch hotfix/critical-fix
cd ../hotfix-branch
# Work on hotfix while main branch stays untouched
git worktree remove ../hotfix-branch    # Clean up
```

### Exercise 9.C.6 — Advanced .gitignore Patterns

```gitignore
# Ignore all .env files
.env
.env.*

# But NOT .env.example
!.env.example

# Ignore build outputs
dist/
build/
*.egg-info/

# Ignore OS files
.DS_Store
Thumbs.db

# Ignore IDE files but keep shared settings
.idea/
.vscode/*
!.vscode/settings.json
!.vscode/extensions.json
```

### Exercise 9.C.7 — Rewriting History with filter-branch/filter-repo

Remove a file from ALL history (e.g., accidentally committed secrets):
```bash
# Using git-filter-repo (recommended over filter-branch):
pip install git-filter-repo
git filter-repo --path secrets.env --invert-paths
```

**WARNING**: This rewrites ALL commit hashes. All collaborators must re-clone.

### Exercise 9.C.8 — Signed Commits

```bash
# Set up GPG signing
gpg --gen-key
git config --global user.signingkey <YOUR_KEY_ID>
git config --global commit.gpgsign true

# Make a signed commit
git commit -S -m "Signed commit"

# Verify signatures
git log --show-signature
```

---

## PART D — ADVANCED DEBUG LAB

### Exercise 9.D.1 — Debug: Detached HEAD State

You accidentally checked out a commit hash instead of a branch:
```bash
git checkout abc1234    # Detached HEAD!
# Any commits here will be "orphaned" when you switch branches
```
**Task**: Recover. Create a branch from detached HEAD, or find the commit in reflog.

### Exercise 9.D.2 — Debug: Lost Commits After Reset

You ran `git reset --hard HEAD~5` and lost 5 commits.
**Task**: Use `git reflog` to find and recover the lost commits.

### Exercise 9.D.3 — Debug: Merge Went Wrong

You merged a feature branch and everything broke. The merge commit is already pushed.
**Task**: Use `git revert -m 1 <merge-commit>` to undo the merge safely without rewriting history.

### Exercise 9.D.4 — Debug: Diverged Branches

`git pull` says "your branch and origin/main have diverged."
**Task**: Resolve using `git pull --rebase` or `git fetch` + `git rebase origin/main`.

### Exercise 9.D.5 — Debug: Large File Accidentally Committed

A 500MB file was committed 10 commits ago. GitHub rejects the push.
**Task**: Remove it from history using `git filter-repo` or BFG Repo Cleaner.

---

## PART E — PRODUCTION SIMULATION

### Scenario: Team Git Workflow

You're on a team of 4 engineers. Simulate a production workflow:

1. **Create a repository** with `main` and `develop` branches
2. **Branch naming**: `feature/<name>`, `bugfix/<name>`, `hotfix/<name>`
3. **Create a feature branch**, make changes, push
4. **Open a PR** (or simulate one with merge)
5. **Code review** — check the diff, leave comments
6. **Resolve conflicts** when two features touch the same file
7. **Squash and merge** to keep history clean
8. **Tag a release** after merge to main
9. **Create a hotfix** branch from a tag, fix, merge back

Deliverables:
- Clean git history with meaningful commit messages
- At least one resolved merge conflict
- At least one interactive rebase (squash)
- At least one tag
- A `.gitignore` and pre-commit hook

---

## Key Takeaways

1. **Git has three areas**: working directory → staging → repository. Understand the flow.
2. **Branches are cheap** — create them for every feature, delete after merge.
3. **Never force push to shared branches** — use `git revert` instead of `git reset` on public history.
4. **The reflog is your safety net** — almost nothing in git is truly lost.
5. **Interactive rebase** keeps history clean — squash WIP commits before merging.
6. **Git hooks automate quality** — enforce linting, testing, commit message format.
7. **Signed commits and tags** prove authenticity in production environments.

---
*Next: [Section 10 — Database Fundamentals](10-database-fundamentals.md)*
