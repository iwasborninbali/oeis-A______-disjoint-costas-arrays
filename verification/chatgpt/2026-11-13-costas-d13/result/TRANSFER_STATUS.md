# GitHub delivery status (updated 2026-11-13)

Draft PR: https://github.com/iwasborninbali/oeis-A______-disjoint-costas-arrays/pull/1
Branch: `chatgpt/2026-11-13-costas-d13`, based on `main`; `main` was not modified.

The branch now includes all four independent source files, `REPORT.md`, all
24 original/continuation logs as separate unchanged text files under `logs/`,
`make_transfer.py`, `restore_logs.py`, `restore_checkpoints.py`, and a
`MANIFEST.sha256` for every delivered payload file.

The checkpoint tree comprises **23,226 UTF-8 `.done` files**, 805 completed
first-array roots and 22,421 second-array branch records, with total text
content size **399,686 bytes**, well below 20 MB.

**Representation choice:** Individual checkpoint paths were not committed as
23,226 separate GitHub blobs because doing so through the connector is
impractical. Instead their complete path/content pairs are encoded in the
single 20,258-byte text source `restore_checkpoints.py` (base85/zlib).
Running `python3 restore_checkpoints.py` from the result directory restores
all 23,226 file paths and byte-identical contents. The stored canonical
snapshot SHA-256 is validated by the restore script; an independent restore
was compared with the original checkpoint directory using `diff -qr`.

Only binary generated catalogues, compiled executables, and the thousands
of *individual* `.done` paths are omitted as separate GitHub files. No
original log or source file is omitted, and the full checkpoint data is
losslessly transferable through the script. All payload files were fetched
through the connector after writing and checked against local copies;
no NUL-byte conversion was detected.

The proof D(13)=11 is **not finished**. After the two resumed roots, 805 of
1,616 symmetry-reduced roots are exhausted, and no 12-array family was found.
