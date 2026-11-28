# 人物复刻项目：原始执行链与本轮采用范围

核对对象是完整源码，不以项目名称或介绍代替实现。精确版本及文件指纹见 `tools/author_clone/upstream.lock.json`；四个项目以固定提交的 Git 子模块保留，初始化后得到完整仓库。此处没有把四套方法拼成新的克隆算法。

## 原始方法

| 项目 | 原始正常处理链与源码入口 | 当前执行状态 |
|---|---|---|
| [genagents](https://github.com/StanfordHCI/genagents) | `GenerativeAgent` 创建或载入人物；`remember` 调重要性评分并保存 observation 与向量；`MemoryStream.retrieve` 按原生近期性/相关性/重要性取回记忆；`reflect` 基于取回记忆生成第一人称认识、评分、关联来源并入记忆；`utterance` 取回记忆、组装人物背景、按原版提示词生成回答；`save` 与构造器保存/重载人物状态。分类与数值问卷是其他交互分支，不是文章学习必经步骤。 | 本轮实际运行的是这条原生人物记忆与回答链，测试结果单独记录。它的既有研究适用范围不能被扩张成已经证明能完整复制经济作者。 |
| [ThinkPersona](https://github.com/Hualeez/ThinkPersona) | `datapro.py`：重写输入、语义分块、背景摘要、六支属性/认识/决策/关系/事件三元组提取、图连接扩展与结构调整、向量编码、Neo4j 图保存；`dataproAndqar.py`：由本地 interviewer 与图增强 `inferenceChain` 产生 QRA；`models/thinkpersona-7B/training_args.yaml`：LLaMA-Factory LoRA 训练；`thinkpersona_inference.py`：载入基础模型及适配器推理。 | 保留整套源码；发现两脚本共四个未闭合路径字符串，提供仅修字符串的补丁。未运行 QRA 全链及 LoRA 训练，未将摘出的模板冒充完整复现。 |
| [Second Me](https://github.com/mindverse/Second-Me) | 原生 `ProcessStep.get_ordered_steps()` 共 14 步，见下文。入口 `TrainProcessService.start_process`。L0/L1/L2、记忆综合、合成训练数据、训练、权重合并与模型转换均有实际代码。 | 保留整套源码；本轮没有执行其本地训练，没有 Second Me 模型产物。不能跳过后半段却声称完成其克隆方法。 |
| [TwinBench](https://github.com/TwinVoice/TwinBench) | `twinvoice.evaluate` 及 discriminative/generative 子模块。三种人格场景；区分式选择或生成后评分。观点一致、记忆、逻辑与语言表现是复刻相似性的评价维度。 | 它是评测项目，不承担从 1508 篇文章训练人物。未把它称为学习引擎，也没有把模型是否同意作者当作评测目标。 |

Second Me 原生顺序（直接取自枚举，未自行改排）：

1. `model_download`
2. `list_documents`
3. `generate_document_embeddings`
4. `process_chunks`
5. `chunk_embedding`
6. `extract_dimensional_topics`
7. `generate_biography`
8. `map_your_entity_network`
9. `decode_preference_patterns`
10. `reinforce_identity`
11. `augment_content_retention`
12. `train`
13. `merge_weights`
14. `convert_model`

这里没有宣布某个项目“最好”，也没有认为四个项目能保证复制所有人的思想。原生记忆链能实际承接 Work 子代理的生成调用，是本轮执行它的具体理由；它与其他完整训练路线的能力差异继续保留为未完成事项。

## 本轮适配边界

| 适配 | 实际内容 | 没有改写的原生部分 |
|---|---|---|
| 文章输入 | 完整 Markdown 作为人物 observation，标题、日期、编号随原文保存；全公众号作为一个学习对象。 | 原生 `remember`、重要性生成、节点和向量写入。 |
| 生成接口 | 原版 `gpt_request` 的真实请求进入文件队列，由该批新 Work 子代理逐次回答；请求、响应、实际代理身份留存。每次带上用户忠实重建要求。 | 原版模板、占位展开、JSON 解析、重要性/反思/回答调用链。 |
| 向量接口 | 无 OpenAI API 密钥的测试显式采用固定版本 BGE 中文神经编码器及 ONNX Runtime；长输入以编码窗口覆盖全文。 | 原生余弦相关性、三项评分、排序、节点取回。该适配不等同于原版 OpenAI 向量，不能报作严格同模型复现。 |
| 上游错误修复 | genagents 的 `GenerativeAgent.reflect(anchor,time_step)` 原版将第二位置参数误传成 `reflection_count`；适配层仅改为关键字传入 `time_step`。 | 原生 `MemoryStream.reflect` 的检索、生成、评分、来源关联与保存全部直接执行。 |
| 批次汇入 | 读取各批原生状态，只重编号节点并对应重映射来源指针，原文、认识、分数和向量保留；再用原生 `reflect/utterance/save`。 | 没有添加另一套跨批提炼或层级归纳算法。 |

原生源码在执行前按固定指纹核对。代码存在、导入成功、模型请求成功、整条链完成、人物复刻效果合格，是不同状态，不能相互替代。

## 实际边界

当前环境没有 OpenAI API 密钥、PyTorch/Transformers 训练栈或 NVIDIA GPU。genagents 的生成接口已由真实 Work 子代理承接，向量接口适配已明确记录；ThinkPersona 与 Second Me 的完整本地训练没有实际发生。不能通过修改状态文件把这些缺口写成完成。

1508 篇的完整正式学习和符合用户全部目标的作者复刻仍未完成。本轮结果只据实记为原生链的真实文章运行和跨批使用。用户要求中的思维、逻辑、观点、价值取舍和语调须在实际回答中进一步比对，不能由链路成功退出推定。
