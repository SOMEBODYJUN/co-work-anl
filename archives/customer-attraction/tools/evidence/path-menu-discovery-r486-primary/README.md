# R-486 path-menu discovery outputs

本证据包保留三个冻结 JSON 源版本的原字节。它们由同目录的 `security/dual/probe_path_menu.py`（源 ID `547e882b4d3ad9496bf3`，另行清洗）生成；本包只复制输出，不把脚本或浮点结果冒作精确证明。

`full=False` 时 `backgrounds` 是沿策略真实路径、强制当前动作后删去该动作的 n−1 槽计数；`full=True` 时保留完整 n 槽计数。程序对随机生成的完整有序策略先构造真实偏离差 `Gamma`，再交替用浮点 LP 更新客户质量和查询分布。LP 归一化是客户质量总和 `sum(w)=1`，不是福利 `W=1`；报告的 `W=c·w` 是根策略实际覆盖质量，`cap` 是背景菜单的最小期望收益，`gap=n·cap−W`。

三个输出都没有正 gap：n=3,k=6 与 n=4,k=5 为零；n=5,k=5 的 full 菜单为 `-5/126`。没有保存 Fraction 对偶、完整精确 Gamma 核验或单位客户重构，因此只能作为有限浮点发现记录，不能推出固定策略的全锥定理、一般安全聚合或六人 half。
