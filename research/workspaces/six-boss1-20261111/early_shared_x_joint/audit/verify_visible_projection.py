#!/usr/bin/env python3
"""Independent 36 visible-query projections from the frozen hidden-tail layer.

Only exact standard-library arithmetic; no generator import, point read, or
optimizer. All outputs stay beside this script.
"""

from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import gzip
import json

HERE = Path(__file__).resolve().parent
LAYER = HERE.parent
WORK = LAYER.parent

SPECS = {
    1: {"C":F(206,5), "alpha":F(25), "middle_safe":F(51,20), "terminal_safe":F(6), "middle_max":F(3,8), "terminal_max":F(0)},
    2: {"C":F(121,4), "alpha":F(20), "middle_safe":F(7,4), "terminal_safe":F(5), "middle_max":F(3,5), "terminal_max":F(0)},
    3: {"C":F(61,3), "alpha":F(15), "middle_safe":F(2,3), "terminal_safe":F(4), "middle_max":F(1), "terminal_max":F(0)},
    4: {"C":F(10), "alpha":F(10), "middle_safe":F(0), "terminal_safe":F(0), "middle_max":F(1), "terminal_max":F(2)},
}


def read(path):
    with gzip.open(path,"rt") if path.suffix==".gz" else path.open() as f:
        return json.load(f)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(",", ":"),ensure_ascii=False).encode()


def add(row, index, value):
    if value:
        row[index] = row.get(index,F())+value
        if not row[index]:
            del row[index]


def addrow(target, row, scale):
    for index, coefficient in row:
        add(target,index,F(coefficient)*scale)


def sparse(row):
    return [[index,str(value)] for index,value in sorted(row.items()) if value]


def share(member, other_load):
    return F(1,1+other_load) if member else F()


def residual(source,b,k,x,ys,t,q):
    """Target minus source, SAFE, MAX and true terminal IC local budgets."""
    spec = SPECS[source]
    r,m = 7-source,5-source
    assert len(ys)==m and 0<=b<=source-1 and 0<=k<=m
    target = -(spec["C"]-1)*F(x,b+r)-q*(F(x,b+r)+F(1-x,b+1))
    source_local = -spec["alpha"]*share(x,b+sum(ys)+t)
    safe_local = -spec["middle_safe"]*F(sum(ys),b+r)-spec["terminal_safe"]*F(t,b+r)
    max_local = (spec["middle_max"]*F(m*x-sum(ys),b+k+1)
                 +spec["terminal_max"]*F(x-t,b+k+1))
    terminal_local = share(t,b+x+sum(ys))-q/F(b+x+sum(ys)+1)
    return target-source_local-safe_local-max_local-terminal_local


