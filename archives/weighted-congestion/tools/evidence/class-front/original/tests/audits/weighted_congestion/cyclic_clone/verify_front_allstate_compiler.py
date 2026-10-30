"""Literal Fraction audit of one front-to-allstate compiler input and clock geometry.

Discovery used floating LP; this script neither imports its code nor uses floats.
No finite check is offered as a proof of the general compiler or growth claim.
"""
from fractions import Fraction as F
from itertools import product, combinations
from pathlib import Path
import argparse, json, hashlib, sys, platform

def digest(b):
    return hashlib.sha256(b).hexdigest()

def local_front(bits):
    return sum(a != b for a,b in zip(bits,bits[1:])) <= 1

def flip(s,i):
    return s[:i]+(1-s[i],)+s[i+1:]

def geometry_audit():
    legal_edges = repair_states = literal_triples = 0
    for n in range(1,8):
        triples=[(0,i,j) for i in range(1,n) for j in range(i+1,n)]
        for s in product((0,1),repeat=n):
            if local_front(s):
                for k in range(n):
                    t=flip(s,k)
                    if not local_front(t):
                        continue
                    legal_edges += 1
                    for tri in triples:
                        if k not in tri:
                            continue
                        sig=dict(zip(tri,(0,1,0)))
                        cur=s[k]^sig[k]
                        old=sum((s[j]^sig[j])==cur for j in tri)
                        post=sum((t[j]^sig[j])==(t[k]^sig[k]) for j in tri)
                        assert old==post==2
                        literal_triples += 1
            else:
                k=next(k for k in range(1,n) if s[k]!=s[0])
                assert any(s[j]==s[0] for j in range(k+1,n))
                t=flip(s,k);full=0
                for tri in triples:
                    if k not in tri:
                        continue
                    sig=dict(zip(tri,(0,1,0)))
                    cur=s[k]^sig[k]
                    old=sum((s[j]^sig[j])==cur for j in tri)
                    post=sum((t[j]^sig[j])==(t[k]^sig[k]) for j in tri)
                    full += old==3
                    assert post<=2
                assert full>=1
                repair_states += 1
    return dict(class_sizes=list(range(1,8)),legal_edges=legal_edges,
                illegal_repair_states=repair_states,legal_literal_triples=literal_triples)

