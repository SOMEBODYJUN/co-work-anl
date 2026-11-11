#!/usr/bin/env python3
"""Point-free exact single-state coefficients. No solver or matrix assembly."""
from fractions import Fraction as F
from itertools import combinations_with_replacement

ACTUAL=[f'A{i}' for i in range(1,7)]
TAILS=['R3','R4','R5','R6']
OLD=ACTUAL+['X','Omean']
NEW=['Q']+TAILS
QUERIES=ACTUAL+['X','Q']+TAILS+['Omean']

def validate_state(atom,q,tail):
    assert len(atom['a'])==6 and len(tail)==4
    assert all(v in (0,1) for v in atom['a']+[atom['x'],atom['o'],q]+list(tail))

def value(label,atom,q,tail):
    if label.startswith('A'):return F(atom['a'][int(label[1:])-1])
    if label=='X':return F(atom['x'])
    if label=='Q':return F(q)
    if label.startswith('R'):return F(tail[int(label[1:])-3])
    if label=='Omean':return F(atom['o'],6)
    raise ValueError(label)

def pair_cost(labels,atom,q,tail,D):
    if labels==['Omean','Omean']:
        # INNER thirty ordered distinct menu positions, then union weakening.
        return F(atom['o'],3*D)
    left,right=[value(x,atom,q,tail) for x in labels]
    return (left+right)/D-left*right/(D*(D+1))

def rhs_form(row):
    f=row['family']
    if f=='IC_SOURCE2':return {'u2':'1'}
    if f=='CAP':return {'K':'1'}
    if f=='ACTUAL_SAFE':return {f'u{row["source"]}':'1'}
    if f=='MAX':return {'F_X':'1'}
    if f=='MX':return {'u5':'1'}
    if f=='ACTUAL_RC':return {'u5':'1','F_X':'1'}
    return {}

def base_atom_coefficient(row,atom):
    a=atom['a'];c=sum(a);P=sum(a[:4]);result=F(0)
    for symbol,weight in rhs_form(row).items():
        w=F(weight)
        if symbol.startswith('u'):
            j=int(symbol[1:]);result+=w*(F(a[j-1],c) if c else F(0))
        elif symbol=='F_X':result+=w*F(atom['x'],P+1)
    return result

def base_K_coefficient(row):return F(rhs_form(row).get('K','0'))

def coefficient(row,atom,q,tail):
    """Return A_R(v,q,tail) in A_R*nu <= b_R(z,K), for ONE state."""
    validate_state(atom,q,tail)
    a=atom['a'];P=sum(a[:4]);f=row['family']
    if f=='IC_SOURCE2':return F(q,a[0]+1+sum(tail))
    if f=='CAP':return value(row['queries'][0],atom,q,tail)
    if f=='ACTUAL_SAFE':
        j=row['source'];return value(row['queries'][0],atom,q,tail)/(sum(a[:j-1])+7-j)
    if f=='MAX':return value(row['queries'][0],atom,q,tail)/(P+1)
    if f=='MX':return value(row['queries'][0],atom,q,tail)/(P+1+atom['x'])
    full=[a[0],q,*tail];total=sum(full)
    if f=='NEW_SAFE':
        j=row['source'];pay=F(full[j-1],total) if total else F(0)
        return value(row['queries'][0],atom,q,tail)/(sum(full[:j-1])+7-j)-pay
    if f=='NEW_PAIR':
        D=sum(full[:4])+1;y,z=tail[2:]
        wallet=F(y,D+z)+F(z,D+y)+F(y,D*(D+1))
        return pair_cost(row['queries'],atom,q,tail,D)-wallet
    if f=='ACTUAL_RC':return pair_cost(row['queries'],atom,q,tail,P+1)
    raise ValueError(f)

def catalogue():
    rows=[]
    def add(f,queries=(),source=None,extension=False):
        name=f+(f'_j{source}' if source else '')+('|'+'|'.join(queries) if queries else '')
        row={'name':name,'family':f,'queries':list(queries),'own_Q_extension':extension}
        if source is not None:row['source']=source
        if len(queries)==2:
            row['inner_averaging']='distinct30_union' if list(queries)==['Omean','Omean'] else ('six_union' if 'Omean' in queries else 'pure_same_outer_index')
        else:row['inner_averaging']='six_union' if 'Omean' in queries else 'pure_same_outer_index'
        row['rhs']=rhs_form(row);rows.append(row)
    add('IC_SOURCE2')
    for t in TAILS:add('CAP',[t])
    for j in range(1,7):
        for t in TAILS:add('ACTUAL_SAFE',[t],j)
    for t in TAILS:add('MAX',[t])
    for t in TAILS:add('MX',[t])
    for j in range(3,7):
        for label in QUERIES:add('NEW_SAFE',[label],j)
    for pair in combinations_with_replacement(QUERIES,2):add('NEW_PAIR',pair)
    for pair in combinations_with_replacement(NEW,2):add('ACTUAL_RC',pair)
    for new in NEW:
        for old in OLD:add('ACTUAL_RC',[new,old])
    assert len(rows)==235
    for f in ('CAP','MAX','MX'):add(f,['Q'],extension=True)
    for j in (1,3,4,5,6):add('ACTUAL_SAFE',['Q'],j,True)
    assert len(rows)==243
    for i,row in enumerate(rows):row['index']=i
    return rows

def fixed_dimensions(positive_old_types):
    assert isinstance(positive_old_types,int) and 0<=positive_old_types<=256
    s=positive_old_types
    return {'nu_columns':32*s,'mass_equations':s,'q_moment_rows':2*s,'genuine_rows':243,'raw_inequalities':243+2*s}

def moment_envelope(a0,a1,o):
    """Exact later elimination contract; caller must supply ALL-type minima."""
    assert o in (0,1);a0=F(a0);a1=F(a1)
    delta=max(a1-a0,F(0));gamma=max(a0-a1,F(0))
    m=a0+delta*F(o,6)-gamma*o
    assert m==(a0 if not o else min((5*a0+a1)/6,a1))
    return {'a0':a0,'a1':a1,'minimum':m,'lower_multiplier':delta,'upper_multiplier':gamma,'mass_multiplier':a0}

if __name__=='__main__':
    # Inventory only; no point lookup, full-domain enumeration or matrix output.
    import json
    rows=catalogue()
    print(json.dumps({'status':'SYMBOLIC_UNBOUND','genuine_rows':len(rows),'optimizer_calls':0,
                      'family_counts':{f:sum(r['family']==f for r in rows) for f in ['IC_SOURCE2','CAP','ACTUAL_SAFE','MAX','MX','NEW_SAFE','NEW_PAIR','ACTUAL_RC']}},indent=2))