def audit_saved_certificate(independent_records,packet,hist):
    certificate_path=LAYER/"visible_prefix_projection.json.gz"
    all_types_path=LAYER/"visible_prefix_all_type_remainders.json.gz"
    certificate,all_types=map(read,(certificate_path,all_types_path))
    assert len(certificate["certificates"])==36
    assert certificate["optimizer_calls"]==0 and certificate["point_values_read"] is False
    assert certificate["append_input_bytes_unchanged"] is True
    expected={(record["source"],tuple(record["query"])):record for record in independent_records}
    seen=set()
    paid_terms=0
    for saved in certificate["certificates"]:
        source=saved["source_player"]
        qdesc=saved["query"]
        query=("A",qdesc["player"]-1) if qdesc["kind"]=="actual" else (qdesc["family"],)
        key=(source,query)
        assert key in expected and key not in seen
        seen.add(key)
        independent=expected[key]
        assert saved["C"]==str(SPECS[source]["C"])
        assert saved["target_row"]==independent["target_row"]
        assert saved["target_row_name"]==independent["target_name"]
        assert saved["target_interface_file"]==("maxb_h3_bridge/rows_17.json" if source==4
                                                else "main_prefix_maxx_interface/rows_51.json")
        assert saved["all_hidden_coefficients_canceled"] is True
        assert saved["target_matches_frozen_interface_exactly"] is True
        saved_payments=[]
        explicit_sum={}
        for payment in saved["nonnegative_budget_payments"]:
            raw_id,unique_id=payment["raw_row_id"],payment["unique_row_id"]
            provenance=packet["raw_inequality_provenance"][raw_id]
            assert provenance["unique_row_id"]==unique_id
            assert provenance["family"]==payment["family"]
            assert provenance["branch_source_player"]==source
            assert F(payment["weight"])>=0
            saved_payments.append([unique_id,str(F(payment["weight"]))])
            addrow(explicit_sum,packet["inequalities"][unique_id]["row"],F(payment["weight"]))
            paid_terms+=1
        assert Counter(map(tuple,saved_payments))==Counter(map(tuple,independent["budget_payments"]))
        expected_remainders=[]
        for offset,descriptor in enumerate(packet["new_columns"]):
            if descriptor["source_player"]!=source:
                continue
            h=descriptor["hist_column"]
            a=tuple(map(int,hist[h]["actual_bits"]))
            if query[0]=="A":
                bits=(a[query[1]],)
            else:
                slot=("T","B","C").index(query[0])
                bits=tuple(word[slot] for word in hist[h]["literal_words"])
            value=sum((residual(source,sum(a[:source-1]),sum(a[source-1:4]),
                                  descriptor["X_bit"],descriptor["middle_bits"],descriptor["terminal_bit"],F(q))
                       for q in bits),F())/len(bits)
            expected_remainders.append([21021+offset,str(value)])
        assert saved["all_source_mu_remainders_including_zero"]==expected_remainders
        assert sha256(canonical(expected_remainders)).hexdigest()==independent["nonnegative_remainder_sha256"]
        expected_positive=[[column,value] for column,value in expected_remainders if F(value)>0]
        assert saved["nonnegative_mu_payments"]==expected_positive
        for column,value in saved["nonnegative_mu_payments"]:
            assert F(value)>0
            add(explicit_sum,column,F(value))
        saved_mass=[]
        for payment in saved["signed_mass_equality_payments"]:
            equality_id=payment["equality_row_id"]
            equality=packet["equalities"][equality_id]
            assert equality["name"][1]==source
            saved_mass.append([equality_id,str(F(payment["weight"]))])
            addrow(explicit_sum,equality["row"],F(payment["weight"]))
        assert Counter(map(tuple,saved_mass))==Counter(map(tuple,independent["mass_equality_payments"]))
        assert sparse(explicit_sum)==saved["target_row"]
    assert seen==set(expected)
    assert len(all_types["records"])==1568 and all_types["all_1568_nonnegative"] is True
    alltypekeys=set()
    for record in all_types["records"]:
        source=record["source"]
        b,k,x,ys,t,q=record["b"],record["actual_k"],record["x"],record["middle_bits"],record["terminal_bit"],record["query_bit"]
        key=(source,b,k,x,*ys,t,q)
        assert key not in alltypekeys
        alltypekeys.add(key)
        assert F(record["E"])==residual(source,b,k,x,ys,t,F(q))>=0
    expected_keys=set()
    for source in range(1,5):
        m=5-source
        for b,k in product(range(source),range(m+1)):
            for bits in product((0,1),repeat=m+3):
                expected_keys.add((source,b,k,*bits))
    assert alltypekeys==expected_keys
    return {"status":"PASS","saved_certificates_checked":36,
            "saved_nonnegative_budget_payment_terms":paid_terms,
            "saved_remainders_including_zeros_checked":17280,
            "saved_mass_equality_terms_checked":1152,
            "saved_full_domain_remainders_checked":1568,
            "every_saved_certificate_reassembled_exactly":True,
            "certificate_sha256":digest(certificate_path),"all_type_table_sha256":digest(all_types_path)}


