# Boss7 批次 C：R-373d root_menu/root_review 三源及 workspace 元数据比较记录

## 实际读取

- `25261bdccbe1c27d137b`：167870B JSON，SHA-256 `fa95ba29...d1f9`；完整解析 status、factor、43 历史、215 IC 行、2 背景、278 trace 和 best 字段。
- `3b4b9db523e90c02ffef`：75139B JSON，SHA-256 `89d34bf1...b8028`；完整解析同一结构、190 trace 和 factor=3 的正浮点 gap。
- `e6b00c3f5833ca19a86a`：2252B Python，SHA-256 `83279a0c...ab62`；逐行读取并独立运行。
- `b4e8e4749c21cde5c993`：10464B JSON，SHA-256 `f52c8264...c1815`；完整读取 36 个有序覆盖条目、42 个激励比较和命名标量。
- `aff821168f7ae8b335a0`：150B workspace JSON，SHA-256 `1125fdec...4701`；读取全部四字段并与同目录证据对照。

## R-373d root_menu 对象比较

现有 `archives/customer-attraction/state/资源/R-373d根菜单容量交替LP浮点发现器--资源.md` 已全文解释同一发现器：固定三人六主题策略、43 个节点、215 条非零 IC 行、63 个客户掩码、外层/内层交替 LP、浮点状态和“no universal assertion”边界。该资源对象引用 `probe_root_cap.py`，并明确相邻两个 JSON 应由自己的 source records 单独处置。

本批两 JSON 的独有内容是完整 trace 和两个不同 factor 的 best 记录。它们不是一般数学证明，也不能被 `gap>0` 解释成完整 SPE 反例。新验证脚本核对结构、非负性、概率归一和 `factor*cap-W=gap`，并重放既有探针的 factor=3 首条输出。建议新建一个计算证据对象或在现有资源证据目录加入 manifest；处置为 `integrated`（若正文只保留资源对象）或 `retained`（若把原 JSON 作为独立 provenance 资产）。本草稿建议 `integrated` 到一个“有限运行记录”对象，同时保留 raw JSON。

## R-373d root_review 对象比较

现有 `archives/customer-attraction/state/计算/最优遗漏族的逐客户与线性证书--计算.md` 已保全 71 客户、两人、六主题、完整 7 个历史、42 项含自身比较、21 个主题对和唯一最优 (TQ) 的另一组 R-171 冻结源；现有反例/资料正文进一步给出 (W=35,OPT_2=38,R=36)，并明确这只否定“遗漏≤W/由实际福利支付全部遗漏”的加强桥，不否定六人 half。

本批 `e6` 脚本与 `b4` 报告逐字定义相同 71 客户重数、同一回复数组 `[1,4,4,4,5,4]`、同一路径 `[0,1]`、同一 (W=35,OPT=38)、唯一最优支持 `[2,3]`、(R=36)，并经本地重放得到 42 comparisons 和 36 coverage rows。它们提供一个不同 R-373d root_review 路径的独立 exact replay，但没有新增命题、参数族或量词。数学结论已由现有 R-171 计算对象和唯一最优反例对象承重；建议 `retained` 作为独立重放 provenance，或 `duplicate`（若只保留一套 exact audit）。本批不新建反例、不把 71 客户重复计入主对象。

## workspace 元数据

`aff821168f7ae8b335a0` 只有 `schema=1`、`save=customer-attraction`、`actor=R-373daba10913464c93771a808d88fce3`、`instance=79cefb89a2254f2cb010c1acd68f51bb`。它不承重数学或实验结果。建议 `retained` 到 R-373d provenance manifest；不进入 `state/`，也不与 JSON 数值源合并成“结果”。
