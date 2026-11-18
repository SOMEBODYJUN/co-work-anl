"""One 13-label completion of the exact marginal obstruction, then exact SPE.

Retains only the eight shared membership bits, plus six comparison labels.
The relaxation's hidden replies are not assumed to carry over.
"""

from collections import defaultdict
from fractions import Fraction
from functools import cache
from itertools import combinations_with_replacement
from math import lcm
from pathlib import Path
import json

from probe_glued_branches import anchors

PLAYERS = 6
LABELS = 13
SCALE = 60


def game():
    witness = Path(__file__).with_name("tau-six-marginal-relaxation-witness.json")
    raw = defaultdict(Fraction)
    for (branch, i, tail), value in json.loads(witness.read_text())["mass"]:
        if branch is None:
            anchor, member = anchors[i]
            indices = tuple(j for j, bit in enumerate(anchor) if bit)
            if member:
                for j in range(7, LABELS):
                    raw[indices+(j,)] += Fraction(value)/6
            elif indices:
                raw[indices] += Fraction(value)
    unit_multiplier = lcm(*(v.denominator for v in raw.values()))
    return {labels:int(value*unit_multiplier) for labels,value in raw.items()},unit_multiplier


def solve(weights):
    @cache
    def terminal(counts):
        values = [0]*LABELS
        w = 0
        for labels, mass in weights.items():
            c = sum(counts[i] for i in labels)
            if c:
                share = (SCALE//c)*mass
                w += mass
                for i in labels:
                    values[i] += share
        return tuple(values), w

    @cache
    def all_spe(counts):
        if sum(counts) == PLAYERS:
            return (counts,)
        sons, minimum = menu(counts)
        value = max(minimum)
        return tuple(set(c for j, child in enumerate(sons) for c in child
                         if terminal(c)[0][j] >= value))

    def menu(counts):
        sons = [all_spe(counts[:j]+(counts[j]+1,)+counts[j+1:]) for j in range(LABELS)]
        minimum = [min(terminal(c)[0][j] for c in child) for j, child in enumerate(sons)]
        return sons, minimum

    outcomes = all_spe((0,)*LABELS)
    worst = min(outcomes, key=lambda c: (terminal(c)[1],c))
    feasible = (tuple(seq.count(j) for j in range(LABELS))
                for seq in combinations_with_replacement(range(LABELS), PLAYERS))
    opt = max(terminal(c)[1] for c in feasible)
    projected = tuple(int(i<6) for i in range(LABELS))
    proposed_payoffs = terminal(projected)[0]
    ordered_obstructions = []
    for i in range(PLAYERS):
        prefix = tuple(int(j<i) for j in range(LABELS))
        _, minimum = menu(prefix)
        best = max(minimum)
        if best > proposed_payoffs[i]:
            ordered_obstructions.append({"actual_position":i+1,
                 "deviation_label":minimum.index(best),
                 "strict_gain_over_proposed_leaf":str(Fraction(best-proposed_payoffs[i],SCALE*opt))})
    return {"labels":LABELS,"nonzero_unit_customer_types":len(weights),
            "all_spe_terminal_count_vectors":len(outcomes),
            "worst_counts":worst,"W":terminal(worst)[1],"OPT6":opt,
            "ratio_exact":str(Fraction(terminal(worst)[1],opt)),
            "projected_path_W":terminal(projected)[1],
            "projected_path_is_spe_outcome":projected in outcomes,
            "ordered_obstructions_as_share_of_OPT6":ordered_obstructions,
            "cached_continuation_states":all_spe.cache_info().currsize}


if __name__ == "__main__":
    weights,normalization = game()
    result=solve(weights)
    print(json.dumps({**result,"target_block_total":normalization,"input_types":len(weights)},indent=2))
