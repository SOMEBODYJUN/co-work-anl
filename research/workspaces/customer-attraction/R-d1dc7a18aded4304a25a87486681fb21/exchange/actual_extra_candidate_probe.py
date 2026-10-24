"""Targeted exact test of m max_T sum_x in T 1/(1+c_actual) <= W.

This is a candidate stronger than half, not a theorem. Negative findings must
be verified with a complete SPE before being used even as candidate refutation.
Run on existing canonical examples only, with no random instance scan.
"""
import json
from fractions import Fraction
from pathlib import Path
from customer_attraction.model import Instance
from customer_attraction.exact import ExactSPESolver
from customer_attraction.certificate import verify_certificate


def query_values(instance, counts):
    return tuple(sum((Fraction(t.multiplicity, 1+sum(counts[b] for b in t.topics))
                      for t in instance.customers if a in t.topics), Fraction())
                 for a in range(instance.topic_count))


def main():
    count = 0
    for p in sorted(Path('examples/customer_attraction').glob('*.json')):
        data=json.loads(p.read_text())
        if 'instance' in data:data=data['instance']
        try:instance=Instance.from_dict(data)
        except (TypeError,ValueError,KeyError):continue
        if instance.players>5 or instance.topic_count>7:continue
        solver=ExactSPESolver(instance)
        outcomes=solver.outcomes()
        violations=[]
        for z in outcomes:
            g=query_values(instance,z)
            w=instance.welfare(z)
            gap=instance.players*max(g)-w
            count += 1
            if gap>0:violations.append((gap,z,g,w))
        print(p.name,len(outcomes),'violations',len(violations),flush=True)
        if violations:
            gap,z,g,w=max(violations)
            cert=solver.certificate(z)
            audit=verify_certificate(instance,cert)
            audit.assert_valid()
            out=Path(__file__).with_name('actual_extra_candidate_failure.json')
            out.write_text(json.dumps({'source':str(p),'candidate':'m max_T sum_{x in T} 1/(1+c_actual) <= W',
               'instance':instance.to_dict(),'certificate':cert.to_dict(),
               'audit':{'valid':audit.valid,'histories':audit.checked_histories,'deviations':audit.checked_deviations,
                        'actual_path':audit.terminal_history},
               'W':w,'mM_minus_W':str(gap),'queries':list(map(str,g))},indent=2)+'\n')
            print('FAIL',str(out),'gap',gap,'queries',g,'path',audit.terminal_history,flush=True)
            return
    print('checked existing exact SPE outcomes',count,'without violating candidate; no proof implied')

if __name__=='__main__':main()
