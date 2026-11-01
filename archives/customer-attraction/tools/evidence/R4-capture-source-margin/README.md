# R4捕获占用与源边际的读域及证据

主源ID `ac49b69fee20f160638e`，路径
`research/workspaces/customer-attraction/R-4ffa8b85fa8847e09e45dcafc8e1326f/transport/capture_occupation_and_source_margin.md`。
两冻结提交为`68fad804ec5946cb296f77dc5b336308a66abf12`与`aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`，内容相同；4134B、SHA-256
`645591887ff6f022c31ea113d85c220ba57bb2e063aee64d439abf16064b455f`。

主源先由`python3 work.py clean show ac49b69fee20f160638e`完整读出，再由同一reader的`--out`导出[冻结原件](capture_occupation_and_source_margin.md)。[读域清单](reading-manifest.json)给9份实际全文读过的冻结MD完整路径、双来源和SHA，以及10份当前正式比较正文的读时SHA。未以检索摘要代替阅读。已完整读根规则和清洗对象/回执合同；本目录不记录凭据、claim或远端写入。

## 实际相关比较

以下冻结Markdown均用`work.py clean show`完整实读；它们是比较材料，本子任务没有认领或完成登记它们。

| ID | 冻结源与本次作用 |
|---|---|
| `ecfa37ee3f376ed273ef` | 同R4工作区`parent/capture_visit_extremum_review.md`：原稿VISIT/SQRT之后补精确达到和根号首项常数一；不倒算成主源原有内容。 |
| `0877495ebcf66e60c973` | 同R4工作区`transport/README.md`：核本条与BG子件的研究范围和历史身份。 |
| `c5363fdb5df8ef8bc699` | R-cd789…/round3/mixed/owner_credit_routing.md：同客户I信用、旧背景份与common whole-IC系数缺口。 |
| `0b3270699560d37bdd32` | R-cd789…/round3/credible/increasing_role_capture_flow.md：actual-prefix真查询、严格future守恒、总吸收标量化与行容量未证。 |
| `efef49e0cb43c7636983` | R-cd789…/round3/mixed/capture_hitting_capacity.md：HIT是曾命中、非总访问，非owner单行半系数及同rho范围。 |
| `2cbfcd673b188e626a02` | R-cd789…/round3/GENERAL_PROOF_WORKING.md：全角色Hall取消、同时局部delta、SOURCE-NET二分及incoming余额合同。 |
| `55b8d5e52a95ea9babf6` | R-cd789…/round4/shared/net_dynamic_rank.md：共同取消的rank/greedy/TOTAL/NET-DUAL及局部delta不可混用，最终动态cut未付。 |
| `5ae96692ee0a89f52e98` | R-cd789…/round5/rank/incoming_density_diagonal_ledger.md：完整原IC密度账、全父M−H、captured自然重分配后补合同和自由trim区别；未得普遍总价。 |

另全文实读并比较当前正式对象（只声明读这些正文，没有冒称重新导出其所有primary或重跑证书）：

- `state/定义/共同目录完整历史模型--定义.md`：完整历史、合法背景、真实后继与全部离轨平局。
- `state/引理/等分递增吸收链的精确访问极值与根号锐阶--引理.md`：本对象不再复制精确达到及渐近证明；补清递推非减性的非循环归纳。
- `state/定理/实际取消的同时源付款与入流余额--定理.md`和`state/候选/真实查询自由指派与残源净钱包的共同接口--候选.md`：同一实际G/eta、SOURCE-NET、IN-NET充分性而非等价。
- `state/定理/递增等份捕获的角色命中与残源协方差界--定理.md`：HIT集合量词及后来重分配不自动继承等份界。
- `state/定理/自然重分配的入密度共同对角账--定理.md`和`state/审查/自然入流余额的作者版本与资金合同史--审查.md`：后续共同账已证内容、后补路由范围与尚未付的T/COV。
- `state/引理/分数源匹配的同时初始化容量与未付入流--引理.md`：源平均只付初始化，不能再领第二份W。
- `state/资源/背景半利润合同与R4ffa根账本的真实边界--资源.md`：根稿历史BG候选与访问工具独立。
- `state/反例/实际前缀的剩余利润与新增覆盖--反例.md`：52客户、四人完整259节点根SPE的AB实际前缀，17<18且新增覆盖0，更新BG历史状态；没有重跑其1554项IC。

全仓当前正式正文及已保原件按SRC-MARGIN、VISIT、源费用、source/incoming和原文件名检索；冻结inventory按完整R4路径及round3/round4/round5相关名字定位，再读上述实际内容。一次`clean search`给空匹配，未把它写成冻结全仓全文扫描成功。

## 本次算术复核和未执行事项

`python3 archives/customer-attraction/tools/evidence/R4-capture-source-margin/check_visit_arithmetic.py`
以标准库Fraction重算VISIT前四值、最大化d及四角色图的续值、10/9与13/12的差1/36，并分开算曾命中2/3；同时核原件字节及SHA。[结果](arithmetic-check.json)为一次实际运行输出。它只核有限算术，不证明全k递推上界或SPE实现；普遍性由正式[审查正文](../../../state/审查/R4捕获占用与源边际运输式--审查.md)的代数和归纳承担。

没有新游戏、搜索、LP、IC扫描、BG反例重跑、一般half或新颖性认证。关系判断在正文末尾给出，三级超图留第三阶段。所有文件当前由父Boss串行保存和登记；本子任务未执行commit、push、checkpoint或clean done。
