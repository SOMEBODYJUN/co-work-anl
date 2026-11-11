#!/usr/bin/env python3
"""Unbound fixed-C lift: full751 audit view,734 local rows, one-state exact oracle."""
from copy import deepcopy
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
LEGACY=HERE/"legacy_751_catalogue.json"
LEGACY_SHA="028a6de290df6e69213439fb702dd7c3357350e2bc628846a924255d8a6f3cdc"
C30_PATH=HERE.parent/"main_thirty_index_strengthening/requery30_envelopes.json"
C30_SHA="14ef732b35d0f859113daf92c8dda1f08330413682b057c69a57543a41a360bc"
VISIBLE_LEGACY_INDICES={180,195,196,197,198,199,200,201,202,235,236,237,238,239,240,241,242}
QUERIES=[f"A{i}" for i in range(1,7)]+["X","C","R3","R4","R5","R6","Omean"]
assert sha256(LEGACY.read_bytes()).hexdigest()==LEGACY_SHA
assert sha256(C30_PATH.read_bytes()).hexdigest()==C30_SHA
LEGACY_ROWS=json.loads(LEGACY.read_text())["rows"]
C30=json.loads(C30_PATH.read_text())

def full_catalogue():
    result=[]
    for old in LEGACY_ROWS:
        row=deepcopy(old)
        row["legacy_index"]=old["index"];row["legacy_name"]=old["name"]
        row["name"]=old["name"].replace("|Q","|C")
        row["queries"]=["C" if q=="Q" else q for q in old["queries"]]
        for key in ["true_prefix","true_history"]:
            if key in row:row[key]=["C" if q=="Q" else q for q in row[key]]
        if "h_bits" in row:row["h_bits"]=["c" if q=="q" else q for q in row["h_bits"]]
        row["legacy_inner_averaging"]=old["inner_averaging"]
        if row["inner_averaging"]=="pure_same_outer_index":row["inner_averaging"]="pure_same_fixed_C_branch"
        row["legacy_own_Q_extension"]=row.pop("own_Q_extension",False)
        row["destination"]=("global_C_size_equality" if old["index"]==235 else
                            "visible_global_prerequisite" if old["index"] in VISIBLE_LEGACY_INDICES else "local_hidden")
        result.append(row)
    assert len(result)==751
    return result

def active_catalogue():
    result=[]
    for row in full_catalogue():
        if row["destination"]=="local_hidden":
            row["index"]=len(result);result.append(row)
    assert len(result)==734
    return result

def validate_state(atom,tail):
    assert len(atom["a"])==6 and len(tail)==4
    assert all(bit in (0,1) for bit in atom["a"]+[atom["x"],atom["o"],atom["c"]]+list(tail))

def atom_from_index(h):
    assert isinstance(h,int) and 0<=h<512
    bits=[(h>>k)&1 for k in range(8,-1,-1)]
    return {"index":h,"a":bits[:6],"x":bits[6],"o":bits[7],"c":bits[8]}

def value(label,atom,tail):
    if label.startswith("A"):return F(atom["a"][int(label[1:])-1])
    if label=="X":return F(atom["x"])
    if label in ("C","Q"):return F(atom["c"])
    if label.startswith("R"):return F(tail[int(label[1:])-3])
    if label=="Omean":return F(atom["o"],6)
    raise ValueError(label)

def rhs_form(row):
    f=row["family"]
    if f=="IC_SOURCE2":return {"u2":"1"}
    if f=="CAP":return {"K":"1"}
    if f=="ACTUAL_SAFE":return {f'u{row["source"]}':"1"}
    if f=="MAX":return {"F_X":"1"}
    if f=="MX":return {"u5":"1"}
    if f=="ACTUAL_RC":return {"u5":"1","F_X":"1"}
    if f=="NESTED_SOURCE25":return {"K":str(F(7-row["source"],2))}
    return {}

def base_atom_coefficient(row,atom):
    actual=atom["a"];total=sum(actual);P=sum(actual[:4]);answer=F(0)
    for symbol,weight in rhs_form(row).items():
        if symbol.startswith("u"):
            answer+=F(weight)*(F(actual[int(symbol[1:])-1],total) if total else F(0))
        elif symbol=="F_X":answer+=F(weight)*F(atom["x"],P+1)
    return answer

