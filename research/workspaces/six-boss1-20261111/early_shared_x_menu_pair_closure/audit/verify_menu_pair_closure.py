#!/usr/bin/env python3
"""Literal, point-free menu-PAIR closure audit; does not import a builder.

Only this new audit directory is writable. Earlier shared-X packages are
read-only, including their output-writing auditors.
"""

from collections import Counter, defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations_with_replacement, product
from pathlib import Path
import gzip
import json

HERE=Path(__file__).resolve().parent
LAYER=HERE.parent
WORK=LAYER.parent
OLD=WORK/"early_shared_x_joint"


def read(path):
    with gzip.open(path,"rt") if path.suffix==".gz" else path.open() as f:
        return json.load(f)


def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(",", ":"),ensure_ascii=False).encode()


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def literal_share(member,background,other):
    return F(1,background+1+other) if member else F()


def literal_tp(background,z,t,q,r):
    return (literal_share(z,background,t)+literal_share(t,background,z)
            +F(z,(background+1)*(background+2))-F(q+r,background+1)
            +F(q*r,(background+1)*(background+2)))


def literal_inputs():
    old_packet=read(OLD/"symbolic_append.json.gz")
    columns=read(OLD/"columns_22941.json.gz")
    assert len(columns)==22941 and len(old_packet["inequalities"])==436
    assert digest(OLD/"symbolic_append.json.gz")=="1ff17a93dc319e05c366424214a722a86577773599ac5692a1fabb6cfaa3a5e0"
    assert columns[21021:]==old_packet["new_columns"]
    hist={j:c for j,c in enumerate(columns[:21021]) if c["kind"]=="hist"}
    assert len(hist)==16
    actual={h:tuple(map(int,c["actual_bits"])) for h,c in hist.items()}
    words={h:tuple(word for word,count in zip(product((0,1),repeat=3),c["hist"])
                   for _ in range(count)) for h,c in hist.items()}
    assert all(len(menu)==6 for menu in words.values())
    by_source={source:[] for source in range(1,5)}
    for offset,state in enumerate(old_packet["new_columns"]):
        by_source[state["source_player"]].append((21021+offset,state))
    return old_packet,columns,hist,actual,words,by_source


