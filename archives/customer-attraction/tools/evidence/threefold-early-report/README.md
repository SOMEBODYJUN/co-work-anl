# 三重早期覆盖残差表证据

正式对象：[完整残差有限表](../../../state/计算/三重早期覆盖的完整残差有限表--计算.md)。原审计入口重放由配套[含交集审计器](../../../state/程序/三重早期覆盖的含交集系数审计器--程序.md)承担，本目录没有重复执行原入口。

| 文件 | 身份 | SHA256 |
|---|---|---|
| original.json | 原1861B报告，主源84c70d3a64e4a4a0d470 | 6b3ff9871170e1179e8d3df35c5e042788d33791541f82e803804faa88889783 |
| source-threefold-proof.md | 原5181B证明，8351aa32dfb923f6c91b | 6b1ec8fb4d89613f325beaf292a7cb078da8a03095e08d65a66148a45ccc63da |
| source-threefold-review.md | 原3176B审查，299d22a338eb2e9757b8 | 90bd865e11853d794c62c1e6a49b0b69d82d9c7e22a663ae8ed8eb112f7e7d7b |
| audit_rho_endpoints.py | 当前新写64×5端点公式核表器 | 最终脚本SHA记录于当前输出 |
| current-endpoint-audit.json | 当前实际执行输出，非原发现输出 | 含输入/脚本SHA、Python版本、全64rho、极值端点和符号数 |

三份原件均由正常work.py clean show ID --out取得；对应两冻结提交为68fad804ec5946cb296f77dc5b336308a66abf12与aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c。原路径前缀为research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/，三个文件名依次为audit_threefold.json、research_1/threefold_penultimate_half.md、review_threefold.md。相关证明/审查只作实读闭包，不代办其主源完成。

已全文实读并直接复用配套目录原字节：

- [3409B父方程序](../threefold-early-auditor/original/audit_threefold.py)，82711e93237a7f66a20c，SHA 0b336908e52a26d5785ef048a9d80c6f79e0bad59f9c4bbf40d4f8c681da8b7e。
- [1847B作者JSON](../threefold-early-auditor/original/research_1/threefold_penultimate_exact.json)，85961fbb929b166658cb，SHA 7adcce9a18beb2654c5fe1a4ef5dc45d8d130e8426f81928243cedd6ea75d35a。
- 1926B作者replay_threefold_penultimate.py亦经clean show全文读取，源5bac2c33a9112ba907b7，SHA 7cb092bb5ffbdb20c8a3398b436d6ca19ce788f74c3ad2e5f06730052d81b285；本目录不运行或导入它。

原父方代码只与作者JSON的rho_actual_membership和complete_restricted_state_count比较，不认证作者全部字段。配套[实际运行记录](../threefold-early-auditor/rerun/run_report.json)已实读：未优化Python3.12.14子进程执行原入口，exit0、stderr空，1861B stdout与冻结报告逐字节全等；[完整输出](../threefold-early-auditor/rerun/audit_threefold.json)也已字节比较确认。这不改写过去审查曾未读代码/未运行的历史陈述。

本目录当前唯一数学入口为audit_rho_endpoints.py，从仓库根用python3执行，参数为--output archives/customer-attraction/tools/evidence/threefold-early-report/current-endpoint-audit.json。最终运行exit0、stdout/stderr空，拒绝Python -O。添加作者“实际比较/未断言字段”记录后重新执行，所交输出脚本SHA对应最终代码。

新核验先由交集消去公式合并实际份额，再将d=0线性域与d≥1双仿射域化为五端点，只执行64×5=320个Fraction标量；核两原表全64rho、主报告八字段、22负/2零/40正、P3的42型、五层界及极值键。2058/3528由组合公式计算，没有重新枚举原全部系数域；五端点充分性由正文解析证明承担。

不是游戏/SPE枚举或P2反例搜索，不认证作者273负Q计数、任意背景五人、无条件六人、七极大、任意人数、外审或新颖性。主报告minimum_residual=0是条件域Q最小，全64rho最低−1079/360，二者无矛盾。
