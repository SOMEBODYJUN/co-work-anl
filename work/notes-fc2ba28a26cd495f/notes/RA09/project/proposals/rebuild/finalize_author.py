# One-time authoring history; use build.py to regenerate from the final page-data files.
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
base=HERE/'page-data'
data={n:json.loads((base/f'p{n:03d}.json').read_text()) for n in range(1,13)}
def target(d,i):return next(t for t in d['target_units'] if t['id']==i)
def change(n,i,text):target(data[n],i)['text']=text
def new(n,i,txt,origin='editorial',src=(),explanation='新增复习章节标题，说明后续内容的逻辑位置。'):
 data[n]['target_units'].append(dict(id=i,text=txt,source_ids=list(src),origin=origin,explanation=explanation,status='resolved'))
def order(n,ids):
 d=data[n];ts={t['id']:t for t in d['target_units']};actual=[k for k in ts if k.startswith('N')]
 assert set(actual)==set(ids),(n,set(actual)-set(ids),set(ids)-set(actual))
 d['target_units']=[t for t in d['target_units'] if t['id'].startswith('T')]+[ts[k] for k in ids]
change(1,'N-title',r'''# 实分析 9：复习笔记

## 目录

1. **$G_\delta$、$F_\sigma$ 与 Borel 集**：定义与基本例子；无理数集不是 $F_\sigma$；度量空间中的开闭集表示。
   - 1.1 **Borel 集与 Lebesgue 可测集**：Borel 集族的基数；Cantor 零测集中的非 Borel 子集；Carathéodory 可测集族严格大于 Borel 族；边界分解。
2. **开集外逼近与闭集内逼近**：有限测度证明；无限测度的局部分解；取补得到内逼近。
   - 2.1 **相差零测集的 Borel 外壳与内核**：$G_\delta$ 外壳、$F_\sigma$ 内核及可测性逆向判别。
   - 2.2 **由开、闭集确定测度**：外正则、闭集内正则与有界集的内外测度判据。
   - 2.3 **边界零测的充分条件**。
3. **积分引入与逆像族**：分层草式；拓扑基判别；逆像的交并补恒等式；$\sigma$ 代数及最大目标拓扑。
4. **可测映射与生成族判别**：两端可测空间；生成族判别的必要性、充分性。
5. **扩展实数与迹 $\sigma$ 代数**。
   - 5.1 **序拓扑**：开区间、端点半直线、邻域与子基。
   - 5.2 **Borel 代数**：端点单点集；从 $\mathbb R$ 到 $\overline{\mathbb R}$；四种半直线；与 $[0,1]$ 的同胚。
   - 5.3 **限制（迹）$\sigma$ 代数**：任意定义域上的构造及可测定义域的简化。
6. **Lebesgue 可测函数**：上水平集定义；$\operatorname{MF}(E)$；Borel 逆像判别；原图中源、目标集合族的选择。
7. **四种可测性的比较与反例**：完整强弱关系；中间条件互不蕴含；有限区间不能区分正负无穷。
8. **可测函数的基本例子**。
   - 8.1 **常函数**：包括正负无穷常值。
   - 8.2 **示性函数**：水平集端点及可测性充要条件。
   - 8.3 **连续函数**：孤立点辨析与水平集直接证明。
   - 8.4 **连续蕴含可测的第二条路线**：相对拓扑、逆像族包含、生成 Borel 代数。
9. **原件终页说明**。

> [!info] 编排说明
> 普通正文保留原稿内容；蓝色信息块分别标明补充解释、补充证明或纠错。原稿明确待填的位置用红色文字保存。中性编号表示尚待判读的字迹，不表示数学练习。原稿页序另见保真转写；这里把基础工具与相应证明排在一起，并保留重复表述、不同路线、旁注及原图。''')
target(data[1],'N-title')['explanation']='新增完整复习目录和颜色类别说明；按知识依赖排列工具、命题、题解及两条连续性证明。'
# Basic examples precede the irrational counterexample; preserve all originals in the transcription.
change(1,'N-P001-U006',r'2. $\mathbb Q$ 是 $F_\sigma$，$\mathbb Q^c$ 是 $G_\delta$。')
change(1,'N-P001-U007',r'3. $\{x\}=\displaystyle\bigcap_{n=1}^{\infty}B(x,1/n)$。单点是 $G_\delta$ 与 $F_\sigma$。')
change(1,'N-P001-U005',r'4. $G_\delta$ 不一定是 $F_\sigma$。〔“不一定”按上下文恢复〕')
order(1,['N-title','N-P001-head']+[f'N-P001-U{k:03d}' for k in [1,2,3,4,6,7]]+['N-P001-S01','N-P001-U005','N-P001-S04']+[f'N-P001-U{k:03d}' for k in [8,9,10,11,12]]+['N-P001-S02','N-P001-U013','N-P001-S03','N-P001-U014'])
# Put each detailed answer directly after its proposition.
new(2,'N-P002-S05',r'''> [!info] 术语澄清：这里的 Borel 测度
> 把 Lebesgue 测度 $m$ 限制在 $\mathcal B(\mathbb R^n)$ 上，所得 $m|_{\mathcal B}$ 的定义域是 Borel $\sigma$ 代数，且继承可列可加性，所以是一种 Borel 测度。一般说“Borel 测度”只说明测度定义在 Borel 集上，并不唯一指定 Lebesgue 测度。此处按原稿的限制式理解。''',origin='supplement',src=['RA09-P002-U008'],explanation='新增术语范围说明，避免把Borel测度误读为唯一的Lebesgue限制测度。')
order(2,['N-P002-head']+[f'N-P002-U{k:03d}' for k in [1,2,3,4]]+['N-P002-S01']+[f'N-P002-U{k:03d}' for k in [5,6]]+['N-P002-S02','N-P002-U007','N-P002-S03','N-P002-U008','N-P002-S05','N-P002-U009','N-P002-U010','N-P002-U011','N-P002-S04','N-P002-U012','N-P002-U013'])
order(4,['N-P004-S00','N-P004-head','N-P004-U001','N-P004-U002','N-P004-U003','N-P004-S01','N-P004-U004','N-P004-U005','N-P004-S02','N-P004-head2','N-P004-U006','N-P004-U007','N-P004-U009','N-P004-S03','N-P004-U008','N-P004-S04'])
new(5,'N-P005-head1','### 2.3 边界零测的充分条件')
new(5,'N-P005-head2','## 3. 积分引入与逆像族')
change(5,'N-P005-U002','### 勒贝格积分')
ns=[t['id'] for t in data[5]['target_units'] if t['id'].startswith('N') and t['id'] not in ['N-P005-head1','N-P005-head2']]
ns.insert(ns.index('N-P005-U001'),'N-P005-head1');ns.insert(ns.index('N-P005-U002'),'N-P005-head2');order(5,ns)
change(6,'N-P006-H','## 4. 可测映射与生成族判别')
new(6,'N-P006-H2',r'## 5. 扩展实数与迹 $\sigma$ 代数')
change(6,'N-P006-U009',r'### 5.1 广义 $\overline{\mathbb R}$ 上的拓扑')
ns=[t['id'] for t in data[6]['target_units'] if t['id'].startswith('N') and t['id']!='N-P006-H2'];ns.insert(ns.index('N-P006-U009'),'N-P006-H2');order(6,ns)
change(7,'N-P007-H','### 5.2 扩展实数的 Borel 代数')
change(7,'N-P007-U011',r'### 5.3 限制 $\Sigma$ 代数')
order(7,['N-P007-H','N-P007-U009','N-P007-U010','N-P007-S04']+[f'N-P007-U{k:03d}' for k in [1,2,3,4,5]]+['N-P007-S01','N-P007-U006','N-P007-U007','N-P007-S02','N-P007-U008','N-P007-S03']+[f'N-P007-U{k:03d}' for k in [11,12,13,14,15]]+['N-P007-S05'])
change(8,'N-P008-H','## 6. Lebesgue 可测函数与 Borel 逆像判别')
change(9,'N-P009-H','## 7. 四种可测性的强弱与无穷端点反例')
t=target(data[9],'N-P009-S01');t['text']=t['text'].replace('第 2 节已经构造','第 1.1 节已经构造')
new(9,'N-P009-H2','## 8. 可测函数的基本例子\n\n### 8.1 常函数')
ns=[t['id'] for t in data[9]['target_units'] if t['id'].startswith('N') and t['id']!='N-P009-H2'];ns.insert(ns.index('N-P009-U012'),'N-P009-H2');order(9,ns)
change(10,'N-P010-H','### 8.2 示性函数')
change(10,'N-P010-U008','### 8.3 连续')
change(11,'N-P011-H','### 8.4 连续蕴含可测：第二条证明路线')
change(12,'N-P012-H','## 9. 原件终页说明\n\n〔物理第 12 页为空白页。上一节已保留第 11 页的最后两行及其补充证明。〕')
for n,d in data.items():
 for t in d['target_units']:
  if t['origin']=='editorial' and t['explanation']=='按原图保留本单元。':t['explanation']='新增物理页定位标题。' if t['id'].startswith('T') else '新增复习章节标题，以知识主题标识后续原稿内容及相邻补证。'
 p=base/f'p{n:03d}.json';tmp=p.with_suffix('.json.tmp');tmp.write_text(json.dumps(d,ensure_ascii=False,indent=2).rstrip()+'\n');tmp.replace(p)
