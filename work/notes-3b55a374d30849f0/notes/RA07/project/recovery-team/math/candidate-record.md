# RA07 independent mathematical candidate record

Method: every unresolved ledger ID is listed below. IDs sharing one source span are explicitly grouped, but the candidate pair applies to each ID in that group. “Forward” means substitution into the local proof/definition; “backward” means constraints from the next/previous page. No candidate is promoted into the black source transcript by this record.

## Source and target units

### p0001 / Q001 span (`RA07-P001-U013`)
**Source candidates**

- **A (working):** “在无限维（可分）赋范空间上不存在平移不变的非平凡测度” (or the same statement with “正则” in the middle). The visible `AM`-like mark can be read as a space/operator qualifier; the final phrase is visibly “非平凡测度”.
- **B:** “在无穷维空间中不存在同时平移不变、正规且非平凡的测度” (with “无穷维” rather than “无限维可分”). This preserves the same theorem family but treats the middle two handwritten characters as “正规性”.

Forward check: either reading is compatible with the subsequent Dirac/countability/cardinality notes and with the later Vitali non-measurability discussion; no displayed equation forces the quantifier. Backward check: p0001’s preceding `c^2=2^c` and p0002’s outer-measure definitions support an existence/nonexistence theorem about measures, but do not distinguish A/B. Source recheck: first two characters visibly begin with “无穷/无限”; middle stroke has two plausible readings; keep both.

**Target IDs covered:** `T-P001-013`, `N-P001-013`, `N-P001-013-S1`, `N-P001-013-S2` (each receives A/B above).

### p0003 outer-measure definition span (`RA07-P003-U007`)
- **A:** “定义 (m^*(E)=inf{sum |R_i|:Esubsetigcup_iR_i, R_i	ext{ rectangles}})” (Lebesgue outer measure by countable boxes).
- **B:** “对 (Esubsetmathbb R^n)，(m^*(E)) 为所有可数矩形覆盖体积和的下确界” (same formula, but the handwritten connective read as a prose definition rather than `inf`).

Forward: both yield the p0004 subadditivity and Carathéodory criterion. Backward: p0002 already introduces Jordan boxes and p0004 uses the cover-infimum; this forces “countable rectangle cover” semantically, not the exact connective. Source recheck: `m^*`, `R^n`, and a cover symbol are clear; the prose/operator between them is not.

**Target IDs:** `T-P003-007`, `N-P003-007`, `N-P003-007-S1` (A/B each).

### p0003 Remark item 12 span (`RA07-P003-U009`)
- **A:** “若 (E) 可测，则 (m^*(E)=m_*(E))” / “内外测度相等（proof）”.
- **B:** “若 (E) 满足 Carathéodory 条件，则 (E) 可测（proof）”.

Forward: A connects directly to the p0005 inner/outer-measure equality; B connects to the p0006 definition and p0007 closure proof. Backward: p0002–p0003 introduce outer measure first, while p0004–p0006 use Carathéodory measurability; both implications are possible from the short item-12 line. Source recheck: item number and trailing “proof” are clear; the middle predicate is not.

**Target IDs:** `T-P003-009`, `N-P003-009` (A/B each).

### p0005 Carathéodory equality bridge (`RA07-P005-U007`)
- **A:** connector “于是/从而 (m^*(E)=m^*(E\cap T)+m^*(T\setminus E))”.
- **B:** connector “故/因此 (m^*(E)=m^*(E\cap T)+m^*(T\setminus E))”.

Forward: both connectors preserve the displayed equality and the next “可测性” note. Backward: p0004 proves the same decomposition; p0006 restates it as the definition. Source recheck: the first character has a rising hook compatible with both “于是” and “故”; no unique visual winner.

**Target IDs:** `T-P005-007`, `N-P005-007`, `N-P005-007-S1` (A/B each).

### p0006 decomposition equality (`RA07-P006-U009`)
- **A:** “由可测性，(m^*(T)=m^*(T\cap E)+m^*(T\cap E^c))”.
- **B:** “若 (E) 可测，则 (m^*(T)=m^*(T\cap E)+m^*(T\cap E^c))”.

Forward: A is the concise proof step; B supplies the explicit hypothesis used in the definition. Backward: p0005 gives the same complement split and p0007 uses it in closure proofs. Source recheck: displayed terms `T`, `E`, `E^c`, and `m^*` are stable; only the introductory words are ambiguous.

**Target IDs:** `T-P006-009`, `N-P006-009` (A/B each).

