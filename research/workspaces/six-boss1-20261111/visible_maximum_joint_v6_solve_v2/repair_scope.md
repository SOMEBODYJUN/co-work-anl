# 修复范围及验收边界

- 原始问题是source_pins固定JSON接口不同，不是缺少来源或数学求解失败。
- 原 `visible_maximum_joint_v6_solve` 的contract、scaffold manifest、input和Main release均未修改；新的失败冻结manifest只是新增不可变回执。
- 新目录原样复制9core。逐行patch只修复严格source-pin接口、增加新release身份门槛、显式绑定X语义更正，以及支持Main授权的0优化repair加载和如实静态记录。
- 原始 `exact_input.json` SHA保持 `8f953bca6b65a8093d5fcf0fdb5a432ba3603137fe1015cd06fc8f6324e68769`；source_pins SHA保持 `d90e383c1824ea5b3eebb8fbe93b9c53c6a071bb72684740f25f28492c6a5fc0`。
- 14个纯parser拒绝用例覆盖unknown/missing/duplicate/path/SHA/bytes/extra/order；实际全部44文件的内容及大小由独立的完整repair load路径逐项验证。
- 零优化repair读取不算Main新release。新模板authorizer为空、optimizer_calls_authorized=0，新目录不含main_release.json。
- 最终按Main要求交付逐行patch、新9core hashes、新静态检查、全输入repair报告和新scaffold manifest后停止写入，等Main审核并另发原额度唯一一次LP许可。
