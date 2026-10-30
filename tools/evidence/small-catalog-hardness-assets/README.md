# 小目录硬度输入资产

本目录保存八份冻结源原字节（15,082字节）、五份完整旁读依赖、三份五地点输入的原入口重放，以及六次四地点构造公式检查。数学对象为`archives/facility-games/state/计算/小目录硬度构造器与五地点样本的精确合同--计算.md`。

- `source-manifest.json`：每源ID、两条冻结commit/path、SHA256、大小、原件位置；执行产物hash与更正前两审查快照hash。
- `original/`：两个构造器、三个五地点整数实例和三个metadata；原字节未修改。
- `related/`：规范模型、五地点完整证明、四地点完整证明与内部review、五地点原审计源码。它们供理解与复现，**不在本批八源done集合**。
- `comparison-before-correction/`：本批实读时两份旧审查的精确快照，保留错误地点/设施词和full-diagonal误判的历史证据；当前正文应读Boss更正后的同ID对象。
- `replay_assets.py`：本批新写调用驱动，导入未修改原代码；原审计直接按条件成本核NE，不导入既有NE solver。本次不声称新造了一份独立NE实现。
- `run/`：三次原CLI的输入实例/参数输出、三次原audit_case完整结果、两个YES的完整25布局规则、总summary（含六个四地点完整生成输入与公式检查）。
- `replay.stdout.txt`、`replay.stderr.txt`：外层真实执行原始输出；stderr为0字节，exit0，Python3.12.14。

当次命令为`python3 replay_assets.py > replay.stdout.txt 2> replay.stderr.txt`，实际cwd和每个CLI绝对argv留在summary。三组五地点输入为([2],1,3/2,True)、([2],2,3/2,True)、([2,3],2,809/500,False)；顺序是numbers,target,a,full-diagonal。三份实例、参数和完整result均与冻结资产逐字段相等。仅最后一例采用同址正规形；正式正文解释其全局最优依据及单个异址factor为放松值的边界。

驱动忠实使用原CLI的`x`独占写模式。再次复现请把本目录的`original/`、`related/`和`replay_assets.py`复制到一个新工作目录，再运行；不要覆盖已有run产物或原件。运行目录可改变，数学输出应一致，绝对argv/cwd等环境字段会改变。

有限执行只覆盖这三份五地点资产、六次四地点构造及14次非法API拒绝。没有重跑原1103参数/96宏测试、14+9全体五地点案例、四地点32/19案例或全仓测试。四地点部分没有求NE/最优值。一般弱NP完全性、无FPTAS与文献地位分别依赖相应解析证明/外审，不由本目录运行次数产生。
