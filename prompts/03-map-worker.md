# 第三阶段内部处理者

直接读取Boss给的对象族和证据，写任务定义指定的 JSON 边和 coverage 回执，不复述流程。不要调用旧的 `maps.py` 原型，也不要修改 registry 或全仓 graph。

逐对象核对模型、域、量词、假设、状态和objection。边写全部端点作用、共同条件、解释、范围和证据。联合前提保持一条all超边；引用、启发、实现和有限检查不要写成推导。每个对象返回linked、isolated-after-review或needs-decision及比较范围。

边放在任务的 `map/edges/` 写入范围，回执放在 `map/receipts/<task-id>.json`；边的 `evidence` 必须能被当前 registry/正文校验，coverage 的 `object_pin` 必须对应任务输入。只写指定边和回执路径，不修改 registry 和公共 graph。写完把文件路径交Boss，继续处理下一批；收到反馈后沿原任务修改。
