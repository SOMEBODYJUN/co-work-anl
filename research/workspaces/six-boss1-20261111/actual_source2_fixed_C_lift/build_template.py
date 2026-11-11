#!/usr/bin/env python3
"""Build the unbound734-row local contract and full751 migration ledger; no solve."""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import importlib.util
import json
import shutil
import sys

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
BASE=HERE.parent
REPO=HERE.parents[3]
OLD=BASE/"actual_source2_nested_requery"
sha=lambda p:sha256(p.read_bytes()).hexdigest()
def dump(name,obj):
    p=HERE/name;assert not p.exists(),name
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n")
assert not (HERE/"freeze_manifest.json").exists()
for src,dest,expected in [
    (OLD/"row_catalogue.json","legacy_751_catalogue.json","028a6de290df6e69213439fb702dd7c3357350e2bc628846a924255d8a6f3cdc"),
    (OLD/"symbolic_coefficients.py","legacy_751_kernel.py.txt","8dfd7b79a7d1d497c890f7164ba6ea119be74121af40135716b818fdfe4d6629"),
    (BASE/"actual_source2_opt_requery/symbolic_coefficients.py","legacy_243_kernel.py.txt","3b8a00fa72b2b15678656f7f2f21f18610ab2f1586d850b080a1d61235e4a205")]:
    assert sha(src)==expected and not (HERE/dest).exists()
    shutil.copyfile(src,HERE/dest);assert sha(HERE/dest)==expected
spec=importlib.util.spec_from_file_location("fixed_c_kernel",HERE/"symbolic_coefficients.py")
kernel=importlib.util.module_from_spec(spec);spec.loader.exec_module(kernel)
full=kernel.full_catalogue();active=kernel.active_catalogue()
assert len(full)==751 and len(active)==734
visible=json.loads((BASE/"visible_maximum_joint/exact_input.json").read_text())
assert sha(BASE/"visible_maximum_joint/exact_input.json")=="b0610bb00298a4ee953423a8066dab050cb9d515fd6d5dde41f5117116f2ba33"
global_by_name={row["name"]:(i,row) for i,row in enumerate(visible["raw_rows"])}
routes=[]
for row in full:
    if row["destination"]=="local_hidden":continue
    old=row["legacy_index"];family=row["family"]
    if old==235:
        target="C_maximum_size";target_index=1;global_row=visible["equalities"][1]
        payment=-1;kind="free_equality"
    else:
        if family=="MAX":target="FMAX_C"
        elif family=="MX":target="MX_C"
        elif family=="ACTUAL_SAFE":target=f'SAFE_{row["source"]}_C'
        else:
            assert family=="ACTUAL_RC" and row["queries"][0]=="C"
            target="RC_C_"+row["queries"][1]
        target_index,global_row=global_by_name[target];payment=1;kind="visible_nonnegative_raw"
    for h in range(512):
        atom=kernel.atom_from_index(h)
        A=kernel.coefficient(row,atom,(0,0,0,0))
        assert all(kernel.coefficient(row,atom,tail)==A for tail in [(1,0,0,0),(0,1,1,0),(1,1,1,1)])
        literal=kernel.base_atom_coefficient(row,atom)-A
        assert literal==payment*F(global_row["a"].get(str(h),"0")),(old,h)
    assert kernel.base_K_coefficient(row)==payment*F(global_row["a"].get("512","0"))
    assert F(global_row["rhs"])==0
    routes.append({"legacy_index":old,"legacy_name":row["legacy_name"],"fixed_C_name":row["name"],
        "route_kind":kind,"global_name":target,"global_raw_or_equality_index":target_index,
        "payment_multiplier":str(payment),"rhs_form":kernel.rhs_form(row),
        "literal_global_row_sha256":sha256(json.dumps(global_row,sort_keys=True,separators=(",",":")).encode()).hexdigest(),
        "all513_coefficient_identity_checks":513,
        "scope":"Same actual A1..A6 and common actual-P maximizer X; true globally maximum C; same six legal query union O.",
        "future_release_check":"Reconfirm this exact formula and actual-role routing on the future visible input; not inferred from a row name alone."})
