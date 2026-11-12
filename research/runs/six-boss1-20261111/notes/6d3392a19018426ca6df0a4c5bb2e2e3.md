# 第一源 λ 扩展：准确闭合，没有新行

Boss1；`six-boss1-20261111`；实际 agent `/root/source1_lambda_complete`。

第一源在 `q₀=1/6,1/5` 下的完整 `[0,25]` 锚域分别具有19个不可冗余facet和90个顶点。换元 `s=25−λ` 后，分别与旧 `all_source_minimal_cap_safe` 和 `ordered_minimal_cap` 的完整根域、全部原尺度行严格相同。

真实 λ 下界分别为5/3和2；根六个双缺面全部必需，准确负例余项仍为−1/192。λ=25保留双全中间锚。Ordered 的 d=1 在整个连续域是唯一最弱正重数。

按 Main 更新后的范围，不物化900条重复raw。保留全部两套90顶点映射、每套全部32尾态、全部513列符号身份，415530个原行列身份和46170个C-only自由等式列身份。新增不等式信息为零。

- [完整正文](source1_lambda_complete/proof.md)
- [完整域及顶点](source1_lambda_complete/parameter_domains.json)
- [全部顶点坐标对应](source1_lambda_complete/endpoint_table.md)
- [独立精确检查](source1_lambda_complete/literal_checker_output.json)
- [独立解析审查](source1_lambda_complete/analytic_review.md)
- [冻结身份](source1_lambda_complete/freeze_manifest.json)

零优化器；不读取全局LP文件，不改旧包、Git、RUN或registry。后续若继续第一源，需要改变真实预算、帽或锚；单纯λ重参数化已无新增行。
