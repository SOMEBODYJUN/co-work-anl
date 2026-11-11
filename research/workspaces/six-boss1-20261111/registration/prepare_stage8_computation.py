"""Register the eighth exact system and the precisely scoped old-point layers."""
from pathlib import Path
from hashlib import sha256
import json

HERE = Path(__file__).resolve().parent
WS = HERE.parent
REPO = WS.parents[2]
BASE = 'research/workspaces/six-boss1-20261111/'
CID = 'customer-attraction/six-providers/cross-branch-necessary-system-20261111'


def evidence(p):
    return {'path': p, 'sha256': sha256((REPO/p).read_bytes()).hexdigest()}


def main():
    rp = REPO/'research/registry.json'
    reg = json.loads(rp.read_bytes())
    obj = next(x for x in reg['objects'] if x['object_id'] == CID)
    assert obj['version'] == 5
    path = REPO/obj['body']['path']
    assert evidence(obj['body']['path']) == obj['body']
    text = path.read_text()
    text = text.replace('七个固定支持必要LP', '八个固定支持必要LP')
    text = text.replace('## 七个有限系统的精确证书', '## 八个有限系统的精确证书')
    text = text.replace('第六、七轮再次提高；', '第六、七、八轮再次提高；')
    line = '| 再加42同行新行和1旧行：19621行、15593列 | 精确原始与105个正对偶行权匹配 | 0.4925763826272197 |'
    assert line in text
    text = text.replace(line, line + '\n| 补齐40同行缺行及1反向624：19662行、15593列 | 精确原始与309个正对偶行权匹配 | 0.49304863743650357 |')
    audit = json.loads((WS/'main_19662_audit.json').read_bytes())
    assert audit['matched_exact_optimum'] and audit['nonnegative_primal_and_dual']
    assert (audit['rows'], audit['columns']) == (19662, 15593)
    num, den = audit['W'].split('/')
    text += r'''

## 完整同行并集与反向末位624：第八个精确系统

Main把同行全部5799行与19621基准逐行作严格正倍数比较，保持全部4849列语义、目标和归一化，发现40条互异缺行。五条在19621点为负，另外35条虽为正也全部接回。再加入Main亲自从16隐藏位、4992字面组合重构的反向末位624行；该行在19621点也严格为正。保留所有已有行，不仅收集当前负行。

反向行的客户成本来自同一个旧Z真实末位节点对新宏主题V的查询：`v/(p4+r+1)−z/(p4+r+z)`。与原共同16隐藏位共同投影，钱包仍是`u4+3862317/10^7*u6+33149/10^6*K`，新查询权为`54741/10^7`，无额外收入。全部4849系数由Main不导入同行生成器独立重构，10744辅助系数为零；见`main_reverse624.py`和绑定审计。一般反向末位合同与同行原证明一起实读；其17hist严格扩张例不能偷换为本16hist系统的严格扩张定理。

新系统为19662×15593，精确最优值为

\[
v_6=\frac{NUMERATOR}{DENOMINATOR}
\approx0.49304863743650357.
\]

366个正原列、1525个正max、727个正min。原始支持秩360/366，六个自由有理值完整冻结；对偶310变量、秩310，309个正行权。Main独立标准库审计重新核全部19662行、15593列、原始与对偶非负及精确取等。计算代理另核7954个canonical max、2790个canonical min、全部旧行原样保留、同行全5799行正比例包含及其原精确原始/对偶，并把同行对偶按比例嵌入本矩阵。

41条新行中4条精确零、37条严格正；仅以下三条有正对偶权：19622的同行dynamic-discounted-2约0.02944754877，19624的dynamic-discounted-4约1.10463160203，19661的反向624约0.59806981614。最后一条在前一点为正，在新点实际承重。这不证明它独自切开旧点，也不证明所有零权新行永久冗余。

一次数值求解后，首次对偶恢复遗漏约3.85e−10的正行权并误将同量级正列余项设零，精确等式拒绝该候选；第一次修复仍有约−5.1e−14的严格负列余项，也被拒绝。保留两次失败，不重跑优化；第二修复对精确原始正列施加互补，并补齐可核的列方程后，全有理核验通过。所有实际源码版本、原始数组、活跃方程、输出与恢复路径见`union_augmented_lp/`。

点SHA为`b0ca65cfe61e5e3ef09537cba2a986c171aeaa7106f673077f803c80ee2b68e3`；矩阵SHA为`99253e05bfe4c5705619777a5989ec9fab5c38dc7e56f934bbe8d9c071040ded`；对偶SHA为`78a7cb206f9e807d0228d20ca7eaeafaf088fc551c719ba44dad4ed10f70f5ef`。Main算术审计在`main_19662_audit.json`。它是固定支持的必要LP精确值，仍不是全域福利界或原模型反例。

### 旧19621点的完整饱和域和同一B4

此前19621点的39个非自查ZZ上界中，恰三轨道`(0,1,0102)`、`(0,1,0122)`、`(0,1,0123)`为零，合计600字面查询。对任何共同完成，同步S6对称化后，非负真IC之和不超过这些零上界，故每个正hist都必须使`|R_e∩Z_f|=min(|R_e|,|Z_f|)`。每处相应的包含、反向包含或相等与own四态零格共同形成132变量2-CNF。

全部十个正hist的SCC、常量、传递闭包与边缘序经独立核验相容。对剩余二元禁止格做符号图翻转，恰化为Boolean偏序域；自由类数为80、0、5、91、9、50、45、5、51、25。每个禁止格双向等价，故这是完整允许零格域，不是有限阈值族。原1306个RR辅助量仍未当作真实交叠。

固定同一B4状态s，条件own四态矩保持原边缘和B4八态，并满足全部包含的条件质量关系。此点所有full-own四态节点只有六个，且其非核心端为图中孤立叶；其它节点有own零格。因此按翻转后的条件单边缘取共同初始区间，可同时实现全部偏序；六叶再分别在核心及补集上分配所需质量。这个论证证明该条件矩域对于所列零格+B4范围充分。精确矩解给76规范原子、同步展开54720记录，满足全部600饱和ZZ及15B4。15B4均严格正，最小约0.001616668757799579，达到F→Z(1,0)单行Frechet上界，故为这一范围的最优共同余量。

同一原子全部RR/RZ/ZR均通过，然而其它10个ZZ轨道1080条字面仍负，最小约−0.0012528955334319186。因此没有全旧网络完成。两个更大条件Frechet必要LP只有浮点候选，精确支撑恢复不相容，均未认领一般可行或不可行。全部域变换、原子、17424精确收益和独立核验在`saturated_rz_b4/`。

### 旧19621点的175共同根尾预算

旧实际分支词`(t_i,b_i,c_i)`与新根`(t_j,e_j1,…,e_j5)`必须同一比较索引。旧C末节点查新尾的真IC为`(c_i−e_jl)/(p3+t_i+b_i+1)`；新根末节点查旧C为`e_j5/(t_j+Σe_j)−c_i/(t_j+Σ_{r≤4}e_jr+1)`。按same的1/6、off的1/30全局固定权，给12轨道216字面行，不逐客户挑权。

固定前轮根状态质量时，全32个incidence耦合有精确负上界，只否定那些固定边缘。允许根质量重配、保持163根预算及16旧hist后，17共同原子使全部216字面通过（156正、60零），根权固定1的剩余正量为

\[
L_C=\frac{27164325730945732880158992673255735533724726360156493844644462215129969}
{1872205520574051593531727838372261636638597306466479779565485535459165000}>0.
\]

对任意175个其它非负权λ，在完整合法共同状态上取局部极小不大于这份可行测度的平均，故全合同余量至少`L_C+Σλ_ν slack_ν≥L_C`。λ无须归一；根权若另放开为ρ，只能写ρL_C。此完成不含旧R/Z own联合、其它family或全SPE。全部字面核验、完整旧hist、每根预算和原子清分母见`root_old_tail_joint/`。

### 新点上的准确下一义务

Main在第八个点从原own边缘重新计算39非自查ZZ上界，全部严格正、零轨道为零；`main_19662_zz_faces.json`绑定新SHA。旧600强制零格和上述175完成都不能未经重新计算迁移。下一共同测度任务从新点全部真实边缘起，保同一B4、原R/Z真实前缀及全部旧查询；另一路重配背景五尾的全局外权。原六人half继续OPEN。
'''.replace('NUMERATOR', num).replace('DENOMINATOR', den)
    path.write_text(text.rstrip()+'\n')
    obj['version'] = 6
    obj['title'] = '八个有限必要系统的精确最优及指定共同测度边界'
    obj['statement'] += ' 第八轮补齐40同行缺行与1反向624，得19662×15593精确最优约0.49304863743650357，309个正对偶中三条新行承重，Main另核全行列。旧19621点完整600饱和ZZ加同B4有76原子完成、其它10ZZ仍失败；175根尾预算有17原子共同完成。新点39ZZ上界全严格正，旧强制面不迁移。'
    obj['scope'] += ' 八轮精确系统分别绑定各点；19621的完整零格+B4及175根尾仅为所列有限投影，不是全旧网络或完整SPE。'
    extra = [BASE+p for p in (
        'union_augmented_lp.md','union_augmented_lp/exact_matrix.json.gz',
        'union_augmented_lp/augmented_lp_exact.json','union_augmented_lp/exact_dual_certificate.json',
        'union_augmented_lp/certificate_verification.json','union_augmented_lp/whole_peer_coverage.json',
        'union_augmented_lp/inherited_peer_dual_lower_bound.json','union_augmented_lp/new_row_results.json',
        'union_augmented_lp/execution_manifest.json','union_augmented_lp/artifact_manifest.json',
        'union_augmented_lp/verify_certificates.py','main_19662_audit.json',
        'main_peer_union.py','peer_union_transfer/audit_19621.json',
        'peer_union_transfer/all_missing_rows_19621.json','peer_union_transfer/reverse624_reviewed_19621.json',
        'main_reverse624.py','main_reverse624_audit.json','main_zz_face_revalue.py','main_19662_zz_faces.json',
        'main_saturated_faces.md','saturated_rz_b4.md','saturated_rz_b4/reduced_domain.json',
        'saturated_rz_b4/conditional_candidate.json','saturated_rz_b4/independent_verification.json',
        'saturated_rz_b4/verify_face_and_atoms.py','saturated_rz_b4/final_manifest.json',
        'root_old_tail_joint.md','root_old_tail_joint/joint_completion_exact.json',
        'root_old_tail_joint/verify_completion.py','root_old_tail_joint/independent_audit.json')]
    obj['body'] = evidence(obj['body']['path'])
    seen = {e['path'] for e in obj['evidence']}
    obj['evidence'] += [evidence(p) for p in extra if p not in seen]
    obj['sources'] = list(dict.fromkeys(obj['sources']+['material:'+p for p in extra]))
    mats = {m['path']:m for m in reg['materials']}
    for e,isb in [(obj['body'],True)]+[(e,False) for e in obj['evidence']]:
        p=e['path']
        if p in mats:
            if mats[p]['sha256'] != e['sha256']:
                assert p == obj['body']['path'],p
                mats[p]['sha256']=e['sha256']
        else:
            m=dict(e,disposition='objects' if isb else 'attachment',object_ids=[CID],
                   reason='Main实读承重证明并独立全行列或字面公式核回；各点与有限投影范围分开。')
            mats[p]=m;reg['materials'].append(m)
    target=HERE/'stage8-computation-registry-candidate.json'
    target.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+'\n')
    summary={'base_registry_sha256':sha256(rp.read_bytes()).hexdigest(),
             'candidate_sha256':sha256(target.read_bytes()).hexdigest(),
             'object':{k:obj[k] for k in ('object_id','version','body')},
             'total_objects':len(reg['objects']),'total_materials':len(reg['materials'])}
    (HERE/'stage8-computation-registration-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    (HERE/'stage8-computation.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(summary,ensure_ascii=False))


if __name__=='__main__':
    main()
