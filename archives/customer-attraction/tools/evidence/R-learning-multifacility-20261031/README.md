# learning 与 equal-light-flow 清洗（2026-10-31）

四个源均用 `clean show --out` 完整导出，原始 stdout/stderr、冻结 SHA/大小与本地字节核对在 `clean-show/` 和 `source-manifest.json`。三个 Markdown 是内部教学/证明路线，`equal_light_flow.py` 是可运行的等权客户盒内选择器。

`equal_light_flow.py` 通过 `py_compile`，并以 `Fraction` 精确运行空网络、单客户、负 base 站点和不等权拒绝四个 harness。它验证：最小费用残余网络逐单位增广、整数容量、前缀槽、完整盒、home 不等式、原始选项精确 NE 与目标函数恒等式。代码明确拒绝一般异权；完整离轨续局仍是另一个有限程序。

三份教学稿互相对照：`01b_proof_map` 将双设施黄金比例路线与任意设施因子 2 路线分开；`05_tools` 给贪心预算、装箱、阈值截断/归位与等权流工具；`06_frontier` 明确旧贪心/势选择反例只否定指定选择规则，并把全输入位多项式构造列为开放问题。它们都声明仓内证明没有外部同行评审记录；本批不把教学叙述自动升级为本六人 CAG 定理。
