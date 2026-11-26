# Project Agent Rules (Antigravity & Claude — Portable Spec)

## 0. Language Split (Token Compression)
- **Human-facing (`chat`, `memory.md`, `README.md`, artifacts):** **Deutsch** (prägnant).
- **Agent wire (subagent prompts, internal handoffs):** **Telegraphic English + diff/symbols** (`+add ~mod -del =read`, `fn()`, `path:L10-40`). Include complete context (goal, paths, constraints, expected output) because subagents start cold.

## 1. Co-work (Antigravity <-> Claude)
- Both Antigravity (Gemini) and Claude work on this repository. Before editing: run `git status -sb` / re-read target lines; never overwrite uncommitted changes you did not make.
- **`memory.md` (Deutsch, <150 Zeilen)** is the shared handoff: read at session start; after features/fixes update in place (replace stale info, no chronological append).

## 2. Git & Security Policy
- **Branches:** `main` = releases; `develop` = integration (if present); `feature/<name>` off `develop` (or `main`).
- **HARD MERGE BAN:** NEVER merge into `develop` or `main` without an explicit user command (e.g. *"bitte in develop/main mergen"*), even after green tests.
- **NO SECRETS IN GIT:** NEVER commit passwords, Wi-Fi/API/private keys, or tokens. Keep secrets untracked (`~/.config/<app>/` or gitignored `.env*`).
- **Cross-platform safety:** No symlinks and no special characters (`:`, `?`, `*`) in filenames.

## 3. Context Hygiene & Direct Action
- **Direct Edits (Fast Path):** Once target lines are identified, edit directly instead of spawning subagents (uses warm prompt cache, avoids 20k–50k token cold-start overhead).
- **Surgical reads:** Search/outline first, then targeted line ranges; never dump large files or full logs; do not re-read files immediately after editing.
- **Short shell output:** Use `-q`, `--tb=short`, `| tail -n 20`. Batch independent tool calls in parallel.
- **Unbuffered & 5-Min Watchdog:** Prefix Python/long runs with `PYTHONUNBUFFERED=1` (`python3 -u`). When backgrounding a long task, immediately arm a ~5-min check (timer/monitor); on wakeup check progress — kill & fix bottleneck if stalled/exploding, otherwise re-arm.
- **Subagent Delegation Criterion:** Delegate ONLY to protect main context from noisy log triage, broad repo sweeps, or truly independent parallel work.
- **Compaction / Checkpoint:** Recommend `/compact` after major milestones or >25 turns — or `/checkpoint` on Cloud/Mobile and before switching between Antigravity and Claude.

## 4. Quality
- Verify before reporting done (run relevant tests/checks); report failures honestly.
- For non-trivial or multi-file changes: brief plan first, then implement. Keep diffs minimal; no unrequested refactors.
