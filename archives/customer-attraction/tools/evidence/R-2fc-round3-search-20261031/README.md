# R-2fc round3_search 八源：早期 floor 有限锥搜索与精确候选复核

八个源全部在认领后 clean show 返回 0。源文件和原始输出保存在 source、clean-show，冻结提交/blob/大小/SHA 在 source-manifest.json。

early_floor_walk.py 是浮点 BI/LP 的有限锥搜索：每条约束使用一份完整策略，浮点只负责提议，若有新点再用 Fraction 恢复并做 canonical all-history 检查。它依赖冻结的 R-18e993… cone_walk.py 与 individual_face_walk.py，两依赖不在本八源中；本次读取了完整代码与依赖路径，未伪称在缺依赖环境中重跑该入口。

## 搜索报告

- m4p6_pos0.json：4 玩家、6 主题、35 步、33 个锥，最佳 7；浮点 proposal 范围约 4 到 7，只有一个 exact recovery 记录。
- m4p6_pos0_multi.json：4 玩家、6 主题、65 步、54 个锥，最佳 7；同一有限早期位置的多起点扩展，只有一个 exact recovery 记录。
- m5p7_pos0_multi.json：5 玩家、7 主题、65 步、56 个锥，最佳 9；浮点 proposal 约 6 到 9，只有一个 exact recovery 记录。

三个 best JSON 都是 one genuine complete-history pure SPE; finite early floor attack only：m=4 两个候选均 u=1,W=5,OPT=7,ratio=7，m=5 候选 u=1,W=6,OPT=9,ratio=9，full_strategy_verified=true。audit_unit_points.py 独立展开单位客户并枚举所有有序历史，用 Fraction 复核得到 4 人实例 259 个历史/1295 个非自身偏离，5 人实例 2801 个历史/16806 个非自身偏离，最小 slack 均为 0、2W-OPT=3。

这些 exact 候选分别达到 2m-1 的早期个人 floor，但不产生 OPT/u>2m-1 的反例。锥搜索的 best 和无新点只属于固定参数、随机种子、步数、support/mode 与时间范围；没有给出任意目录、全部完整 SPE 或 Q-CAG-HALF 的普遍证明。validation.json 记录源码哈希、编译、三候选 Fraction 复核和依赖边界。