def base_K_coefficient(row):return F(rhs_form(row).get("K","0"))

def pair_cost(labels,atom,tail,D):
    if list(labels)==["Omean","Omean"]:return F(atom["o"],3*D)
    t,q=[value(label,atom,tail) for label in labels]
    return (t+q)/D-t*q/(D*(D+1))

def source25_cost(prefix,n,forcing,query,atom,tail):
    A=F(n+1,2)+F(24,prefix+n+1)
    B=F(1,prefix+1);E=F(n,(prefix+1)*(prefix+n+1))
    if forcing==query=="Omean":return F(atom["o"],6)*(A+B)
    if forcing=="Omean":
        q=value(query,atom,tail);return B*q+F(atom["o"],6)*(A-E*q)
    t=value(forcing,atom,tail)
    if query=="Omean":return A*t+F(atom["o"],6)*(B-E*t)
    q=value(query,atom,tail);return A*t+B*q-E*t*q

def c30_index(atom,tail):
    bits=[atom["a"][0],atom["c"],*tail,atom["o"]]
    return sum(bit<<(6-i) for i,bit in enumerate(bits))

def coefficient(row,atom,tail):
    """Original unscaled A(h,tail) in A nu <= b(w,K); no outer-average factor."""
    validate_state(atom,tail)
    actual=atom["a"];P=sum(actual[:4]);f=row["family"]
    full=[actual[0],atom["c"],*tail];total=sum(full)
    if f=="IC_SOURCE2":return F(atom["c"],total) if total else F(0)
    if f=="CAP":return value(row["queries"][0],atom,tail)
    if f=="ACTUAL_SAFE":
        i=row["source"];return value(row["queries"][0],atom,tail)/(sum(actual[:i-1])+7-i)
    if f=="MAX":return value(row["queries"][0],atom,tail)/(P+1)
    if f=="MX":return value(row["queries"][0],atom,tail)/(P+1+atom["x"])
    if f=="NEW_SAFE":
        i=row["source"];pay=F(full[i-1],total) if total else F(0)
        return value(row["queries"][0],atom,tail)/(sum(full[:i-1])+7-i)-pay
    if f=="NEW_PAIR":
        D=1+sum(full[:4]);r5,r6=tail[2:]
        wallet=F(r5,D+r6)+F(r6,D+r5)+F(r5,D*(D+1))
        return pair_cost(row["queries"],atom,tail,D)-wallet
    if f=="ACTUAL_RC":return pair_cost(row["queries"],atom,tail,P+1)
    if f=="NESTED_SOURCE25":
        i=row["source"];assert i in (3,4,5)
        pay=F(full[i-1],total) if total else F(0)
        return source25_cost(sum(full[:i-1]),6-i,*row["queries"],atom,tail)-25*pay
    if f=="NESTED_C30":
        entry=C30[c30_index(atom,tail)]
        assert entry["bits"]==full+[atom["o"]]
        wallet=F(126000*full[2]+65719*full[3]+4962*full[5],total) if total else F(0)
        result=F(entry["m30"])-wallet
        assert result==-F(entry["cut"])
        return result
    raise ValueError(f)

def symbolic_dimensions(s):
    assert isinstance(s,int) and 0<=s<=512
    return {"physical_nu_columns":16*s,"mass_equalities":s,"outer_q_moment_rows":0,
            "local_hidden_inequalities":734,"visible_prerequisite_rows":16,
            "global_C_size_equality":1,"full_symbolic_state_domain":8192}

def single_type_envelope(weights,atom):
    """Symbolic nonnegative-weight interface, no point/matrix/optimizer binding."""
    by_name={r["name"]:r for r in active_catalogue()}
    assert all(name in by_name and F(w)>=0 for name,w in weights.items())
    costs=[]
    for tail in product([0,1],repeat=4):
        cost=sum((F(w)*coefficient(by_name[name],atom,tail) for name,w in weights.items()),F(0))
        costs.append((tail,cost))
    minimum=min(cost for _,cost in costs)
    return {"mass_multiplier":minimum,"minimum":minimum,
            "tail_residuals":[{"tail":list(t),"residual":v-minimum} for t,v in costs]}
