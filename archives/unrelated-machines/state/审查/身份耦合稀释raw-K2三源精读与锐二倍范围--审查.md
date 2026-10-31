---
id: unrelated-machines/identity-coupling-diluted-raw-k2-review-20261031
kind: review
type_tag: 审查
title: 身份耦合稀释 raw K2 三源精读与锐二倍范围
status: integrated-raw-k2-exact-and-final-read-after
truth_status: restricted-raw-k2-certificate-and-actual-gap
review_level: full-source-read-including-gzip-export
scope: explicit raw K2 typed certificate, exact actual gap family, and final read-after; no software replay or generic UM hardness
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_identity_coupling_diluted_shared_terminal_raw_k2_exact_reconstruction.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_identity_coupling_diluted_shared_terminal_raw_k2_author_proof_read_after.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_identity_coupling_diluted_shared_terminal_raw_k2_final_actual_read.md.gz
source_ids: [f89eb57bfb90e7e89fa7, 9de7832e06ab669adc28, 347281a40d6394f7d817]
source_sha256:
  - 622cafcc002d4b507ae8905cf2b4d2cc0cc16f538b33974f51695bd9fb58cb0f
  - f960b9f1cf8751aa82396c286929a950e3fa1ef563ea3b2deee5a4eff1f5e4b9
  - 372fbef7e8313285a5b10ebb44ff40af4a8782916fe9ca3bf4e9cd91dcb7909f
evidence_manifest: ../../tools/evidence/retired-identity-coupling-raw-k2-20261031/manifest.json
---

# 对象身份和实际 gap

三源处理显式 raw K2 typed certificate。参数为 k>=2、L=2k^2、M=1+120k^6 的大量物理互不相交组件；每个 h 通过 U 选 f，每个被选 B 再选 e 到 distinct unit terminals。完整 matrix 逐一列出机器、jobs、finite endpoints，dense size O(k^17)，finite times 位长 O(log k)。该对象不是 canonical-C2、一般 UM 或硬度证明。

最终稿和 Exact-first 共同核对：若完整 actual 的峰 C<2，h 所在 U 至少送 r=ceil(k(2−C)) 枚 f，B 再至少送 r 枚 e 到 distinct unit terminals，故 r^2<=k。反向取 floor(sqrt(k)) 个 f 与每个 B 同数 e、其它 jobs 全部留 home，达到 OPT(P_k)=2−floor(sqrt(k))/k。因而这是完整 ordinary jobs 的实际 family gap，非矩法则坏支持点的假象。

# raw 四次证书的准确强度

共同 raw assignment variables、Boolean/exclusivity/cover identities、global raw M2、每机 CONFIG first/pair 及全部 affine load localizers 均在同一有限 law 下成立；每个 sample 每 job 恰执行一次。B 的合法 rows 与 unit/home/mixed pairs 按 labels 逐项检查，最高 legal load 1+1/k。最终稿保留两个重要边界：同一 row triple 可能为负/不匹配（例如 F(R_jY_lY_l')=a/L>0 而 legal CONFIG 为零），且更强跨行两事件条件仍失败。raw M2 不被偷换为共同 Boolean CONFIG indicator M2，更不代表高阶 load localizers 自动成立。

所有 global affine contexts 的单组估计、slack 均值、截距与跨组件独立条件化均给出固定常数；M−1=60Lk^4 支付全局维度，不引入隐藏连续性常数。证书 monomial 数 O(E^4)，condition 后只处理至多四组件；未枚举指数 injections/permutations/samples。位复杂度关于显式 expanded input 多项式，未声称一般 SDP/CONFIG finder。

# 全类二倍上界与上确界

给任意普通 UM 的 raw K2 可行目标 T，令 y_jv=F(x_jv)。cover 等式和 CONFIG first 给 fractional row work<=T、每 resource fractional capacity<=1；按 processing time 排序切成容量一 slots，job-slot fractional matching 的整数性覆盖全部 jobs。第一 slot 负载<=T，后续 slot 的时间由前一满 slot work 支付，因此每行整数负载<=2T。于是 OPT(P)<=2 tau(P)，其中 tau 是 raw K2 可行阈值的 infimum；不要求 infimum 取得。P_k 给 ratio >=(2−floor(sqrt(k))/k)/(1+1/k) ->2，和全类上界合起来得到该 raw 证书类的 supremum 正好为 2。

最终稿还核了缩放 finite times 的合同：把 times 乘 k/(k+1) 同步缩放 legal CONFIG 与 OPT，target 归一化到 1，不残留单位 job 或外部负载。

# 三源比较、二进制证据与范围

| ID | 独有内容 | 处置 |
|---|---|---|
| `f89eb57bfb90e7e89fa7` | Exact-first 独立重构：完整矩阵/OPT gap、raw rows、global contexts、二倍 matching 上界与位复杂度 | integrated；独立重构不冒称软件执行 |
| `9de7832e06ab669adc28` | 作者 Proof read-after：raw M2/CONFIG rows、global affine contexts、证书生成和二倍上界前置链 | integrated；保留知情后身份和未读 audit 边界 |
| `347281a40d6394f7d817` | gzip final actual read-after：19100B/245行最终稿、全族实际 gap、supremum=2、scale 与软件范围 | integrated；gzip 原件和解压全文均保存，未读/执行 finite audit |

第三源原件是 gzip，已用 `gzip -dc` 完整导出；压缩源 SHA 为 `372fbef7e8313285a5b10ebb44ff40af4a8782916fe9ca3bf4e9cd91dcb7909f`，解压全文副本 SHA 为 `1ffa72b0838dac59855ddf39a90b4da540329b3f973cf67c5b7a031fc8011836`。证据目录的 validation PASS 只核源/副本哈希，不认证软件运行。

该对象仍不证明一般 UM hardness、native canonical-C2 gap、NP-hardness、actual-YES barrier 或六人 SPE。raw K2 certificate 的 full jobs、supremum=2 与 stronger localizer failure 需保持独立身份；未读其它 higher-d 合作或 finite audit 不得并入本页。