def independent_candidates():
    old_packet,columns,hist,actual,words,by_source=literal_inputs()
    old_vectors=defaultdict(list)
    for row in old_packet["inequalities"]:
        old_vectors[canonical(row["row"])].append(row["id"])
    candidates=[]
    averaging_checks=Counter()
    def samples(query,state):
        if query[0]=="X":
            return (state["X_bit"],)
        if query[0]=="A":
            return (actual[state["hist_column"]][query[1]],)
        if query[0]=="Y":
            return (state["middle_bits"][query[1]],)
        if query[0]=="Tnew":
            return (state["terminal_bit"],)
        assert query[0]=="menu"
        slot=("T","B","C").index(query[1])
        return tuple(word[slot] for word in words[state["hist_column"]])
    for source in range(1,5):
        m=5-source
        queries=[("X",)]+[("A",j) for j in range(6)]+[("Y",j) for j in range(m)]+[("Tnew",)]
        queries += [("menu",family) for family in ("T","B","C")]
        assert len(queries)==16-source
        for left,right in combinations_with_replacement(queries,2):
            row=[]
            for column,state in by_source[source]:
                h=state["hist_column"]
                background=sum(actual[h][:source-1])+state["X_bit"]+sum(state["middle_bits"][:-1])
                z,t=state["middle_bits"][-1],state["terminal_bit"]
                qbits,rbits=samples(left,state),samples(right,state)
                value=sum((literal_tp(background,z,t,q,r) for q,r in product(qbits,rbits)),F())/F(len(qbits)*len(rbits))
                # Independent cartesian expansion must match its distributive
                # closed expression, including a mean squared on menu self.
                qbar,rbar=F(sum(qbits),len(qbits)),F(sum(rbits),len(rbits))
                d=background+1
                wallet=literal_share(z,background,t)+literal_share(t,background,z)+F(z,d*(d+1))
                assert value==wallet-(qbar+rbar)/d+qbar*rbar/(d*(d+1))
                averaging_checks[(len(qbits),len(rbits))]+=1
                if value:
                    row.append([column,str(value)])
            candidates.append({"source":source,"left":left,"right":right,"row":row})
    assert len(candidates)==394
    assert Counter(row["source"] for row in candidates)=={1:120,2:105,3:91,4:78}
    groups={}
    categories=Counter()
    flags=Counter()
    retained=[]
    for raw_id,record in enumerate(candidates):
        vector=canonical(record["row"])
        zero=not record["row"]
        nonnegative=all(F(value)>=0 for _,value in record["row"])
        old_ids=old_vectors.get(vector,[])
        duplicate=vector in groups
        if not duplicate:
            groups[vector]=len(groups)
        group=groups[vector]
        if zero:
            category="zero"
        elif old_ids:
            category="old436_duplicate"
        elif duplicate:
            category="within_candidate_duplicate"
        elif nonnegative:
            category="mu_nonnegative"
        else:
            category="new_nontrivial"
            retained.append(record)
        record.update(raw_id=raw_id,group=group,category=category,is_zero=zero,
                      mu_coefficientwise_nonnegative=nonnegative,old436_exact_row_ids=old_ids)
        categories[category]+=1
        flags["zero"]+=zero
        flags["mu_nonnegative_including_zero"]+=nonnegative
        flags["old436_exact_duplicate"]+=bool(old_ids)
        flags["within_candidate_duplicate"]+=duplicate
        assert all(column>=21021 for column,_ in record["row"])
    return {"candidates":candidates,"retained":retained,
            "summary":{"status":"INDEPENDENT_LITERAL_CANDIDATES_BUILT","raw_rows":394,
                       "per_source_raw_rows":{"1":120,"2":105,"3":91,"4":78},
                       "unique_candidate_vectors":len(groups),"primary_classification":dict(categories),
                       "flags":dict(flags),"retained_unique_nontrivial_rows":len(retained),
                       "raw_nonzero_coefficients":sum(len(row["row"]) for row in candidates),
                       "retained_nonzero_coefficients":sum(len(row["row"]) for row in retained),
                       "literal_hidden_state_query_expansions":{str(key):value for key,value in averaging_checks.items()},
                       "nonzero_candidates_cannot_equal_old23676_by_disjoint_column_support":True,
                       "menu_self_uses_all36_pairs_not_six_diagonal_pairs":True,
                       "old436_is_read_only":True,"point_files_read":0,"optimizer_calls":0,
                       "retained_vector_multiset_sha256":sha256(canonical(sorted([row["row"] for row in retained],key=canonical))).hexdigest()}}


def universal_literal_identities():
    counts=Counter()
    for background in range(5):
        for z,t,q,r,reply in product((0,1),repeat=5):
            first=literal_share(z,background,t)-literal_share(q,background,reply)
            second=literal_share(reply,background,q)-literal_share(r,background,q)
            third=literal_share(t,background,z)-literal_share(reply,background,z)
            nonnegative=F(z*(1-reply),(background+1)*(background+2))
            assert literal_tp(background,z,t,q,r)==first+second+third+nonnegative
            assert nonnegative>=0
            counts["three_IC_plus_nonnegative_PAIR_cases"]+=1
        for z,t in product((0,1),repeat=2):
            assert literal_tp(background,z,t,z,t)==F(z*(1-t),(background+1)*(background+2))>=0
            counts["actual_penultimate_terminal_trivial_identity_cases"]+=1
    menus=list(product((0,1),repeat=6))
    for left,right in product(menus,repeat=2):
        literal_cartesian=sum(q*r for q,r in product(left,right))
        assert literal_cartesian==sum(left)*sum(right)
        counts["all_six_bit_menu_cartesian_overlap_identities"]+=1
    for menu in menus:
        diagonal=sum(q*q for q in menu)
        all36=sum(q*r for q,r in product(menu,repeat=2))
        degree=sum(menu)
        assert diagonal==degree and all36==degree*degree
        assert F(diagonal,6)-F(all36,36)==F(degree,6)*(1-F(degree,6))>=0
        counts["menu_self_full36_vs_six_diagonal_identities"]+=1
    return {"status":"PASS","counts":dict(counts),
            "cartesian_product_is_distributivity_not_probabilistic_independence":True,
            "all_IC_budgets_global_not_customerwise":True}


