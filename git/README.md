# Git

```bash
git log --oneline --graph --all --decorate   # the single most useful "what's actually going on" view
git reflog                                     # recover commits after a bad reset — your safety net
git bisect start / good / bad                   # binary search for the commit that introduced a bug
git stash -p                                     # interactively stash only some hunks, not everything
git rebase -i HEAD~5                              # squash/reorder/edit the last 5 commits
git blame -L 40,60 file.py                         # who changed just these lines, not the whole file
git cherry-pick <sha>                               # apply one specific commit onto the current branch
git worktree add ../hotfix hotfix-branch             # work on two branches in two directories, no stashing
git diff --stat                                       # summary of what changed, file by file, no noise
```

**Enhanced:**
```bash
git log -S"functionName" --oneline                # find every commit that added or removed a specific string/function — much sharper than blame when you're hunting for when something was introduced
git rebase -i --autosquash HEAD~10                   # auto-orders fixup!/squash! commits into place — pair with `git commit --fixup <sha>` while working, then one clean rebase at the end
```

## Health check

1. **Working tree is clean, or intentionally not** — `git status` — red flag: uncommitted changes you don't remember making — confirm before you do anything destructive nearby.
2. **In sync with the remote** — `git fetch && git status` — red flag: unexpectedly ahead or behind — someone else may have pushed, or your last push didn't actually land.
3. **Nothing oversized or sensitive about to be committed** — `git diff --stat --cached` — red flag: a suspiciously large diff or a file that looks like it holds credentials — much cheaper to catch before the commit than after.

## Troubleshooting

**Merge conflict:**
```bash
git status                        # lists every conflicted file
git diff --name-only --diff-filter=U   # same info, easier to pipe into a script
git checkout --ours <file>            # take your version entirely for one file, if that's the right call
git checkout --theirs <file>            # or take theirs entirely — for anything more nuanced, edit the conflict markers by hand
```

**Accidentally committed a secret:**
```bash
git reset --soft HEAD~1                # if it's only in the last commit and NOT pushed yet, undo the commit, fix, recommit
```
If it's already pushed, a reset isn't enough — the secret is in history and needs rotating at the source (the credential itself), plus a history rewrite (`git filter-repo` or BFG) if it must be scrubbed. Rotate first; history cleanup is damage control, not the fix.

**Detached HEAD:**
```bash
git checkout -b temp-branch   # save your current work under a real branch name before it becomes unreachable
git branch --contains <sha>     # confirm which branches already contain a given commit, useful before deleting anything
```

---
