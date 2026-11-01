# 来源 0179ef4dff41dd5df619 清洗复核

## 冻结来源

- 路径：`research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/new_potential_global/README.md`
- 来源提交：`68fad804ec5946cb296f77dc5b336308a66abf12`；`main` 的 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c` 为同字节来源
- SHA-256：`75238c50b1c6f48940275140f988d544011b3a0917bff83ea44f562f574fdc64`
- 大小：1693 字节

通过 `work.py clean show` 实读 README，并全文读取同目录原稿 `causal_attraction_and_hierarchical_potential.md`（源 ID `a2435072e35b12e57366`，9426 字节，SHA-256 `718101d908a54343ca95c621ac21b965fb39557c701ecc2c15008e1d5beedd8f`）。

## 数学内容和边界

README 是导航/状态摘要，保留原模型：有限单位客户、有限非空共同目录、提供者观察完整有序历史、完整历史纯 SPE、任意离轨平局；明确六人 Q-CAG-HALF 仍开放。它概括原稿中的单客户协方差与插入恒等式、只假定 `0≤K≤r−1` 的尖锐坐标松弛包络、全树真实 IC 展开但仍有删除余项、平稳流只给边际而缺联合历史一致性，以及 `m=5,b=0` 的压力值 `q*=12/25`、`E_max=24/125>0`。

这些量的正确解释是：松弛坐标模型允许正的局部查询亏空，但没有给出共同目录/同一策略下的实现；全树势展开没有消除共同付款或高阶历史一致性；局部 `C^+≤D` 已知为假不自动否定较弱桥或主 half 命题；没有五人或六人 SPE 反例，也没有一般不可能性证明。README 不含新增定义、推导、数据、程序输出或独立审计。

## 全仓比较

同目录原稿的全部数学承重内容已收录于：

`archives/customer-attraction/state/引理/因果吸引亏空的单客户锐包络--引理.md`

该对象保留定义域、量词、(2)–(11) 的推导、松弛锐性和端点、压力代入、SPE/松弛停止线、后续银行/末位/平稳对象的比较及证据入口。相关证据在 `archives/customer-attraction/tools/evidence/r105-causal/`。本次还核对了现行五人半覆盖定理、末位去相关、完整终局信用/协方差、完整后继替换、银行根菜单反例和中间平稳障碍，均无 README 独有数学内容。

README 的独有用途是冻结工作区导航与“非证明/非反例”边界；这类元数据已由正式引理的 `source_refs`、状态和接续段落吸收。不存在应新增的数学对象、程序或关系边。

## 处置

建议 `duplicate`，目标为上述正式引理。理由是该 README 的每个数学主张都能在同一冻结版本原稿和正式引理中定位，没有独有假设、量词、证明步骤、实验输入或输出；保留原 README 作为冻结来源即可，不再复制一份对象。此结论不把历史 OPEN 摘要升级为主问题结论。

本代理没有执行 Git 写入、checkpoint 或 done；Boss7 应在目标正式引理已确认 pushed 后串行登记该源的 receipt/done。