def run(input_path):
    data_bytes=Path(input_path).read_bytes();data=json.loads(data_bytes)
    m=int(data['class_count']);N=int(data['class_size']);p=int(data['degree'])
    alpha=F(data['alpha']);w=list(map(F,data['class_weights']))
    assert m>=1 and N>=1 and p>=0 and alpha>=1
    assert len(w)==m and all(v>0 for v in w)
    terms=[(tuple(x['test']),F(x['theta'])) for x in data['terms']]
    for term, ((a,b,K,o), theta) in zip(data['terms'],terms):
        assert F(term['actual_coefficient']) == theta/(w[a]+K*w[b])**p
    assert all(0<=a<m and 0<=b<m and a!=b and 1<=K<=N and o in (-1,1) and theta>=0 for (a,b,K,o),theta in terms)
    players=[(a,j) for j in range(N) for a in range(m)]
    idx={u:i for i,u in enumerate(players)};weights=[w[a] for a,j in players]
    resources=[]
    for (a,b,K,o),theta in terms:
        W=w[a]+K*w[b]
        for j in range(N):
            us={idx[(a,j)]:0}
            for k in range(K):
                v=(j+int(a>b)+k)%N
                us[idx[(b,v)]]=int((v*m+b)>(j*m+a))^int(o<0)
            resources.append((us,theta/W**p,p))
    def costs(s,res):
        ret=[F(0) for _ in players]
        for us,c,k in res:
            loads=[sum(weights[i] for i,sig in us.items() if (s[i]^sig)==side) for side in (0,1)]
            vals=[c*x**k for x in loads]
            for i,sig in us.items():
                ret[i]+=vals[s[i]^sig]
        return ret
    def front(s):
        return all(local_front(tuple(s[idx[(a,j)]] for j in range(N))) for a in range(m))
    states=list(product((0,1),repeat=len(players)));cache={s:costs(s,resources) for s in states}
    fronts=[s for s in states if front(s)];records=[];selectors=[]
    base_pne_states=[s for s in states if all(cache[s][i]<=alpha*cache[flip(s,i)][i] for i in range(len(players)))]
    assert all(not front(s) for s in base_pne_states)
    for s in fronts:
        candidates=[(cache[s][i]-alpha*cache[flip(s,i)][i],i) for i in range(len(players)) if front(flip(s,i))]
        v,i=max(candidates);assert v>0,(s,v)
        records.append((v,i,s));selectors.append({'state':''.join(map(str,s)),'mover':i,'margin':str(v)})
    eta,_,worst=min(records);B=max(v for cc in cache.values() for v in cc)
    L=(N-1)*(N-2)//2 if N>=3 else 0
    assert L>=1
    M=2*alpha*B
    uniform_bound=eta/(4*alpha**2*B*L)
    split_bound=min(F(1)/(4*alpha*L),eta/(4*alpha*(alpha-1)*B*L)) if alpha>1 else F(1)/(4*L)
    outputs=[]
    for budget,bound in [('uniform',uniform_bound),('split',split_bound)]:
        D=1
        while F(2,3)**D>bound:
            D+=1
        assert D==1 or F(2,3)**(D-1)>bound
        clock=[]
        for a in range(m):
            for i in range(1,N):
                for j in range(i+1,N):
                    us={idx[(a,0)]:0,idx[(a,i)]:1,idx[(a,j)]:0}
                    clock.append((us,M/(3*w[a])**D,D))
        compiled={s:costs(s,resources+clock) for s in states};best=[];specified=[]
        for s in states:
            margins=[compiled[s][i]-alpha*compiled[flip(s,i)][i] for i in range(len(players))]
            assert max(margins)>0,(budget,s,margins)
            best.append(max(margins))
            if front(s):
                i=max((cache[s][i]-alpha*cache[flip(s,i)][i],i) for i in range(len(players)) if front(flip(s,i)))[1]
            else:
                a=next(a for a in range(m) if not local_front(tuple(s[idx[(a,j)]] for j in range(N))))
                k=next(k for k in range(1,N) if s[idx[(a,k)]]!=s[idx[(a,0)]])
                i=idx[(a,k)]
            assert margins[i]>=eta/2,(budget,s,i,margins[i],eta/2)
            specified.append(margins[i])
        outputs.append({'budget':budget,'bound':str(bound),'D':D,'D_minus_one_fails':D==1 or F(2,3)**(D-1)>bound,
                        'compiled_degree':max(p,D),'added_resources':2*len(clock),
                        'min_allstate_best_margin':str(min(best)),
                        'min_specified_exit_margin':str(min(specified))})
    return {'scope':'finite fixture and literal clock geometry; no growth or optimality assertion',
            'input':str(input_path),'input_sha256':digest(data_bytes),
            'parameters':{'m':m,'N':N,'p':p,'alpha':str(alpha),'weights':[str(x) for x in w]},
            'terms':[{'test':t,'theta':str(z),'actual_coefficient':str(z/(w[t[0]]+t[2]*w[t[1]])**p)} for t,z in terms],
            'base_pairs':len(resources),'base_resources':2*len(resources),'all_states':len(states),
            'front_states':len(fronts),'relative_front_states':len(fronts)//(2*N),
            'eta':str(eta),'B':str(B),'worst_front':worst,'M':str(M),
            'base_pne_count':len(base_pne_states),'base_pne_states':[''.join(map(str,s)) for s in base_pne_states],
            'compilations':outputs,'front_selector_certificate':selectors,
            'geometry':geometry_audit(),
            'exact_arithmetic':'Python fractions.Fraction; literal resource users and true post-deviation loads',
            'python':platform.python_version(),'command':sys.argv,
            'source_sha256':digest(Path(__file__).read_bytes())}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',required=True)
    parser.add_argument('--output')
    args=parser.parse_args()
    result=run(args.input);encoded=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
    if args.output:
        with open(args.output,'x',encoding='utf-8') as f:
            f.write(encoded)
    else:
        print(encoded,end='')
if __name__=='__main__':
    main()
