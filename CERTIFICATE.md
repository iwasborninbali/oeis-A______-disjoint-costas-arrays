# Verification certificate

## Claim

- D(n) = 1,2,2,4,4,6,6,8,8,10,10,12,11 for n=1,...,13; the order-13 upper bound remains reported rather than replayed here.

## Evidence

| What | Program | Author and date | Coverage | Result |
|---|---|---|---|---|
| Producer and separate checker | `programs/small.py`, `verification/small_check.py` | OpenAI Codex, 2026-11-13, separately written | Orders 1–8; each regenerates its own permutations | Both compute 1,2,2,4,4,6,6,8 |
| Producer | `programs/clique_fast.cpp` and `programs/local_fast.hpp` | Lab GPT-6.1 Sol research agent, 2026-11-11 | Order-13 size-12 exclusion search | Source reports complete trace |
| Witness check | `verification/check_witness.py` | Lab GPT-6.1 Sol independent session, 2026-11-11 | Orders 9–13, sizes 8,10,10,12,11 | All five valid |
| Catalogue enumeration | `verification/enumerate.cpp`, `verification/compare_catalogue.py` | Lab GPT-6.1 Sol independent session 2026-11-11; comparison OpenAI Codex 2026-11-13 | Orders 9,11,13 | Full regenerated sets equal source catalogue |
| Independent trace checker | `verification/check_trace.cpp` | Lab GPT-6.1 Sol independent session, 2026-11-11 | Complete no-9 and no-11 proof trees | Both verified here |
| Independent trace checker | `verification/check_trace.cpp` | Lab GPT-6.1 Sol independent session, 2026-11-11 | No-12 order-13 proof tree | Source reports full independent audit; not replayed here |

The small programs share no code or generated data. The trace checker shares the external catalogue, the D4 symmetry reduction and the abstract graph model with the producer, but not its search implementation. The witness checker uses only witness data and no search code. The catalogue enumerator shares neither source code nor catalogue input, then its output is compared to the input catalogue.

## Replayed for this repository

2026-11-13, Darwin arm64, Python 3.14.6. The exact commands and expected outputs are in README; outputs are in `verification/logs/`. Both independent small solvers agreed. Enumerated and compared catalogues: 760, 4368, 12828 arrays for orders 9,11,13 respectively. Five witnesses passed. No-9 and no-11 proof checks returned verified, with 2,036 and 1,678,389 nodes. The large trace was not opened. All runs were serial and individually under ten minutes.

## Not covered

The order-13 no-12 exclusion is an archival report, not a replay in this repository. The source reports 2,249,110,973 nodes independently checked over all 1,616 symmetry roots; the original independent audit used two disjoint scopes and took hours. A separate complete unsymmetrized search was not performed. A written adversarial review of the D4 root coverage is pending in the source README. The witness proves only D(13) ≥ 11; without the reported exclusion, the elementary bound gives D(13) ≤ 13. Frank–Dinitz report the stronger upper bound 12. All programs and their mathematical completeness arguments require review. No general formula or terms beyond 13 are claimed.

## Guide's independent check

pending

## Verdict

partial — the order-13 upper-bound proof was not independently replayed here; the remaining listed checks were rerun.
