# OEIS candidate (no A-number yet): maximum disjoint Costas arrays

<!-- oeis-status:begin -->
**OEIS status: not submitted.** (replaced by the registry tool)
<!-- oeis-status:end -->

## Definition

For n ≥ 1, D(n) is the maximum size of a family of pairwise cell-disjoint Costas arrays of order n; the offset is 1. A Costas array is an n by n permutation array whose vectors between pairs of occupied cells are all distinct when oriented from the smaller row to the larger row. At n=1 its unique singleton array is Costas and D(1)=1. The upper bound D(n) ≤ n follows from any row.

## Terms / result

| n | D(n) |
|---:|---:|
| 1 | 1 |
| 2 | 2 |
| 3 | 2 |
| 4 | 4 |
| 5 | 4 |
| 6 | 6 |
| 7 | 6 |
| 8 | 8 |
| 9 | 8 |
| 10 | 10 |
| 11 | 10 |
| 12 | 12 |
| 13 | 11 |

The values through 12 were already published; D(13)=11 is the lab's reported result, with its upper-bound replay pending here. `data/terms.txt` is in b-file format.

## How it was obtained

For each order, form a graph whose vertices are all Costas permutations and join disjoint pairs; a maximum packing is a maximum clique. The lab search used a symmetry-reduced clique search and a proof trace for the exclusion of 12 at order 13, plus a direct 11-array witness. Frank and Dinitz had previously reported 11 ≤ D(13) ≤ 12.

Two separate programs enumerate and solve orders 1–8 afresh. The earlier source report `speed.md` correctly called the exclusion conditional on the supplied catalogue at that stage; a later separate program enumerated every order-13 permutation and matched the catalogue. The full exclusion has one independent trace audit, not a second complete independent search.

## Verification

Independent checks rerun here cover orders 1–12 and the order-13 11-packing and catalogue completeness. The order-13 no-12 trace audit is reported from the source, not replayed here; its symmetry reduction also awaits the source-requested adversarial review. The certificate verdict is partial; see CERTIFICATE.md.

## Prior art and credit

Dinitz, Östergård and Stinson published D(1)–D(12); Frank and Dinitz published the order-13 interval and the lower bound 11. See PRIOR-ART.md for exact citations, OEIS searches and qualifications.

## Reproduce

Python 3, C++17 and zlib are required. Excluding the network fetch, the commands below took under one minute here. Fetch the independently published catalogue, then independently enumerate and compare all its rows:

```sh
python3 programs/small.py
python3 verification/small_check.py
python3 programs/fetch_catalogues.py /tmp/costas-catalogues
clang++ -O3 -std=c++17 verification/enumerate.cpp -o /tmp/costas-enumerate
for n in 9 11 13; do
  /tmp/costas-enumerate "$n" "/tmp/costas-generated$n.txt"
  python3 verification/compare_catalogue.py "$n" "/tmp/costas-generated$n.txt" "/tmp/costas-catalogues/costas_$n.txt"
done
for n in 9 10 11 12 13; do python3 verification/check_witness.py "verification/certificates/witness$n.json"; done
clang++ -O3 -std=c++17 verification/check_trace.cpp -lz -o /tmp/costas-check-trace
for n in 9 11; do /tmp/costas-check-trace "/tmp/costas-catalogues/costas_$n.txt" "verification/certificates/no$n.proof.gz" "$n"; done
```

Expected: both small computations print `1,2,2,4,4,6,6,8`; catalogue comparisons report `identical_sets=True` with counts 760, 4368, 12828; five witnesses and both trace checks report verified. Full output is in `verification/logs/`. The large order-13 trace is deliberately excluded from this replay. Its full check exceeded ten minutes in the original work.

## Provenance

`athanor-combinatorics`, commit `825364bac9d797e04ba76921d04c630e3b6e29fa`, paths `costas-d13/search-and-certificate/` and `costas-d13/independent-solver-and-catalogue/`; source files copied from that commit. Archive: [Zenodo 10.5281/zenodo.24140011](https://doi.org/10.5281/zenodo.24140011). The 379,174,621-byte `no_12_order13.proof.gz` is archived there, SHA-256 `95244d728ab911ce882b71f39d8edc794670daf5a7457bbf0ba26af43ad35d9e`; it is not included here or opened in this work. The source manifest is `verification/order13_manifest.json`.

## Author, licence

Aleksei Kudriashov (ORCID 0009-0006-8885-5338), Athanor lab, with AI assistance (OpenAI Codex cores; Claude Code as the lab's guide). Code: MIT; data and text: CC BY 4.0 (see LICENSE.md).
