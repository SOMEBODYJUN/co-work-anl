"""Independent integer-arithmetic reconstruction of the frozen six-provider ledger."""
import hashlib
import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
RUN = ROOT / "research/runs/n6-boss2-astra-20261118"
FREEZE = "9fc7aa6c0c97d0449a511682f7dc7a9cb0cd937c59c2247c7a1f060e0ea7947c"


def read(path):
    return json.loads(path.read_text())


def exact_div(a, b):
    value, remainder = divmod(a, b)
    assert remainder == 0
    return value


def reconstruct():
    frozen = read(RUN / "studio/freezes/SIX-FC-71-15-R1" / (FREEZE + ".json"))
    for ref in frozen["content_refs"]:
        content = (ROOT / ref["path"]).read_bytes()
        assert hashlib.sha256(content).hexdigest() == ref["sha256"], ref
        if ref["path"].endswith(".json"):
            json.loads(content)
    packet = read(RUN / "packet-full.json")
    obstacle = read(RUN / "packet-obstacle.json")
    spec = read(ROOT / "research/workspaces/n6-boss2-astra-20261118/spec.json")
    for cp in (packet, obstacle):
        assert cp["target"] == (ROOT / spec["problem"]["path"]).read_text()
        assert cp["definitions"] == [(ROOT / d["path"]).read_text() for d in spec["definitions"]]
    assert packet["context"]["seed_ids"] == spec["seed_ids"]
    assert frozen["application_refs"] == []
    evidence = ROOT / "tools/evidence/six-fractional-cover-71-15"
    replay = read(evidence / "exact-replay.json")

    denominator = 15694520331
    f_weight = {2:2855229330, 3:3594568740, 4:4772603160, 6:6679333080}
    h_weight = {(1,4):1894381596, (1,5):9747236520, (1,6):6589896378,
                (2,6):5443408970, (3,6):4067148532}
    tail_weight = 5954631480
    all_weights = {f"F{i}":v for i, v in f_weight.items()}
    all_weights.update({f"H{i}_{j}":v for (i,j),v in h_weight.items()})
    all_weights["R1/2"] = tail_weight
    source = read(evidence / "certificate.json")
    assert source["integer_multipliers"] == all_weights
    assert source["common_denominator"] == denominator
    assert Fraction(source["tau"]) == Fraction(71, 15)

    bank = {}
    scale = 1800
    for mask in range(64):
        players = {j for j in range(1,7) if mask & (1 << (j-1))}
        capacity = {j:6-len(set(range(1,j))-players) for j in range(1,7)}
        load = len(players)
        hits = lambda j: int(j in players)
        key = tuple(hits(j) for j in range(1,7))
        for target in (0,1):
            # Charge income, restore each deviation debit directly, then subtract
            # the nonnegative tail price refund. Everything is on a single integer grid.
            balance = denominator * scale * (2*int(bool(players))-target)
            income = 0
            for j,multiplier in f_weight.items():
                income += exact_div(scale*71*hits(j), 15*max(1,load))*multiplier
                balance += exact_div(scale*target,capacity[j])*multiplier
            for (i,j),multiplier in h_weight.items():
                income += exact_div(scale*hits(i),max(1,load))*multiplier
                balance += exact_div(scale*hits(j),capacity[i])*multiplier
            income += tail_weight*(exact_div(scale*71*hits(5),15*max(1,load))+
                                   exact_div(scale*hits(6),2*max(1,load)))
            past = len(players & {1,2,3,4})
            balance += tail_weight*exact_div(scale*target,1+past)
            if target and hits(5) and past == 0:
                balance -= tail_weight*exact_div(scale,4)
            balance -= income
            assert balance >= 0, (mask,target,balance)
            bank[key,target] = Fraction(balance, scale*denominator)
    archived = {(tuple(row["e"]),row["o"]):Fraction(row["remainder"]) for row in replay["residuals"]}
    assert len(replay["residuals"]) == len(archived) == 128 and bank == archived
    print("checked",len(frozen["content_refs"]),"frozen digests;",len(bank),"distinct exact integer coefficients")
    print("zero",sum(v == 0 for v in bank.values()),"least positive",min(v for v in bank.values() if v>0))
    print("smallest positive types",[(k,e) for (k,e),v in bank.items() if v==min(k for k in bank.values() if k>0)])
    print("scope: all client coefficients; conditional bound alone")


if __name__ == "__main__":
    reconstruct()
