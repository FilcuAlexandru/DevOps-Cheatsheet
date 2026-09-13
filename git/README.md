# Git

```bash
git init                                       # start a new repo in the current directory — creates the .git folder, nothing else changes
git clone <url>                                  # copy an existing remote repo locally — includes full history, not just the current files
git status                                         # what's changed, staged, and untracked right now — the first command to run before doing anything else
git add <file>                                       # stage a file's changes for the next commit — staging is separate from committing, lets you build a commit piece by piece
git add .                                              # stage everything changed in the current directory — fast, but review with status first so you don't stage something unintended
git commit -m "message"                                 # commit staged changes with a message — only what was staged goes in, not everything changed
git commit -am "message"                                  # stage tracked changes and commit in one step — skips new/untracked files
git push                                                    # send local commits to the remote — makes your work visible/available to others
git pull                                                      # fetch + merge the remote's changes into your current branch — the combined step most people mean by "pull"
git fetch                                                       # download remote changes without merging them yet — lets you inspect what changed before integrating it
git branch                                                        # list local branches — the current one is marked with an asterisk
git branch <name>                                                    # create a new branch without switching to it — useful when setting up branches ahead of time
git checkout <branch>                                                   # switch to an existing branch — your working directory updates to match it
git checkout -b <branch>                                                   # create a branch and switch to it in one step — the common case when starting new work
git switch <branch>                                                          # the newer, clearer alternative to checkout — checkout historically did too many unrelated things
git merge <branch>                                                              # merge another branch into the current one — brings its commits in, may create a merge commit
git log                                                                            # commit history, full form — shows author, date, and full message for each commit
git log --oneline                                                                    # commit history, one line per commit — much easier to scan than the full form
git diff                                                                                # unstaged changes vs the last commit — what you'd be committing if you staged everything right now
git diff --staged                                                                         # staged changes vs the last commit — exactly what the next commit would actually contain
git remote -v                                                                                # every remote configured, with their URLs — confirms you're pushing/pulling from where you think
git tag <name>                                                                                  # tag the current commit, e.g. for a release — tags mark a specific point in history by name
```

**Enhanced:**
```bash
git log --oneline --graph --all --decorate   # the single most useful "what's actually going on" view — shows branches, merges, and history together
git reflog                                     # recover commits after a bad reset — your safety net
git bisect start / good / bad                   # binary search for the commit that introduced a bug — far faster than checking commits one by one
git stash -p                                     # interactively stash only some hunks — useful when only part of your changes should be set aside
git rebase -i HEAD~5                              # squash/reorder/edit the last 5 commits — cleans up history before sharing it
git blame -L 40,60 file.py                         # who changed just these lines, not the whole file — narrows blame output to what actually matters
git cherry-pick <sha>                               # apply one specific commit onto the current branch — grabs just that fix without merging the whole branch
git worktree add ../hotfix hotfix-branch             # work on two branches in two directories — no stashing/switching needed to jump between them
git diff --stat                                       # summary of what changed, file by file — the line-count overview without the actual diff noise
git log -S"functionName" --oneline                      # find every commit that added or removed a specific string/function — much sharper than blame when you're hunting for when something was introduced
git rebase -i --autosquash HEAD~10                        # auto-orders fixup!/squash! commits into place — pair with `git commit --fixup <sha>` while working, then one clean rebase at the end
```

## Health check

1. **Working tree is clean, or intentionally not** — `git status` — red flag: uncommitted changes you don't remember making — confirm before you do anything destructive nearby.
2. **In sync with the remote** — `git fetch && git status` — red flag: unexpectedly ahead or behind — someone else may have pushed, or your last push didn't actually land.
3. **Nothing oversized or sensitive about to be committed** — `git diff --stat --cached` — red flag: a suspiciously large diff or a file that looks like it holds credentials — much cheaper to catch before the commit than after.

## Troubleshooting

**Merge conflict:**
```bash
git status                        # lists every conflicted file — the starting point for resolving a merge conflict
git diff --name-only --diff-filter=U   # same info as status, but easier to pipe into a script — just the filenames, no extra formatting
git checkout --ours <file>            # take your version entirely for one file — only right when the whole file should just be yours, not a real merge
git checkout --theirs <file>            # or take theirs entirely — for anything more nuanced, edit the conflict markers by hand
```

**Accidentally committed a secret:**
```bash
git reset --soft HEAD~1                # undo the last commit — only safe if not pushed yet
```
If it's already pushed, a reset isn't enough — the secret is in history and needs rotating at the source (the credential itself), plus a history rewrite (`git filter-repo` or BFG) if it must be scrubbed. Rotate first; history cleanup is damage control, not the fix.

**Detached HEAD:**
```bash
git checkout -b temp-branch   # save your current work under a real branch name — detached HEAD commits become unreachable once you switch away
git branch --contains <sha>     # confirm which branches contain a commit — check before deleting anything
```

---
