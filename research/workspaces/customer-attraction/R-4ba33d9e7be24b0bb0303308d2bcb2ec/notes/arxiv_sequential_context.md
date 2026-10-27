# Literature context: Deng et al. (2023), sequential CAG

**Status:** literature background only; no claim about Q-CAG-HALF-6 and no promotion of the paper's results to this repository's exact model.

Source: Xiaotie Deng, Hangxin Gan, Ningyuan Li, Weian Li, Qi Qi, *Equilibrium Analysis of Customer Attraction Games*, arXiv:2307.07174v2, especially §2 and §5, [public HTML](https://arxiv.org/html/2307.07174v2). The paper's Theorem 5.2 states that the sequential price of anarchy is (3/2) for two symmetric agents and gives a lower bound (2-1/|A|) for more agents. The paper explicitly leaves the upper bound 2 for more than two agents as a conjectural direction (its §6 discussion). Thus the six-agent half-coverage target is consistent with the known literature gap.

## Model correspondence

The paper's symmetric sequential CAG has a finite customer/node set, a common strategy/topic catalog, unit agent weights in the symmetric case, and proportional splitting of each attracted node's value among the agents selecting a topic containing that node. Its social welfare is the number/value of attracted customers, matching the identity (W=\sum_i u_i) when every customer is unit-valued.

Our exact Q-CAG-MODEL fixes a narrower but history-strong setting: a finite **unit** customer set; one common finite catalog (\mathcal S\subseteq2^N); exactly (m) providers choosing in the fixed order (1,\ldots,m); every provider observes the entire ordered history; and a complete pure SPE quantifying every ordered off-path history and every tie. Repeated and empty themes, zero customers, and arbitrary history-dependent tie choices remain allowed. The target is, for every such SPE terminal outcome, (2W\ge OPT_m), where (OPT_m) is the best union of (m) catalog themes.

The paper's notation permits a more general asymmetric model (agent strategy spaces, weights, and customer values), and its sequential section's theorem is an efficiency statement over the paper's sequential-game class. It does not supply a proof of the all-(m\ge3) upper bound 2, nor a certificate for our full-history pure-SPE quantifiers. Accordingly this note is only a map to prior context; it is not an imported theorem.

## Reusable mathematical hint, with a boundary

The paper's static PoA proof uses the harmonic potential (\Phi(s)=\sum_x H_{c_x(s)}) and a duplicated equilibrium profile. In the sequential game, a player's terminal utility is the marginal of (\Phi) when that player's topic is inserted while later loads are held fixed. This identity is useful for checking candidate dynamic telescoping arguments, but it does not by itself imply that a complete SPE maximizes (\Phi), and it does not justify replacing an off-path continuation by a fixed or anonymous continuation. Any use here must preserve the ordered-history continuation selected by the original SPE.
