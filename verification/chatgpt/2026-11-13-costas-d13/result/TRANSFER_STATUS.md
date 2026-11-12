# GitHub delivery scope (2026-11-13)

This draft branch is an **in-progress partial delivery**. The exhaustive order-13
nonexistence proof is unfinished.

Included under `result/`: the four independent source files, REPORT.md,
MANIFEST.sha256, and 19 of the 22 original computation logs in `logs/`.
Each included log has its original, unmodified UTF-8 text and an SHA-256 entry.

**Not yet transferred to GitHub:**

- `search-n9k9.log` (4,098 bytes)
- `search-n11k11.log` (22,832 bytes)
- `search-n13k12-attempt2.log` (34,126 bytes)
- The 22,647 order-13 `.done` checkpoint files: 803 top-level roots and
  21,844 completed second-array branches. Their combined file contents are
  only 387,519 bytes (text, below the requested 20 MB ceiling), but the
  22,647 separate filesystem entries occupy approximately 90 MiB of disk.
  These remain in the working container at
  `/mnt/data/costas-d13-work/checkpoints/n13k12/`, not in the GitHub branch.

The partial order-13 search can be resumed locally from these checkpoint files,
using `./exact 13 12 300 5` and the root-specific commands in REPORT.md.
The GitHub branch alone is **not** sufficient to resume at the same detailed
checkpoint state; it must not be represented as a complete archival copy.

The MANIFEST.sha256 file hashes every delivered file other than itself, as
is conventional for a self-referential checksum manifest. More artifacts may
be added to this draft branch in subsequent work.