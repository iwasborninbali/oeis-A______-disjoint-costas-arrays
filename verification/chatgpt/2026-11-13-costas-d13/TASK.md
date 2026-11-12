# Independent recount: maximum number of pairwise disjoint Costas arrays, D(n) for n <= 13

You are asked to check a computational claim **independently**: write your own programs from the definition below, run them
in your container, and report. Do not try to find or reuse the authors' search code; this archive deliberately contains only
this brief and the witness files.

## Definitions
- A Costas array of order n is a permutation p of {0, ..., n-1} (dot in row i, column p(i)) such that the displacement
  vectors (j - i, p(j) - p(i)) for all pairs i < j are pairwise distinct.
- Two arrays are *disjoint* if they share no cell: p(i) != q(i) for every row i.
- D(n) = the largest number of pairwise disjoint Costas arrays of order n. Trivially D(n) <= n (each array has one dot per row).

## Claim to check
D(1..13) = 1, 2, 2, 4, 4, 6, 6, 8, 8, 10, 10, 12, 11. The new part is **D(13) = 11**, that is: (a) 11 pairwise disjoint
Costas arrays of order 13 exist (a witness is in `verification/certificates/witness13.json`), and (b) **no 12 pairwise
disjoint Costas arrays of order 13 exist**. (b) is the main point. Values up to 12 are from the literature
(Dinitz, Ostergard, Stinson 2012); please recompute as many as you can.

## What to do
1. Report your container: `nproc`, memory (`free -m` or `/proc/meminfo`), compiler versions.
2. Enumerate all Costas arrays of order n for n = 1..13 with your own program. Expected counts (OEIS A008404):
   1, 2, 4, 12, 40, 116, 200, 444, 760, 2160, 4368, 7852, 12828. Report yours.
3. Check every witness file in `verification/certificates/` (orders 9..13): each array is Costas and the arrays are pairwise disjoint.
4. Compute D(n) exactly for n = 1..12 (or as far as feasible), with an exact search (maximum clique in the disjointness graph,
   exact cover style search, SAT, or ILP; any exact method; state which).
5. The main job: decide whether 12 pairwise disjoint Costas arrays of order 13 exist. Use an exact method. Symmetry breaking
   is allowed if you justify it (for example: the 8 symmetries of the square map Costas arrays to Costas arrays and preserve
   disjointness, so a family can be normalised; or fix the array that covers a given cell). Explain every reduction you use.
6. This may run for a long time. Start it **in the background** (for example `nohup ./search > search.log 2>&1 &`), use all
   cores, write progress and checkpoints to files so that the run can be resumed if the container is reset, and make the
   progress measurable (fraction of the top-level branches done). If you can, set yourself a reminder, a scheduled task or a
   cron job that reports progress; if you cannot, say so: we will ask for progress in this chat. Reply now with what you started
   and an estimate of the run time; do not wait for the run to finish in this reply.
7. When it finishes, report: the result for every n, run times, node counts, the exact commands, and the SHA-256 of your
   source files and logs. Give your programs' source code in the reply (we will review it and rerun it ourselves).

Answer in English. Be exact; say plainly what was not finished or not checked.
