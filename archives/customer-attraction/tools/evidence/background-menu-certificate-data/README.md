# 背景菜单证书的数据合同与精确账

对象正文是[背景菜单的有限证书](../../../state/计算/背景菜单的有限证书--计算.md)。主源 `b9595537628e7f8219f5` 的[完整原表](original/background_menu_certificate.json)为186B；`slacks`实际保存四个非负行乘子，不是游戏中测量的IC余量。原生成器由[配套程序对象](../../../state/程序/背景菜单的有限证书程序--程序.md)保存，本包不再复制。

本包从客户均分收益独立重构全部39个候选IC列和384个fresh/p1/slope系数行。四个非零乘子是floor_B=1/2、floor_H=1、last_B_A_T=last_B_A_S=1；余项80零、304正，最小0。48个有效余项类各在完整八位表中出现8次。384行包含斜率，不能说成384个游戏、完整SPE或背景长度。

## 文件与执行分工

| 文件 | 作用 |
| --- | --- |
| [original/background_menu_certificate.json](original/background_menu_certificate.json) | 冻结成功报告，五字段全部保留 |
| [audit_certificate.py](audit_certificate.py) | 本轮独立标准库有理审计，从真实终局分母构造39条IC，不导入原模块、不运行原helper或LP |
| [exact-audit.json](exact-audit.json) | 实际独立运行输出：14976个系数、384个余项、48有效类、全部乘子、符号接口和限制 |
| [case-ledger.json](case-ledger.json) | 每个case的八位会员编码、类别、target、完整39系数、四活跃项、加权和与余项 |
| [related/workspace-README.md](related/workspace-README.md) | 已全文读过的1744B原工作区路线图，仅供来源和开放状态比较 |
| [source-manifest.json](source-manifest.json) | 主源与共享程序原件、唯一原事件、比较材料及独立核查来源绑定 |
| [check_package.py](check_package.py) | 仅核保存记录的一致性、来源指纹、本地链接和回执；不重跑数学审计或发现入口 |
| [self-check.json](self-check.json) | 当前静态收尾结果和文件指纹；不冒充原程序输出 |

原main的唯一一次重新执行由程序任务完成，见[共享执行事件](../background-menu-certificate-program/replay/execution.json)：0.87286651秒，exit0、stderr0，1次原main与1次LP，新JSON及stdout均与冻结原表逐字相同。本数据任务没有再次执行该入口。当前独立审计的首次执行成功，原import/helper/main及LP计数均为0；其输出已原样保存。报告中的输入路径保留实际运行时位置，正式对应文件的SHA和路径另在manifest绑定。

如未来输入发生变化而需要重做独立核查，可以从本目录执行下述命令；这是复用接口，不是本轮新增执行记录：

```sh
python -B audit_certificate.py --source ../background-menu-certificate-program/original/background_menu_certificate.py --output /absolute/scratch/new-background-menu-audit
```

## 可接续结论与不能省略的条件

固定有限单位客户共同目录游戏的一份完整历史纯SPE。合法背景前缀H重复L≥1次、随后恰余两人，实际尾主题A、B，新增覆盖Δ、两尾利润P。对任意合法比较T、S，四条真实IC与逐客户非负余项给出

\[
P+\Delta-|\,(T\cup S)\setminus H\,|
=\tfrac12 C_B+C_H+L_T+L_S+\sum_x\rho_x/[(p_x+1)(p_x+2)]\ge0.
\]

fresh余项为 `a*((1-t)*(1-s)+t*s)+(1-a)*(b/2+2*t*s)`；旧p=1余项为 `(1-b)*(2-3*a/2)+(t+s)*(3-a)`；旧斜率为 `1-(a+b)/2+t+s`。旧全p余项等于p=1项加(p−1)倍斜率，故全整数p≥1非负由显式代数证明得到，不靠有限扫描外推。若前缀已覆盖并集恰等于一道合法题H，各旧客户的p可以不同；这是正文单列的符号推论，不是原CLI的额外输入范围。

不能删去H的合法目录身份。52客户完整SPE的实际前缀已有P=17、Δ=0、freshOPT₂=18，一般前缀预算已被否定；该例旧覆盖并集34客户不属于六题目录。也没有认证乘子和最优、四项支持最少、所有会员位同属一份可实现策略、三人以上尾局或一般根half。有限系数核查、无界背景参数的条件恒等式、原LP发现和完整SPE反例各有不同的量词。