def audit_saved_packet(independent):
    all_path=LAYER/"all_pair_candidates.json.gz"
    usable_path=LAYER/"usable_pair_append.json.gz"
    dominance_path=LAYER/"diagonal_menu_dominance.json.gz"
    all_pairs,usable,dominance=map(read,(all_path,usable_path,dominance_path))
    old_packet,columns,hist,actual,words,by_source=literal_inputs()
    old_hash=digest(OLD/"symbolic_append.json.gz")
    old_freeze_hash=digest(OLD/"freeze_manifest.json")
    expected_base={"shape":[23676,21021],"sha256":"1b4a4e544e5b9eeea1fa64b3849a9d4cc532b997a5ad972ce33df81c224551e7"}
    expected_old={"shape_ge":[24112,22941],"new_eq":128,"sha256":old_hash,"freeze_sha256":old_freeze_hash}
    for packet in (all_pairs,usable):
        assert packet["base_old_matrix"]==expected_base
        assert packet["frozen_four_source_layer"]==expected_old
        assert packet["columns"]==22941 and packet["new_columns"]==packet["new_equalities"]==0
        assert packet["all_existing_equalities_bounds_and_normalization_retained"] is True
        assert packet["no_cone_independence_claim"] is True
        assert packet["optimizer_calls"]==0 and packet["point_values_read"] is False
    assert len(all_pairs["raw_pairs"])==len(all_pairs["exact_vector_groups"])==394
    assert len(usable["rows"])==usable["row_count"]==306
    assert usable["new_GE_shape"]==[24418,22941]
    assert usable["nonzeros"]==131721
    assert usable["support_excludes_old23676_duplicates_without_large_matrix_scan"] is True

    def parse_query(query,source):
        kind=query["kind"]
        if kind=="X":return ("X",)
        if kind=="actual":
            assert 1<=query["player"]<=6
            return ("A",query["player"]-1)
        if kind=="indexed-average":
            family=query["family"]
            assert family in ("T","B","C")
            assert query["members"]==[f"{family}{j}" for j in range(1,7)]
            assert query["weights"]==["1/6"]*6
            assert query["not_a_pure_action"] is True
            return ("menu",family)
        assert kind=="new-tail" and query["source_player"]==source
        index=query["tail_index"]
        m=5-source
        assert 0<=index<=m and query["player"]==source+index+1
        assert query["name"]==(f"Y{index+1}_at_source{source}" if index<m else f"T_at_source{source}")
        return ("Y",index) if index<m else ("Tnew",)

    expected_by_key={(row["source"],row["left"],row["right"]):row for row in independent["candidates"]}
    classifications={"zero":"zero", "old436_duplicate":"exact_duplicate_old436",
                     "within_candidate_duplicate":"exact_duplicate_earlier_candidate",
                     "mu_nonnegative":"trivial_from_mu_nonnegativity",
                     "new_nontrivial":"new_nontrivial_candidate"}
    append_seen=set()
    key_seen=set()
    first_group_vectors={}
    for source in range(1,5):
        queries=all_pairs["queries_by_source"][str(source)]
        parsed=[parse_query(query,source) for query in queries]
        expected_queries=[("X",)]+[("A",j) for j in range(6)]+[("Y",j) for j in range(5-source)]+[("Tnew",)]+[("menu",f) for f in ("T","B","C")]
        assert parsed==expected_queries
    for raw_id,record in enumerate(all_pairs["raw_pairs"]):
        assert record["raw_pair_id"]==raw_id
        source=record["source_player"]
        queries=all_pairs["queries_by_source"][str(source)]
        li,ri=record["left_query_index"],record["right_query_index"]
        assert 0<=li<=ri<len(queries)
        assert record["left_query"]==queries[li] and record["right_query"]==queries[ri]
        left,right=parse_query(record["left_query"],source),parse_query(record["right_query"],source)
        key=(source,left,right)
        assert key in expected_by_key and key not in key_seen
        key_seen.add(key)
        independent_row=expected_by_key[key]
        group_id=record["vector_group_id"]
        group=all_pairs["exact_vector_groups"][group_id]
        assert group["group_id"]==group_id
        assert group["row"]==independent_row["row"] and group["rhs"]=="0"
        assert group["is_zero"]==independent_row["is_zero"]
        assert group["mu_coefficientwise_nonnegative"]==independent_row["mu_coefficientwise_nonnegative"]
        assert group["old436_exact_row_ids"]==independent_row["old436_exact_row_ids"]
        assert group["old23676_exact_duplicate_possible"] is False
        assert group["raw_pair_ids"]==record["same_vector_raw_pair_ids"]==[raw_id]
        assert record["flags"]=={"is_zero":independent_row["is_zero"],
                                  "mu_coefficientwise_nonnegative":independent_row["mu_coefficientwise_nonnegative"],
                                  "old436_exact_row_ids":independent_row["old436_exact_row_ids"]}
        assert record["primary_outcome"]==classifications[independent_row["category"]]
        vector=canonical(group["row"])
        assert vector not in first_group_vectors
        first_group_vectors[vector]=group_id
        provenance=record["provenance"]
        m=5-source
        expected_history=[f"A{j}" for j in range(1,source)]+["X"]+[f"Y{j}_at_source{source}" for j in range(1,m)]
        assert provenance["history"]==expected_history and len(expected_history)==4
        assert provenance["actual_penultimate"]==f"Y{m}_at_source{source}"
        assert provenance["actual_terminal"]==f"T_at_source{source}"
        assert provenance["actual_u5_u6_used"] is False
        assert provenance["cross_forced_branch_overlap_used"] is False
        append_id=record["usable_append_row_id"]
        assert append_id==group["usable_append_row_id"]
        if independent_row["category"]=="new_nontrivial":
            assert append_id is not None and append_id not in append_seen
            append_seen.add(append_id)
            appended=usable["rows"][append_id]
            assert appended["id"]==append_id
            assert appended["global_ge_row_index"]==24112+append_id
            assert appended["vector_group_id"]==group_id
            assert appended["raw_pair_ids"]==[raw_id]
            assert appended["row"]==independent_row["row"]
            assert appended["rhs"]=="0" and appended["sense"]==">="
        else:
            assert append_id is None
        if independent_row["category"]=="mu_nonnegative":
            assert (left,right)==(("Y",m-1),("Tnew",))
    assert key_seen==set(expected_by_key)
    assert append_seen==set(range(306))
    assert Counter(canonical(row["row"]) for row in usable["rows"])==Counter(canonical(row["row"]) for row in independent["retained"])
    expected_checks={"coefficient_states":209920,"literal_ordered_pairs":937600,
                     "pure_pure_states":133504,"pure_menu_states":64896,"menu_menu_states":11520}
    assert all_pairs["literal_checks"]==expected_checks

    assert dominance["old_bytes_unchanged"] is True and len(dominance["records"])==12
    dominance_seen=set()
    dominance_coefficients=0
    for record in dominance["records"]:
        source,family=record["source_player"],record["menu"]
        assert (source,family) not in dominance_seen
        dominance_seen.add((source,family))
        old_raw=old_packet["raw_inequality_provenance"][record["old_diagonal_raw_row_id"]]
        assert old_raw["family"]=="branch-true-PAIR" and old_raw["mode"]=="Q,Q"
        assert old_raw["branch_source_player"]==source
        assert old_raw["query_left"]["kind"]=="indexed-average" and old_raw["query_left"]["family"]==family
        assert old_raw["query_right"]==old_raw["query_left"]
        assert old_raw["unique_row_id"]==record["old_diagonal_unique_row_id"]
        new_raw=all_pairs["raw_pairs"][record["new_full36_raw_pair_id"]]
        assert new_raw["source_player"]==source
        assert parse_query(new_raw["left_query"],source)==parse_query(new_raw["right_query"],source)==("menu",family)
        assert new_raw["usable_append_row_id"]==record["new_full36_append_row_id"]
        old_row=dict((column,F(value)) for column,value in old_packet["inequalities"][old_raw["unique_row_id"]]["row"])
        new_row=dict((column,F(value)) for column,value in usable["rows"][record["new_full36_append_row_id"]]["row"])
        difference={column:old_row.get(column,F())-new_row.get(column,F()) for column in set(old_row)|set(new_row)}
        expected_difference={}
        slot=("T","B","C").index(family)
        for column,state in by_source[source]:
            h=state["hist_column"]
            q=F(sum(word[slot] for word in words[h]),6)
            d=1+sum(actual[h][:source-1])+state["X_bit"]+sum(state["middle_bits"][:-1])
            value=q*(1-q)/F(d*(d+1))
            assert value>=0 and difference.get(column,F())==value
            if value:
                expected_difference[column]=value
            dominance_coefficients+=1
        expected_sparse=[[column,str(value)] for column,value in sorted(expected_difference.items())]
        assert record["old_minus_full36_nonnegative_row"]==expected_sparse
    assert dominance_seen==set(product(range(1,5),("T","B","C")))
    assert dominance_coefficients==5760
    assert digest(OLD/"symbolic_append.json.gz")==old_hash
    assert digest(OLD/"freeze_manifest.json")==old_freeze_hash
    return {"status":"PASS","all_raw_pairs_and_vector_groups_verified":394,
            "usable_append_rows_verified":306,"all_source_query_and_row_maps_verified":True,
            "all_12_diagonal_dominance_rows_verified":True,"diagonal_difference_state_coefficients_checked":5760,
            "old_frozen_layer_and_freeze_manifest_unchanged":True,
            "nonzero_candidate_old23676_exclusion_proved_by_column_support":True,
            "no_cone_independence_or_strict_separation_claim":True,
            "new_total_GE_shape":[24418,22941],"existing_mass_equalities_retained":128,
            "audited_inputs":[{"path":path.name,"sha256":digest(path)} for path in (all_path,usable_path,dominance_path)]}