### p0006 left-edge fragment (`RA07-P006-U014`)
- **A:** fragment belongs to “σ-代数/集合代数” (the next lines enumerate closure under complement, union and intersection).
- **B:** fragment belongs to “(A\setminus B=A\cap B^c)” (set-difference identity begun at the cropped left margin).

Forward: A leads to p0007’s closure proof; B leads to p0009’s explicit set-difference notation. Backward: p0006’s visible “不可测集合” and p0009’s `A∩B=∅`, `A\B` both support either continuation. Source recheck: only a left-edge vertical stroke and a superscript-like mark are present; retain both.

**Target IDs:** `T-P006-014`, `N-P006-014` (A/B each).

### p0010 Vitali prompt bridge (`RA07-P010-U008`)
- **A:** “取（令）V 为 Vitali 集，(V\subset[0,1])，并考虑平移 (V+q)”.
- **B:** “将/把 (V) 视为 Vitali 集，(V\subset[0,1])，再取有理平移”.

Forward: either reading yields pairwise-disjoint rational translates and the usual contradiction with countable additivity. Backward: p0010 visibly contains `Vitali`, `[2,3]^c`/translated interval, and p0011 uses the resulting measurable/non-measurable split. Source recheck: first bridge stroke fits “取/将”; post-name connective fits “集于/在于”; no unique choice.

**Target IDs:** `T-P010-008`, `N-P010-008`, `N-P010-008-S1`, `N-P010-008-S2` (A/B each).

### p0011 first bridge (`RA07-P011-U008`)
- **A:** “于是有 (m^*(T\cap A)+m^*(T\cap A^c)=m^*(T))”.
- **B:** “随后有/从而 (m^*(T\cap A)+m^*(T\cap A^c)=m^*(T))”.

Forward: both introduce exactly the displayed Carathéodory equality. Backward: p0006 defines this equality; p0012 repeats finite/countable additivity. Source recheck: three short Chinese strokes before the equation are compatible with both; equation itself is clear.

**Target IDs:** `T-P011-008`, `N-P011-008`, `N-P011-008-S1` (A/B each).

### p0011 second bridge (`RA07-P011-U010`)
- **A:** “同理/因而，对两两不交集合有 (m(\bigcup_iA_i)=\sum_i m(A_i))”.
- **B:** “故/于是，对有限（再推广可数）并有 (m(\bigcup_iA_i)=\sum_i m(A_i))”.

Forward: A is the standard induction step from p0011’s split; B is the explicit finite-to-countable transition. Backward: p0012 writes the same union identity and disjointness condition. Source recheck: bridge glyph is too short to distinguish “同理/故/于是”.

**Target IDs:** `T-P011-010`, `N-P011-010`, `N-P011-010-S1` (A/B each).

## Unresolved recovery records

- **VS-REC-004** (`RA07-P005-U007`): candidate A = “于是/从而” bridge; candidate B = “故/因此” bridge. Forward/backward/source checks are exactly those for p0005 U007 above; status remains unresolved until a source-level visual tie-break.
- **VS-REC-006** (`RA07-P006-U009`): candidate A = “由可测性” decomposition; candidate B = “若 E 可测，则” decomposition. Both satisfy the Carathéodory equation; source does not force one.
- **VS-REC-010** (`RA07-P011-U010`): candidate A = “同理/因而” finite-union bridge; candidate B = “故/于是” finite-to-countable bridge. Both are consistent with p0012; connective remains unresolved.

## Open issues (each has two candidates and checks)

### RA07-Q001 (p0001 question)
- **A:** “无限维可分赋范空间不存在平移不变非平凡测度”.
- **B:** “无穷维空间不存在同时平移不变、正规且非平凡的测度”.
Forward: both fit the subsequent measure/cardinality notes. Backward: p0002 outer measure and p0010 Vitali supply context but no unique quantifier. Source recheck: middle strokes are genuinely ambiguous; retain issue open.

### RA07-Q002 (p0003 Remark(2))
- **A:** `I_n` may be a **closed rectangle/closed box** (`[a_i,b_i]` product).
- **B:** `I_n` may be an **open rectangle/open box** (`(a_i,b_i)` product).
Forward: outer-measure covers permit either, with endpoint enlargement giving the same infimum; backward: p0002 uses closed intervals while p0004 uses arbitrary covers. Source recheck: bracket strokes are incomplete, so closed/open cannot be uniquely read.

