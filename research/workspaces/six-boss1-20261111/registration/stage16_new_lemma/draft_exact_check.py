"""Read-only source replay for a formal-return draft; no optimizer imports.

Only this draft directory is written. The frozen builders are not executed.
"""
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import json
import re

HERE = Path(__file__).resolve().parent
WS = HERE.parents[1]
REPO = WS.parents[2]
SCALE = 2291851735510680
DB = 458370347102136


def digest(p):
    return sha256(p.read_bytes()).hexdigest()


def load(rel, expected=None):
    p = WS / rel
    if expected is not None:
        assert digest(p) == expected, str(p)
    return json.loads(p.read_text())


def payoff(seq, j):
    return F(seq[j], sum(seq)) if sum(seq) else F(0)


def guaranteed(bit, prefix, followers=0):
    return F(bit, prefix + 1 + followers)


def pair_wallet(seq):
    d = 1 + sum(seq[:4])
    return payoff(seq, 4) + payoff(seq, 5) + F(seq[4], d*(d+1))


def query_cost(menu, d, distinct):
    values = []
    for i, t in enumerate(menu):
        for j, q in enumerate(menu):
            if distinct and i == j:
                continue
            values.append(F(t, d+q)+F(q, d))
    return sum(values, F(0))/len(values)


def source_cost(bits, state, distinct):
    old, o = bits[:6], bits[6]
    q, r, y, t = state
    new = old[:2] + state
    d = 1 + sum(new[:4])
    ans = 126000 * payoff(new, 2)
    for bit, weight in zip((r, y, t), (43, 31218, 34458)):
        ans += weight * guaranteed(bit, sum(old[:3]), 2)
    for bit in (r, y, t):
        ans += 1654 * guaranteed(bit, sum(old[:5]))
    ans += 5400 * (guaranteed(o, sum(new[:5]))/6-payoff(new, 5))
    ans += 7740 * (query_cost((o, 0, 0, 0, 0, 0), d, distinct)-pair_wallet(new))
    return ans


def explicit_phi30(bits, state):
    p, y2, y3, y4, y5, z, o = bits
    q, r, y, t = state
    b = p+y2
    d = 1+b+q+r
    return (F(126000*q, b+1+r+y+t)
            + F(43*r+31218*y+34458*t, b+y3+3)
            + F(1654*(r+y+t), b+y3+y4+y5+1)
            + 5400*(F(o, 6)-t)/(d+y)
            + 7740*(F(o, 3*d)-F(y, d+t)-F(t, d+y)-F(y, d*(d+1))))


def root_atom(name, bits, minimum, distinct):
    seq, o = bits[:6], bits[6]
    if name == 'ROOT_IC':
        return -payoff(seq, 0)
    if name.startswith('CAP_B'):
        return -F(seq[int(name[-1])-1])
    if name.startswith('SAFE_j'):
        j = int(name.split('|')[0][-1])
        return payoff(seq, j-1)-guaranteed(o, sum(seq[:j-1]), 6-j)/6
    if name == 'PAIR|Omean|Omean':
        d = 1+sum(seq[:4])
        return pair_wallet(seq)-query_cost((o, 0, 0, 0, 0, 0), d, distinct)
    assert name == 'OPT_SOURCE3_REQUERY_CUT'
    return 126000*payoff(seq, 2)+65719*payoff(seq, 3)+4962*payoff(seq, 5)-minimum


def patch_appendix(label, contents):
    p = HERE / 'body.md'
    text = p.read_text()
    marker = f'<!-- APPENDIX_{label}_' + ('TABLE -->' if label == 'A' else 'EVIDENCE -->')
    start, end = f'<!-- BEGIN VERIFIED APPENDIX {label} -->', f'<!-- END VERIFIED APPENDIX {label} -->'
    block = start+'\n\n'+contents+'\n\n'+end
    if marker in text:
        assert text.count(marker) == 1
        text = text.replace(marker, block)
    else:
        pattern = re.escape(start)+'.*?'+re.escape(end)
        text, count = re.subn(pattern, lambda _: block, text, flags=re.S)
        assert count == 1
    p.write_text(text)


