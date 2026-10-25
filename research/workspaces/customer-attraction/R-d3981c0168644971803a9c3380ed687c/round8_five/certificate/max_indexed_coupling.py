"""True maximum-root successors query the old indexed reply menus.

This module retains, rather than projects away, the shared maximum-path
state.  All expressions are necessary conditions for the original complete
ordered-history SPE.  Floating discovery is not a welfare certificate.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations_with_replacement
from collections import defaultdict
import json, sys, hashlib, time
import numpy as np
from scipy.optimize import linprog

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'customer_attraction/__init__.py').exists())
SOURCE = ROOT / 'research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round13/certificate'
sys.path.insert(0, str(SOURCE))
import max_menu_tuple_pricing as mt
import max_menu_joint_pricing as mj
import menu_ap_pricing as mp
import lift_maximum_branch as lm


def specs():
    out = []
    for tag, menus in mp.MENUS.items():
        extern = list(mp.LABELS) + [f'z{j}' for j in range(5)] + ['opt']
        pairs = [(c, d) for c in menus for d in extern]
        pairs += [(c, d) for c in extern for d in menus]
        pairs += [(c, d) for c in menus for d in menus]
        for i in range(1, 4):
            for c, d in pairs:
                out.append((f'{tag}:MaxCoupled:AP:{i}:{c}:{d}', tag, 'AP', i, c, d))
        for i in range(1, 5):
            for c in menus:
                out.append((f'{tag}:MaxCoupled:K:{i}:{c}', tag, 'K', i, c, None))
        for c in menus:
            for d in extern + list(menus):
                if d in menus and menus.index(d) < menus.index(c):
                    continue
                out.append((f'{tag}:MaxCoupled:Tax:3:{c}:{d}', tag, 'Tax', 3, c, d))
        for rem in (3, 4):
            for c in menus:
                for n in range(1, rem + 1):
                    for qs in combinations_with_replacement(range(5), rem - n):
                        key = f'{tag}:MaxCoupled:Tuple:{rem}:{c}:{n}:{"".join(map(str,qs))}'
                        out.append((key, tag, 'Tuple', rem, c, (n, qs)))
    return out


SPECS = specs()
SPEC = {s[0]: s for s in SPECS}


def counts(a, tag):
    k = 4 if tag == 'Sbranch' else 3
    return {menu: sum(n * t[j] for n, t in zip(a[mp.FIELDS[tag]], mp.TYPES[k]))
            for j, menu in enumerate(mp.MENUS[tag], 1)}


def one_row(spec, b, dopt, mb, cc):
    _, tag, kind, i, c, d = spec
    total = sum(mb)
    if kind == 'Tuple':
        rem = i
        n, qs = d
        p = sum(mb[:5-rem]); s = sum(mb[j] for j in qs)
        beta = F(5,3) if rem == 3 else F(1499,750)
        val = 5 * beta * lm.q(sum(mb[5-rem:]), total)
        val -= (5 - cc[c]) * lm.q(s, p+s) + cc[c] * lm.q(s+n, p+s+n)
        if rem == 4:
            val -= 5 * mj.RHOMIN[mb[0], tuple(mb[1:])]
        return val
    p = sum(mb[:i]); k = 5-i; u = lm.q(mb[i], total)
    def query(t):
        if t == 'opt': return dopt, 5
        if t in cc: return cc[t], 5
        if t.startswith('z'): return mb[int(t[1:])], 1
        return b[t], 1
    cv, nc = query(c)
    if kind == 'K': return 5*u - lm.q(cv, p+k)
    dv, nd = query(d)
    if kind == 'AP': return mp.ap_value(u, p, k, cv, dv, nc, nd)
    assert kind == 'Tax' and i == 3
    h = lm.q(mb[3]+mb[4], total) + lm.q(mb[3], (p+1)*(p+2))
    return nc*nd*h - lm.q(nd*cv+nc*dv-2*cv*dv, p+1) - lm.q(2*cv*dv, p+2)


def coupled_rows(a, mb):
    b = dict(zip(mp.LABELS, map(int, a['bits'])))
    dopt = sum(a['AB_hist'][4:])
    ct = {tag: counts(a, tag) for tag in mp.MENUS}
    return {s[0]: one_row(s, b, dopt, mb, ct[s[1]]) for s in SPECS}


class Universe(mt.Universe):
    """Full finite-type pricing conditions on all 32 maximum-path states.

    Given the old ten bits, optimal multiplicity, and these five new bits,
    every added query cost depends on just one old family histogram.  Thus
    the three histogram maximizations remain independent.  Conditioning
    only on the maximum-path last-prefix load would lose the AP queries.
    """
    def __init__(self):
        super().__init__()
        self.names += [s[0] for s in SPECS]
        # Added rows live wholly in family_score, including their constants.
        self.active_max = None
        print(json.dumps({'coupled_rows': len(SPECS), 'total_rows': len(self.names)}), flush=True)

    def atom_rows(self, a):
        rr = super().atom_rows(a)
        rr.update(coupled_rows(a, tuple(map(int,a['max_bits']))))
        return rr

    def maximum_scores(self, lam):
        # The inherited block has 1386 rows. Coupled rows are evaluated by
        # family_score instead, so do not pass them to block_coeff.
        score = super().maximum_scores(lam[:len(self.names)-len(SPECS)])
        assert self.active_max is not None
        score[:, :, np.arange(32) != self.active_max] = -1e100
        return score

    def family_score(self, bits, tag, weights, integer=False):
        own = [(n,v) for n,v in weights if n in SPEC]
        rest = [(n,v) for n,v in weights if n not in SPEC]
        key, const, vec, me, mh = super().family_score(bits, tag, rest, integer=integer)
        mb = lm.STATES[self.active_max]
        b = dict(zip(mp.LABELS,bits))
        arr = self.countarr[tag]
        # A row is at most quadratic in one family's menu/optimal counts.
        co = defaultdict(int if integer else float)
        ckey = []
        for n, w in own:
            spec = SPEC[n]; kind=spec[2]; i=spec[3]; c=spec[4]; d=spec[5]
            total=sum(mb)
            def add(factor, variables=()):
                nonlocal const
                z = F(120)*factor
                if integer:
                    assert z.denominator == 1
                    z = int(z)
                else: z = float(z)
                if variables: co[tuple(sorted(variables))] += w*z
                else: const += w*z
            if kind == 'Tuple':
                rem=i; num,qs=d; p=sum(mb[:5-rem]); ss=sum(mb[j] for j in qs)
                beta=F(5,3) if rem==3 else F(1499,750)
                base=5*beta*lm.q(sum(mb[5-rem:]),total)-5*lm.q(ss,p+ss)
                if rem==4: base-=5*mj.RHOMIN[mb[0],tuple(mb[1:])]
                add(base);add(lm.q(ss,p+ss)-lm.q(ss+num,p+ss+num),(c,))
                continue
            p=sum(mb[:i]);k=5-i;u=lm.q(mb[i],total)
            if kind=='K':add(5*u);add(-lm.q(1,p+k),(c,));continue
            def query(t):
                if t in arr:return None,5
                if t.startswith('z'):return mb[int(t[1:])],1
                return b[t],1
            cv,nc=query(c);dv,nd=query(d)
            if kind=='AP':
                a=mp.aa(k); add(nc*nd*a*u)
                cf=-lm.q((a-2)*nd,p+k);df=-lm.q(2*nc,p+1)
                prod=-lm.q(2,p+k)+lm.q(2,p+1)
            else:
                assert kind=='Tax'
                h=lm.q(mb[3]+mb[4],total)+lm.q(mb[3],(p+1)*(p+2))
                add(nc*nd*h);cf=-lm.q(nd,p+1);df=-lm.q(nc,p+1)
                prod=lm.q(2,p+1)-lm.q(2,p+2)
            add(cf, (c,)) if cv is None else add(cf*cv)
            add(df, (d,)) if dv is None else add(df*dv)
            if cv is None and dv is None:add(prod,(c,d))
            elif cv is None:add(prod*dv,(c,))
            elif dv is None:add(prod*cv,(d,))
            else:add(prod*cv*dv)
        for variables, v in sorted(co.items()):
            if not v:continue
            ar=np.ones(len(self.hist[key[0]]),dtype=np.int64)
            for t in variables:ar=ar*arr[t]
            vec.append((v,ar));ckey.append((variables,v))
        return (key[0],key,tuple(ckey)),const,vec,me,mh

    def price(self, lam, beta, batch=60, **kw):
        assert not kw.get('integer',False), 'Use the Fraction separation auditor for exact results.'
        best=[];minimum=None;contexts=0
        for si in range(32):
            self.active_max=si
            value,cols,count=super().price(lam,beta,batch=batch,**kw)
            minimum=value if minimum is None else min(minimum,value)
            best.extend(cols);contexts+=count
        self.active_max=None
        best.sort(key=lambda z:z[0]);chosen=[];seen=set()
        for value,a in best:
            key=mp.atom_key(a)+(a['max_bits'],)
            if key not in seen:chosen.append((value,a));seen.add(key)
            if len(chosen)>=batch:break
        return minimum,chosen,contexts


def audit_frozen():
    reports={}
    for name in ('exact_max_menu_joint_primal.json','exact_max_menu_tuple_primal.json'):
        source=SOURCE/name;src=json.loads(source.read_text());sl={s[0]:F(0) for s in SPECS}
        for a in src['atoms']:
            mass=F(a['exact_mass'])
            for n,v in coupled_rows(a,tuple(map(int,a['max_bits']))).items():sl[n]+=mass*v
        neg={n:str(v) for n,v in sl.items() if v<0}
        reports[name]={'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'rows':len(sl),
                       'negative_rows':len(neg),'negative_slacks':neg,
                       'minimum_exact_slack':str(min(sl.values()))}
    report={'scope':'Exact separation of frozen necessary-condition points by valid original-SPE query rows; no factor-two or game claim.',
            'sources':reports,'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE/'exact_indexed_separation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({n:{k:v for k,v in d.items() if k!='negative_slacks'} for n,d in reports.items()},indent=2))


def run(maxiter=12):
    U=Universe();target=HERE/'coupled_discovery.json'
    source=target if target.exists() else SOURCE/'max_menu_tuple_discovery.json'
    src=json.loads(source.read_text());atoms=[];cols=[];keys=set();ww=[];oo=[]
    def add(a):
        key=mp.atom_key(a)+(a['max_bits'],)
        if key in keys:return 0
        rr=U.atom_rows(a);assert set(rr)==set(U.names)
        atoms.append(a);cols.append([float(rr[n]) for n in U.names]);keys.add(key)
        ww.append(int(any(map(int,a['bits'][:5]))));oo.append(int(any(a['AB_hist'][4:])))
        return 1
    for a,v in zip(src['atoms'],src['primal_float']):
        if v>1e-9:add(a)
    for d in (0,5):
        h3=[0]*8;h3[3 if d==0 else 7]=5;h4=[0]*16;h4[7 if d==0 else 15]=5
        add({'bits':'1111111111','AB_hist':h3,'AE_hist':h3,'second_hist':h4,'menus_lh':[(5,d)]*3,'max_bits':'11111'})
    history=[]
    for it in range(maxiter):
        start=time.time();mat=np.asarray(cols).T
        lp=linprog(-np.array(oo,float),A_ub=-mat,b_ub=np.zeros(len(U.names)),A_eq=[ww],b_eq=[1.],bounds=(0,None),method='highs')
        assert lp.success,lp.message
        beta=-lp.fun;lam=-lp.ineqlin.marginals
        print(json.dumps({'iteration':it,'restricted_beta':beta,'columns':len(atoms),'pricing':'started'}),flush=True)
        if beta>2+1e-7:minimum=None;new=[];contexts=None
        else:minimum,new,contexts=U.price(lam,beta,batch=90)
        count=sum(add(a) for _,a in new)
        rec={'iteration':it,'restricted_beta':beta,'columns':len(atoms),'new_columns':count,'minimum_scaled_residual':minimum,'pricing_contexts':contexts,'seconds':time.time()-start};history.append(rec)
        print(json.dumps(rec),flush=True)
        report={'scope':'Floating original-SPE necessary-row discovery. Not full-universe exact bound, actual OPT, or complete SPE.',
                'row_names':U.names,'atoms':atoms,'primal_float':lp.x.tolist()+[0.]*count,
                'dual_beta_float':beta,'dual_multipliers_float':{n:float(v) for n,v in zip(U.names,lam) if v>1e-10},
                'history':history,'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
        target.write_text(json.dumps(report,indent=2)+'\n')
        if beta>2+1e-7 or count==0:break


if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='audit':audit_frozen()
    else:run(int(sys.argv[1]) if len(sys.argv)>1 else 12)
