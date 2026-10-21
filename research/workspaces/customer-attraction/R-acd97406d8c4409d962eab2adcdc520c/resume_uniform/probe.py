"""Attack the exact uniform actual-prefix deviation interface, using full SPEs.

Run from repository root. No finite pass proves the arbitrary-m interface.
"""
from fractions import Fraction as F
from itertools import combinations
import json
from pathlib import Path
from customer_attraction.model import Instance
from customer_attraction.certificate import StrategyCertificate, verify_certificate
from customer_attraction.exact import ExactSPESolver


def deviation_data(game, cert):
    report = verify_certificate(game, cert)
    report.assert_valid()
    path = report.terminal_history
    def follow(h):
        while len(h) < game.players:
            h += (cert.actions[h],)
        return h
    values = []
    for i in range(game.players):
        row = []
        for a in range(game.topic_count):
            z = follow(path[:i]+(a,))
            row.append(game.player_payoffs(z)[i])
        values.append(row)
    return path, values


def check(game, cert):
    path, matrix = deviation_data(game, cert)
    m, p = game.players, game.topic_count
    w = game.welfare(cert.terminal_counts)
    costs = [sum((matrix[i][a] for i in range(m)), F(0)) for a in range(p)]
    best = None
    for k in range(1, min(m,p)+1):
        for supp in combinations(range(p), k):
            q = tuple(int(a in supp) for a in range(p))
            cheap = min(supp, key=lambda a: costs[a])
            comp = supp + (cheap,)*(m-k)
            total = sum((costs[a] for a in comp), F(0))
            coverage = game.welfare(q)
            gap = (m-1)*w + total - m*coverage
            if best is None or gap < best[0]:
                best = (gap, comp, coverage, total)
    return {"m":m,"p":p,"path":path,"W":w,"OPT":game.optimal_welfare(),
            "minimum_gap":str(best[0]),"comparison":best[1],
            "comparison_coverage":best[2],"deviation_sum":str(best[3]),
            "matrix":[list(map(str,row)) for row in matrix]}


def main():
    results=[]
    for path in sorted(Path('examples/customer_attraction').glob('*.json')):
        raw = json.loads(path.read_text())
        if not all(k in raw for k in ('topics','customers','players')):
            continue
        game = Instance.from_dict(raw)
        cp = Path('evidence/certificates/customer_attraction')/path.name
        cert = None
        if cp.exists():
            data=json.loads(cp.read_text())
            if 'strategy' in data and 'terminal_counts' in data['strategy']:
                cert=StrategyCertificate.from_dict(data['strategy'])
            elif 'actions' in data and 'terminal_counts' in data:
                cert=StrategyCertificate.from_dict(data)
        if cert is None and game.players <= 5 and game.topic_count <= 7:
            cert=ExactSPESolver(game).worst_certificate()
        if cert is None:
            continue
        result=check(game,cert)
        result['source']=str(path)
        results.append(result)
        print(json.dumps(result),flush=True)
    out=Path(__file__).with_name('existing_results.json')
    out.write_text(json.dumps(results,indent=2)+'\n')


if __name__ == '__main__':
    main()
