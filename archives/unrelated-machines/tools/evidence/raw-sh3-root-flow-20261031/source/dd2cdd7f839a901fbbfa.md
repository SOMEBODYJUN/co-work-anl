# Raw SH3 子树流的实数配额与单位走廊精度

2026-10-18. Author precision note to the two frozen raw-SH3 flow files. Their bytes are unchanged. This note does not claim an independent review, an integer decoder, or a new near-two hierarchy gap.

## 1. General native rows have a real demand

In the native model, an internal row owns k original jobs with home time 1/k and only unit alternatives. Let C be its unit incoming occupancy, H its home count, O=k-H, and 1<=T<2. The preceding M3 argument gives, for an original unit-entry endpoint E,

    L(E C O) >= k(2-T)L(E C).

The coefficient r=k(2-T) is a real rational number. Neither this inequality nor the resulting first-moment canonical subtree flow permits replacing r by ceil(r). An actual active row has the integer requirement O>=ceil(r), but the moment relaxation has not thereby acquired that integer requirement.

Consequently, an integer-fullquota half-star theorem cannot be applied after rounding r upwards. The frozen addendum's CONFIG first-moment reconstruction is restricted to the stated integral threshold grid (T-1)k integral. No arbitrary-grid CONFIG reconstruction follows from the real-demand inequality alone.

## 2. Extra full-row pair information makes k=1 corridors exact

There is an additional implication for a row with k=1. Its unique home endpoint Y has processing time one, and O=1-Y. Write C=sum_j R_j for all its original incoming unit endpoints. Complete same-row CONFIG(T) pair agreement, with T<2, supplies

    L(R_j Y)=0 for every j.                       (2.1)

These incoming/home pair zeros are additional to the incoming/incoming pair zeros used in the general real-demand proof. With M3 and the original Boolean ideals, the degree-two polynomial R_j Y has squared norm L(R_jY)=0, hence is orthogonal to every polynomial of degree at most three. In particular

    L(E C Y)=sum_j L(E R_jY)=0,
    L(E C O)=L(E C).                              (2.2)

Thus the conditional outgoing weights y_x=L(E C x) at this row sum exactly to b=L(E C). The topological construction can send outgoing total exactly a when the new incoming activity is a<=b: multiply all these y_x by a/b. It need not thin the outgoing total to (2-T)a.

A path of any explicit number of such k=1 rows therefore transmits its constructed first-moment flux without attenuation for every T<2. Merges still obey their unit incoming capacity. Empty or zero-mass rows use the zero branch. This is a consequence of the full row CONFIG pair information, not a consequence of the coefficient 2-T by itself. If only incoming/incoming pair zeros are assumed in an abstract system, the nonattenuating corridor conclusion is not claimed.

## 3. Mixed paths and soundness

One may use coefficient one at k=1 rows satisfying (2.1), and the real coefficient k(2-T) at other rows, in the same new canonical first-flow construction. In a layered product cut, replace only those k=1 coefficients by one. This preserves the original hypotheses and all sound-FAIL quantifiers: infeasibility of a necessary endpoint-rooted LP forces that endpoint's mass to zero; rejecting one endpoint or one proposed moment point does not alone prove OPT>T.

All formulas concern the explicit original jobs and a common M3 functional. No exact semidefinite feasibility finder, original moment extension, or unknown actual source solution is assumed. Rational construction and the corresponding ordinary LP tests retain polynomial total-bit complexity in their explicit input and moment certificate.
