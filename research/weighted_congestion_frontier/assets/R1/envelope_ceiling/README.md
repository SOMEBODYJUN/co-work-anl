# A uniform ceiling for the standard two-attack envelope

## Claim identity

- ID/version: **WC-ENVELOPE-CEILING v1**.
- Objects: the two ratios in Christodoulou et al., arXiv:2002.07466v3, Theorem 1, equation (3).
- Domain/quantifiers: every integer d>=1, n>=1, 1<=k<=d, real 0<w<=1 and 0<=beta<=1. Let R be the minimum of those two ratios.
- Assumptions: only the stated parameter domain; in the conclusion with R>=exp(2), beta is necessarily positive.
- Definitions/scope: this is a necessary condition for that particular two-attack certificate. It is not an upper bound on the full-class equilibrium threshold, nor on the actual best equilibrium factor of the two-column topology.
- Exact statement/conclusion: if R>=exp(2), then

  $$R^2\le {8d\log\log R\over(\log R)^2}.$$

  Consequently, if log d>=16, then

  $$R\le\sqrt{128}\,{\sqrt{d\log\log d}\over\log d}.$$

- Dependencies: the exact equation (3); elementary logarithmic inequalities and maximization of u exp(-a u).
- Evidence: the general proof below; `verify.py` checks algebraic necessary conditions with exact rational arithmetic and the logarithmic inequality with Decimal numerical arithmetic.
- Counterevidence/objections: no fatal objection currently identified; the clean-attack review found no fatal objection; external review and priority remain unverified. Decimal tests are sanity checks, not rigorous interval enclosures or a universal proof.
- Status: complete proof, independently reconstructed and attacked by the clean-attack member; no external review. Truth proposed; value is a precise ceiling for a certificate mechanism; novelty unverified; mechanism is the coupling of light-player attenuation and the heavy-player load jump; ambition does not solve WC-TARGET v1.
- Related files: `../lower_family/sharp_envelope.md` (combined asymptotics, when available); branch MODEL.md, LITERATURE.md, CLAIMS.md; `verification.json`.
- Contribution: primary R3 research dialogue, publicly operating as R1; independent reconstruction also reported by the lower-family member.

## Proof

Set

$$E=(1+w)^d,\quad Q=\beta E,\quad B=(1+w)^k,\quad A=(1+nw)^k,$$

$$z={w\over1+w},\qquad y=nz,\qquad h=\log R.$$

The light-player inequality is

$$R(nw)^k+\bigl(R-(w/(1+w))^d\bigr)Q\le B.$$

Since R>1 and w/(1+w)<1, it follows that

$$0<y<1,\qquad y^k\le1/R,\qquad Q\le B/(R-1). \tag{1}$$

The heavy-player inequality gives

$$RA-1\le nQ(1-R/E). \tag{2}$$

Its left side is positive. Thus Q>0 and E>R. Combining (1) and (2), and using A>=1, gives

$$nB/A\ge (R-1)(R-1/A)\ge(R-1)^2\ge R^2/2. \tag{3}$$

For the last inequality, R>=exp(2)>4. In particular n>=R^2/2>=8, so z=y/n<1/8. Since E>R,

$$h/d<-\log(1-z)\le z/(1-z)<2z,$$

hence z>=h/(2d) and n=y/z<=2dy/h. Also

$$A/B=(1+(n-1)z)^k\ge(1+y/2)^k,$$

and k>=h/log(1/y) by (1). As log(1+y/2)>=y/4 for 0<y<1, (3) yields

$$R^2\le {4d\over h}\,y\exp\left(-{hy\over4\log(1/y)}\right). \tag{4}$$

For h>=2 the last scalar factor is at most 2 log h/h. Indeed, for y<=1/h it is at most 1/h<=2 log h/h. For y>1/h, log(1/y)<log h, and

$$y\exp\left(-{hy\over4\log(1/y)}\right)
\le y\exp\left(-{hy\over4\log h}\right)
\le {4\log h\over eh}< {2\log h\over h}.$$

The maximum in the second step is taken over all positive y. Substitution into (4) proves the first conclusion.

For the second conclusion write D=log d>=16, H=log D and S=sqrt(dH)/D. The function S(D)=exp(D/2)sqrt(log D)/D is increasing for D>=16, and S(16)>exp(2). If R<exp(2), then R<S. If exp(2)<=R<d^(1/4), again R<S: the ratio d^(1/4)/S=D exp(-D/4)/sqrt(log D) is decreasing for D>=16 and is less than one there. If R>=d^(1/4), h>=D/4>=4. The function log h/h^2 is decreasing for h>=2, so the first conclusion gives

$$R^2\le {8d\log(D/4)\over(D/4)^2}\le128S^2.$$

The w=0 boundary, outside the legal positive-weight domain, has heavy ratio one wherever interpreted; beta=0 likewise has heavy ratio at most one. Neither boundary affects any envelope supremum above one. No attainment of the supremum is assumed.

## Use and remaining obligation

This necessary condition can reject a proposed super-envelope certificate without optimizing n,k,w,beta. Together with the separate explicit lower construction, it identifies the order of the published certificate envelope. To improve beyond this order one must change the certificate or construction; the statement does not exclude another deviation cover on the same topology.

## Source and verification

Primary source checked 2026-10-14: https://arxiv.org/html/2002.07466v3#S3, Theorem 1, equation (3), with its two-state-class proof. No claim of original invention of the topology or two ratios is made.

Run from the repository root:

```sh
python3 research/weighted_congestion_frontier/assets/R1/envelope_ceiling/verify.py
```