def audit_direct_BR_redundancy(independent):
    redundancy_path=LAYER/"direct_BR_redundancy.json.gz"
    certificate=read(redundancy_path)
    old_packet,columns,hist,actual,words,by_source=literal_inputs()
    all_pairs=read(LAYER/"all_pair_candidates.json.gz")
    usable=read(LAYER/"usable_pair_append.json.gz")
    expected={}
    for record in independent["retained"]:
        source=record["source"]
        zquery=("Y",4-source)
        left,right=record["left"],record["right"]
        if left==zquery:
            other=right
        elif right==zquery:
            other=left
        else:
            continue
        assert other[0] in ("A","menu","Y") and other!=zquery
        if other[0]=="Y":
            assert other[1]<4-source
        expected[source,other]=record
    assert len(expected)==42
    assert Counter(source for source,_ in expected)=={1:12,2:11,3:10,4:9}
    def qtoken(query):
        if query["kind"]=="actual":return ("A",query["player"]-1)
        if query["kind"]=="indexed-average":return ("menu",query["family"])
        assert query["kind"]=="new-tail"
        return ("Y",query["tail_index"])
    assert certificate["record_count"]==len(certificate["records"])==42
    assert certificate["counts_by_source"]=={"1":12,"2":11,"3":10,"4":9}
    assert certificate["optimizer_calls"]==0
    assert certificate["old436_and_306_packet_bytes_unchanged"] is True
    input_files={"early_shared_x_joint/symbolic_append.json.gz":OLD/"symbolic_append.json.gz",
                 "early_shared_x_menu_pair_closure/all_pair_candidates.json.gz":LAYER/"all_pair_candidates.json.gz",
                 "early_shared_x_menu_pair_closure/usable_pair_append.json.gz":LAYER/"usable_pair_append.json.gz"}
    assert certificate["input_sha256"]=={name:digest(path) for name,path in input_files.items()}
    seen=set()
    omittable=[]
    state_checks=nonzeros=0
    for saved in certificate["records"]:
        source=saved["source_player"]
        query=qtoken(saved["query"])
        key=(source,query)
        assert key in expected and key not in seen
        seen.add(key)
        independent_row=expected[key]
        raw=all_pairs["raw_pairs"][saved["raw_pair_id"]]
        append_id=saved["append306_row_id"]
        assert raw["source_player"]==source and raw["usable_append_row_id"]==append_id
        assert usable["rows"][append_id]["row"]==independent_row["row"]
        old_raw=old_packet["raw_inequality_provenance"][saved["old_BR_raw_row_id"]]
        assert old_raw["family"]=="branch-terminal-BR" and old_raw["branch_source_player"]==source
        assert old_raw["query"]==saved["query"]
        assert old_raw["unique_row_id"]==saved["old_BR_unique_row_id"]
        old_row={column:F(value) for column,value in old_packet["inequalities"][old_raw["unique_row_id"]]["row"]}
        new_row={column:F(value) for column,value in independent_row["row"]}
        literal_remainder=[]
        for column,state in by_source[source]:
            h=state["hist_column"]
            d=1+sum(actual[h][:source-1])+state["X_bit"]+sum(state["middle_bits"][:-1])
            z,t=state["middle_bits"][-1],state["terminal_bit"]
            value=F(z*(1-t),d*(d+1))
            assert new_row.get(column,F())==old_row.get(column,F())+value
            assert value>=0
            state_checks+=1
            if value:
                literal_remainder.append([column,str(value)])
                nonzeros+=1
        assert saved["nonnegative_mu_remainder"]==literal_remainder
        assert all(column>=21021 for column in set(new_row)|set(old_row))
        omittable.append(append_id)
    assert seen==set(expected) and len(set(omittable))==42
    omittable=sorted(omittable)
    retained=[row["id"] for row in usable["rows"] if row["id"] not in set(omittable)]
    assert certificate["append306_row_ids_omittable_with_certificate"]==omittable
    assert certificate["append306_row_ids_retained_after_this_one_rule"]==retained
    assert certificate["retained_rows"]==len(retained)==264
    assert certificate["retained_nonzeros"]==sum(len(usable["rows"][row_id]["row"]) for row_id in retained)==116034
    assert state_checks==21632 and nonzeros==5408
    return {"status":"PASS","exact_old_BR_implications_checked":42,
            "counts_by_source":{"1":12,"2":11,"3":10,"4":9},
            "literal_state_coefficients_checked":state_checks,"nonnegative_remainder_nonzeros":nonzeros,
            "core_rows_after_this_certified_omission":264,"core_nonzeros":116034,
            "core_total_GE_shape":[24376,22941],
            "all_42_omitted_rows_implied_by_old436_and_mu_nonnegativity":True,
            "remaining264_irredundancy_not_claimed":True,
            "original306_packet_unchanged":True,
            "certificate_sha256":digest(redundancy_path)}


if __name__=="__main__":
    independent=independent_candidates()
    result={"candidate_construction":independent["summary"],
            "universal_literal_identities":universal_literal_identities(),
            "packet_audit":audit_saved_packet(independent),
            "direct_BR_redundancy":audit_direct_BR_redundancy(independent)}
    (HERE/"independent_verification.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(result,ensure_ascii=False,indent=2))
