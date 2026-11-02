"""Attack monotonicity of incumbent utility under a later clone deviation."""
import json
import random
from customer_attraction import CustomerType, Instance, ExactSPESolver, verify_certificate


def follow(instance, cert, history):
    while len(history) < instance.players:
        history += (cert.actions[history],)
    return history


def probe(seed=20261023, trials=2000):
    rng = random.Random(seed)
    for it in range(trials):
        types = tuple(CustomerType(frozenset(a for a in range(4) if mask >> a & 1), r)
                      for mask in range(1, 16) if (r := rng.randrange(4)))
        inst = Instance(tuple("ABCD"), types, 3)
        solver = ExactSPESolver(inst)
        for path in solver.ordered_outcomes():
            cert = solver.certificate(on_path=path)
            for i in range(1, 3):
                for j in range(i):
                    if path[i] == path[j]:
                        continue
                    clone = follow(inst, cert, path[:i] + (path[j],))
                    before = inst.player_payoffs(path)[j]
                    after = inst.player_payoffs(clone)[j]
                    if after > before:
                        verify_certificate(inst, cert).assert_valid()
                        return {"seed": seed, "trial": it, "instance": inst.to_dict(),
                                "certificate": cert.to_dict(), "path": path,
                                "clone_position": i, "incumbent_position": j,
                                "clone_path": clone, "before": str(before), "after": str(after)}
    return {"seed": seed, "trials": trials, "found": False}


if __name__ == "__main__":
    print(json.dumps(probe(), indent=2))
