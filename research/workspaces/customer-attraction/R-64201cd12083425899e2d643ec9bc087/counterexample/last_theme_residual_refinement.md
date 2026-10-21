# Residual refinement of the final-theme containment condition

Status: additional candidate extension, exact algebra checked locally,
independent review agreed with the algebra and supplied the maximality
clarification below. This keeps the positive residual from
`last_theme_containment.md` instead of dropping it.

Use that file's notation. Let `g` be the number of actual themes containing
`B=S_m`, let `k` be the number of actual themes exactly equal to `B`, and
put `d=m-g` and `h=m-k`. Thus `0<=d<=h<=m-1`. These count chosen sets,
not distinct labels. **In an actual SPE, maximality of the last best
response implies `g=k` and `d=h`**: a strict catalog superset of `B` would
strictly improve the last player's payoff at its fixed prefix. The
two-parameter presentation below is an algebraic relaxation of the actual
situation, not a stronger genuine model range. The substantive sufficient
condition is (4). Write `S=|B|`, `V=W-S`, and

\[
R=\sum_{x\in(\cup_i S_i)\setminus B}\frac1{c_x+1}.
\]

The preceding argument gives

\[
\operatorname{OPT}_m\le W+(m-1)u-R,
\quad gu\le S\le mu,
\quad V\ge g(u-S/m).
\tag{1}
\]

Every customer outside `B` is covered by at most the `h` players whose
actual sets differ from `B`, so `R>=V/(h+1)`. Therefore

\[
W+R\ge S+\frac{h+2}{h+1}V
\ge S+\frac{h+2}{h+1}g(u-S/m).
\tag{2}
\]

The final expression is affine in `S` on `[gu,mu]`. Its two endpoint
values are

\[
\left[g+\frac{(h+2)gd}{m(h+1)}\right]u,
\qquad mu.
\]

The second is always at least `(m-1)u`. The first is at least `(m-1)u`
exactly when

\[
\boxed{m(h+d+1)\ge d^2(h+2).}
\tag{3}
\]

Under (3), equation (2) implies `W+R>=(m-1)u`, and equation (1) gives
`OPT_m<=2W`. This proof uses no division by `u` and covers `u=0`, `m=1`,
and `d=h=0`.

In every actual SPE, every catalog theme containing `B` equals `B`, so
`g=k` and `h=d`, and (3) becomes

\[
m(2d+1)\ge d^2(d+2).
\tag{4}
\]

For example, seven players with four exact copies of the last theme and
no proper superset choice have `d=h=3` and satisfy `49>=45`. This is a
half-coverage subcase beyond the simpler `(m-g)^2<=m` condition. It does
not resolve five players whose last theme occurs once or twice.

The extension contains the basic sufficient condition: when `d^2<=m`,
the difference in (3) is at least
`m(h+d+1)-m(h+2)=m(d-1)>=0` for `d>=1`; `d=0` is immediate.

Audit: `last_theme_residual_refinement_audit.py` checks the exact endpoint
algebra and all count triples through `m=60`, plus all selected canonical
SPE paths used in `last_theme_containment_audit.py`.
