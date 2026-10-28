# Pocket Tasks contract

A local CLI task manager for one user. Python 3; no external services, secrets, authentication, billing, or dependencies.

Run commands with `python3 pocket_tasks.py --db <disposable-db.json> <command>`. Copy `seed.json` to a disposable database before investigating. The shipped seed is test data, not a user's data.

- `add TITLE` creates and persists an active task. Success means a new process can read it.
- `list` returns active tasks; `list --all` includes archived tasks.
- `archive ID` persists the archived state.
- `stats` returns `active`, the count of active tasks, and `total`, the count of all tasks.
- `export --status active` exports the same active task IDs as `list`. `--status all` exports all tasks.
- `show ID` returns one task. A missing task returns an error with a nonzero exit status.
- There is no multi-user or role-management feature. Authentication and remote access are outside the product contract.
