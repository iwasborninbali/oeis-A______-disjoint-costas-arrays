# Prior art

OEIS searches on 2026-11-13 through `https://oeis.org/search` with `fmt=json`; null means zero results. Requests were spaced by at least one second.

| Exact query | Results |
|---|---:|
| `1,2,2,4,4,6,6,8,8,10,10,12,11` | 0 |
| `2,2,4,4,6,6,8,8,10,10,12,11` | 0 |
| `2,4,4,6,6,8,8,10,10,12,11` | 0 |
| `disjoint Costas arrays` | 3: A008404, A000225, A001047 |
| `Costas Latin squares` | 4: A000051, A002450, A002623, A014551 |

A008404 counts all Costas arrays, rather than maximum disjoint families; the other keyword matches are unrelated arithmetic sequences. Prefix searches with one and two initial values removed cover obvious shifts. No search establishes priority.

- J. H. Dinitz, P. R. J. Östergård, D. R. Stinson, [*Packing Costas Arrays*](https://arxiv.org/abs/1102.1332), Journal of Combinatorial Mathematics and Combinatorial Computing (2012), Table 1: published D(1)–D(12), and D(13) ≤ 12. Our small-order computations reproduce already published values, not new discoveries.
- Morgan R. Frank and Jeffrey H. Dinitz, [*On Maximal Partial Costas Latin Squares*](https://site.uvm.edu/jdinitz/files/2021/04/costasPaper.jcmcc_.pdf), JCMCC 93 (2015), 23–32, Table 3.1: D(1)–D(12), and the interval 11–12 at order 13. The published table's order-2 number of arrays is a misprint (1 instead of 2), not a different value of D(2).
- J. K. Beard et al., [searched Costas catalogue archive](https://jameskbeard.com/Files_for_download/Costas_folder_Searches.zip), and Silverman, Vickers and Mooney, *On the number of Costas arrays as a function of array size*, Proceedings of the IEEE 76 (1988), 851–853, [DOI 10.1109/5.7156](https://doi.org/10.1109/5.7156): searched arrays and historical enumeration. The complete order-13 catalogue was independently regenerated here, so the exclusion no longer relies only on a historical completeness assertion.

The accelerated source report conditioned its conclusion on catalogue completeness because it did not itself enumerate all permutations; the later independent enumeration in the source root README did so and matched the catalogue. The source reports a complete trace audit, but its additional independent solver checked only 35 heavy roots at order 13. Any historical novelty for D(13)=11 remains subject to literature review.

The two primary papers can be fetched with `python3 programs/fetch_papers.py /tmp/costas-papers`; the script checks recorded SHA-256 hashes.
