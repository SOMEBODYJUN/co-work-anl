# A strict greedy full-box lexicographic maximum need not be a customer equilibrium

Current counterexample, 2026-10-04. The exact instance and analytic classification below
refute one selector on the fixed greedy occupancy. They do not refute boxed
equilibrium existence, the greedy occupancy's factor-two feasibility, or a
different selector. An independent Fraction audit by Sol Attack agrees with the
greedy run, all 24 boxed states, the unique maximizer, and its failed client
inequality. No external review or priority claim is made.

## `SC-K-BOX-LEXMAX-NO`: selector being refuted

Run the canonical greedy procedure, keeping its fixed occupied sites,
multiplicities `q_t`, and positive final score `gamma`. Consider every feasible
assignment that gives each served client one covered occupied site and then
independently mixes uniformly among that site's facilities. Require the full
boxes `q_t gamma <= W_t <= (q_t+1)gamma`. Form the increasingly sorted vector
of all labeled facility revenues, repeating `W_t/q_t` exactly `q_t` times.
Choose a lexicographically greatest such vector and any assignment attaining
it. This rule does **not** require client NE among its candidates.

The instance below has a unique maximizing site assignment, and that assignment
fails exact client NE. Thus a different tie-breaking rule among maximizers
cannot repair this selector.

## Positive integer input and strict canonical greedy run

There are five common sites `H,M,N,L,R` and `k=11` labeled facilities. The
clients are:

| Client | Weight | Covered sites |
| --- | ---: | --- |
| `P_H` | 446 | H |
| `P_M` | 230 | M |
| `P_N` | 189 | N |
| `P_L` | 159 | L |
| `P_R` | 100 | R |
| `X` | 46 | H,M |
| `x` | 2 | H,M |
| `Y` | 82 | M,N |
| `y` | 81 | M,N |
| `Z` | 4 | N,L |
| `z` | 30 | N,L |

Every selected greedy score is the unique largest score, so the choice of tie
order is irrelevant. The sites and scores are:

| Insertion | Site | Score |
| ---: | --- | ---: |
| 1 | H | 494 |
| 2 | M | 393 |
| 3 | H | 247 |
| 4 | N | 223 |
| 5 | M | 393/2 |
| 6 | H | 494/3 |
| 7 | L | 159 |
| 8 | M | 131 |
| 9 | H | 247/2 |
| 10 | N | 223/2 |
| 11 | R | 100 |

Consequently `q=(4,3,2,1,1)`, `gamma=100`, and the original greedy assignment
has site totals `W^0=(494,393,223,159,100)`. Its light-client opening graph is
the consistently directed chain `H -> M -> N -> L`. Both clients of each edge
start at its earlier-opened endpoint. Each edge contains two different light
weights; every variable weight is strictly below `gamma`.

The full boxes are:

| Site | Full box |
| --- | --- |
| H | [400,500] |
| M | [300,400] |
| N | [200,300] |
| L | [100,200] |
| R | [100,200] |

## Analytic classification proving uniqueness of the boxed lexmax

R has its forced total 100 and contributes a fixed first coordinate 100. There
is a boxed candidate whose other facility revenues all exceed `223/2=111.5`:

`X:M, x:H, Y:M, y:N, Z:L, z:N`.

Its totals are `(448,358,300,163,100)`. Its increasingly sorted vector is

`(100, 112,112,112,112, 358/3,358/3,358/3, 150,150, 163)`.

In particular, its second coordinate is 112. Therefore any lexmax must have
every facility other than R strictly above 111.5. The following cases exhaust
all possible light-client assignments.

1. **X stays H.** If neither M--N client moves to N, then N's total is at most
   `189+4+30=223`, so an N facility has revenue at most 111.5. If at least one
   M--N client moves, M's total is at most `230+2+82=314`, so an M facility has
   revenue at most `314/3<111.5`. This case cannot maximize.
2. **X moves M and x also moves M.** H's total is 446, so its facility revenues
   are exactly 111.5. This case cannot maximize. Thus `X:M, x:H` is forced.
3. **Neither M--N client moves.** Again N's total is at most 223, so this case
   cannot maximize.
4. **Both M--N clients move.** Even if both N--L clients leave N, its total is
   at least `189+82+81=352>300`. This violates N's upper box. Thus exactly one
   M--N client moves.
5. **Y, of weight 82, moves N; y stays M.** M's total is 357. To respect N's
   upper box, `z`, of weight 30, must move to L: moving only `Z` would leave
   N at `189+82+30=301>300`. The two possible remaining choices have N totals
   275 or 271 and L totals 189 or 193. Both are boxed. H has revenue 112 and
   M has revenue 119, while N and L have larger revenues. Both lose to the
   displayed candidate at the first M coordinate, because `119<358/3`.
6. **y, of weight 81, moves N; Y stays M.** M's total is 358. At least one
   N--L client must leave N; otherwise N has total 304. The three boxed
   possibilities are:

   | N--L choices | N total | L total | N facility revenue |
   | --- | ---: | ---: | ---: |
   | Z:L, z:N | 300 | 163 | 150 |
   | Z:N, z:L | 274 | 189 | 137 |
   | Z:L, z:L | 270 | 193 | 135 |

   H and M contribute the same first eight coordinates after the fixed R
   coordinate in all three cases. N revenues precede L's revenue in all
   three. The first case uniquely wins at its first N coordinate.

Hence the displayed assignment is the **unique** full-box site assignment
with lexicographically greatest increasingly sorted facility revenues. The
classification above is exhaustive and does not infer uniqueness from a
finite numerical search.

## The unique maximizer is not an exact customer NE

For a client of weight w assigned to site s, site-uniform exact client NE
requires `(W_s-w)/q_s <= W_t/q_t` for every occupied covered alternative t.
The common additional own-weight term cancels in this comparison.

At the unique maximizer, client Z, of weight 4, is at L. Its external cost is
`(163-4)/1=159`, while N's normalized load is `300/2=150`. Thus Z strictly
improves by returning L->N. The new N total would be `304>300`, so the move
is blocked by the full-box constraint. Its true conditional costs are 163
at L and 154 at a facility at N. The other five variable clients satisfy
their site NE inequalities; Z is the sole strict improvement.

## A boxed exact customer NE exists at this same occupancy

The original greedy assignment already has all clients at best responses.
Its variable-client comparisons are:

| Client | Source external cost | Alternative normalized load |
| --- | ---: | ---: |
| X:H | 112 | 131 |
| x:H | 123 | 131 |
| Y:M | 311/3 | 223/2 |
| y:M | 104 | 223/2 |
| Z:N | 219/2 | 159 |
| z:N | 193/2 | 159 |

Each source quantity is at most its alternative quantity. Every private client
has only its own occupied site. Independent uniform mixing within each site
therefore gives an exact customer NE in all five boxes. BOX-TO-2 applies to
that initial NE. The bad lexmax result is consequently an obstruction to the
specified **selection rule**, with no claim of boxed-NE nonexistence or a
factor-two lower bound for the greedy layout.

## Exact audit artifact

The exact audit `tests/audits/kfac_box_lexmax.py` reimplements strict greedy scores
and enumerates all 64 binary site assignments with Fraction arithmetic. Exactly
24 satisfy all boxes; it confirms the unique maximizer and initial exact NE.
The analytic proof above supplies the full argument for this explicit instance.