def main():
    old = load('maximal_root_tail_wallet_v2/exact_certificate.json',
               '8b38a322e3b6ddffefee25d3db157e3fbbddb284a4b636143360bd00d4db5b46')
    root_input = load('maximal_root_tail_wallet_v2/exact_input.json',
                      '86a235bf210862ef8f8bbbdea7ac324e71f691a8aa7af455a821e6379cfe117d')
    new = load('main_thirty_index_strengthening/exact_certificate.json',
               '5289fd26dcb0bc7c3cf619fe80649d4277b0d59932073b609b44e90e94071e39')
    cap = load('main_root30_capacity_feedback/exact_certificate.json')
    assert digest(WS/'main_root30_capacity_feedback/proof.md') == '1577d3468acff67c715a69f25df6e2bae18f5c9e0b0ae8a4c5aeaa085ce8da87'
    oldenv = load('maximal_root_opt_requery/universal_moment_envelope.json')
    newenv = load('main_thirty_index_strengthening/requery30_envelopes.json')
    states = {(v['h'], tuple(v['state'])):v for v in load('main_thirty_index_strengthening/requery30_states.json')}
    assert len(oldenv) == len(newenv) == 128 and len(states) == 2048
    bits_all = list(product((0, 1), repeat=7))
    for menu in product((0, 1), repeat=6):
        mult, o = sum(menu), int(any(menu))
        for d in range(1, 6):
            h30 = F(mult, 3*d)-F(mult*(mult-1), 30*d*(d+1))
            h36 = F(mult, 3*d)-F(mult*mult, 36*d*(d+1))
            assert query_cost(menu, d, True) == h30 >= F(o, 3*d)
            assert query_cost(menu, d, False) == h36 >= F(o, 3*d)-F(o, 36*d*(d+1))
            assert h30-h36 == F(mult*(6-mult), 180*d*(d+1)) >= 0
    minima = {False:[], True:[]}
    residual_counts = {}
    for distinct in (False, True):
        pos = zero = 0
        deltas = []
        for h, bits in enumerate(bits_all):
            vals = {state:source_cost(bits, state, distinct) for state in product((0, 1), repeat=4)}
            aq = [min(v for state, v in vals.items() if state[0] == q) for q in (0, 1)]
            delta, gamma = max(aq[1]-aq[0], F(0)), max(aq[0]-aq[1], F(0))
            o = bits[6]
            mm = aq[0] if not o else min((5*aq[0]+aq[1])/6, aq[1])
            assert mm == aq[0]+delta*o/6-gamma*o
            minima[distinct].append(mm)
            deltas.append(delta)
            expected = newenv[h] if distinct else oldenv[h]
            assert aq == [F(expected['a0']), F(expected['a1'])]
            assert mm == F(expected['m30'] if distinct else expected['minimum'])
            for state, phi in vals.items():
                rho = phi+(gamma-delta)*state[0]-aq[0]
                assert rho >= 0
                assert -phi+(delta-gamma)*state[0]+rho+aq[0] == 0
                pos += rho > 0
                zero += rho == 0
                if distinct:
                    assert phi == explicit_phi30(bits, state) == F(states[h, state]['cost'])
                    assert rho == F(states[h, state]['residual'])
                    d = 1+sum(bits[:2])+sum(state[:2])
                    oldphi = source_cost(bits, state, False)
                    assert phi-oldphi == F(215*o, d*(d+1)) >= F(43*o, 6)
                    assert oldphi == F(states[h, state]['old36_cost'])
            assert gamma == 0
        residual_counts['30' if distinct else '36'] = {'positive':pos,'zero':zero,'min_delta':str(min(deltas))}
    m36, m30 = minima[False], minima[True]
    for h, bits in enumerate(bits_all):
        assert m30[h]-m36[h] >= F(43*bits[6], 6)
        assert m36[h] == F(newenv[h]['m36'])

    integer_weights = dict(ROOT_IC=458370347102136, CAP_B2=4033570568923,
                           CAP_B3=25119410737975, CAP_B4=25161094195332,
                           CAP_B5=24498952230168, CAP_B6=25979555609712)
    integer_weights.update({'SAFE_j4|Omean':10777983121512, 'SAFE_j6|Omean':9469251673344,
                            'PAIR|Omean|Omean':15684175951632,'OPT_SOURCE3_REQUERY_CUT':166490928})
    lam = {k:F(v, DB) for k,v in integer_weights.items()}
    assert lam == {k:F(v) for k,v in old['dual']['original_unscaled_row_weights'].items()}
    assert lam == {k:F(v) for k,v in new['root_fixed_weights'].items()}
    pi_k, pi_o = F(5418522406187, 16370369539362), F(2285403817169, 114592586775534)
    a, b = F(7821007338521, 76395057850356), pi_o
    eta = F(10132956584, 286481466938835)
    delta_cap = F(77334949597, 572962933877670)
    assert eta == F(new['root_eta']) and delta_cap == F(cap['delta'])
    lam_cap = dict(lam)
    lam_cap['CAP_B2'] += delta_cap
    assert lam_cap == {k:F(v) for k,v in cap['new_weights'].items()}
    raw = {r['name']:r for r in root_input['raw_rows']}
    residuals = [[], [], []]
    shifted = []
    for h, bits in enumerate(bits_all):
        r36 = {name:root_atom(name, bits, m36[h], False) for name in lam}
        r30 = {name:root_atom(name, bits, m30[h], True) for name in lam}
        for name in lam:
            assert r36[name] == F(raw[name]['a'].get(str(h), 0)), (h, name)
        rho36 = -sum((lam[n]*r36[n] for n in lam), F(0))-pi_k*bits[0]-pi_o*bits[6]
        rho30 = -sum((lam[n]*r30[n] for n in lam), F(0))-pi_k*bits[0]-(pi_o+eta)*bits[6]
        rhocap = -sum((lam_cap[n]*r30[n] for n in lam), F(0))-pi_k*bits[0]-(pi_o+eta+delta_cap)*bits[6]
        assert rho36 == F(old['dual']['column_residuals'][str(h)]) >= 0
        assert rho30 == F(new['root_all129_residuals'][str(h)]) >= 0
        assert rhocap == F(cap['all129_residuals'][str(h)]) >= 0
        d = 1+sum(bits[:4])
        shift = rho36+lam['PAIR|Omean|Omean']*F(bits[6], 36*d*(d+1))+lam['OPT_SOURCE3_REQUERY_CUT']*(m30[h]-m36[h])
        assert rho30 == shift-eta*bits[6]
        assert rhocap == rho30+delta_cap*(bits[1]-bits[6])
        shifted.append(shift)
        for bucket, rho in zip(residuals, (rho36, rho30, rhocap)):
            assert (SCALE*rho).denominator == 1
            bucket.append(rho)
    assert min(shifted[h] for h in range(128) if bits_all[h][6]) == eta
    assert [h for h in range(128) if bits_all[h][6] and shifted[h] == eta] == [125]
    assert min(residuals[1][h] for h in range(128) if bits_all[h][6] and not bits_all[h][1]) == delta_cap
    assert [h for h in range(128) if bits_all[h][6] and not bits_all[h][1] and residuals[1][h] == delta_cap] == [9]
    assert [h for h in range(128) if residuals[1][h] == 0] == [0,2,125]
    assert all(bits_all[h][0] == bits_all[h][6] for h in range(128) if residuals[1][h] == 0)
    for weights, pi, slope, intercept in [(lam,pi_o,a,b),(lam,pi_o+eta,a,b+eta),(lam_cap,pi_o+eta+delta_cap,a-delta_cap,b+eta+delta_cap)]:
        assert weights['ROOT_IC'] == 1
        assert sum((v for name,v in weights.items() if name.startswith('CAP_B')), F(0))-pi_k == -slope
        assert -pi == -intercept
    assert F(23463022015563,229185173551068) == a
    assert F(4570807634338,229185173551068) == b
    assert F(117315110077815,1145925867755340) == a
    assert F(22894569998026,1145925867755340) == b+eta
    assert F(117160440178621,1145925867755340) == a-delta_cap
    assert F(23049239897220,1145925867755340) == b+eta+delta_cap

    table = ['| 编号 | 旧型 | \\(m_{36}\\) | \\(m_{30}\\) | \\(R_{36}\\) | \\(R_{30}\\) | \\(R_{\\rm cap}\\) |',
             '|---:|---|---:|---:|---:|---:|---:|']
    for h, bits in enumerate(bits_all):
        numbers = [str(int(SCALE*r[h])) for r in residuals]
        table.append('| '+str(h)+' | `'+''.join(map(str,bits))+'` | '+str(m36[h])+' | '+str(m30[h])+' | '+' | '.join(numbers)+' |')
    patch_appendix('A', '\n'.join(table))

    paths = [
        ('archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md', '完整历史真实IC与共同目录'),
        ('archives/customer-attraction/state/引理/末两人重叠比较与任意索引聚合--引理.md', 'PAIR及任意索引聚合原owner'),
        ('research/workspaces/six-boss1-20261111/maximal_root_opt_requery/proof.md', 'C36九预算、全型矩消元；不并入发现点结论'),
        ('research/workspaces/six-boss1-20261111/maximal_root_opt_requery/exact_certificate.json', 'C36 universal_cut及真预算权字段'),
        ('research/workspaces/six-boss1-20261111/maximal_root_opt_requery/universal_moment_envelope.json', 'C36全部128型包络'),
        ('research/workspaces/six-boss1-20261111/maximal_root_opt_requery/check_literal.py', 'C36字面份额与证书检查'),
        ('research/workspaces/six-boss1-20261111/maximal_root_opt_requery/literal_certificate_check.json', 'C36全2048状态和128列检查输出'),
        ('research/workspaces/six-boss1-20261111/main_opt_requery_any_history.md', '任意两行动有序历史与actual提升'),
        ('research/workspaces/six-boss1-20261111/maximal_root_opt_requery_audit.md', '独立来源审计、完整矩付款及附录A量词'),
        ('research/workspaces/six-boss1-20261111/maximal_root_opt_requery_audit/check_exact.py', 'C36独立字面审计程序'),
        ('research/workspaces/six-boss1-20261111/maximal_root_opt_requery_audit/audit_result.json', 'C36独立证书审计输出'),
        ('research/workspaces/six-boss1-20261111/main_thirty_index_strengthening/proof.md', '仅第1—4节PAIR30、C30与ROOT30'),
        ('research/workspaces/six-boss1-20261111/main_thirty_index_strengthening/check_and_build.py', '仅三十索引、九预算包络与固定根付款；本次只读'),
        ('research/workspaces/six-boss1-20261111/main_thirty_index_strengthening/pair30_literal.json', '全部64菜单串及五个D的320个平均'),
        ('research/workspaces/six-boss1-20261111/main_thirty_index_strengthening/requery30_envelopes.json', '全部128型新旧包络'),
        ('research/workspaces/six-boss1-20261111/main_thirty_index_strengthening/requery30_states.json', '全部2048新状态与余项'),
        ('research/workspaces/six-boss1-20261111/main_thirty_index_strengthening/exact_certificate.json', 'C30与ROOT30相关字段；不采用其他源组合及全局界'),
        ('research/workspaces/six-boss1-20261111/maximal_root_tail_wallet_v2/proof.md', 'ROOT36十预算、自由质量乘子与全131列'),
        ('research/workspaces/six-boss1-20261111/maximal_root_tail_wallet_v2/exact_input.json', '原未缩放根行及独立K/O参数'),
        ('research/workspaces/six-boss1-20261111/maximal_root_tail_wallet_v2/exact_certificate.json', 'ROOT36十原行权与全129列余项'),
        ('research/workspaces/six-boss1-20261111/maximal_root_tail_wallet_v2/check_literal.py', 'ROOT36未缩放付款检查'),
        ('research/workspaces/six-boss1-20261111/maximal_root_tail_wallet_v2/literal_certificate_check.json', 'ROOT36全列与两参数检查输出'),
        ('research/workspaces/six-boss1-20261111/actual_source2_opt_requery_audit/root30_context.md', 'C30及ROOT30独立来源、符号和全131列审查'),
        ('research/workspaces/six-boss1-20261111/actual_source2_opt_requery_audit/check_root30_context.py', 'C30及ROOT30独立Fraction复建'),
        ('research/workspaces/six-boss1-20261111/actual_source2_opt_requery_audit/root30_context_result.json', '独立全128/2048/131列输出'),
        ('research/workspaces/six-boss1-20261111/main_root30_capacity_feedback/proof.md', 'ROOT30取等障碍与同一第二尾容量反馈'),
        ('research/workspaces/six-boss1-20261111/main_root30_capacity_feedback/build_exact.py', '容量反馈新权、自由乘子与131列重建；本次只读'),
        ('research/workspaces/six-boss1-20261111/main_root30_capacity_feedback/exact_certificate.json', '容量反馈全128余项、真权和参数；不采用固定点应用')
    ]
    evidence = [{'path':path, 'sha256':digest(REPO/path), 'section':section} for path,section in paths]
    assert evidence[1]['sha256'] == '4dacbe163ea4ea9459395dd4445c0dea25ed28070d0723a750ea6351832f4d2c'
    evidence_table = ['| 证据及本页用途 | SHA256 |', '|---|---|']
    for e in evidence:
        evidence_table.append('| `'+e['path']+'` — '+e['section']+' | `'+e['sha256']+'` |')
    patch_appendix('B', '\n'.join(evidence_table))
    result = {
        'status':'PASS_FORMAL_DRAFT_LITERAL_ENVELOPES_AND_THREE_131_COLUMN_IDENTITIES',
        'optimizer_calls':0, 'frozen_builders_imported_or_executed':False,
        'pair_menu_states':320, 'requery_states_per_cost':2048, 'old_types':128,
        'state_residual_counts':residual_counts, 'root_homogeneous_columns_per_identity':131,
        'root_zero_types':[[h for h in range(128) if rr[h] == 0] for rr in residuals],
        'root_eta':str(eta), 'capacity_delta':str(delta_cap),
        'body_sha256':digest(HERE/'body.md'), 'evidence':evidence,
        'writing_scope':str(HERE.relative_to(REPO)),
        'canonical_body_written':False, 'registry_or_graph_written':False
    }
    (HERE/'draft_exact_check.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','pair_menu_states','requery_states_per_cost','state_residual_counts','root_zero_types','body_sha256']}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
