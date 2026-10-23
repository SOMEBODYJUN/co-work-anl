"""Independent replay of the uploaded 34-unit-client strategy certificate.

No discovery/review/solver code is imported. Exact arithmetic only; this checks
one counterexample and does not infer a universal claim from finite searches.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[5]
SOURCE = ROOT / "research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/representation/terminal_pushforward_34_D_lt_C_exact.json"


def main():
    data = json.loads(SOURCE.read_text())
    inst = data["instance"]
    clients = [set(c["topics"]) for c in inst["customers"]
               for _ in range(c["multiplicity"])]
    m, n = inst["players"], len(inst["topics"])
    policy = {tuple(e["history"]): e["action"]
              for e in data["certificate"]["actions"]}

    def finish(history):
        a = list(history)
        while len(a) < m:
            a.append(policy[tuple(a)])
        return tuple(a)

    def share(a, topic, extra=0):
        return sum((F(1, sum(t in likes for t in a) + extra)
                    for likes in clients if topic in likes), F())

    checked = 0
    for k in range(m):
        for h in product(range(n), repeat=k):
            actual = finish(h)
            chosen = policy[h]
            u = share(actual, chosen)
            for t in range(n):
                if t == chosen:
                    continue
                assert u >= share(finish(h+(t,)), t)
                checked += 1

    actual = finish(())
    u = [share(actual, t) for t in actual]
    W = sum(u, F())
    assert W == sum(any(t in likes for t in actual) for likes in clients)
    rows = []
    for i in range(m):
        zq = finish(actual[:i] + (2,))
        ze = finish(actual[:i] + (6,))
        rows.append({"i": i+1, "Z_query": zq, "Z_empty": ze,
                     "D": share(zq, 2),
                     "H_empty": share(ze, 2, 1),
                     "G_query": share(zq, 2, 1)})
    D = sum((r["D"] for r in rows), F())
    H = sum((r["H_empty"] for r in rows), F())
    G = sum((r["G_query"] for r in rows), F())
    assert (D,H,G) == (F(63,2),F(65,2),F(41,2))
    eps = F(1,24)
    p = {2:eps,6:1-eps}
    DD = GG = F()
    for i in range(m):
        for t,pt in p.items():
            z = finish(actual[:i] + (t,))
            DD += pt*share(z,t)
            for s,ps in p.items():
                GG += pt*ps*share(z,s,1)
    assert DD == eps*D and GG == eps*(1-eps)*H + eps*eps*G
    assert (DD,GG,DD-GG) == (F(21,16),F(4,3),F(-1,48))
    assert W-DD == F(491,16)
    opt = max(sum(any(t in likes for t in a) for likes in clients)
              for a in product(range(n), repeat=m))
    print(json.dumps({"source":str(SOURCE.relative_to(ROOT)),
                      "method":"expanded unit customers; Fraction; independent replay",
                      "clients":len(clients),"histories":len(policy),
                      "nonself_deviations":checked,"actual":actual,
                      "u":u,"W":W,"OPT":opt,"rows":rows,
                      "D":D,"H_empty":H,"G_query":G,"epsilon":eps,
                      "D_epsilon":DD,"G_epsilon":GG,"gap":DD-GG,
                      "root_slack":W-DD},default=str,indent=2))


if __name__ == "__main__":
    main()
