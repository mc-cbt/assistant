# Andavo Repo — Local Layout & Worktrees

Local checkout layout for the **andavo** repository.

## Layout

- `~/repos/andavo/` — root directory containing all checkouts.
- `~/repos/andavo/andavo` — the **`main`** branch.
- Every other directory under `~/repos/andavo/` is a **git worktree** for a different branch of active work, stored as a **sibling** to the main-branch directory.

## Worktree convention

Each worktree branch gets its own **sibling directory** under `~/repos/andavo/`:

```
~/repos/andavo/
├── andavo/          # main branch
├── <branch-a>/      # worktree
├── <branch-b>/      # worktree
└── ...
```

This keeps directory path patterns consistent for command-line tools and lets multiple agents work on different branches in parallel.
