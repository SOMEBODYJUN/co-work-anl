"""Independent integer reconstruction from the input only.

Does not import the parent's verifier or the repository CAG implementation.
All sums are in units of 1/60; the customer list is expanded literally.
"""
from itertools import combinations_with_replacement
from pathlib import Path
from fractions import Fraction
import json

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "parent" / "suffix_envelope_input.json"
data = json.loads(SOURCE.read_text())
m = data["m"]
actual = tuple(data["actual"])
topic_count = len(data["catalog_order"])
assert m == 6 and topic_count == 12
customers = []
for block in data["mask_weights"]:
    for j in range(m):
        interests = frozenset(i for i in range(m) if block["actual_mask"] >> i & 1) | {m+j}
        customers.extend([interests] * block["multiplicity_per_T_index"])
assert len(customers) == 6000
catalog = [frozenset(i for i,x in enumerate(customers) if a in x)
           for a in range(topic_count)]
assert len(set(catalog)) == topic_count

# Integer 60-scaled arithmetic; no floating values and no omitted denominators.
def share(k):
    assert 1 <= k <= 6
    return 60 // k

actual_load = [sum(a in x for a in actual) for x in customers]
profits = [sum(share(c) for x, c in zip(customers, actual_load) if a in x) for a in actual]
welfare = sum(c > 0 for c in actual_load)
assert sum(profits) == 60*welfare
assert welfare == 2940
assert all(any(a in x for a in range(m,2*m)) for x in customers)
optimum = len(customers)  # T1,...,T6 covers every customer; nothing covers > N.

safe = []
suffixes = []
for i in range(m):
    background = [sum(a in x for a in actual[:i]) for x in customers]
    r = m-i
    for a in range(topic_count):
        query = sum(share(b+r) for x,b in zip(customers,background) if a in x)
        safe.append({"position":i+1,"query":a,"slack":str(Fraction(profits[i]-query,60))})
        assert profits[i] >= query
    tax = 0
    for j in range(i,m):
        previous = [sum(a in x for a in actual[:j]) for x in customers]
        tax += sum(share(p+1)-share(p+m-j)
                   for x,p in zip(customers,previous) if actual[j] in x)
    budget = sum(profits[i:]) + tax
    max_potential = -1
    maximizing = None
    comparisons = 0
    # Group equal interest sets solely to speed this independent computation.
    counts = {}
    for x,b in zip(customers,background):
        counts[x,b] = counts.get((x,b),0)+1
    for comparison in combinations_with_replacement(range(topic_count),r):
        comparisons += 1
        potential = 0
        for (x,b),multiplicity in counts.items():
            d = sum(a in x for a in comparison)
            potential += multiplicity*sum(share(q) for q in range(b+1,b+d+1))
        if potential > max_potential:
            max_potential,maximizing = potential,comparison
        assert potential <= budget
    suffixes.append({"position":i+1,"remaining":r,"comparisons":comparisons,
                     "suffix_profit":str(Fraction(sum(profits[i:]),60)),
                     "self_copy_tax":str(Fraction(tax,60)),
                     "budget":str(Fraction(budget,60)),
                     "maximum_relative_potential":str(Fraction(max_potential,60)),
                     "minimum_envelope_slack":str(Fraction(budget-max_potential,60)),
                     "one_maximizer":maximizing})

def payoff(terminal,own):
    return sum(share(sum(a in x for a in terminal)) for x in customers if own in x)

# At the actual penultimate history, the original nominated own payoff is u5.
# Test every current deviation against every genuine last best reply.
penultimate = []
for query in range(topic_count):
    prefix = actual[:4] + (query,)
    replies = [payoff(prefix+(reply,),reply) for reply in range(topic_count)]
    best = max(replies)
    brs = [a for a,v in enumerate(replies) if v == best]
    own = [payoff(prefix+(reply,),query) for reply in brs]
    penultimate.append({"query":query,"all_last_best_replies":brs,
                        "last_value":str(Fraction(best,60)),
                        "minimum_current_payoff":str(Fraction(min(own),60)),
                        "maximum_current_payoff":str(Fraction(max(own),60)),
                        "strict_gain_for_every_last_best_reply":str(Fraction(min(own)-profits[4],60))})

report = {"claim":data["claim"],"status":"independent exact audit passed; not an SPE",
          "customer_count":len(customers),"welfare":welfare,"optimum":optimum,
          "actual_profit_vector":[str(Fraction(u,60)) for u in profits],
          "safe_rows":len(safe),"minimum_safe_slack":str(min(Fraction(r["slack"]) for r in safe)),
          "suffix_comparisons":sum(s["comparisons"] for s in suffixes),"suffixes":suffixes,
          "penultimate_deviations":penultimate,
          "profitable_penultimate_queries":[r["query"] for r in penultimate if Fraction(r["strict_gain_for_every_last_best_reply"])>0]}
assert report["suffix_comparisons"] == 18563
assert report["profitable_penultimate_queries"]
(HERE/"suffix_envelope_independent_audit.json").write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps(report,indent=2))
