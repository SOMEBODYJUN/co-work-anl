"""Independent exact check of the theta_2-versus-lambda_3 obstruction.

No repository solver is imported. All clients are different unit clients.
"""
from fractions import Fraction as F
from itertools import combinations

# Hub is 0; eight peripheral themes are 1,...,8. Each of 70 core
# clients likes the hub and exactly four peripheral themes. Each peripheral
# additionally has 24 private clients.
clients = [(0,) + c for c in combinations(range(1, 9), 4)]
for a in range(1, 9):
    clients.extend([(a,)] * 24)
themes = [{i for i, interests in enumerate(clients) if a in interests}
          for a in range(9)]
q = (F(0),) + (F(1, 8),) * 8

def utility(a, competitors):
    return sum((F(1, 1 + sum(x in themes[c] for c in competitors))
                for x in themes[a]), F(0))

alpha = [sum((q[b] * q[c] * utility(a, (b, c))
              for b in range(9) for c in range(9)), F(0))
         for a in range(9)]
lam = sum((q[a] * alpha[a] for a in range(9)), F(0))
assert len(clients) == 262
assert alpha[0] == F(245, 6)
assert all(v == F(997, 24) for v in alpha[1:])
assert lam == F(997, 24)
assert all(v <= lam for v in alpha)
assert all(q[a] == 0 or alpha[a] == lam for a in range(9))

br_against_hub = max(utility(a, (0,)) for a in range(9))
assert br_against_hub == F(83, 2)
theta = min(max(utility(a, (b,)) for a in range(9))
            for b in range(9))
assert theta == br_against_hub
assert lam - theta == F(1, 24)

# Choosing hub in the actual two-player game guarantees 105/2: each
# peripheral is a best response, and all give this same hub payoff.
hub_replies = [a for a in range(9)
               if utility(a, (0,)) == br_against_hub]
assert hub_replies == list(range(1, 9))
assert {utility(0, (a,)) for a in hub_replies} == {F(105, 2)}
assert F(105, 2) > lam

print({"unit_clients": len(clients), "lambda3": str(lam),
       "theta2": str(theta), "gap": str(lam-theta),
       "hub_first_guarantee": "105/2"})
