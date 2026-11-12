# Independent recount of pairwise disjoint Costas arrays, n <= 13

This directory is a reproducible computational partial verification of
`verification/chatgpt/2026-11-13-costas-d13/TASK.md`.

## Definitive completed results

- All Costas arrays for n=1..13 enumerated from the given definition. Counts:
  `1 2 4 12 40 116 200 444 760 2160 4368 7852 12828`.
- Independently checked all five supplied witnesses (n=9..13), including their
  original catalogue indices and their actual permutations.
- Exact D(n) for n=1..12:
  `1 2 2 4 4 6 6 8 8 10 10 12`.
- Exact exhaustive nonexistence proof for n=3,5,7,9,11 at target k=n.
  For larger even n the verified full-size packings give D(n)=n trivially.
- For n=13: existence of 11 verified. Nonexistence of 12 **NOT PROVED**.

## Order-13 partial verification / checkpoints

- Target: 12 disjoint Costas arrays.
- There are 1616 canonical first-array roots under the D4 square symmetries.
- 803 first-array roots completely exhausted and checkpointed.
- Five more first-array roots (1158,1159,1161,1162,1163) have been subdivided
  into independent second-array jobs. The first one is fully exhausted and
  included among the 803 completed roots. The others are partial.
- All checkpoint files ending in `.done` were written only after the corresponding
  branch returned exhaustively without a witness. Interrupted branches do
  not have `.done` files and are recomputed when resumed.
- These are search results from a partial computation, NOT a proof of D(13)=11.

## Building

From this directory, with GCC 14.2 and Python 3:

```bash
g++ -std=c++20 -O3 -march=native enumerate.cpp -o enumerate
g++ -std=c++20 -O3 -march=native -fopenmp exact.cpp -o exact
./enumerate catalogues 13
python verify.py
python audit_small.py
```

## Exact search commands

```bash
./exact 3 3 15 5
./exact 5 5 15 5
./exact 7 7 15 5
./exact 9 9 25 5
./exact 11 11 25 5
# Resume still-unfinished order-13 work, five threads, 300-second call:
./exact 13 12 300 5
# To resume second-array branches inside a difficult canonical root:
./exact 13 12 300 5 1159
./exact 13 12 300 5 1161
./exact 13 12 300 5 1162
./exact 13 12 300 5 1163
```

The third CLI argument is a *maximum runtime cap* (seconds), not an estimate.
The program runs in the foreground, writes checkpoint files as it completes
branches, and stops with an `INCOMPLETE` status if interrupted or time-limited.
A completed impossibility proof must say `EXHAUSTED`, with all canonical roots
completed; no `INCOMPLETE` result is a proof of nonexistence.

To test one root at finer granularity, specify the final root index argument.
The canonical roots are D4-orbit representatives, so every possible packing
can be normalized to have a canonical first-array root, and its smallest
array in that normalized family must be the root. The solver searches only
higher-index arrays after this first choice. The greedy coloring bound is
valid because a clique needs distinct colors in every proper graph coloring.
The row-column necessary condition is just the pigeonhole principle.

## Recorded run details

- `enumerate.log`: all counts; enumeration wall time 4.76 s; n=13 DFS
  33,831,238 nodes.
- `verify.log`: all certificate and catalogue checks pass.
- `audit-small.log`: independent brute-force Python packings for n<=7.
- `search-n9k9.log`: exhaustive, 100 roots, 9,818 nodes, 0.031 s.
- `search-n11k11.log`: exhaustive, 555 roots, 11,955,997 nodes, 13.125 s.
- `search-n13k12-*.log`: several bounded/partial searches, some killed by
  the shell's timeout; no impossibility conclusion.
- `search-n13k12-prefix*.log`: finer-grained checkpointed partial work.

The supplied witness files are preserved in `verification/certificates/`.
Sources and logs are checksummed in `sha256sums.txt`.