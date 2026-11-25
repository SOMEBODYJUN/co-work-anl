# RA07 finite forward/backward mathematics checks

These are finite consistency checks for the candidate pairs; they do not turn a visually uncertain glyph into a certain transcription.

## 1. Outer-measure cover candidates (p0003 U007/U009)

For either candidate cover family `I_k` (closed boxes) or `R_k` (open boxes), define
\[
 m^*(E)=\inf\left\{\sum_k |Q_k|:E\subseteq\bigcup_k Q_k\right\}.
\]
If `Q_k` is enlarged by an arbitrarily small factor, open and closed boxes have the same infimum. For `E⊂⋃Q_k` and `E=E_1∪E_2`, splitting each `Q_k` gives
\[
 m^*(E)\le m^*(E_1)+m^*(E_2),
\]
which is the forward check used by every p0003 candidate. The p0004/p0006 Carathéodory line then requires, for measurable `E`,
\[
 m^*(T)=m^*(T\cap E)+m^*(T\cap E^c).
\]
Thus candidate A (inner/outer equality) and candidate B (Carathéodory condition) both point to the same subsequent formula; neither is excluded by algebra alone.

## 2. Carathéodory connector candidates (p0005 U007, p0006 U009, p0011 U008)

Set `T_1=T∩E`, `T_2=T∩E^c`; they are disjoint and `T=T_1∪T_2`. For a measurable `E`, the defining equality is exactly
\[
 m^*(T)=m^*(T_1)+m^*(T_2).
\]
Replacing a connector “于是/故/若…则/从而” does not alter the formula. Conversely, p0004’s complement split and p0012’s set algebra force the terms to be `E` and `E^c`; a candidate using a different set would fail the backward check and is rejected.

## 3. Finite-to-countable additivity (p0011 U010)

For disjoint measurable `A_1,\ldots,A_N`, induction from the two-set identity yields
\[
 m\!\left(\bigcup_{i=1}^N A_i\right)=\sum_{i=1}^N m(A_i).
\]
For a countable family, continuity from below gives
\[
 m\!\left(\bigcup_{i\ge1} A_i\right)=\lim_N\sum_{i=1}^N m(A_i)=\sum_{i\ge1}m(A_i).
\]
Both candidate bridges (“同理/因而” and “故/于是”) are valid prose for this step; p0012 confirms the symbols and disjointness condition.

## 4. Vitali candidates (p0010 U008/Q003)

Choose one representative from each equivalence class of `x-y∈Q` in `[0,1]`, obtaining `V⊂[0,1]`. For `q∈Q∩[-1,1]`, the translates `V+q` are pairwise disjoint and
\[
 [0,1]\subseteq\bigcup_{q\in Q\cap[-1,1]}(V+q)\subseteq[-1,2].
\]
If `V` were measurable with `m(V)=0`, the union would have measure 0, contradicting `m([0,1])=1`; if `m(V)>0`, countable disjointness gives an infinite measure inside `[-1,2]`, contradiction. This validates both “取/令 V 为 Vitali 集” and “将 V 视作 Vitali 集” readings. The visible `[2,3]^c`/translated interval is consistent after shifting the base interval.

## 5. p0001 Q001 theorem-family check

A translation-invariant nontrivial measure on all subsets of an infinite-dimensional normed space would conflict with countably many disjoint translates of a bounded set (the same counting mechanism as Vitali). A weaker reading restricted to separable infinite-dimensional spaces is also coherent. The page’s later Dirac measure and cardinality reminders do not force whether “可分/正规” is present, so A/B remain live.

## 6. p0006 edge fragment U014

The visible neighboring text supports either the σ-algebra closure heading or the set-difference identity. Algebraically,
\[
 A\setminus B=A\cap B^c,
\]
and closure under complement/intersection implies closure under difference; hence both candidates are mathematically compatible with p0006→p0009. No finite calculation distinguishes the cropped glyph.

## 7. Candidate rejection rules

Reject any reading that (i) changes `m^*` to `m` before measurability is established, (ii) replaces `E^c` by an unrelated set, (iii) makes Vitali translates overlap, or (iv) asserts a countable union equality without disjointness/measurability. None of the retained A/B pairs violates these checks.
