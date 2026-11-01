"""Independent rational certificate audit from literal equal-share utilities.

No original module/helper, optimizer, game search, or strategy enumerator is run.
The 384 rows are fresh membership rows, old p=1 rows and old affine slopes.
"""
import argparse
import ast
from collections import Counter,defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

LABELS='ABTSQRHV'
ROOTS=(('T','Q'),('S','R'),('H','V'))
LAST=(('B','A'),('Q','T'),('R','S'),('V','H'))
NAMES=tuple([f'root_{a}_{b}' for a,b in ROOTS]+[f'floor_{a}' for a in LABELS]+[f'last_{chosen}_{prior}_{other}' for chosen,prior in LAST for other in LABELS if other!=chosen])

def fingerprint(path):
    b=path.read_bytes();return {'path':str(path),'bytes':len(b),'sha256':sha256(b).hexdigest()}

def utility(bits,chosen,other,p):
    m=bits[chosen]
    return F(m,p+m+bits[other]) if m else F()

def literal_coefficients(bits,p):
    """All 39 scaled IC coefficients, using actual terminal load denominators."""
    current=utility(bits,'A','B',p)
    values=[current-utility(bits,a,b,p) for a,b in ROOTS]
    values += [current-F(bits[a],p+2) for a in LABELS]
    values += [utility(bits,chosen,prior,p)-utility(bits,other,prior,p) for chosen,prior in LAST for other in LABELS if other!=chosen]
    D=(p+1)*(p+2)
    return tuple(D*x for x in values)

