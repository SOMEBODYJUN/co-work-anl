---
id: "unrelated-machines/dual-rail-scalar-split-final-review-contracts"
kind: review
type_tag: 审查
title: "双轨标量与拆分unit的共同调度及锐例审查"
status: complete-primary-read-and-scoped-mathematical-reconstruction
summary: "同一审查中的两个不同原矩阵：半槽scalar与split整数流；绝对三半锐不等于近似比锐，保真实独立顺序和有限软件范围。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/dual_rail_threshold_soundness_boundary_review.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/reviews/unrelated_machines/dual_rail_threshold_soundness_boundary_review.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/dual_rail_threshold_soundness_boundary.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/current/unrelated_machines/dual_rail_threshold_soundness_boundary.md"
evidence_manifest: ../../../../tools/evidence/um-next-available-reviews/source-manifest.json
---

# 完整原任务与两种外端合同

本页处置主源72273b87376cc8657417的归一化scalar及split-unit部分。主源全文22583B/204行已读；它拼接根研究者实现核对和两位内部审者记录，不能当成三次新盲审。当前数学47781e3c6375a3868f86全文148行已比较，SHA为069d7ac109263c410b0874e86840d5ad8fb0720b03b4acaae80825c7d11550ee，与最终所审版本一致。单例外/cube的不同身份另见[续页](双轨指定例外与完整cube精确前沿的版本审查--审查.md)。

每变量v有互异的两轨U(v,+)、U(v,−)及一个仅能在两轨运行、时间1的selector。每个真实occurrence e=(v,s,c)是独立port；重复文字仍是不同任务。轨实际出现K(v,s)>0时内端时间1/K，K=0没有port，不除零。两类模型均没有额外预载或任务，空机器集可添空dummy；所有任务必须实际分配一次。

| 身份 | clause外端 | arity | 共同输出 |
|---|---|---|---|
| UM-NORMALIZED-DUAL-RAIL-UNIVERSAL-THREE-HALVES-v1 | 一台scalar机，各port时间1/A_c | m_c≤2A_c−1，整数A_c≥1 | 轨≤3/2、clause≤1 |
| UM-SPLIT-CAPACITY-DUAL-RAIL-THREE-HALVES-v1 | L_c=min(A_c,m_c)台不同unit机，各port可去其中任一台，时间1 | m_c≤2A_c | 轨≤3/2、各unit≤1 |

split port通常不止两个端点。不能把scalar的10机锐例σ原封用于14机split实例，或将两个模型的物理assignment枚举数混用。A_c二进制给出；L_c截实际arity，避免按巨大数值造空机器。

# scalar半质量有序槽与经典工具

每任务在两真实端点各放半片。轨上selector半片排首（K=1平局仍排首），其后port半片两两成单位槽；clause端也两两成槽。任意任务集S有2|S|半片，槽至多装两半片，所以邻槽至少|S|，同一次Hall匹配覆盖全部原任务。

收到selector的轨，其第一槽被selector占用；余下至多floor(K/2)个port，实际负载≤1+floor(K/2)/K≤3/2。K=0只有selector。没有selector的轨即使接全部port也至多1。clause最多ceil(m_c/2)个port，故负载≤1。所有界来自一个共同匹配。

一般半质量行的非增时间w_1,w_2,…给奇序和O=w_1+w_3+…；O−w_1≤w_2+w_4+…，所以O≤(Σw+w_1)/2。半分数负载≤T、最大支持时间≤T即得3T/2。这是ST有序槽的直接特例，未改进一般LP的二倍舍入，也未声称一般矩阵都能取得这种半质量点。

另一个规范quarter-flow实现仅承诺全局3/2：K≥2候选轨中1/4内留、3/4外送满足K/4≤floor(K/2)、3m_c/4≤floor(3A_c/2)；K1/K1变量的一单位供给需与它们共用同一clause容量。独立half-slot实现另保证clause≤1，不能给quarter-flow API补上更强输出。

# split的共同整数流与完整回填

先将含空轨的变量selector放空轨，其余port全部内留。剩余变量两轨均非空，令D_v=K_++K_-、b_v=floor(D_v/2)。网络为source→变量容量b_v、变量→每occurrence容量1、occurrence→clause容量1、clause→sink容量A_c（可截m_c）。每occurrence半流使clause≤m_c/2≤A_c；D_v奇时删掉一枚半流即可使变量供给恰b_v。因此整数满流存在。

若整数流挑出的两符号数z_s都小于ceil(K_s/2)，则z_++z_-≤ceil(K_+/2)+ceil(K_-/2)−2≤b_v−1，矛盾。挑一条合格轨放selector，只保留该符号中被流选中的port外送，另一符号全收回。选轨负载≤1+floor(K_s/2)/K_s，另一轨≤1；回收只减少clause使用。每clause至多min(A_c,m_c)件外送，逐件注入不同unit机。每件selector/port均保留原资格和身份。

单位增广次数受真实occurrence数控制，不按A_c或分母数值循环。构造无需源赋值、YES见证或OPT。变量非空时selector给OPT≥1，从绝对3/2可推本类3/2近似；空任务单独给0。

# 两个绝对锐例与源解码边界

A_c=2的四clause依次为(x+,x+,y+)、(x−,x−,y+)、(y−,z+,z+)、(y−,z−,z−)。每轨K=2。若y真，前两clause迫x同时真/假；故y假，后两再迫z同时真/假。严格阈值源无解。

C≤1时selector轨不能留任何正port，所有真port必须外送；clause容量保证真occurrence数≤A_c。反向给严格源解，真port全外送、假port全内留即得C≤1。因此无C≤1；所有处理时间是1或1/2，故OPT≥3/2。C>1后真轨可部分外送，不能继续同样解码。

scalar是10机15任务，selectors全放正轨、正port外送、负port内留得到轨全1、clause(3/2,1/2,1,0)，OPT=3/2。split是14机15任务；其上界须由前述流或实际unit注入得到，源记录独立完整σ的轨负载(3/2,1,3/2,1,3/2,1)、八unit负载(1,1,0,0,1,0,0,0)。下界仍由严格源和半整数网格给出。它们证明绝对上界锐；该例算法输出本身最优，未证明近似比3/2锐。

# 实际审读和有限实现记录

cover_consistency在先前单例外statement-first之后才读主文，其余合同属读后攻击。另一审者的normalized半槽/原scalar枚举及cube先按statement独立完成；split和one-exception则是canonical读后，不能全称为盲审。两者最初读1a75b459…版，最终069d7ac…版的§4说明性改句由实际重读/字节复原核对；数学合同未变。

主源记录根研究者亲读六代码并重跑：scalar12565完整模板、2000随机、748实际小OPT；独立half-slot250随机及32768份scalar原σ（13824份C=3/2，18944份C=2）；split18479模板、2000随机、32768内外模式。split的4251528份物理σ没有全枚举，不能拿模式数代替。另有12份原资格重建证书（scalar10/15、split14/15、两份cube42/165、单例外A1..8），由历史记录承担；本轮未读六代码或重跑这些程序。

现有双源正文只作数学比较，不重登记。该页简写单例外“一变量一exception”不足以表达另一合同，本批续页明确每条非空rail各一指定exception。外审、全球新颖性与一般UM近二正反面均未认证；相关状态不因历史无fatal或checkpoint升级。
