"""Main's assembly of reviewed stable proofs; no changes to agent originals."""
from pathlib import Path
B=Path(__file__).resolve().parent
R=B.parents[2]
lem=R/'archives/customer-attraction/state/引理'
calc=R/'archives/customer-attraction/subarchives/six-providers/state/计算'
lem.mkdir(parents=True,exist_ok=True);calc.mkdir(parents=True,exist_ok=True)
run='research/workspaces/six-boss2-20261111-cross/'
s=(B/'formal_joint_pair.md').read_text()
s=s.replace('正式回流稿：2026-11-11。','2026-11-11，Boss2，RUN `six-boss2-20261111-cross`。')
s=s.replace('## 4. 比较合同与待完成精确见证','## 4. 比较合同与严格投影增强')
s=s.replace('以下均位于 `research/workspaces/six-boss2-20261111-cross/`，正式归档时应保留相同字节或记录迁移后的SHA。','以下文件均位于 `research/workspaces/six-boss2-20261111-cross/`，其实际字节由登记及证据引用绑定。')
s=s.replace('`state/','`archives/customer-attraction/state/')
s=s.replace('本RUN `main_verify_pair.py` / `main_verify_pair.json`','本RUN根目录的 `main_verify_pair.py` / `main_verify_pair.json`')
start=s.index('最先发现的一份更小可见域见证亦保留在')
end=s.index('## 7.',start)
s=s[:start]+'早期抽象见证中出现的(p,ell)=(2,5)、(0,5)不满足actual第四源的ell≤p+2；这类背景只能用于离轨源，不能把其r记为u4。本节的13原子从实际六位联合域重新构造，避免了该域混用。早期诊断留在RUN工作区，不作为本节严格性的承重证据。\n\n'+s[end:]
(lem/'同源双末对跨枝配对与严格联合投影--引理.md').write_text(s.rstrip()+'\n')
s=(B/'coverage_bridge/formal_discounted.md').read_text()
s=s.replace('建议对象ID：`M-b233ef00a9c34e189817cdfb7a495107`（Main已分配）。','对象ID：`M-b233ef00a9c34e189817cdfb7a495107`。2026-11-11，Boss2，RUN `six-boss2-20261111-cross`。')
s=s.replace('最强逐客户势是收缩Bellman方程','按逐坐标顺序最大的可行势是收缩Bellman方程')
s=s.replace('的唯一解。右端在最大范数下','的唯一解。若一个有限势满足V≤T(V)，反复应用单调算子T得到V≤Tⁿ(V)，取极限即V≤V*，所以该解确为最大可行势。右端在最大范数下')
old='四状态(previous,current)的新查询扩展正在5727新点上计算：每步真实末位可以合法查询上一轨道主题，初态可取(R_e,Z_e)，转移(a,t)->(t,c)。其一般合法性可按同样证明给出，但不把尚未回报的四状态数值发现纳入本页六个已认证两状态切面，也不因程序已写就宣称进一步数值进展。'
new='后续在固定5727点做完四状态(previous,current)的120个结构/参数LP。唯一负行满足theta=0且上一主题查询权为0，准确归为普通单步portfolio权重更新；没有发现正折扣四状态负行。该有限扫描不证明整个四状态族冗余。其唯一行已还原为标准两状态接口，Main独立全列核对通过；详见 `coverage_bridge/new5727_single_portfolio_cut.json` 与RUN根目录 `main_verify_portfolio_5727.py/json`。它不混入本页固定5716输入的六行统计。'
assert old in s;s=s.replace(old,new)
s+='\n## 九、平衡源权时连续折扣的精确有限化\n\n'
bal=(B/'main_pair/balanced_discount_proof.md').read_text()
s+='\n'.join(bal.splitlines()[4:]).replace('## 一般平衡特例','### 一般平衡特例').replace('## 有限有理质量输入上的全区间优化','### 有限有理质量输入上的全区间优化').replace('## 对5727点的明确失败边界','### 对5727点的明确失败边界')+'\n'
s+='\n## 十、完整文件定位\n\n本页计算输入和脚本均位于 `'+run+'`。第七节无目录前缀的发现器、六行包与有限深度审计位于其 `coverage_bridge/`；Main独立核验位于RUN根目录；第九节脚本、精确折点结果和详细证明位于 `main_pair/`。初始母点位于 `master_cuts/`。全部通用不等式由本页逐式证明，有限JSON只承担所声明点的精确分离或有限参数族边界。\n'
front='---\nid: M-b233ef00a9c34e189817cdfb7a495107\nkind: lemma\ntype_tag: 引理\ntitle: 同源真实末回复的折扣闭包与二状态精确投影\nstatus: proved-general-local-inequality\ntruth_status: proved\nscope: 有限共同标签目录、完整有序历史纯SPE、固定同一源；有限投影计算不构成全域half证明\n---\n\n'
(lem/'同源真实末回复的折扣闭包与二状态精确投影--引理.md').write_text(front+s.rstrip()+'\n')
s=(B/'master_cuts/formal_finite_gap.md').read_text()
s=s.replace('共同模型仍采用有限非空标签目录、单位客户和六位单位权提供者。','共同模型仍采用有限非空标签目录、单位客户和六位单位权提供者。继承母矩阵含OPT单换行，故整套必要系统采用达到OPT6的六比较主题；本文新增局部IC行本身只要求这些查询主题合法。')
s=s.replace('回流目标：既有计算对象','对象ID：')
s=s.replace('本稳定稿只记录已完成的5716和5727两轮；任何后续候选、扫描或正在恢复的点不计入本稿的已证结果。','本节至第六节记录已完成的5716和5727两轮；后续精确结果在独立续节明确绑定，不将候选或未认证点混入已证结果。')
s=s.replace('所有下面文件均在本 `master_cuts/` 目录。','下表中的相对文件名均以仓库根下的 `'+run+'master_cuts/` 为基准；`../` 依此目录解析。')
s=s.replace('本稿到5727精确证书为止。随后更早源、四状态Bellman或新PAIR切面须另绑定其真实输入点SHA、独立核合法行并重新优化，不能并入本稿已有数值与已证范围。','前两轮冻结结果到5727精确证书为止。更早源、四状态Bellman或新PAIR切面均须另绑定真实输入点SHA、独立核合法行并重新优化。新点同W不代表隐藏向量相同；复核冻结负值必须读该切面包绑定的准确原点。完整重优化宜在工作副本执行，避免不同求解器版本选择另一最优完成后覆盖后续包绑定的旧点。')
front='---\nid: M-ddceaa3d53064498b3e833a32e1f3b6f\nkind: exact-finite-LP-optimum\ntype_tag: 计算\ntitle: 同源跨枝增强必要图的精确最优值与剩余半界缺口\nstatus: exact-rational-primal-dual-certificates\ntruth_status: finite\nscope: 固定16hist、4849列的明示必要LP；不是完整SPE或全输入半覆盖结论\n---\n\n'
s=s.replace('# 两轮切面并入后的固定16hist必要图精确最优值','# 固定16hist必要图的三轮精确最优值')
third=(B/'master_cuts/formal_5744_gap.md').read_text()
third=third.replace('# 第三轮：更早同源PAIR并入后的5744行精确最优值','## 7. 第三轮：更早同源PAIR并入后的5744行精确最优值')
third=third.replace('## 已认证结论','### 已认证结论').replace('## 新行来源及合法性','### 新行来源及合法性').replace('## 最优值提升由哪几条新行承担','### 最优值提升由哪几条新行承担').replace('## 原始/对偶证明合同','### 原始/对偶证明合同').replace('## 稳定产物与身份','### 稳定产物与身份')
third=third.replace('模型、全部有序历史/平局及固定支持局限沿用[两轮稳定稿](formal_finite_gap.md)。','模型、全部有序历史/平局及固定支持局限沿用本页前六节。以下相对文件名仍以 `'+run+'master_cuts/` 为基准。')
third=third.replace('只有16行的5743矩阵曾作准备','仅并入16条新增行的5743矩阵曾作准备')
third+='\nMain另用不导入构造器或求解器的 `'+run+'main_verify_primal_dual.py` 逐行/列复核第三轮，确认5727前缀矩阵字节结构未改、5744条原始约束和4849个对偶剩余均非负、原始与对偶严格取等；报告 `main_verify_dynamic_5744.json` 的三份输入SHA与上表全同。\n'
(calc/'同源跨枝增强必要图的精确最优值与半界缺口--计算.md').write_text(front+s.rstrip()+'\n\n'+third.rstrip()+'\n')
print('Prepared three reviewed formal bodies.')