### RA07-Q003 (p0010 Vitali)
- **A:** “取（令）V 为 Vitali 集，且 (V\subset[0,1])”.
- **B:** “将 V 视作 Vitali 集，在 (V\subset[0,1]) 后取有理平移”.
Forward: both produce the rational-translate contradiction and `[2,3]^c` line. Backward: p0011’s disjoint-union argument requires only the set and its translates. Source recheck: initial verb and the connective after “Vitali” are not unique.

### RA07-Q004 (p0011 connector before split)
- **A:** “待后有/随后有 (m^*(T\cap A)+m^*(T\cap A^c)=m^*(T))”.
- **B:** “从而/于是有 (m^*(T\cap A)+m^*(T\cap A^c)=m^*(T))”.
Forward: both make the displayed equality a valid Carathéodory step. Backward: p0006’s definition and p0012’s union formula support both. Source recheck: three connector glyphs cannot be separated reliably; keep neutral issue marker.

## Mapping and status

All IDs in `ledger-integration-v2.json` with status `unresolved` or `open` are covered above: 9 source units, 26 target/note units, 3 unresolved recoveries, and 4 issues. No old-unit record exists. Candidate pairs are intentionally preserved; selecting one requires a subsequent source recheck and ledger/draft synchronization by the coordinator.

## Explicit per-ID coverage index (mechanical audit)

Each row has two candidates by reference to the source-span entries above; retaining the reference avoids duplicating identical evidence while still giving every ledger ID its required pair.

| unresolved ID | candidate A | candidate B |
|---|---|---|
| RA07-P001-U013 | P1-A theorem reading | P1-B theorem reading |
| RA07-P003-U007 | P3-07-A outer-measure cover | P3-07-B prose cover |
| RA07-P003-U009 | P3-09-A inner/outer equality | P3-09-B Carathéodory implication |
| RA07-P005-U007 | P5-A “于是/从而” | P5-B “故/因此” |
| RA07-P006-U009 | P6-09-A “由可测性” | P6-09-B “若 E 可测，则” |
| RA07-P006-U014 | P6-14-A σ-algebra fragment | P6-14-B set-difference fragment |
| RA07-P010-U008 | P10-A “取/令 V” | P10-B “将 V 视作” |
| RA07-P011-U008 | P11-08-A “于是有” | P11-08-B “随后有/从而” |
| RA07-P011-U010 | P11-10-A “同理/因而” | P11-10-B “故/于是” |
| T-P001-013 | P1-A | P1-B |
| N-P001-013 | P1-A | P1-B |
| N-P001-013-S1 | P1-A | P1-B |
| N-P001-013-S2 | P1-A | P1-B |
| T-P003-007 | P3-07-A | P3-07-B |
| N-P003-007 | P3-07-A | P3-07-B |
| N-P003-007-S1 | P3-07-A | P3-07-B |
| T-P003-009 | P3-09-A | P3-09-B |
| N-P003-009 | P3-09-A | P3-09-B |
| T-P005-007 | P5-A | P5-B |
| N-P005-007 | P5-A | P5-B |
| N-P005-007-S1 | P5-A | P5-B |
| T-P006-009 | P6-09-A | P6-09-B |
| N-P006-009 | P6-09-A | P6-09-B |
| T-P006-014 | P6-14-A | P6-14-B |
| N-P006-014 | P6-14-A | P6-14-B |
| T-P010-008 | P10-A | P10-B |
| N-P010-008 | P10-A | P10-B |
| N-P010-008-S1 | P10-A | P10-B |
| N-P010-008-S2 | P10-A | P10-B |
| T-P011-008 | P11-08-A | P11-08-B |
| N-P011-008 | P11-08-A | P11-08-B |
| N-P011-008-S1 | P11-08-A | P11-08-B |
| T-P011-010 | P11-10-A | P11-10-B |
| N-P011-010 | P11-10-A | P11-10-B |
| N-P011-010-S1 | P11-10-A | P11-10-B |
| VS-REC-004 | P5-A | P5-B |
| VS-REC-006 | P6-09-A | P6-09-B |
| VS-REC-010 | P11-10-A | P11-10-B |
| RA07-Q001 | Q1-A | Q1-B |
| RA07-Q002 | Q2-A closed box | Q2-B open box |
| RA07-Q003 | Q3-A take/let Vitali | Q3-B view-as Vitali |
| RA07-Q004 | Q4-A “随后有” | Q4-B “从而有” |
