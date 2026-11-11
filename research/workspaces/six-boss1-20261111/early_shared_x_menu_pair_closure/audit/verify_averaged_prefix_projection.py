#!/usr/bin/env python3
"""Independently derive the nine corrected averaged-prefix projections.

The old 436-row package is only read. No generator or prior output-writing
audit is imported or executed. All arithmetic is exact and point-free.
"""

from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import gzip
import json

HERE=Path(__file__).resolve().parent
LAYER=HERE.parent
WORK=LAYER.parent
OLD=WORK/"early_shared_x_joint"
SPECS={1:(F(31),F(25),F(6),F(4,5)),
       2:(F(25),F(20),F(5),F(19,20)),
       3:(F(19),F(15),F(4),F(7,6))}


def read(path):
    with gzip.open(path,"rt") if path.suffix==".gz" else path.open() as f:
        return json.load(f)


def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(",", ":"),ensure_ascii=False).encode()


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def share(member,other_load):
    return F(1,other_load+1) if member else F()


def add(row,column,value):
    if value:
        row[column]=row.get(column,F())+value
        if not row[column]:
            del row[column]


def addrow(target,row,weight):
    for column,value in row:
        add(target,column,F(value)*weight)


def sparse(row):
    return [[column,str(value)] for column,value in sorted(row.items()) if value]


def literal_residual(source,b,k,x,ys,t,theta):
    C,alpha,terminal_safe,max_middle=SPECS[source]
    r,m=7-source,5-source
    assert len(ys)==m and C==alpha+terminal_safe
    target=-(C-1)*F(x,b+r)-theta*(F(x,b+r)+F(1-x,b+1))
    source_IC_local=-share(x,b+sum(ys)+t)
    terminal_SAFE_local=-F(t,b+r)
    maximum_local=F(m*x-sum(ys),b+k+1)
    terminal_IC_local=share(t,b+x+sum(ys))-theta/F(b+x+sum(ys)+1)
    return target-(alpha*source_IC_local+terminal_safe*terminal_SAFE_local
                   +max_middle*maximum_local+terminal_IC_local)


def formula_pi(source,b,k,degree):
    n=b+1
    a=SPECS[source][3]
    return max(F(j)* (F(degree,6*n*(n+j))-a/F(n+k)) for j in range(6-source))


def universal_audit():
    counts=Counter()
    zero_thresholds={}
    pi_contexts=[]
    for source in range(1,4):
        m,r=5-source,7-source
        C,alpha,sT,a=SPECS[source]
        assert a==F(5*r-6,r*(r-1))
        always_zero=[]
        for degree in range(7):
            all_zero=True
            for b,k in product(range(source),range(m+1)):
                pi=formula_pi(source,b,k,degree)
                # Independently minimize the literal residual over the true
                # hidden continuation states, including t=1, with x fixed 0.
                negatives=[]
                for bits in product((0,1),repeat=m+1):
                    ys,t=bits[:-1],bits[-1]
                    negatives.append(-literal_residual(source,b,k,0,ys,t,F(degree,6)))
                minimal_needed=max(F(),*negatives)
                assert minimal_needed==pi>=0
                all_zero=all_zero and not pi
                assert pi<=F(max(degree-1,0)*m,6*(b+1)*(b+1+m))
                pi_contexts.append({"source":source,"b":b,"k":k,"degree":degree,"Pi":str(pi)})
                counts["Pi_exact_minimum_contexts"]+=1
                for bits in product((0,1),repeat=m+2):
                    x,ys,t=bits[0],bits[1:-1],bits[-1]
                    raw=literal_residual(source,b,k,x,ys,t,F(degree,6))
                    corrected=raw+(1-x)*pi
                    assert corrected>=0
                    if x or t:
                        assert raw>=0
                    else:
                        j=sum(ys);n=b+1
                        assert raw==F(j)*(a/F(n+k)-F(degree,6*n*(n+j)))
                    counts["all_ordered_corrected_remainders"]+=1
                    counts["corrected_zero" if corrected==0 else "corrected_positive"]+=1
                    # The union indicator o is not a legal action. It enters
                    # only via the weakened average terminal IC (UBR).
                    union_indicator=int(degree>0)
                    denominator=b+1+x+sum(ys)
                    average_BR=share(t,b+x+sum(ys))-F(degree,6*denominator)
                    union_BR=share(t,b+x+sum(ys))-F(union_indicator,6*denominator)
                    extra=F(degree-union_indicator,6*denominator)
                    assert union_BR==average_BR+extra and extra>=0
                    assert formula_pi(source,b,k,union_indicator)==0
                    assert literal_residual(source,b,k,x,ys,t,F(union_indicator,6))>=0
                    counts["union_query_weakening_and_no_penalty_cases"]+=1
            if all_zero:
                always_zero.append(degree)
        zero_thresholds[str(source)]=max(always_zero)
        assert always_zero==list(range(max(always_zero)+1))
    assert counts["all_ordered_corrected_remainders"]==5040
    assert counts["Pi_exact_minimum_contexts"]==154
    assert zero_thresholds=={"1":1,"2":2,"3":4}
    return {"status":"PASS","counts":dict(counts),"uniform_zero_Pi_degree_thresholds":zero_thresholds,
            "Pi_is_exact_minimum_nonnegative_x0_correction_for_fixed_weights":True,
            "union_bridge_uses_legal_query_average_plus_nonnegative_weakening":True,
            "union_indicator_not_added_as_action":True,
            "all_possible_true_continuation_membership_bits_retained":True,
            "Pi_contexts":pi_contexts}


