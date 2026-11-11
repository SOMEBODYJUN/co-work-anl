"""Assemble the independently reviewed next formal increment, without editing witnesses."""
from pathlib import Path
import hashlib,json,re
B=Path(__file__).resolve().parent
R=B.parents[2]
RUN='research/workspaces/six-boss2-20261111-cross/'
ids={'hierarchy':'M-b1b4276f0ec747ed8c347bda65c9e0af',
     'prefix':'M-63c882b0c8414805a43d4d8d4e43f4e3',
     'price':'M-043045ec129b4a5f82a3368b324accf9',
     'finite':'M-ddceaa3d53064498b3e833a32e1f3b6f'}
paths={
 'hierarchy':'archives/customer-attraction/state/引理/共同真实回复与跨查询配对的严格投影层级--引理.md',
 'prefix':'archives/customer-attraction/state/引理/共享真实末端的独立初段与折扣尾闭包--引理.md',
 'price':'archives/customer-attraction/state/引理/任意尾长平衡末回复闭包的统一正客户价格--引理.md',
 'finite':'archives/customer-attraction/subarchives/six-providers/state/计算/同源跨枝增强必要图的精确最优值与半界缺口--计算.md'}
sources={
 'hierarchy':B/'joint_requery/formal_query_projection_hierarchy_v1.md',
 'prefix':B/'coverage_bridge/formal_prefix_tail.md',
 'price':B/'main_pair/balanced_any_tail_price.md'}
titles={'hierarchy':'共同真实回复与跨查询配对的严格投影层级',
        'prefix':'共享真实末端的独立初段与折扣尾闭包',
        'price':'任意尾长平衡末回复闭包的统一正客户价格'}
for key,source in sources.items():
    s=source.read_text()
    if key=='hierarchy':
        s=s.replace('正式对象拟承接：','对象ID：')
        s=s.replace('前三个带横线的符号','三个带横线的符号')
    front=f'---\nid: {ids[key]}\nkind: lemma\ntype_tag: 引理\ntitle: {titles[key]}\nstatus: proved-with-exact-scope\ntruth_status: proved\nscope: 完整有序历史纯SPE的局部必要不等式及所明示投影；不含六人全域半覆盖结论\n---\n\n'
    s+='\n## 文件定位与证据等级\n\n'
    s+=f'本页来自Boss2 Main实读、推导和独立审计后的正式回流。RUN为 `six-boss2-20261111-cross`，工作区根为 `{RUN}`。'
    if key=='hierarchy':
        s+='未加目录前缀的层级计算材料均在工作区的 `joint_requery/`；17份旧提升与500权包在其 `portfolio_comparison/`；Main独立程序及报告在RUN根目录。'
    elif key=='prefix':
        s+='未加目录前缀的16行包、发现器及精简器均在工作区的 `coverage_bridge/`；Main独立程序及报告在RUN根目录。'
    else:
        s+='本一般命题原推导在 `main_pair/balanced_any_tail_price.md`；独立审查在 `coverage_bridge/audit_balanced_any_tail_price.md`。'
    s+='全部原始点位于 `master_cuts/`。一般命题由本页证明承担；具体有理点、严格包含或有限LP结果分别以明确SHA和完整回代承担。\n'
    (R/paths[key]).write_text(front+s.rstrip()+'\n')

fp=R/paths['finite']
s=fp.read_text()
marker='## 8. 第四、五轮：5752与5775的精确原始/对偶'
assert marker not in s,'Formal round already assembled; do not append twice'
assert hashlib.sha256(fp.read_bytes()).hexdigest()=='5d13402bbaad268e1695427ae1e8aa99e8112d46016e856f4dc4316ccdafb435'
s=s.replace('# 固定16hist必要图的三轮精确最优值','# 固定16hist必要图的六轮精确最优值')
intro='''
本对象版本2补入5752、5775和5783三轮精确证书及正尾行的有限消融；前版到5744的全部结论保留。各轮最优值小数仅供阅读，证明使用后文绑定的准确原始/对偶。

| 行数 | 归一化O | 精确最优W的小数显示 | 主要新增约束 |
| ---: | ---: | ---: | --- |
| 5716 | 1 | 0.4900905644294647 | 三份冻结包的24个不同向量 |
| 5727 | 1 | 0.4901508813179543 | 6条折扣/组合查询与5条共享PAIR |
| 5744 | 1 | 0.4908340074462763 | 16条更早源PAIR与1条普通组合查询 |
| 5752 | 1 | 0.4916608461765668 | 8条共同17查询投影 |
| 5775 | 1 | 0.49192027032608004 | 7条共同查询更新与16条共享末端初段/尾闭包 |
| 5783 | 1 | 0.4926332627883867 | 8条616特征的跨旧查询PAIR |

5752早期对偶支撑恢复失败的记录保留。后续修正候选等式选择后，原点字节未改，已得到全部非负的匹配有理对偶；不能把早期未认证状态回填成当时已完成，也不能继续把现状态记成仅原始可行。
'''
heading='# 固定16hist必要图的六轮精确最优值\n'
s=s.replace(heading,heading+intro+'\n',1)

def section(text,heading):
    lines=text.splitlines()
    lines[0]=heading
    for i in range(1,len(lines)):
        if re.match(r'^#{2,5} ',lines[i]):lines[i]='#'+lines[i]
    # Markdown targets in the agent originals are relative to master_cuts/.
    text='\n'.join(lines)
    text=re.sub(r'\[([^\]]+)\]\(([^):]+)\)',lambda m:f'`{RUN}master_cuts/{m.group(2)}`（{m.group(1)}）',text)
    return text.rstrip()+'\n'

s+='\n'+section((B/'master_cuts/formal_5752_5775_gap.md').read_text(),marker)
s+='\nMain独立 `main_verify_primal_dual.py` 对5752和5775的全部原始行/对偶列与继承矩阵前缀再次核验通过，分别见RUN根目录 `main_verify_dynamic_5752.json`、`main_verify_dynamic_5775.json`。5775只在本轮四条新行上使用正对偶，故5752加这四行的5756子系统具有同一精确最优值；不主张其它行全域冗余。\n'
s+='\n'+section((B/'master_cuts/formal_5775_tail_ablation.md').read_text(),'## 9. 正尾合同的严格有限目标提升')
s+='\nMain独立重构删行集合、所有5763条保留约束和5775完整对偶，全部精确通过；见RUN根目录 `main_verify_tail_ablation.py/json`。无需证明消融点本身最优即可得到严格有限改进。\n'
s+='\n'+section((B/'master_cuts/formal_5783_gap.md').read_text(),'## 10. 第六轮：跨旧查询PAIR的5783行证书')
s+='\nMain独立全部行/列证书重放为 `main_verify_primal_dual.py dynamic_5783 --base dynamic_5775`，报告 `main_verify_dynamic_5783.json`；5783全行、4849对偶列、继承5775前缀、源点/矩阵/对偶SHA及目标取等全部通过。新增行背后的两个严格投影包含由 `M-b1b4276f0ec747ed8c347bda65c9e0af` 的独立提升与分离见证承担，不能用目标上升替代完整锥严格性证明。\n'
fp.write_text(s.rstrip()+'\n')
out={'ids':ids,'bodies':paths,'body_sha256':{k:hashlib.sha256((R/p).read_bytes()).hexdigest() for k,p in paths.items()},'new_finite_version':2}
(B/'formal-round4-identities.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
