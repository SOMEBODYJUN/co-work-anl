#!/usr/bin/env python3
"""One stdlib fixed-input audit; no author/project imports, LP or random search."""
import argparse
import hashlib
import json
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import combinations_with_replacement, product
from math import lcm
from pathlib import Path


def all_counts(p,m):
    return [tuple(z.count(a) for a in range(p))
            for z in combinations_with_replacement(range(p),m)]


class FixedGame:
    def __init__(self,p,m,weights):
        assert p>=1 and m>=1 and len(weights)==(1<<p)-1
        assert all(type(w) is int and w>=0 for w in weights)
        self.p,self.m,self.weights=p,m,tuple(weights)
        self.scale=lcm(*range(1,m+1))
        self.types=[(t,w) for t,w in enumerate(weights,1) if w]
        self.terminals=all_counts(p,m)
        self.U={q:tuple(sum(w*(self.scale//sum(q[b] for b in range(p) if t>>b&1))
                            for t,w in self.types if t>>a&1 and sum(q[b] for b in range(p) if t>>b&1))
                        for a in range(p)) for q in self.terminals}
        self.W={q:sum(w for t,w in self.types if any(q[a] and t>>a&1 for a in range(p)))
                for q in self.terminals}
        self.states_evaluated=0

    @staticmethod
    def child(k,a):
        return k[:a]+(k[a]+1,)+k[a+1:]

    @lru_cache(None)
    def outcomes(self,k):
        self.states_evaluated+=1
        if sum(k)==self.m:
            return frozenset([k])
        children=[self.outcomes(self.child(k,a)) for a in range(self.p)]
        threshold=max(min(self.U[q][a] for q in children[a]) for a in range(self.p))
        out=frozenset(q for a in range(self.p) for q in children[a] if self.U[q][a]>=threshold)
        assert out
        return out

    def construct_path_policy(self,path):
        target=tuple(path.count(a) for a in range(self.p))
        assert target in self.outcomes((0,)*self.p)
        policy={}
        def visit(h,k,q):
            if len(h)==self.m:
                assert k==q
                return
            children=[self.outcomes(self.child(k,a)) for a in range(self.p)]
            threshold=max(min(self.U[r][a] for r in children[a]) for a in range(self.p))
            legal=[a for a in range(self.p) if q in children[a] and self.U[q][a]>=threshold]
            assert legal
            a=path[len(h)] if tuple(path[:len(h)])==h else legal[0]
            assert a in legal, (h,a,legal)
            policy[h]=a
            for b in range(self.p):
                goal=q if b==a else min(children[b],key=lambda r:(self.U[r][b],r))
                visit(h+(b,),self.child(k,b),goal)
        visit((),(0,)*self.p,target)
        return policy

    def verify_policy(self,policy):
        histories=[h for d in range(self.m) for h in product(range(self.p),repeat=d)]
        assert set(policy)==set(histories) and len(policy)==len(histories)
        assert all(type(a) is int and 0<=a<self.p for a in policy.values())
        @lru_cache(None)
        def end(h):
            return h if len(h)==self.m else end(h+(policy[h],))
        def counts_of(z): return tuple(z.count(a) for a in range(self.p))
        payloads=[];payload_ids={};node_payload_ids=[];by_depth=[]
        for d in range(self.m):
            counter=Counter();smallest=None
            for h in product(range(self.p),repeat=d):
                vals=tuple(self.U[counts_of(end(h+(a,)))][a] for a in range(self.p))
                a=policy[h];assert vals[a]==max(vals),(h,a,vals)
                if vals not in payload_ids:
                    payload_ids[vals]=len(payloads);payloads.append(vals)
                node_payload_ids.append(payload_ids[vals])
                for b in range(self.p):
                    if b==a:counter['self']+=1;continue
                    gap=vals[a]-vals[b]
                    assert gap>=0
                    counter['strict' if gap else 'ties']+=1
                    smallest=gap if smallest is None else min(smallest,gap)
            by_depth.append({'depth':d,'histories':self.p**d,**dict(counter),
                             'minimum_nonself_slack_scaled':smallest})
        z=end(());q=counts_of(z)
        layers=[''.join(str(policy[h]) for h in product(range(self.p),repeat=d)) for d in range(self.m)]
        return {'action_layers_depth_lex':layers,'actual_path':z,'terminal_counts':q,
                'scale':self.scale,'utilities':list(map(str,(Fraction(self.U[q][a],self.scale) for a in z))),
                'W':self.W[q],'by_depth':by_depth,'payloads_scaled':payloads,
                'node_payload_ids_depth_lex':node_payload_ids,
                'histories':len(histories),'comparisons_including_self':len(histories)*self.p,
                'nonself_comparisons':len(histories)*(self.p-1),
                'strict':sum(x.get('strict',0) for x in by_depth),'ties':sum(x.get('ties',0) for x in by_depth)}

    def static_table(self):
        rows=[]
        for q in self.terminals:
            profitable=[]
            for a in range(self.p):
                if not q[a]:continue
                for b in range(self.p):
                    r=list(q);r[a]-=1;r[b]+=1;r=tuple(r)
                    gain=self.U[r][b]-self.U[q][a]
                    if gain>0:profitable.append({'from':a,'to':b,'gain':str(Fraction(gain,self.scale))})
            rows.append({'q':q,'W':self.W[q],'is_static_PNE':not profitable,
                         'first_profitable_deviation':profitable[0] if profitable else None})
        return rows


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',required=True,type=Path)
    args=ap.parse_args();assert not args.output.exists();args.output.mkdir(parents=True)
    package=Path(__file__).resolve().parent
    manifest=json.loads((package/'manifest.json').read_text())
    for row in manifest['sources']:
        data=(package/row['package_path']).read_bytes()
        assert len(data)==row['size'] and hashlib.sha256(data).hexdigest()==row['sha256']
    original=package/'original'
    raw=json.loads((original/'notes/global_ne_boundary.json').read_text())
    ins=raw['instance'];p=len(ins['topics']);m=ins['players'];weights=[0]*((1<<p)-1)
    for row in ins['customers']:
        mask=sum(1<<a for a in row['topics']);weights[mask-1]+=row['multiplicity']
    game=FixedGame(p,m,weights)
    policy={tuple(row['history']):row['action'] for row in raw['certificate']['actions']}
    assert len(policy)==len(raw['certificate']['actions'])
    witness=game.verify_policy(policy)
    assert list(witness['terminal_counts'])==raw['certificate']['terminal_counts']
    roots=sorted(game.outcomes((0,)*p))
    assert roots==sorted(map(tuple,raw['all_spe_counts']))
    assert min(game.W[q] for q in roots)==raw['minimum_spe_welfare']==witness['W']
    static=game.static_table();pnes=[row for row in static if row['is_static_PNE']]
    assert min(row['W'] for row in pnes)==raw['minimum_ne_welfare']
    assert sorted(tuple(row['q']) for row in pnes if row['W']==raw['minimum_ne_welfare'])==sorted(map(tuple,raw['minimum_ne_counts']))
    witness.update({'source_literal_policy':True,'clients':sum(weights),'weights':weights,
                    'topic_sizes':[sum(w for t,w in enumerate(weights,1) if t>>a&1) for a in range(p)],
                    'all_spe_counts':roots,'minimum_spe_welfare':min(game.W[q] for q in roots),
                    'minimum_ne_welfare':min(row['W'] for row in pnes),'all_static_PNE':pnes,
                    'all_static_counts':static,'OPT':max(game.W.values()),'DP_states':game.states_evaluated})
    q=tuple(witness['terminal_counts']);witness['actual_static_deviations']=[row for row in static if tuple(row['q'])==q]
    (args.output/'global-boundary-fixed.json').write_text(json.dumps(witness,ensure_ascii=False,indent=2)+'\n')
    old=json.loads((original/'experiments/cex_last_half_probe.json').read_text())
    games={};reports=[]
    for i,row in enumerate(old['records']):
        key=tuple(row['weights'])
        if key not in games:games[key]=FixedGame(old['topics'],old['players'],key)
        current=games[key];path=tuple(row['path']);target=tuple(path.count(a) for a in range(current.p))
        vals=[current.U[target][a] for a in path]
        assert vals==row['payoffs_scaled'] and current.scale==row['scale']
        individual=Fraction(vals[-1],min(vals[:-1]));aggregate=Fraction((current.m-1)*vals[-1],2*sum(vals[:-1]))
        assert str(individual)==row['individual'] and str(aggregate)==row['aggregate']
        expanded=current.construct_path_policy(path)
        check=current.verify_policy(expanded)
        assert tuple(check['actual_path'])==path
        check.update({'record_index':i,'trial':row['trial'],'weights':row['weights'],
                      'source_literal_policy':False,'policy_origin':'new deterministic full-history construction for the preserved ordered path; not restoration of an unsaved author policy',
                      'individual':str(individual),'aggregate':str(aggregate),
                      'OPT':max(current.W.values()),'clients':sum(key)})
        (args.output/f'last-record-{i:02d}-new-policy.json').write_text(json.dumps(check,ensure_ascii=False,indent=2)+'\n')
        reports.append({k:check[k] for k in ('record_index','trial','actual_path','W','OPT','clients','utilities',
                      'histories','comparisons_including_self','nonself_comparisons','strict','ties','individual','aggregate')})
    assert max(Fraction(row['individual']) for row in reports)==Fraction(old['best_individual'])
    assert max(Fraction(row['aggregate']) for row in reports)==Fraction(old['best_aggregate'])
    summary={'identity':'Boss3','scope':'one original literal finite witness and eight preserved ordered paths; no trial replay',
             'global':{k:witness[k] for k in ('clients','topic_sizes','actual_path','utilities','W','OPT','minimum_spe_welfare','minimum_ne_welfare','all_spe_counts','histories','comparisons_including_self','nonself_comparisons','strict','ties','DP_states')},
             'last_payoff_records':reports,'distinct_last_record_inputs':len(games),
             'last_record_DP_states':[g.states_evaluated for g in games.values()],
             'original_CLI_calls':0,'original_self_test_calls':0,'project_solver_or_verifier_calls':0,
             'LP_calls':0,'random_search_calls':0,'mature_all_big_seed_rechecks':0,
             'new_fixed_audit_processes':1,'new_full_policies_constructed':8,'all_checks_passed':True}
    (args.output/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(summary,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