def independent_projections():
    packet_path=OLD/"symbolic_append.json.gz"
    packet=read(packet_path)
    columns=read(OLD/"columns_22941.json.gz")
    original_hash=digest(packet_path)
    assert original_hash=="1ff17a93dc319e05c366424214a722a86577773599ac5692a1fabb6cfaa3a5e0"
    hist={j:c for j,c in enumerate(columns[:21021]) if c["kind"]=="hist"}
    xcols={c["hist_column"]:j for j,c in enumerate(columns[:21021]) if c["kind"]=="common-X-mass"}
    actual={h:tuple(map(int,c["actual_bits"])) for h,c in hist.items()}
    words={h:tuple(word for word,count in zip(product((0,1),repeat=3),c["hist"])
                   for _ in range(count)) for h,c in hist.items()}
    assert len(hist)==16 and set(xcols)==set(hist)
    assert all(sum(word[0] for word in menu)==1 for menu in words.values())
    mass={(row["name"][1],row["name"][2],row["name"][3]):row for row in packet["equalities"]}
    records=[]
    stats=Counter()
    nonzero_pi=[]
    for source in range(1,4):
        m,r=5-source,7-source
        C,alpha,sT,a=SPECS[source]
        for family,slot in zip(("T","B","C"),range(3)):
            pi_by_hist={}
            theta_by_hist={}
            target={}
            pi_records=[]
            for h,abits in actual.items():
                b,k=sum(abits[:source-1]),sum(abits[source-1:4])
                degree=sum(word[slot] for word in words[h])
                theta=F(degree,6)
                pi=formula_pi(source,b,k,degree)
                pi_by_hist[h]=pi
                theta_by_hist[h]=theta
                add(target,h,C*share(abits[source-1],sum(abits)-abits[source-1])-theta/F(b+1)+pi)
                add(target,xcols[h],-(C-1)/F(b+r)+theta*F(r-1,(b+1)*(b+r))-pi)
                pi_records.append({"hist_column":h,"degree":degree,"Pi":str(pi)})
                if pi:
                    nonzero_pi.append({"source":source,"query_family":family,"hist_column":h,"Pi":str(pi)})
            if family=="T":
                assert not any(pi_by_hist.values())

            paid={}
            payments=[]
            for provenance in packet["raw_inequality_provenance"]:
                if provenance["branch_source_player"]!=source:
                    continue
                kind=provenance["family"]
                weight=F()
                if kind=="source-IC":
                    weight=alpha
                elif kind=="actual-source-SAFE" and provenance["actual_source_player"]==source and provenance["query"]["tail_index"]==m:
                    weight=sT
                elif kind=="same-P-MAX" and provenance["query"]["tail_index"]<m:
                    weight=a
                elif kind=="branch-terminal-BR" and provenance["query"]["kind"]=="indexed-average" and provenance["query"]["family"]==family:
                    weight=F(1)
                if weight:
                    unique_id=provenance["unique_row_id"]
                    payments.append({"raw_row_id":provenance["raw_id"],"unique_row_id":unique_id,
                                     "family":kind,"weight":str(weight)})
                    addrow(paid,packet["inequalities"][unique_id]["row"],weight)
            assert len(payments)==m+3
            remainders=[]
            for offset,state in enumerate(packet["new_columns"]):
                if state["source_player"]!=source:
                    continue
                h=state["hist_column"]
                abits=actual[h]
                b,k=sum(abits[:source-1]),sum(abits[source-1:4])
                bits=tuple(word[slot] for word in words[h])
                x=state["X_bit"]
                # Expand six actual query bits before adding the deterministic
                # Pi correction; this separately checks the average operation.
                raw=sum((literal_residual(source,b,k,x,state["middle_bits"],state["terminal_bit"],F(q))
                         for q in bits),F())/6
                assert raw==literal_residual(source,b,k,x,state["middle_bits"],state["terminal_bit"],theta_by_hist[h])
                corrected=raw+(1-x)*pi_by_hist[h]
                assert corrected>=0
                remainders.append([21021+offset,str(corrected)])
                add(paid,21021+offset,corrected)
                stats["total"]+=1
                stats["zero" if corrected==0 else "positive"]+=1
            equality_payments=[]
            for h,abits in actual.items():
                b,p=sum(abits[:source-1]),sum(abits[:4])
                theta,pi=theta_by_hist[h],pi_by_hist[h]
                common={0:-theta/F(b+1)+pi,
                        1:-(C-1+theta)/F(b+r)-m*a/F(p+1)}
                for x in (0,1):
                    equality=mass[source,h,x]
                    hidden=[column for column,_ in equality["row"] if column>=21021]
                    assert {paid.get(column,F()) for column in hidden}=={common[x]}
                    multiplier=-common[x]
                    addrow(paid,equality["row"],multiplier)
                    equality_payments.append({"equality_row_id":equality["id"],"weight":str(multiplier)})
            assert all(column<21021 for column in paid)
            assert sparse(paid)==sparse(target)
            records.append({"source_player":source,"query_family":family,"C":str(C),
                            "target_row":sparse(target),"Pi_by_hist":pi_records,
                            "nonnegative_budget_payments":payments,
                            "all_corrected_mu_remainders_including_zero":remainders,
                            "signed_mass_equality_payments":equality_payments,
                            "all_hidden_columns_cancel":True})
    assert len(records)==9 and stats["total"]==5376
    assert digest(packet_path)==original_hash
    return {"status":"PASS_INDEPENDENT_PROJECTIONS","projection_count":9,
            "source_constants":{"1":"31","2":"25","3":"19"},
            "all_source_T_degrees_equal_one":True,"all_T_projections_have_zero_Pi":True,
            "nonzero_stored_hist_Pi":nonzero_pi,"corrected_remainder_statistics":dict(stats),
            "all_old436_payment_multipliers_nonnegative":True,
            "all_corrected_mu_remainders_nonnegative":True,
            "all_hidden_columns_cancel_by_mass_equalities":True,
            "old_package_unchanged":True,"point_files_read":0,"optimizer_calls":0,
            "records":records}


