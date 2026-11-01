# fixed_bridge_mult2 / fixed_bridge_mult3 实读与比较

## 来源与实际读取

本批处理两个当前未完成的冻结源版本：

- 7cdb308f85a723cb0b0d，路径 research/workspaces/customer-attraction/R-373daba10913464c93771a808d88fce3/credible/fixed_bridge_mult2.json，源 SHA-256 808c20a5fa44dcb11d91924a63849825e3fc7a3c984dd4433eeb5d6c5e885bbc。
- 3c4874a0fc772404d552，路径 research/workspaces/customer-attraction/R-373daba10913464c93771a808d88fce3/credible/fixed_bridge_mult3.json，源 SHA-256 c3b17b2b8b9e03caafcd3656ddb6904613e1430b5e75f9c3348310e09f283d84。

两源在冻结 legacy-cleanup 与 main 提交中各自同路径同字节；本地已用 tools/cleanup.py clean show 读取并保存为 fixed_bridge_mult2.json、fixed_bridge_mult3.json。没有执行 claim、done 或 push。

我同时实际读取了同一 R-373d 工作区的 README.md、credible/fixed_bridge_attack.py，以及相关的 count_milp.py、三类扫描器、global/unique_*、independent/menu_pure_attack.py、independent/query_existing.py 和独立 root-menu 审查。结果与已入库的 archives/customer-attraction/state/障碍/R-373d耦合桥与计数MILP有限证书--障碍.md 和其证据目录交叉核对，并运行了现有验证器：

    python3 archives/customer-attraction/tools/evidence/R-373d-coupling-credible-20261031/validate_r373coupling.py

验证器返回 passed=true、fixed_bridge_runs=2，同时核对三份计数 MILP 候选、780 条 full-history 检查及其它已入库证据。

## 两个 JSON 的数学含义

两个文件都由 fixed_bridge_attack.py 产生，固定参数 p=6,m=3。这里 p=6 是六个客户主题标签/列，m=3 是三名顺序提供者；不是当前六人目标的 m=6。脚本载入既有的 individual_security_failure 策略证书，把其完整有序历史动作表固定为一个 StrategyCone，在该固定策略锥中枚举三主题 portfolio，并以线性规划寻找一个客户类型权重向量。LP 解再用有理数恢复为整数克隆客户，并由 verify_certificate 检查该固定策略证书的全部历史最佳回应。

mult=2 文件的主要字段为：

- path=[0,3,4]，portfolio=[1,2,4]；
- objective=-6/23；
- 沿策略的提供者收益 (48,48,42)；
- 终局覆盖福利 W=138，比较 portfolio 的最优覆盖 OPT=198；
- 终端主题计数 [1,0,0,1,1,0]。

mult=3 文件的主要字段为：

- 同一 path=[0,3,4]，portfolio=[1,2,5]；
- objective=-123/206；
- 收益 (69/2,73/2,32)；
- W=103，OPT=145；
- 终端主题计数同为 [1,0,0,1,1,0]。

objective 是固定策略锥中针对辅助 bridge 目标的 LP 值，不是 2W-OPT_6。两例都满足半覆盖不等式：2*138-198=78>0，2*103-145=61>0。因此它们不是六人 half 反例，也不是一般 Q-CAG-HALF 的反例。

## 比较与独有内容

两源共享同一完整策略表、同一三提供者/六主题实例骨架和同一路径；差别是 LP 中的桥乘数 mult=2 与 mult=3、最优 portfolio 和对应客户类型权重。mult=2 的整数克隆总客户数为 198，mult=3 的总客户数为 145；它们不能互相覆盖为单一 JSON，但数学作用相同：分别给出两个辅助 bridge 强度下的最优固定策略锥攻击屏幕。

已入库障碍正文已经逐字记录这两组数值和边界，并在证据目录中保留两个 replay JSON，路径为：

- archives/customer-attraction/tools/evidence/R-373d-coupling-credible-20261031/replay/fixed_bridge/research/workspaces/customer-attraction/R-373daba10913464c93771a808d88fce3/credible/fixed_bridge_mult2.json
- archives/customer-attraction/tools/evidence/R-373d-coupling-credible-20261031/replay/fixed_bridge/research/workspaces/customer-attraction/R-373daba10913464c93771a808d88fce3/credible/fixed_bridge_mult3.json

两 replay 文件与 clean-show 内容逐字节相同（SHA-256 分别为 808c20a5fa44dcb11d91924a63849825e3fc7a3c984dd4433eeb5d6c5e885bbc 和 c3b17b2b8b9e03caafcd3656ddb6904613e1430b5e75f9c3348310e09f283d84）。因此本批没有新增第三份正式数学对象；独有字节内容已由证据文件保留，语义结论已由障碍正文承接。

## 准确处置

建议两个源都登记为 retained，目标同时指向现有障碍正文与 exact replay JSON。理由是：源文件的精确输出已在结果分支证据目录保全，且数值、参数、策略锥边界已在正式障碍正文中解释；它们不应被标为当前 half 定理或反例。下一步若写端点恢复，可直接提交 receipt-draft.json 中两条语义处置记录；在此之前保持 pushed=false、done=false。
