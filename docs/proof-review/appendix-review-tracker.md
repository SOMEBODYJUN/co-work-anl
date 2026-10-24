# Multiple-facilities proof-review tracker

| Target | Proof lines | Required chunks | Blueprint | Note file | Gate deps | Status |
| --- | --- | --- | --- | --- | --- | --- |
| `lem:onpath` | `research/manuscripts/multiple_facilities/main.tex:88-100` | `1` | `N` | `docs/proof-review/appendix-notes/lem-onpath.md` | `none` | `closed: verified as written` |
| `lem:transfer` | `research/manuscripts/multiple_facilities/main.tex:120-132` | `1` | `N` | `docs/proof-review/appendix-notes/lem-transfer.md` | `none` | `closed: verified as written` |
| `lem:packing` | `research/manuscripts/multiple_facilities/main.tex:142-149` | `1` | `N` | `docs/proof-review/appendix-notes/lem-packing.md` | `none` | `closed: verified as written` |
| `lem:capped` | `research/manuscripts/multiple_facilities/main.tex:156-168` | `1` | `N` | `docs/proof-review/appendix-notes/lem-capped.md` | `none` | `closed: verified as written` |
| `lem:deviation` | `research/manuscripts/multiple_facilities/main.tex:178-198` | `2` | `N` | `docs/proof-review/appendix-notes/lem-deviation.md` | `lem:transfer, lem:packing, lem:capped` | `closed: verified as written` |
| `thm:main` | `research/manuscripts/multiple_facilities/main.tex:206-208` | `1` | `N` | `docs/proof-review/appendix-notes/thm-main.md` | `lem:onpath, lem:deviation` | `closed: verified as written` |
| `prop:certificate` | `research/manuscripts/multiple_facilities/main.tex:217-221` | `1` | `N` | `docs/proof-review/appendix-notes/prop-certificate.md` | `thm:main, lem:packing, lem:capped` | `closed: verified as written` |