def audit_saved_projection(independent,universal):
    certificate_path=LAYER/"averaged_prefix_projection.json.gz"
    rows_path=LAYER/"averaged_prefix_rows_9.json"
    domain_path=LAYER/"averaged_prefix_full_domain.json.gz"
    certificate,interfaces,domains=map(read,(certificate_path,rows_path,domain_path))
    packet=read(OLD/"symbolic_append.json.gz")
    columns=read(OLD/"columns_22941.json.gz")
    hist={j:c for j,c in enumerate(columns[:21021]) if c["kind"]=="hist"}
    xcols={c["hist_column"]:j for j,c in enumerate(columns[:21021]) if c["kind"]=="common-X-mass"}
    actual={h:tuple(map(int,c["actual_bits"])) for h,c in hist.items()}
    old_prefix_path=WORK/"main_prefix_maxx_interface/rows_51.json"
    old_prefix=read(old_prefix_path)
    old_rows={canonical(row["name"]):row for row in old_prefix["rows"]}
    expected={(record["source_player"],record["query_family"]):record for record in independent["records"]}
    assert len(certificate["certificates"])==len(interfaces["rows"])==9
    assert certificate["all_pair_closure_rows_used"] is False
    assert certificate["old_36_projection_unchanged"] is True
    assert certificate["no_point_values"] is True and certificate["optimizer_calls"]==0
    assert interfaces["columns"]==22941 and interfaces["new_columns"]==0
    assert interfaces["point_values_read"] is False
    expected_inputs={"old_append":digest(OLD/"symbolic_append.json.gz"),
                     "old_prefix_rows":digest(old_prefix_path),
                     "averaged_menu_proof":digest(WORK/"main_averaged_menu_prefix.md"),
                     "optimal_union_proof":digest(WORK/"main_optimal_union_prefix.md")}
    assert certificate["input_sha256"]==expected_inputs
    interface_by_key={(row["source_player"],row["menu"]):row for row in interfaces["rows"]}
    seen=set()
    counts=Counter()
    for saved in certificate["certificates"]:
        key=(saved["source_player"],saved["menu"])
        assert key in expected and key not in seen
        seen.add(key)
        own=expected[key]
        source,family=key
        C,alpha,sT,a=SPECS[source]
        assert saved["C"]==own["C"]==str(C)
        assert saved["target_row"]==own["target_row"]
        assert saved["all_hidden_coefficients_canceled"] is True
        paid={}
        payment_key=lambda payment:(payment["raw_row_id"],payment["unique_row_id"],payment["family"],str(F(payment["weight"])))
        assert Counter(map(payment_key,saved["nonnegative_budget_payments"]))==Counter(map(payment_key,own["nonnegative_budget_payments"]))
        for payment in saved["nonnegative_budget_payments"]:
            raw=packet["raw_inequality_provenance"][payment["raw_row_id"]]
            assert raw["unique_row_id"]==payment["unique_row_id"] and raw["family"]==payment["family"]
            assert raw["branch_source_player"]==source
            assert F(payment["weight"])>=0
            addrow(paid,packet["inequalities"][payment["unique_row_id"]]["row"],F(payment["weight"]))
            counts["saved_nonnegative_budget_payments"]+=1
        pi_by_hist={record["hist_column"]:F(record["Pi"]) for record in own["Pi_by_hist"]}
        degree_by_hist={record["hist_column"]:record["degree"] for record in own["Pi_by_hist"]}
        own_corrected=dict((column,F(value)) for column,value in own["all_corrected_mu_remainders_including_zero"])
        expected_columns=[21021+offset for offset,state in enumerate(packet["new_columns"]) if state["source_player"]==source]
        assert [record["column"] for record in saved["mu_remainders"]]==expected_columns
        for remainder in saved["mu_remainders"]:
            column=remainder["column"]
            state=packet["new_columns"][column-21021]
            assert state["source_player"]==source
            h=state["hist_column"]
            abits=actual[h]
            b,k=sum(abits[:source-1]),sum(abits[source-1:4])
            raw_E=literal_residual(source,b,k,state["X_bit"],state["middle_bits"],state["terminal_bit"],F(degree_by_hist[h],6))
            assert F(remainder["E"])==raw_E
            assert F(remainder["Pi"])==pi_by_hist[h]
            assert F(remainder["corrected_E"])==raw_E+(1-state["X_bit"])*pi_by_hist[h]==own_corrected[column]>=0
            add(paid,column,F(remainder["corrected_E"]))
            counts["saved_mu_remainders"]+=1
        mass_key=lambda payment:(payment["equality_row_id"],str(F(payment["weight"])))
        assert Counter(map(mass_key,saved["signed_mass_equality_payments"]))==Counter(map(mass_key,own["signed_mass_equality_payments"]))
        for payment in saved["signed_mass_equality_payments"]:
            row=packet["equalities"][payment["equality_row_id"]]
            assert row["name"][1]==source
            addrow(paid,row["row"],F(payment["weight"]))
            counts["saved_mass_equation_payments"]+=1
        assert sparse(paid)==saved["target_row"]

        interface=interface_by_key[key]
        assert interface["row"]==saved["target_row"] and interface["C"]==str(C)
        assert interface["rhs"]=="0" and interface["sense"]==">="
        assert interface["no_penalty_on_current_support"]==(not any(pi_by_hist.values()))
        assert len(interface["hist_corrections"])==16
        for correction in interface["hist_corrections"]:
            h=correction["hist_column"]
            abits=actual[h]
            assert correction["X_column"]==xcols[h]
            assert correction["n"]==sum(abits[:source-1])+1
            assert correction["k"]==sum(abits[source-1:4])
            assert correction["menu_count"]==degree_by_hist[h]
            assert F(correction["Pi"])==pi_by_hist[h]
            assert correction["old_column_correction"]==[[h,str(pi_by_hist[h])],[xcols[h],str(-pi_by_hist[h])]]
            counts["saved_hist_Pi_corrections"]+=1
        comparison=saved["comparison_to_old_Cstar"]
        old=old_rows[canonical(comparison["old_row_name"])]
        assert old["name"]==["common-X-prefix-SAFE-MAX",source,family]
        delta=F(old["C"])-C
        assert F(comparison["delta"])==delta=={1:F(51,5),2:F(21,4),3:F(4,3)}[source]
        compared={column:F(value) for column,value in old["row"]}
        for h,abits in actual.items():
            b=sum(abits[:source-1])
            add(compared,h,-delta*share(abits[source-1],sum(abits)-abits[source-1])+pi_by_hist[h])
            add(compared,xcols[h],delta/F(b+7-source)-pi_by_hist[h])
        assert sparse(compared)==interface["row"]
        counts["old_Cstar_exact_coefficient_identities"]+=1
    assert seen==set(expected)==set(interface_by_key)
    assert counts["saved_nonnegative_budget_payments"]==54
    assert counts["saved_mu_remainders"]==5376 and counts["saved_mass_equation_payments"]==288
    assert counts["saved_hist_Pi_corrections"]==144

    assert domains["all_5040_corrected_remainders_nonnegative"] is True
    assert domains["all_154_Pi_are_minimal_x0_corrections"] is True
    assert len(domains["Pi_table"])==154 and len(domains["remainder_records"])==5040
    expected_context={(record["source"],record["b"]+1,record["k"],record["degree"]):record for record in universal["Pi_contexts"]}
    seen_context=set()
    for record in domains["Pi_table"]:
        key=(record["source"],record["n"],record["k"],record["menu_count"])
        assert key in expected_context and key not in seen_context
        seen_context.add(key)
        source,n,k,degree=key
        m=5-source
        values=[-literal_residual(source,n-1,k,0,(1,)*j+(0,)*(m-j),0,F(degree,6)) for j in range(m+1)]
        pi=max(F(),*values)
        assert record["values_by_middle_count"]==[str(value) for value in values]
        assert record["maximizing_middle_counts"]==[j for j,value in enumerate(values) if value==pi]
        assert F(record["Pi"])==pi==F(expected_context[key]["Pi"])
        assert F(record["minimum_nonnegative_x0_correction"])==pi
    assert seen_context==set(expected_context)
    seen_remainders=set()
    for record in domains["remainder_records"]:
        source,n,k,degree,x=record["source"],record["n"],record["k"],record["menu_count"],record["x"]
        ys,t=tuple(record["middle_bits"]),record["terminal_bit"]
        key=(source,n,k,degree,x,*ys,t)
        assert key not in seen_remainders
        seen_remainders.add(key)
        raw=literal_residual(source,n-1,k,x,ys,t,F(degree,6))
        pi=formula_pi(source,n-1,k,degree)
        assert F(record["E"])==raw and F(record["Pi"])==pi
        assert F(record["corrected_E"])==raw+(1-x)*pi>=0
    expected_remainder_keys=set()
    for source in range(1,4):
        m=5-source
        for n,k,degree in product(range(1,source+1),range(m+1),range(7)):
            for bits in product((0,1),repeat=m+2):
                expected_remainder_keys.add((source,n,k,degree,*bits))
    assert seen_remainders==expected_remainder_keys
    assert domains["counts"]=={"zero":523,"total":5040,"positive":4517}
    assert domains["union_bridge"]["checked_states"]==5040
    assert domains["union_bridge"]["union_E_nonnegative"] is True
    assert domains["union_bridge"]["no_union_action_or_customer_deletion"] is True
    return {"status":"PASS","saved_certificates_checked":9,"saved_interface_rows_checked":9,
            "counts":dict(counts),"saved_full_domain_Pi_records_checked":154,
            "saved_full_domain_remainders_checked":5040,
            "every_saved_certificate_reassembled_exactly":True,
            "old_Cstar_subtraction_used_only_as_coefficient_identity":True,
            "all_projection_budgets_from_frozen_old436_only":True,
            "audited_inputs":[{"path":path.name,"sha256":digest(path)} for path in (certificate_path,rows_path,domain_path)]}


if __name__=="__main__":
    universal=universal_audit()
    projections=independent_projections()
    result={"universal":universal,"projections":projections,
            "saved_certificate_audit":audit_saved_projection(projections,universal)}
    (HERE/"averaged_prefix_verification.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    brief={"universal":{k:v for k,v in result["universal"].items() if k!="Pi_contexts"},
           "projections":{k:v for k,v in result["projections"].items() if k!="records"},
           "saved_certificate_audit":result["saved_certificate_audit"]}
    print(json.dumps(brief,ensure_ascii=False,indent=2))