assert len(routes)==17 and sum(r["route_kind"]=="visible_nonnegative_raw" for r in routes)==16
route_by_old={r["legacy_index"]:r for r in routes}
ledger=[]
reason={
    "IC_SOURCE2":"The actual source2 IC against one fixed legal C and that history's prescribed successors; averaging was only an optional later sum.",
    "CAP":"Every generated R label and fixed C is legal and has size at most global K; C itself attains K.",
    "ACTUAL_SAFE":"A generated legal label can be queried at each original actual source using that query's own prescribed continuation.",
    "MAX":"The single X maximizes f at the unchanged original actual four-action prefix over the entire catalogue.",
    "MX":"Original actual source5 IC, its own true reply, and actual-prefix X maximality; the generating R6 is not frozen as that reply.",
    "NEW_SAFE":"Sources3..6 are genuine decisions after the fixed legal history(A1,C); all query roles are legal or inner menu means.",
    "NEW_PAIR":"The true last-two prefix is(A1,C,R3,R4); arbitrary legal query roles share its same true-reply payment.",
    "ACTUAL_RC":"The RC wallet remains original actual u5+F_X; generated pure query roles are legal, with literal same-client overlaps.",
    "NESTED_SOURCE25":"Apply P25 only at genuine inner sources3,4,5 using their branch payoffs/prefixes and each inner forcing's own true successors.",
    "NESTED_C30":"C30 is valid at any fixed legal two-action history, here(A1,C); its internal six-query moments are separately eliminated in the frozen128 table."}
for row in full:
    record={"legacy_index":row["legacy_index"],"legacy_name":row["legacy_name"],"fixed_C_name":row["name"],
        "family":row["family"],"valid_for_any_fixed_legal_outer_label":True,
        "depends_on_outer_six_index_average":False,"destination":row["destination"],"reason":reason[row["family"]]}
    if row["legacy_index"] in route_by_old:record["visible_route"]=route_by_old[row["legacy_index"]]
    ledger.append(record)
dump("migration_audit.json",{"status":"ALL751_KERNELS_TRANSFER_POINTWISE_OUTER_MOMENTS_REMOVED","optimizer_calls":0,
    "all751_row_records":ledger,"inapplicable_genuine_kernel_indices":[],
    "removed_outer_interfaces":[
        {"old":"-sum(q*nu[v,q,r]) <= -o_v*z_v/6","reason":"q averaged a six-query membership. Fixed c is one label and need not be at least o/6."},
        {"old":"sum(q*nu[v,q,r]) <= o_v*z_v","reason":"A global largest C can contain clients outside an optimal six-query union."},
        {"old":"moment_envelope(a0,a1,o) with lower/upper multipliers","replacement":"m(h)=min over the16 tail states W(h,r); one free mass multiplier m(h), no outer moment multiplier."},
        {"old":"nu includes an outer1/6 and32 states per old8-bit type","replacement":"nu is physical same-client mass for one fixed C branch;16 tail states per full9-bit type."}],
    "inner_menu_moments_preserved":"P25 inner means and the C30 theorem's separate inner six-forcing-index moment elimination remain valid and unchanged."})
dump("full751_audit_view.json",{"status":"SYMBOLIC_UNBOUND","count":751,"rows":full,
    "legacy_descriptor_bytes":"legacy_751_catalogue.json","legacy_kernel_bytes":"legacy_751_kernel.py.txt",
    "note":"All751 kernels remain valid after the state reinterpretation q=c. Seventeen are routed to visible prerequisites/equality, not invalidated."})
dump("active734_catalogue.json",{"status":"SYMBOLIC_UNBOUND","convention":"A_R nu <= b_R(w,K)",
    "row_count":734,"family_counts":dict(Counter(r["family"] for r in active)),"query_descriptors":kernel.QUERIES,
    "rows":active,"zero_and_duplicate_kernels_retained":True,
    "minimality_scope":"Local hidden-row contract after routing17 purely visible rows; no irredundancy or globally minimal inequality-basis claim."})
dump("visible_prerequisite_routing.json",{"status":"EXACT_ALL513_ROUTING","route_count":17,"nonnegative_visible_rows":16,
    "free_C_size_equalities":1,"all_coefficient_checks":17*513,"routes":routes,
    "current_formula_reference_input":"research/workspaces/six-boss1-20261111/visible_maximum_joint/exact_input.json",
    "current_formula_reference_sha256":"b0610bb00298a4ee953423a8066dab050cb9d515fd6d5dde41f5117116f2ba33",
    "no_point_read_or_bound":True,"future_reconfirmation_required":True,
    "scope_note":"These16 visible inequalities are prerequisites, not claimed consequences of the734 hidden rows. CAP(C) is exactly minus the global |C|-K equality."})
