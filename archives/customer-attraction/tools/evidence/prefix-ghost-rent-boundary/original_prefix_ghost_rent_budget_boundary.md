# Unweighted prefix ghost-rent errors cannot be paid once by root coverage

Exploratory mechanism boundary, 2026-10-21. General Q-CAG-HALF remains OPEN.
This does not refute any claimed complete global transport theorem. It rules
out the explicit natural reserve inequality below; a weighted transport is
not addressed. The motivating r=2,s=1 pair-circuit error is being studied by
the direct_global agent; this note only analyzes its ghost-rent form.

Let Ω be an auxiliary universal topic, and for a prefix H and two topics A,B
define the old-provider rent loss

\[
 E_H(A,B)=\sum_{j\in H}\{U_j(H+\Omega)-U_j(H+\Omega+A+B)\}.
\]

For true coverage this is nonnegative customer by customer; the same
positivity holds for common monotone submodular Shapley payoffs by the
positive marginal/clock representation. Ω is only an algebraic auxiliary,
not a legal deviation.

Consider the legal catalogue A={x,z}, B={x}, two unit customers, m providers.
Choosing A strictly dominates choosing B at every history and continuation:
the x share is identical for the two actions, and A adds the strictly
positive z share. Thus the strategy choosing A at every ordered history is
a complete pure SPE, and actual W=2.

At the actual prefix H=A^h, customer x is hit by both A,B while z is hit only
by A. Directly,

\[
 E_{A^h}(A,B)=\frac{2h}{(h+1)(h+3)}+
             \frac{h}{(h+1)(h+2)}.
\]

For c>=1, summing over the first c actual prefix lengths gives

\[
 \sum_{h=0}^{c-1}E_{A^h}(A,B)
 =3H_c+\frac5{c+1}+\frac3{c+2}-\frac{13}2.
\]

Take m=9,c=7. Every auxiliary profile in this sum has at most m providers,
since h+3<=9, but the sum is 1879/840>2=W by 199/840. It diverges
logarithmically as c grows. Hence the concrete proposed reserve inequality

\[
 \sum_{h=0}^{m-3}E_{A^h}(A,B)\le W
\]

is false even on this two-topic complete SPE. Merely observing that all
errors are supported on already covered prefix customers does not establish
a once-per-client root budget.

Scope detail: these auxiliary rent profiles have varying total populations
at different h. The note does not assert that a valid transport certificate
for one fixed m actually uses all these r=2,s=1 circuit errors with unit
multipliers. That multiplicity/weight obligation is exactly what a global
construction would need to supply.

For one added hit rather than two, a customer with prefix load h has old-rent
loss h/((h+1)(h+2)), which is h times the increment of rho(h)=h/(h+1).
A 1/h factor would make that particular sum telescope, but h is customer
dependent and cannot simply be substituted for a legal whole-row multiplier.
This indicates the weight needed, without constructing the global transport.
