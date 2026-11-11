# 真最大根270行：精确根线和v6定量缺口

Boss1；RUN `six-boss1-20261111`。本轮一次LP发现后，已用纯有理线性代数得到匹配原始/原未缩放对偶，并用独立字面checker核完整270行、129列及自由K/O的131列恒等式。

普遍根线为

\[
\boxed{16877573861922720u\ge1767904008200582K+337340181272013O.}
\]

这里u是actual根收益，K是全目录最大裸大小；取真正最大合法C并沿同一完整策略的真实分支。正对偶不使用OPT并集帽，因此O允许任意六个合法查询标签的覆盖并。空覆盖、同覆盖异标签、重复行动、任意弱平局、零客户和全部128型均保留。

指定 `K=87254934961879537539921985657780687995/449980920529477462633417363589807278334`、O=1时，该270行必要锥的精确最优根收益为

`607251973322914948830755482094789247557599475346983/15068623457722685512542318581642800231287811506822120`

即0.04029910064623041…，比v6精确点actual根收益高

`1580874673362541092769542716418280918504570717094/4395015175169116607824842919645816734125611689489785`

即0.00035969720475463666…。正权预算为原ROOT_IC、五CAP、SAFE6(Omean)、PAIR30、C30，以及P25真实source4的T=B6/Q=Omean。后者K成本必须作为独立参数恢复。

完整论证和证据：

- [proof.md](maximal_root_tail_wallet_v3/proof.md)：预算定义、来源、十权整数恒等式、匹配点及准确范围。
- [source_review.md](maximal_root_tail_wallet_v3/source_review.md)：求解前实读来源、完整模型、任意历史及菜单量词。
- [exact_input.json](maximal_root_tail_wallet_v3/exact_input.json)：保旧72参数行与顺序，追加PAIR30、C30及196 P25；SHA `01c57b65a82b682d222cb449407416c4db0de60961c90d6eaafd35d15b1f79d0`。
- [exact_certificate.json](maximal_root_tail_wallet_v3/exact_certificate.json)：精确匹配点、全270原slack、原未缩放对偶、全部129余项与131列身份；SHA `b7d27bcddc6da34bed635bf7c36a607ffea130b56bcb0f62803b94b3c20dc925`。
- [literal_input_check.json](maximal_root_tail_wallet_v3/literal_input_check.json)、[literal_certificate_check.json](maximal_root_tail_wallet_v3/literal_certificate_check.json)：独立全域重建与原始/对偶检查。
- [all_129_column_checks.tsv](maximal_root_tail_wallet_v3/all_129_column_checks.tsv)：全部零型和非零型的精确质量及余项。

此次匹配点仅证明指定必要锥的最优性，不是完整SPE、根锐性或half证明；未重跑751行phase-I，未改旧包、Git、RUN或registry，没有下一次优化。
