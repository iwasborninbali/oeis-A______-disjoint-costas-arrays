# Order-13 continuation after original independent recount

This file supersedes the earlier order-13 progress counts in REPORT.md and TRANSFER_STATUS.md. The central claim D(13)=11 remains **unproved**.

## Three resumed commands

From this result directory, after rebuilding the catalogue and binary as instructed in REPORT.md:

```bash
./exact 13 12 120 5 1162
./exact 13 12 120 5 1163
./exact 13 12 90 5
```

| Search | Outcome | Nodes in this run | Wall seconds |
|---|---|---:|---:|
| Root 1162, second-array prefix | EXHAUSTED (4704/4704) | 11728091 | 36.2388 |
| Root 1163, second-array prefix | EXHAUSTED (4547/4547) | 9742361 | 30.4475 |
| Full top-level search | INCOMPLETE (807/1616 roots) | 33724364 | 90.9918 |

**Combined 55194816 nodes, 157.6781 seconds of summed wall time. No 12-family was found.** Five top-level roots were interrupted and have no `.done` file. There are now **807 of 1616 completed canonical root branches**.

## Resume from GitHub checkout

The original `restore_checkpoints.py` embeds a full, lossless snapshot from **805** completed roots. The two new `checkpoints/n13k12/root_1162.done` and `root_1163.done` files committed alongside this note advance the *root-level resumption state* to **807** completed roots, even though the extra 630 detailed second-array `.done` records from the continuation are not separately transferred. Those 630 details remain in the original working container; the two root-level markers are sufficient for the top-level solver to skip these exhaustively verified roots.

Run:

```bash
python3 restore_checkpoints.py
# This restores the earlier 805-root snapshot without deleting the two new root markers.
g++ -std=c++20 -O3 -march=native enumerate.cpp -o enumerate
./enumerate catalogues 13
g++ -std=c++20 -O3 -march=native -fopenmp exact.cpp -o exact
./exact 13 12 300 5
```

The 300 seconds is a cap, not a completion estimate. Keep the checkpoint directory intact between calls. This continuation is not a proof of nonexistence of 12 disjoint arrays at n=13.