dump("symbolic_template.json",{"status":"SYMBOLIC_UNBOUND_FIXED_C","owner":"Boss1","RUN":"six-boss1-20261111",
    "state":{"visible_bits":["a1","a2","a3","a4","a5","a6","x","o","c"],"tail_bits":["r3","r4","r5","r6"],
        "true_branch":["A1","C","R3","R4","R5","R6"],"visible_types":512,"tail_states_per_type":16,
        "full_symbolic_state_count":8192,"same_client_joint_law":True,"outer_index_average":False},
    "mass_equation":"sum_{r3,r4,r5,r6} nu[h,r]=w[h] for every complete visible9-bit h",
    "outer_q_moment_rows":[],"local_hidden_inequalities":734,"visible_prerequisites":"visible_prerequisite_routing.json",
    "dimensions_for_future_positive_type_count_s":{"nu_columns":"16*s","mass_equalities":"s","local_inequalities":734,"outer_moment_rows":0},
    "projection_contract":{"weights":"lambda_R>=0 on local A_R nu<=b_R(w,K)","W":"sum_R lambda_R*A_R(h,r)",
        "minimum":"m(h)=min_{r in {0,1}^4} W(h,r)","free_mass_multiplier":"m(h), unrestricted sign",
        "state_residual":"W(h,r)-m(h)>=0","projected_inequality":"sum_R lambda_R*b_R(w,K)-sum_h m(h)*w[h]>=0",
        "full_domain_required":"all512 visible types and all8192 joint states for any eventual universal cut"},
    "fixed_input":None,"fixed_atom_masses":None,"fixed_K":None,"fixed_O":None,"support":None,"fixed_matrix":None,
    "phaseI":None,"certificate":None,"projection_weights":None,"optimizer_calls":0,"optimizer_authorized":False,
    "forbidden_bindings":"Previously excluded1002/1003 candidates; no old-point phaseI or numerical solver is included.",
    "future_gate":"Main separately releases a surviving future candidate after newer necessary-family screening and rechecks16 visible prerequisites plus C-size equality."})
dump("future_point_release_template.json",{"status":"UNBOUND_NO_AUTHORIZATION","released_by":None,"future_input_path":None,
    "future_input_sha256":None,"future_exact_primal_path":None,"future_exact_primal_sha256":None,"full512_mass_vector":None,
    "K":None,"O":None,"positive_visible_type_count":None,"confirmed_visible_prerequisites":None,
    "confirmed_C_size_equality":None,"explicit_instantiation_authorization":None,"explicit_optimizer_authorization":None,
    "old1002_and1003_candidates_not_eligible":True})

paths=[OLD/n for n in ["derivation.md","source_review.md","symbolic_coefficients.py","row_catalogue.json","symbolic_template.json","literal_samples.json","freeze_manifest.json"]]
paths += [BASE/"actual_source2_nested_requery_audit"/n for n in ["audit_result.json","proof_audit.json","freeze_manifest.json"]]
paths += [BASE/"actual_source2_opt_requery"/n for n in ["derivation.md","source_review.md","symbolic_coefficients.py","row_catalogue.json"]]
paths += [BASE/"main_all_source25_family"/n for n in ["proof.md","exact_family.json"]]
paths += [BASE/"main_thirty_index_strengthening"/n for n in ["proof.md","requery30_envelopes.json","requery30_states.json"]]
paths += [BASE/"visible_maximum_joint"/n for n in ["exact_input.json","source_review.md"]]
paths += [REPO/"archives/customer-attraction/state"/n for n in ["定义/共同目录完整历史模型--定义.md","引理/真实末回复的共同潜力上限与重叠参数端点--引理.md","引理/末两人重叠比较与任意索引聚合--引理.md"]]
pins={str(p.relative_to(REPO)):sha(p) for p in paths}
dump("source_pins.json",{"status":"SYMBOLIC_UNBOUND","source_count":len(pins),"sources":pins,
    "old_numeric_primal_or_optimal_face_files_read":False})
dump("build_result.json",{"status":"SYMBOLIC_UNBOUND_FIXED_C","full_audit_rows":751,"active_hidden_rows":734,
    "visible_prerequisite_rows":16,"global_C_size_equality_routes":1,"full_joint_states":8192,
    "outer_q_moment_rows":0,"full_513_routing_checks":17*513,"optimizer_calls":0,"point_bound":False,"matrix_constructed":False})
print((HERE/"build_result.json").read_text())
