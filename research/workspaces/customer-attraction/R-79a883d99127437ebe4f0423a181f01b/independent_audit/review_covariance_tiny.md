# Independent review: a clientwise covariance monotonicity assertion is false

2026-10-24. Independent definition-level reconstruction completed. The
reviewer received the instance, prescribed complete strategy and distribution
before receiving the peer's definitions or proof, and reconstructed all
subgame comparisons first. No peer proof or implementation was imported.

## Contract and verdict

For root forced action F drawn from p, let Z(F) be its actual continuation,
q_x=P(x in F), and h_F(x)=c_x(Z(F))-1_(x in F). Define

    H0_x=E[1/(h_F(x)+1) | x not in F],
    H1_x=E[1/(h_F(x)+1) | x in F],
    D_x=E[1_(x in F)/(h_F(x)+1)],
    C_x=E[q_x/(1+c_x(Z(F)))].

The proposed universal implication H0_x<=H1_x is false, even for a
two-player complete pure SPE. In the example below C_x-D_x=1/12>0 for x.
This does not refute a sum over clients, any aggregate safety bridge, or
Q-CAG-HALF. The aggregate here is paid strictly.

## Complete game and all subgames

There are four unit clients x,y,z,w and common catalog

    A={x,z}, B={y}, D={x,y}, E={z,w}.

The root chooses D. The last replies after A,B,D,E are respectively D,E,E,D.
Every possible one-action history is present. In the following table columns
are the four possible actions A,B,D,E of the player currently moving.

| decision history | payoff after A | after B | after D | after E | prescribed |
|---|---:|---:|---:|---:|---|
| root, following prescribed future replies | 3/2 | 1 | 2 | 2 | D |
| A | 1 | 1 | 3/2 | 3/2 | D |
| B | 2 | 1/2 | 3/2 | 2 | E |
| D | 3/2 | 1/2 | 1 | 2 | E |
| E | 3/2 | 1 | 2 | 1 | D |

Each prescribed action is a row maximum. This verifies all five decision
nodes and all twenty including-self comparisons, including off-path ties.
The root row uses the actual specified last reply after each root action;
it does not freeze the actual E reply after a root deviation.

The actual terminal is (D,E), with utilities (2,2), W=4 and OPT_2=4 because
D and E are disjoint and cover the entire four-client universe. The topic
sets are distinct; repetitions are legal and included among the table's
actions. All players and clients have unit weight.

## Clientwise computation and aggregate accounting

Take p(A)=p(B)=1/2 and p(D)=p(E)=0. The forced terminal paths are
Z(A)=(A,D) and Z(B)=(B,E). For x, h_A(x)=1 and h_B(x)=0, whereas x belongs
to A and not to B. Thus H0_x=1>1/2=H1_x. Direct calculation gives the
following complete client table. A dash means the conditional event has
probability zero, so that conditional expectation need not be defined.

| client | q | H0 | H1 | D | C | C-D |
|---|---:|---:|---:|---:|---:|---:|
| x | 1/2 | 1 | 1/2 | 1/4 | 1/3 | 1/12 |
| y | 1/2 | 1/2 | 1 | 1/2 | 1/4 | -1/4 |
| z | 1/2 | 1/2 | 1 | 1/2 | 1/4 | -1/4 |
| w | 0 | 3/4 | — | 0 | 0 | 0 |

Consequently D=5/4, C=5/6, and D-C=5/12>0. The actual root payoff is 2,
so its incentive slack is e=2-D=3/4 and

    u_root-C = 7/6 = e+(D-C).

The positive x deficit is more than paid by y and z. The failure concerns
clientwise conditional monotonicity and clientwise nonnegative adaptation
credit only. It is not an aggregate or welfare counterexample.

## Reproducibility and status

`audit_covariance_tiny.py` independently constructs every payoff using the
four explicit sets and exact Fraction arithmetic. It imports neither the
canonical solver nor the peer's program. Its assertions cover all complete
SPE comparisons, every table entry and the aggregate identity. This is an
exact finite counterexample to the stated universal auxiliary assertion,
not negative-search evidence or a general positive theorem.
