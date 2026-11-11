"""Package the verified exact tail certificate without changing its input."""
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
WORK = HERE.parent


def sha(p):
    return sha256(p.read_bytes()).hexdigest()


def serial(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, dict):
        return {str(k): serial(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [serial(v) for v in x]
    return x


def save(name, value):
    (HERE / name).write_text(json.dumps(serial(value), ensure_ascii=False, indent=2) + '\n')


def main():
    source = WORK / 'fifth_reply_common/common_atoms_with_D.json'
    expected_sha = '91599404ee03184bbb072767d7d55761b95bcc89e1d55e748aebf2ee60f19c54'
    assert sha(source) == expected_sha
    mp = json.loads((HERE / 'labels_and_orbits.json').read_bytes())
    mat = json.loads((HERE / 'matrix_certificate.json').read_bytes())
    sol = json.loads((HERE / 'tail_solution.json').read_bytes())
    ver = json.loads((HERE / 'independent_verification.json').read_bytes())
    summary = json.loads((HERE / 'build_summary.json').read_bytes())
    assert ver['status'] == 'PASS' and not sol['actual']['actual_two_tail_is_supported']
    assert ver['verifier_sha256'] == sha(HERE / 'verify.py')
    assert summary['producer_sha256'] == sha(HERE / 'build.py')
    names = [d['name'] for d in mp['labels']]
    ids = {n: i for i, n in enumerate(names)}
    B = [F(mat['B_by_single_orbit'][o]) for o in mp['single_orbit_index']]
    jvalues = [F(v) for v in mat['J_by_ordered_pair_orbit']]

    def J(q, r):
        return jvalues[mp['ordered_pair_orbit_index'][q][r]]

    all_D = {f'D{i}' for i in range(1, 7)}
    all_C = {f'C{i}' for i in range(1, 7)}
    off = [(i, j) for i in range(1, 7) for j in range(1, 7) if i != j]
    all_R0 = {f'R0_{i}_{j}' for i, j in off}
    all_R1off = {f'R1_{i}_{j}' for i, j in off}
    all_Z0 = {f'Z0_{i}_{j}' for i, j in off}
    all_Z1off = {f'Z1_{i}_{j}' for i, j in off}
    descriptions = {}
    for q, d in enumerate(mp['labels']):
        kind = d['kind']
        ix = [i + 1 for i in d['movable_indices']]
        if kind in ('A1', 'A2', 'A4', 'A6', 'H2'):
            br = all_D
            text = '全部 D_k'
        elif kind == 'A3':
            br = all_Z0 | all_Z1off | all_D
            text = '全部 Z_{0ij}、非对角 Z_{1ij}、全部 D_k'
        elif kind == 'A5':
            br = {'A6', 'H2'} | all_C | all_R0 | all_R1off | all_Z0 | all_Z1off | all_D
            text = 'A₆、H₂、全部 C_k、全部 R_{0ij}、非对角 R_{1ij}、全部 Z_{0ij}、非对角 Z_{1ij}、全部 D_k'
        elif kind == 'T':
            i, = ix
            br = {f'Z0_{j}_{i}' for j in range(1, 7) if j != i} | {f'D{i}'}
            text = 'D_i；Z_{0ji}（j≠i）'
        elif kind == 'B':
            i, = ix
            br = {f'C{i}'}
            text = 'C_i'
        elif kind == 'C':
            i, = ix
            br = {f'B{i}'}
            text = 'B_i'
        elif kind == 'R0':
            i, j = ix
            br = {f'Z0_{i}_{j}'} | {f'Z1_{i}_{k}' for k in range(1, 7) if k not in (i, j)} | {f'D{k}' for k in range(1, 7) if k not in (i, j)}
            text = 'Z_{0ij}；Z_{1ik}、D_k（k∉{i,j}）'
        elif kind == 'R1':
            i, j = ix
            if i == j:
                br = {f'C{i}', f'Z1_{i}_{i}'}
                text = 'C_i、Z_{1ii}'
            else:
                br = {f'C{j}', f'Z1_{i}_{j}', f'D{j}'}
                text = 'C_j、Z_{1ij}、D_j'
        elif kind == 'Z0':
            i, j = ix
            br = {f'C{j}'}
            text = 'C_j'
        elif kind == 'Z1':
            i, j = ix
            if i == j:
                br = {f'B{i}'}
                text = 'B_i'
            else:
                br = {'A6'}
                text = 'A₆（唯一）'
        elif kind in ('H1', 'D'):
            br = {'H2'}
            text = 'H₂'
        else:
            raise AssertionError(kind)
        assert br == set(sol['rows'][q]['BR_names'])
        descriptions[q] = text
    orbit_rows = []
    row_names = ['A₁', 'A₂', 'A₃', 'A₄', 'A₅', 'A₆', 'T_i', 'B_i', 'C_i',
                 'R_{0ij}，i≠j', 'R_{1ii}', 'R_{1ij}，i≠j',
                 'Z_{0ij}，i≠j', 'Z_{1ii}', 'Z_{1ij}，i≠j', 'H₁', 'H₂', 'D_i']
    for orbit, display in zip(mp['single_orbits'], row_names):
        q = orbit['representative']
        row = sol['rows'][q]
        for q2 in orbit['members']:
            assert F(sol['rows'][q2]['m']) == F(row['m'])
        orbit_rows.append(dict(orbit_id=orbit['id'], label_family=display,
                               label_count=len(orbit['members']), representative=names[q],
                               all_BR_formula=descriptions[q], BR_count=len(row['BR']),
                               B=F(row['B']), m=F(row['m']), m_approx=float(F(row['m'])),
                               m_minus_actual_U5=F(row['m']) - F(sol['actual']['U5'])))
    save('orbit_summary.json', dict(input_sha256=expected_sha, all_164_BR_formulas_checked=True, rows=orbit_rows))

    forced = sol['forcing_deviation_certificate']
    q = forced['Q']
    assert names[q] == 'Z1_1_2' and sol['rows'][q]['BR'] == [ids['A6']]
    rstar = ids['A6']
    max_u6 = B[rstar] - J(q, rstar)
    replies = []
    for r in range(164):
        u5 = B[q] - J(q, r)
        u6 = B[r] - J(q, r)
        gap = max_u6 - u6
        assert gap >= 0 and (gap == 0) == (r == rstar)
        replies.append(dict(R=r, R_name=names[r], original_U5=u5, original_U6=u6,
                            U6_A6_minus_U6_R=gap, is_best_reply=(gap == 0)))
    minimum_terminal_gap = min(r['U6_A6_minus_U6_R'] for r in replies if r['R'] != rstar)
    runnerups = [r['R_name'] for r in replies if r['U6_A6_minus_U6_R'] == minimum_terminal_gap]
    assert runnerups == ['H2'] and minimum_terminal_gap > 0
    M = F(sol['M'])
    u5 = F(sol['actual']['U5'])
    assert M > u5
    exclusion = dict(
        status='EXACT_FIXED_INSTANCE_EXCLUSION', input_sha256=expected_sha,
        prefix=['A1', 'A2', 'A3', 'A4'], actual_tail=['A5', 'A6'],
        complete_directory_label_count=164, unit_customer_scale=mat['unit_customer_scale'],
        payoff_normalization='Divide finite unit-customer payoffs by unit_customer_scale; signs and all best replies are unchanged.',
        forcing_action='Z1_1_2', all_optimal_terminal_replies=['A6'],
        all_164_terminal_payoffs_and_margins=replies,
        smallest_strict_terminal_margin=minimum_terminal_gap, terminal_runnerups=runnerups,
        guaranteed_fifth_payoff=M, actual_fifth_payoff=u5, strict_improvement=M-u5,
        proof='Every complete pure SPE must choose a terminal best reply after the actual ordered history (A1,A2,A3,A4,Z1_1_2). The only best reply in this complete directory is A6; it pays player 5 M>u5. Therefore the specified actual six-action path cannot occur in a pure SPE of this fixed finite instance.',
        limitation='Only this frozen customer law and this 164-label common directory are excluded. Additional labels or another common customer coupling may repair it. This is not an SPE counterexample and does not resolve six-player 2W>=OPT6.')
    save('exclusion_certificate.json', exclusion)

    common_denominator = u5.denominator
    assert M.denominator == common_denominator
    numerator_gap = M.numerator-u5.numerator
    table = '\n'.join('| ' + ' | '.join([r['label_family'], str(r['label_count']),
                                          r['all_BR_formula'], str(r['BR_count']),
                                          f"{r['m_approx']:.15f}"]) + ' |' for r in orbit_rows)
    report = rf'''# 164 标签共同有限实例：actual 末两位完整 SPE 精确排除

本义务已完成、独立核验通过并冻结。范围是给定客户律、共同目录和前缀 `(A1,A2,A3,A4)`；六人 `2W≥OPT₆` 仍 **OPEN**。

## 1. 精确结论

**这个具体实例的指定 actual 末两位 `(A5,A6)` 不能由完整纯 SPE 支持。**
实际 A₆ 确实属于 BR(A₅)，失败在第五位：

| 量 | 精确判定 | 约值，仅展示 |
| --- | --- | ---: |
| actual 第五收益 u₅ | 严格小于 M | {float(u5):.17g} |
| actual 第六收益 u₆ | 是 A₅ 后的最优收益 | {float(F(sol['actual']['U6'])):.17g} |
| 最低可实现第五均衡收益 M | 精确达到 | {float(M):.17g} |
| 强制第五改进 M−u₅ | 严格为正 | {float(M-u5):.17g} |

取一条明确偏离 **Q=Z₁,₁,₂**（机器标签 `Z1_1_2`）。对完整 164 标签逐一比较，

\[
BR(Q)=\{{A_6\}},\qquad U_5(Q,A_6)=M>u_5.
\]

因此任何完整策略在真实离轨历史 `(A1,A2,A3,A4,Z1_1_2)` 都被末位最优性强制选 A₆，第五位严格获利。
末位唯一性也有严格余量：A₆ 对其余 163 个回复的最小优势为 **{float(minimum_terminal_gap):.17g}**，唯一达到该最小优势的标签为 H₂。
`exclusion_certificate.json` 保存了全部 164 项原始收益、精确差、全部最优末回复和第五位严格改进。

令

```text
K = {common_denominator}
```

则本证书可直接写为三个精确整数比较：

```text
u5 = {u5.numerator} / K
M  = {M.numerator} / K
M-u5 = {numerator_gap} / K > 0
```

以上是总客户质量归一化为 1 后的数值。乘证书中的 595 位单位客户缩放整数 N，即为有限单位客户的真实收益；所有最优回复、平局及严格符号不变。

## 2. 充要判据的独立审查

已亲自逐客户审查 Main 的 TT1–TT4，结论 **PASS**。完整推导在 `proof_audit.md`。
在固定前缀负载 p_x 上，

\[
B_Q=\sum_x\frac{{q_x}}{{p_x+1}},\qquad
J_{{QR}}=\sum_x\frac{{q_xr_x}}{{(p_x+1)(p_x+2)}},
\]

从原始份额直接得到 U₅(Q,R)=B_Q−J_QR、U₆(Q,R)=B_R−J_QR。
每个第五行动 Q 后都必须选完整 BR(Q) 内的回复；第五位最低可强制收益为

\[
m_Q=B_Q-\max_{{R\in BR(Q)}}J_{{QR}},\qquad M=\max_Qm_Q.
\]

指定 `(A5,A6)` 可支持，当且仅当 `A6∈BR(A5)` 且 `u5≥M`。
充分性是在每个其它第五行动后独立选择使第五收益最小的最优末回复；同覆盖异标签也保留为不同历史。
M 是该末两位子博弈全部纯 SPE 中第五收益的最小值。该充分性不证明前四位的最优性。

## 3. 输入与目录逐项核对

唯一客户输入为 `fifth_reply_common/common_atoms_with_D.json`，SHA-256：

`{expected_sha}`。

| 标签块 | 数量 | 实际会员来源 |
| --- | ---: | --- |
| A₁,…,A₆ | 6 | 各 block 的 `actual_bits`，置换时固定 |
| T_i、B_i、C_i | 18 | hist 中 6 个三位旧词，三个坐标分别读取 |
| R₀,ᵢ,ⱼ，i≠j | 30 | 对应 `states` 的高位 |
| R₁,ᵢ,ⱼ，所有 i,j | 36 | 对应 `states` 的高位 |
| Z₀,ᵢ,ⱼ，i≠j | 30 | 对应 `states` 的低位 |
| Z₁,ᵢ,ⱼ，所有 i,j | 36 | 对应 `states` 的低位 |
| H₁、H₂ | 2 | `B4_state` 前两位，置换时固定 |
| D₁,…,D₆ | 6 | 同时置换的 `D_bits` |
| **总计** | **164** | B4 第三位是目录均值，不是行动 |

100 个规范正原子、10 个 hist，各按全部 720 个 S6 同步排列展开，得到 72,000 个正有理原子。总质量严格为 1。
每个展开原子质量为 `mass/720`，分母最小公倍数 N 有 595 位；显式整数复制数均严格为正，总单位客户数恰为 N。
actual 与 H 位固定，旧词、R/Z 两索引和 D 索引同步移动；R family 不变。
目录无合并、允许重复行动，164×164 矩阵包含全部对角。检查后本实例恰好没有同覆盖异标签，但程序没有依赖这一事实。

## 4. 全部 BR 与 m_Q

同步 S6 给 18 个单标签轨道和 552 个有序双标签轨道。下表的 BR 描述覆盖该族每一个标签，已逐一比对完整字面集合。
i,j,k∈{{1,…,6}}；只在表中特别注明时要求不等。m_Q 约值仅供阅读，全部精确分数在 `orbit_summary.json`、`tail_solution.json`。

| 第五标签 Q | 本族标签数 | 全部最优末回复 BR(Q) | 每行 BR 数 | m_Q 约值 |
| --- | ---: | --- | ---: | ---: |
{table}

actual 行 A₅ 有 **134 个**最优末回复，全部平局保留。
满足 m_Q>u₅ 的标签有 **87 个**：A₆；全部 B、C、Z₀、Z₁、D；H₁、H₂。
T_i 与对角 R₁,ᵢ,ᵢ 的 m_Q 恰等于 actual u₅，未误判为严格偏离。

达到 M 的第五标签恰为 30 个非对角 Z₁,ᵢ,ⱼ。
按完整充要条件，**全部可实现末两题恰为**

\[
\{{(Z_{{1ij}},A_6):i\ne j\}},
\]

共 **30 对**。本实例每份该子博弈纯 SPE 的第五收益都等于 M。
`tail_solution.json` 同时保存全部 30 对，以及一份包含所有 164 个第六位历史回复的完整最低值纯 SPE 策略。
这份策略的第五行动是 Z₁,₁,₂，不是指定 actual A₅。

## 5. 可重建精确矩阵与独立字面核验

构造器对每个规范原子显式生成 720×164 的 0/1 会员矩阵 X，使用 `int64` 整数 dot 得到所有 26,896 项交叠计数 XᵀX。
每一项计数都与其轨道代表比对，随后以 Fraction 质量累加。没有浮点容差、优化器或完整六人策略枚举。

证书分为三个可复原层：

- `labels_and_orbits.json`：完整标签来源、单/双轨道、全部 164×164 轨道映射；
- `integer_orbit_counts.json`：每个规范原子的精确质量、前缀负载、18 个单计数和 552 个双计数；
- `matrix_certificate.json`：精确 B 和 J 轨道值、单位客户缩放数及复原公式。任意格由 U₅=B_Q−J_QR、U₆=B_R−J_QR 得到。

独立 `verify.py` 不导入构造器或旧验证器，重新解析冻结客户，使用**正向**置换移动会员位，与构造器的逆索引实现不同。
直接计算 `(q,r)=(1,0),(0,1),(1,1)` 的整数个数，以原始份额

\[
U_5=\sum_a\frac{{\mu_a}}{{720}}
\left(\frac{{n_{{10,a}}}}{{p_a+1}}+\frac{{n_{{11,a}}}}{{p_a+2}}\right)
\]

及第六位的对称式逐格验算。全矩阵先按单位复制数精确整数累加，再逐格转 Fraction；另外每个双轨道代表均按每原子 Fraction 直接累加，独立交叉核对。
结果 **PASS**：

| 核验项目 | 数量/结果 |
| --- | ---: |
| 每原子全部字面单计数和双计数 | 2,706,000 项 |
| 164×164 原始收益 Fraction 比对 | 26,896 格，每格两位收益 |
| 逐原子轨道代表原始份额 Fraction | 110,400 项 |
| 全部 BR、所有平局、m_Q、M | 全部一致 |
| 全部可实现末两题与完整离轨策略 | 全部一致 |
| 原始输入 SHA、有限单位复制数 | 全部一致 |

独立原始收益矩阵按 `(Q,R,U5,U6)` 行优先编码的 SHA：

`{ver['row_major_original_payoff_matrix_sha256']}`。

成功构造约 {summary['elapsed_seconds']:.3f} 秒，独立核验约 {ver['elapsed_seconds']:.3f} 秒，均为本地小算。

## 6. 范围、复现与冻结

这一失败**只排除本客户律和本 164 标签目录中的指定 actual 路径**。额外合法目录主题可能改变末位最优回复和惩罚能力，其他客户共同耦合也仍可能修复；本轮没有对此量化。
它不是完整 SPE 的福利反例，也不否定六人 `2W≥OPT₆`；总问题仍 OPEN。

`build.py` 可重建精确证书，`verify.py` 可只核验现有证书；二者只写本目录。
首次构造启动因多余右括号在解析阶段退出，未产生数学计算；失败源码和日志保存在 `build_01_syntax_failed.py`、`build_01.stderr.txt`。
仅修正括号后，构造和独立验证各一次成功，冻结输入未改、没有优化候选被筛掉。

主要交付还有 `proof_audit.md`、`exclusion_certificate.json`、`orbit_summary.json`、`tail_solution.json`、`independent_verification.json`。
`source_reading.json` 记录已读取输入；`execution_manifest.json` 绑定成功/失败执行源码与日志；`final_manifest.json`、`frozen_receipt.json` 绑定交付并冻结。
本义务完成并释放，无后台计算，无完整六人枚举，无 Git、registry 或全局运行状态操作。
'''
    (WORK / 'finite_two_tail_164.md').write_text(report)
    source_paths = [WORK / 'main_exact_two_tail_contract.md', WORK / 'fifth_reply_common.md', source,
                    WORK / 'fifth_reply_common/verify.py', WORK / 'fifth_reply_common/verify_old.py']
    save('source_reading.json', dict(files=[dict(path=str(p.relative_to(WORK)), bytes=p.stat().st_size, sha256=sha(p)) for p in source_paths]))
    save('execution_manifest.json', dict(
        input_sha256=expected_sha, optimizer_calls=0, full_six_player_enumerations=0,
        attempts=[dict(program='build_01_syntax_failed.py', status='SYNTAX_ERROR_BEFORE_COMPUTATION', exit_code=1,
                       sha256=sha(HERE / 'build_01_syntax_failed.py'), stdout_sha256=sha(HERE / 'build_01.stdout.txt'), stderr_sha256=sha(HERE / 'build_01.stderr.txt')),
                  dict(program='build.py', status='COMPLETE', exit_code=0, sha256=sha(HERE / 'build.py'),
                       stdout_sha256=sha(HERE / 'build.stdout.txt'), stderr_sha256=sha(HERE / 'build.stderr.txt')),
                  dict(program='verify.py', status='PASS', exit_code=0, sha256=sha(HERE / 'verify.py'),
                       stdout_sha256=sha(HERE / 'verify.stdout.txt'), stderr_sha256=sha(HERE / 'verify.stderr.txt'))],
        allowed_write_scope=['finite_two_tail_164/', 'finite_two_tail_164.md']))
    files = [p for p in HERE.iterdir() if p.is_file() and p.name not in ('final_manifest.json', 'frozen_receipt.json')]
    files.append(WORK / 'finite_two_tail_164.md')
    save('final_manifest.json', dict(status='VERIFIED_COMPLETE', input_sha256=expected_sha,
                                     files=[dict(path=str(p.relative_to(WORK)), bytes=p.stat().st_size, sha256=sha(p)) for p in sorted(files)]))
    save('frozen_receipt.json', dict(status='FROZEN_RELEASED', frozen_utc=datetime.now(timezone.utc).isoformat(),
                                     final_manifest_sha256=sha(HERE / 'final_manifest.json'),
                                     input_sha256=expected_sha, independent_verification='PASS',
                                     actual_tail_supported=False, conclusion='Fixed-instance exclusion only; six-player 2W>=OPT6 remains OPEN.',
                                     background_computation=False))
    assert sha(source) == expected_sha
    print(json.dumps(dict(status='FROZEN_RELEASED', final_manifest_sha256=sha(HERE / 'final_manifest.json'),
                          exclusion_certificate_sha256=sha(HERE / 'exclusion_certificate.json'),
                          report_sha256=sha(WORK / 'finite_two_tail_164.md')), ensure_ascii=False))


if __name__ == '__main__':
    main()
