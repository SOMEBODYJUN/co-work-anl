"""Replay the 24/5 certificate with exact fractions and no optimizer."""
from fractions import Fraction
from itertools import product
from pathlib import Path
import json

def validate():
    record = json.loads(Path(__file__).with_name("root-max-24-5-certificate.json").read_text())
    tau = Fraction(record["tau"])
    factor = Fraction(record["factor_exact"])
    weights = {name: Fraction(value) for name, value in record["nonzero_weights"].items()}
    if tau != Fraction(24, 5) or not 0 < factor < 2 or not all(v >= 0 for v in weights.values()):
        raise ValueError("Incorrect threshold, factor, or coefficient signs")
    minimum = None
    zeros = 0
    count = 0
    for bits, member in product(product((0, 1), repeat=12), (0, 1)):
        row = {}
        root = []
        for offset, label in ((0, "A"), (6, "B")):
            word = bits[offset:offset+6]
            load = sum(word)
            payoff = [Fraction(bit, load) if load else Fraction(0) for bit in word]
            root.append(payoff[0])
            for i in range(1, 6):
                bound = sum(word[:i]) + 6 - i
                row[f"{label}-F{i+1}"] = tau*payoff[i] - Fraction(member, bound)
                for j in range(12):
                    row[f"{label}-H{i+1}-{j+1}"] = payoff[i] - Fraction(bits[j], bound)
            prefix = sum(word[:4])
            row[f"{label}-R1/2"] = (tau*payoff[4] + payoff[5]/2
                                    - Fraction(member, prefix+1)
                                    + Fraction(member*word[4]*(prefix == 0), 4))
        for j, chosen in enumerate(bits, 1):
            row[f"CAP-{j}"] = bits[6] - chosen
        row["BRANCH-IC"] = root[0] - root[1]
        residual = factor*int(any(bits[:6])) - member - sum(
            coefficient*row[name] for name, coefficient in weights.items()
        )
        if residual < 0:
            raise ValueError(f"Negative residual at {bits}, {member}: {residual}")
        minimum = residual if minimum is None else min(minimum, residual)
        zeros += residual == 0
        count += 1
    if count != record["types"] or zeros != record["zero_types"]:
        raise ValueError("Replay counts differ from the certificate")
    return {"threshold":str(tau),"factor":str(factor),"rows":len(weights),
            "cases":count,"minimum_residual":str(minimum),"zero_cases":zeros}

if __name__ == "__main__":
    print(json.dumps(validate(), indent=2))