def literal_target(bits,p):
    a,b,t,s=(bits[c] for c in 'ABTS')
    D=(p+1)*(p+2)
    if not bits['H']:
        assert p==0
        return D*(2*int(a or b)-int(t or s))
    return D*(utility(bits,'A','B',p)+utility(bits,'B','A',p))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--source',type=Path,required=True)
    ap.add_argument('--certificate',type=Path,default=Path(__file__).parent/'original/background_menu_certificate.json')
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();assert __debug__
    cert=json.loads(args.certificate.read_bytes())
    assert fingerprint(args.certificate)['sha256']=='db25a2460aa58d9a8438f7aea0e20445c12264f717c587cafdd9974338d58689'
    assert fingerprint(args.source)['sha256']=='06a392ce682cbc6429fe34ca5806398bb0cbdc2dd67e0c20908816d57e0c5db0'
    tree=ast.parse(args.source.read_bytes())
    assignments={n.targets[0].id:n.value for n in tree.body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
    assert ast.literal_eval(assignments['LABELS'])==LABELS
    assert tuple(ast.literal_eval(assignments['ROOTS']))==ROOTS
    assert tuple(ast.literal_eval(assignments['LAST']))==LAST
    assert set(cert)=={'success','labels','slacks','cases','minimum'}
    assert cert['success'] is True and cert['labels']==LABELS and cert['cases']==384
    expected={'floor_B':F(1,2),'floor_H':F(1),'last_B_A_T':F(1),'last_B_A_S':F(1)}
    active={k:F(v) for k,v in cert['slacks'].items()}
    assert active==expected and set(active)<=set(NAMES) and all(v>=0 for v in active.values())
    multipliers=[active.get(name,F()) for name in NAMES]
    assert len(NAMES)==39 and len(active)==4
    cases=[];effective=defaultdict(list);signs=defaultdict(Counter)
    for bit_tuple in product((0,1),repeat=8):
        bits=dict(zip(LABELS,bit_tuple));a,b,t,s=(bits[k] for k in 'ABTS')
        if not bits['H']:
            entries=[('fresh',literal_coefficients(bits,0),F(literal_target(bits,0)),
                      a*((1-t)*(1-s)+t*s)+(1-a)*(F(b,2)+2*t*s))]
        else:
            c1,c2=literal_coefficients(bits,1),literal_coefficients(bits,2)
            t1,t2=F(literal_target(bits,1)),F(literal_target(bits,2))
            entries=[('p1',c1,t1,(1-b)*(2-F(3*a,2))+(t+s)*(3-a)),
                     ('slope',tuple(y-x for x,y in zip(c1,c2)),t2-t1,1-F(a+b,2)+t+s)]
        for kind,row,target,closed in entries:
            assert len(row)==39 and all(x.denominator==1 for x in row)
            remainder=target-sum(x*y for x,y in zip(row,multipliers))
            assert remainder==closed>=0,(bit_tuple,kind,remainder,closed)
            signs[kind]['zero' if remainder==0 else 'positive']+=1
            entry={'index':len(cases),'bits':''.join(map(str,bit_tuple)),'case':kind,
              'scaled_target':str(target),'all_39_scaled_IC_coefficients':[str(x) for x in row],
              'four_active_IC_coefficients':{name:str(row[NAMES.index(name)]) for name in active},
              'weighted_IC_coefficient':str(target-remainder),'remainder':str(remainder),'closed_form':str(closed)}
            cases.append(entry);effective[kind,a,b,t,s].append(entry['index'])
    assert len(cases)==384 and len(effective)==48 and all(len(v)==8 for v in effective.values())
    assert dict(signs['fresh'])=={'zero':56,'positive':72}
    assert dict(signs['p1'])=={'positive':112,'zero':16}
    assert dict(signs['slope'])=={'positive':120,'zero':8}
    assert min(F(x['remainder']) for x in cases)==F(cert['minimum'])==0
    reduced=[]
    for (kind,a,b,t,s),indices in effective.items():
        rows=[cases[i] for i in indices]
        assert len({r['remainder'] for r in rows})==1
        reduced.append({'case':kind,'ABTS':[a,b,t,s],'remainder':rows[0]['remainder'],'full_case_indices':indices})
    args.output.mkdir(parents=True,exist_ok=True)
    (args.output/'case-ledger.json').write_text(json.dumps({'scope':'all 384 rational coefficient rows, not games or strategies','labels':LABELS,'ordered_slack_names':NAMES,'cases':cases},ensure_ascii=False,indent=2)+'\n')
    report={'status':'PASS_EXACT_CERTIFICATE_AND_SYMBOLIC_REMAINDER_INTERFACE',
      'scope':'independent equal-share reconstruction of the saved four nonnegative multipliers; all fresh/p1/slope rows; no original import/helper/main/LP or complete SPE scan',
      'inputs':[fingerprint(args.certificate),fingerprint(args.source)],'certificate_fields':cert,
      'ordered_slack_names':NAMES,'multipliers':[str(x) for x in multipliers],
      'active_column_indices':[NAMES.index(n) for n in active],'positive_multipliers':len(active),'zero_multipliers':sum(x==0 for x in multipliers),
      'multiplier_sum':str(sum(multipliers)),'multiplier_sum_is_certified_optimum':False,
      'rows':len(cases),'exact_IC_coefficients_reconstructed':len(cases)*len(NAMES),'minimum_remainder':'0','zero_remainders':80,'positive_remainders':304,
      'by_case':{k:dict(v) for k,v in signs.items()},'effective_residual_classes':reduced,
      'analytic_remainders':{'fresh':'a*((1-t)*(1-s)+t*s)+(1-a)*(b/2+2*t*s)',
       'old_p1':'(1-b)*(2-3*a/2)+(t+s)*(3-a)',
       'old_slope':'1-(a+b)/2+t+s',
       'old_all_p':'old_p1+(p-1)*old_slope for p>=1'},
      'analytic_domain':'binary A,B,T,S,H; fresh iff H=0 and p=0; old H=1 and p>=1. Positivity for all p>=1 is supplied by displayed nonnegative factors and affine identity, not finite extrapolation.',
      'global_conclusion':'fresh_coverage(T union S) <= 2*fresh_coverage(A union B)+old_two_tail_profit = total_two_tail_profit+fresh_coverage(A union B), for a legal background topic H exactly equal to the covered prefix set; in particular any nonempty repeated-H prefix.',
      'not_certified':['an arbitrary legal prefix whose covered union is not a legal topic','all-background P+Delta >= freshOPT2','full-game half for arbitrary total players','optimality of the multiplier sum','realizability of all enumerated bit patterns as one SPE'],
      'original_entrypoint_calls':0,'original_helper_calls':0,'LP_calls':0}
    (args.output/'exact-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('status','rows','exact_IC_coefficients_reconstructed','active_column_indices','minimum_remainder','zero_remainders','positive_remainders','by_case','original_entrypoint_calls','original_helper_calls','LP_calls')},indent=2))

if __name__=='__main__':main()
