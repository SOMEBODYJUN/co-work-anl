"""Freeze the completed finite obligation; no additional solve or search."""
from collections import Counter,defaultdict
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
WORK=HERE.parent
REPO=WORK.parents[2]


def sha(p):return sha256(p.read_bytes()).hexdigest()


def save(n,v):(HERE/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')


def main():
    lift=json.loads((HERE/'symbolic_lift.json').read_bytes())
    exact=json.loads((HERE/'exact_certificate.json').read_bytes())
    audit=json.loads((HERE/'independent_certificate_audit.json').read_bytes())
    inputs=json.loads((HERE/'input_audit.json').read_bytes())
    numerical=json.loads((HERE/'phase_I_discovery.json').read_bytes())
    assert exact['kind']=='primal' and exact['phase_I']=='0'
    assert audit['all_776_rational_values_and_893_rows_verified']
    assert audit['point_sha256']==exact['point_sha256']==lift['point_sha256']
    assert audit['symbolic_lift_sha256']==exact['symbolic_lift_sha256']==sha(HERE/'symbolic_lift.json')
    assert numerical['linprog_calls']==1 and exact['optimization_calls_during_recovery']==0
    kernels=[];categories=Counter()
    for j,(c,m,v) in enumerate(zip(lift['new_columns'],inputs['old_states'],exact['new_values'])):
        M=F(m['value']);x=F(v)
        assert (c['hist_column'],c['group'],c['old_state'])==(m['hist_column'],m['group'],m['old_state'])
        assert 0<=x<=M
        cat='zero-mass' if not M else 'E0' if not x else 'E1' if x==M else 'fractional'
        categories[cat]+=1
        kernels.append({'local_column':j,'symbolic_column':4849+j,
                        'hist_column':c['hist_column'],'group':c['group'],'old_state':c['old_state'],
                        'named_nodes':c['named_nodes'],'old_mass':str(M),
                        'E1_mass':str(x),'E0_mass':str(M-x),'conditional_E1':None if not M else str(x/M),
                        'category':cat})
    save('conditional_marginals_exact.json',{'scope':'Separate own-RZ conditional marginal kernels only; not a joint law of all E/R/Z labels.',
                                             'point_sha256':exact['point_sha256'],'exact_certificate_sha256':sha(HERE/'exact_certificate.json'),
                                             'counts':dict(categories),'columns':kernels})
    families=defaultdict(list)
    binding=[]
    for row,sv in zip(lift['rows'],exact['row_slacks']):
        s=F(sv);families[row['name'][0]].append(s)
        if not s and row['name'][0]!='E-at-most-old-state':binding.append(row['name'])
    stats=[{'family':family,'rows':len(v),'zero':sum(not q for q in v),'positive':sum(q>0 for q in v),
            'minimum':str(min(v)),'minimum_float':float(min(v))} for family,v in families.items()]
    source=[]
    for row,sv in zip(lift['rows'],exact['row_slacks']):
        if row['name'][0] in ('A5-force-Z-with-E','A6-to-E','capacity-E','own-Z-to-E'):
            source.append({'name':row['name'],'slack':sv,'slack_float':float(F(sv))})
    summary={'status':'completed-and-frozen','point_sha256':exact['point_sha256'],
             'point_W':inputs['W'],'point_O':inputs['O'],'phase_I':'0',
             'scope':lift['scope'],'all_16_histograms_retained':True,'zero_histograms':lift['zero_mass_hist_columns'],
             'named_nodes':66,'old_groups':194,'new_columns':776,'explicit_rows':893,'global_rows':117,
             'nonzero_symbolic_coefficients':audit['all_nonzero_coefficients_checked'],
             'orbit_types':53,'permutation_images':38160,'linprog_calls':1,
             'exact_recovery_rank':exact['rank'],'free_variables':exact['free_variables'],
             'positive_E_masses':exact['positive_new_values'],'kernel_counts':dict(categories),
             'minimum_exact_slack':'0','negative_exact_rows':0,
             'source_and_capacity_slacks':source,'family_statistics':stats,'binding_global_rows':binding,
             'new_negative_row':False,
             'next_obligation':'A coherent cross-E/R/Z conditional law and its omitted cross queries; then replies after fifth-source forces E and full ordered-history strategy closure.',
             'no_same_parameter_grid_followup':True,
             'verification_command':'python research/workspaces/six-boss1-20261111/z_successor_20910/literal_audit.py --certificate'}
    save('summary.json',summary)
    table='\n'.join(f"| {x['family']} | {x['rows']} | {x['zero']} | {x['positive']} |" for x in stats)
    md=f'''# 新 20910 点：Z 后继 E 四态提升精确可行，有限义务已冻结

RUN `six-boss1-20261111`；Boss1 内部义务。**完整明定提升得到精确 δ=0；没有产生可追加的负行。** 该结果只关于下述条件边缘层，不是跨全部 E/R/Z 的共同客户实现或完整六人 SPE。

## 绑定输入

绑定 `full624_augmented_lp/recovery/augmented_lp_exact.json`，SHA256 `{exact['point_sha256']}`。Main 的 `main_20910_audit.json` 已独立核该 20,910×20,585 点；本次重新核点和旧矩阵的 SHA、全部描述符身份及原 4,849 列的四态非负边缘，没有迁移旧 `b0ca…` 点的完成。

- O = 1。
- W = `{inputs['W']}`，约 0.49304863960834766。
- 全 16 个 hist 保留，零质量 hist 为 1、59、366、449、524、574。
- 66 个具名 R/Z/E 节点、194 个旧 R/Z 组，每组四态均新增 E=1 质量，共 **776 个 x**。旧 00 态始终为符号式 H−m01−m10−m11。

## 完整行域与数学边界

保留全部 requested 基本域：actual 第五源强制 Z 并由 E 真实回复；E 在前缀 P+z 上查询六个 actual、T/B/C 的所有三索引相等型及自己同源 R/Z；旧同源 Z→E；E 容量、actual 第六精确价格及前五位正确 SAFE。

还加入了 **42 条四索引轨道的全部旧 R→E**，其中已含三条同源 R→E。它们只读取旧词确定的源前缀，不需要跨旧组的交叠。没有加入未经保存的 E→跨 R/Z、跨 Z→E、E-E 查询，也没有假设不同组独立。

三个 family/diag 节点轨道分别使用全局固定权重 1/30、1/30、1/6。T/B/C 的八种相等型及 R→E 的 42 种相等型均由全部 720 个同步 S6 置换核频数。不同标签仅在行中平均，未合并事件；所有收入预算在每一行只支付一次。

完整模型为 **893 条显式行 = 776 条 x≤m 上界 + 117 条全局行**，另含 776 个 x 非负域。完整推导与历史分母见 [derivation.md](z_successor_20910/derivation.md)，符号系数见 [symbolic_lift.json](z_successor_20910/symbolic_lift.json)。

## 精确结果

只有一次 893×777 phase-I 数值调用，返回 δ=0。随后只作有理线性消元，没有新的优化调用：活动方程秩 **776**，没有自由参数，恢复全部 776 个精确 x。

其中 56 个 x 严格正：44 个等于旧态总质量，12 个是严格分数拆分。其余 720 个为零；从旧质量角度分为 604 个零旧态、116 个正旧态且 E 恒为零、44 个 E 恒为一、12 个分数态。每个旧态的 E0/E1 质量和条件概率均已保存在 [conditional_marginals_exact.json](z_successor_20910/conditional_marginals_exact.json)。它们只说明单组边缘，不能直接当作跨全部标签的联合网络。

全部 893 行精确非负，最小余量为 0。三个 actual 第五源强制 Z 行、三个 actual 第六价格行、三个同源 Z→E 行均严格精确打平。所有 42 个旧 R→E 行严格为正，最小余量约 0.01692474971580953；所有前五 SAFE 行严格为正，最小余量约 0.010540789943368664。三个 E 容量余量分别约 0.04006520547059150、0.04028807447530903、0.04823616679690030。

| 行类 | 总数 | 精确零 | 严格正 |
| --- | ---: | ---: | ---: |
{table}

完整分数与所有余量见 [exact_certificate.json](z_successor_20910/exact_certificate.json)；简明结果及全部打平的全局行见 [summary.json](z_successor_20910/summary.json)。

## 独立重建与冻结

独立校验器不导入构造器，从 E=0、E=1 的字面终局收益和真实历史重新生成全矩阵，比较 **全部 43,382 个非零符号系数**，并核全部 776 个有理 x 和 893 个行余量。此检查包含六个零 hist，不只覆盖正支撑。另有 53 种轨道、38,160 个同步置换像、实际早期 SAFE 和全部末位差值的标量真值表。详细结果见 [independent_certificate_audit.json](z_successor_20910/independent_certificate_audit.json) 与 [wallet_audit.json](z_successor_20910/wallet_audit.json)。

只需执行以下命令，即可独立重读证书并重建全域行；无需再次调用优化器：

```bash
python research/workspaces/six-boss1-20261111/z_successor_20910/literal_audit.py --certificate
```

本有限义务已完成并冻结。下一数学缺口是跨 E/R/Z 的共同条件律及遗漏的真实交叉查询，继而是第五源强制新增 E 时的后继和完整有序历史策略闭包。本层可行不能替代这些义务；没有继续同参数网格扫描。文件及输入哈希见 [freeze_manifest.json](z_successor_20910/freeze_manifest.json)。
'''
    (WORK/'z_successor_20910.md').write_text(md)
    files=[p for p in HERE.iterdir() if p.is_file() and p.name!='freeze_manifest.json']
    files.append(WORK/'z_successor_20910.md')
    save('freeze_manifest.json',{
        'status':'completed-and-frozen','task':'z_successor_20910','run':'six-boss1-20261111',
        'point_sha256':exact['point_sha256'],'result':'Exact feasible stated necessary lift; no new negative row.',
        'allowed_write_scope':['research/workspaces/six-boss1-20261111/z_successor_20910/','research/workspaces/six-boss1-20261111/z_successor_20910.md'],
        'input_hashes_rechecked':[{'path':x['path'],'sha256':sha(REPO/x['path']),'matches_recorded':sha(REPO/x['path'])==x['sha256']} for x in inputs['inputs']],
        'files':[{'path':str(p.relative_to(REPO)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(files)],
        'finite_obligation_complete':True,'new_optimization_calls_after_discovery':0,
        'unresolved':['Cross-E/R/Z common customer realization and missing cross queries','Successor replies after fifth-source E deviations','Full ordered-history SPE closure']})
    freeze=json.loads((HERE/'freeze_manifest.json').read_bytes())
    assert all(x['matches_recorded'] for x in freeze['input_hashes_rechecked'])
    print(json.dumps({'status':summary['status'],'point_sha256':summary['point_sha256'],
                      'result':'exact feasible','new_negative_row':False,'files':len(files),
                      'symbolic_lift_sha256':sha(HERE/'symbolic_lift.json'),
                      'exact_certificate_sha256':sha(HERE/'exact_certificate.json'),
                      'independent_audit_sha256':sha(HERE/'independent_certificate_audit.json'),
                      'freeze_manifest_sha256':sha(HERE/'freeze_manifest.json')},ensure_ascii=False))


if __name__=='__main__':main()