def verify():
    packet_path = LAYER/"symbolic_append.json.gz"
    contract_path = LAYER/"base_coordinate_contract.json"
    early_path = WORK/"main_prefix_maxx_interface/rows_51.json"
    h3_path = WORK/"maxb_h3_bridge/rows_17.json"
    packet,contract,early,h3 = map(read,(packet_path,contract_path,early_path,h3_path))
    before_hash = digest(packet_path)
    hist = {record["hist_column"]:record for record in contract["histograms"]}
    targets = {}
    for row in early["rows"]:
        suffix = row["name"][2:]
        if suffix[0] == "A" or suffix in (["T"],["B"],["C"]):
            query = ("A",suffix[1]) if suffix[0]=="A" else (suffix[0],)
            targets[row["actual_player"],query] = row
    for row in h3["rows"]:
        suffix = row["name"][1:]
        if suffix[0] == "A" or suffix in (["T"],["B"],["C"]):
            query = ("A",suffix[1]) if suffix[0]=="A" else (suffix[0],)
            targets[4,query] = row
    assert len(targets)==36

    def query_token(query):
        if query["kind"] == "actual":
            return ("A",query["player"]-1)
        if query["kind"] == "indexed-average":
            return (query["family"],)
        return None

    def literal_bits(h,query):
        if query[0] == "A":
            return (int(hist[h]["actual_bits"][query[1]]),)
        slot = ("T","B","C").index(query[0])
        return tuple(word[slot] for word in hist[h]["literal_words"])

    # All mathematically legal local domains, not just the stored support.
    universal = Counter()
    smallest_positive = None
    for source,spec in SPECS.items():
        m = 5-source
        assert spec["C"]==spec["alpha"]+m*spec["middle_safe"]+spec["terminal_safe"]
        for b,k in product(range(source),range(m+1)):
            for bits in product((0,1),repeat=m+3):
                x,*tail = bits
                ys,t,q = tail[:m],tail[m],tail[m+1]
                value = residual(source,b,k,x,ys,t,F(q))
                assert value>=0,(source,b,k,bits,value)
                universal[str(source)]+=1
                universal["zero" if value==0 else "positive"]+=1
                if value>0 and (smallest_positive is None or value<smallest_positive):
                    smallest_positive=value
    assert [universal[str(i)] for i in range(1,5)] == [640,512,288,128]

    rows = packet["inequalities"]
    raw = packet["raw_inequality_provenance"]
    mass = {(row["name"][1],row["name"][2],row["name"][3]):row for row in packet["equalities"]}
    records=[]
    remainder_stats=Counter()
    for (source,query),target in targets.items():
        spec=SPECS[source]
        m,r=5-source,7-source
        paid={}
        payments=[]
        for provenance in raw:
            if provenance["branch_source_player"] != source:
                continue
            family=provenance["family"]
            weight=F()
            if family=="source-IC":
                weight=spec["alpha"]
            elif family=="actual-source-SAFE" and provenance["actual_source_player"]==source:
                terminal=provenance["query"]["tail_index"]==m
                weight=spec["terminal_safe"] if terminal else spec["middle_safe"]
            elif family=="same-P-MAX":
                terminal=provenance["query"]["tail_index"]==m
                weight=spec["terminal_max"] if terminal else spec["middle_max"]
            elif family=="branch-terminal-BR" and query_token(provenance["query"])==query:
                weight=F(1)
            if weight:
                unique_id=provenance["unique_row_id"]
                assert weight>=0
                addrow(paid,rows[unique_id]["row"],weight)
                payments.append([unique_id,str(weight)])

        expected_count=(1+m+1+m+1) if source<4 else 4
        assert len(payments)==expected_count
        remainder=[]
        for offset,descriptor in enumerate(packet["new_columns"]):
            if descriptor["source_player"] != source:
                continue
            h=descriptor["hist_column"]
            a=tuple(map(int,hist[h]["actual_bits"]))
            b,k=sum(a[:source-1]),sum(a[source-1:4])
            x,ys,t=descriptor["X_bit"],descriptor["middle_bits"],descriptor["terminal_bit"]
            qbits=literal_bits(h,query)
            value=sum((residual(source,b,k,x,ys,t,F(q)) for q in qbits),F())/len(qbits)
            qavg=F(sum(qbits),len(qbits))
            assert value==residual(source,b,k,x,ys,t,qavg)>=0
            remainder_stats["zero" if value==0 else "positive"]+=1
            remainder_stats["total"]+=1
            remainder.append([21021+offset,str(value)])
            add(paid,21021+offset,value)
        # Derive cancellation directly from μ columns; assert it depends only
        # on the common (hist,X) mass, then add exact zero equality rows.
        equality_payments=[]
        extra_f=m*spec["middle_max"]+spec["terminal_max"]
        for h,hist_record in hist.items():
            a=tuple(map(int,hist_record["actual_bits"]))
            b,p=sum(a[:source-1]),sum(a[:4])
            qbits=literal_bits(h,query)
            qavg=F(sum(qbits),len(qbits))
            expected_common={0:-qavg/F(b+1),
                             1:-(spec["C"]-1+qavg)/F(b+r)-extra_f/F(p+1)}
            for x in (0,1):
                equality=mass[source,h,x]
                hidden=[column for column,_ in equality["row"] if column>=21021]
                assert hidden
                values={paid.get(column,F()) for column in hidden}
                assert values=={expected_common[x]}
                multiplier=-expected_common[x]
                addrow(paid,equality["row"],multiplier)
                equality_payments.append([equality["id"],str(multiplier)])
        assert all(column<21021 for column in paid)
        assert sparse(paid)==target["row"],(source,query,"old target mismatch")
        records.append({"source":source,"query":list(query),"target_name":target["name"],
                        "target_row":target["row"],"budget_payments":payments,
                        "mass_equality_payments":equality_payments,
                        "nonnegative_remainder_count":len(remainder),
                        "nonnegative_remainder_sha256":sha256(canonical(remainder)).hexdigest(),
                        "all_hidden_columns_cancel":True,"exact_old_target_match":True})
    assert len(records)==36 and remainder_stats["total"]==17280
    assert digest(packet_path)==before_hash
    saved_certificate_audit=audit_saved_certificate(records,packet,hist)
    return {"status":"PASS","projection_count":36,"sources":4,"visible_queries_per_source":9,
            "source_constants":{str(i):str(spec["C"]) for i,spec in SPECS.items()},
            "universal_boolean_remainders":dict(universal),
            "minimum_positive_universal_remainder":str(smallest_positive),
            "stored_state_remainders":dict(remainder_stats),
            "all_budget_multipliers_nonnegative":True,"all_mu_remainders_nonnegative":True,
            "all_hidden_columns_cancel_using_mass_equalities":True,
            "all_projected_vectors_equal_existing_exact_target_rows":True,
            "saved_certificate_audit":saved_certificate_audit,
            "append_packet_unchanged":True,"generator_imports":False,"point_files_read":0,"optimizer_calls":0,
            "inputs":[{"path":str(path.relative_to(WORK)),"sha256":digest(path)}
                      for path in (packet_path,contract_path,early_path,h3_path)],"records":records}


if __name__=="__main__":
    result=verify()
    (HERE/"visible_projection_verification.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({key:value for key,value in result.items() if key!="records"},ensure_ascii=False,indent=2))
