# 运行原版人物模拟链

先读仓库的 `docs/AUTHOR_CLONE_REQUIREMENTS.md` 和 `docs/AUTHOR_CLONE_SOURCE_AUDIT.md`。本目录不是已经完成的人物复刻成果；运行记录在 `research/author_clone/`。

源码为四个固定提交的完整子模块。不要把其中几个提示词抽出来后改写成另一套学习流程：

```sh
git submodule update --init --recursive tools/author_clone/upstream
python -m pip install --target .runtime/author-clone -r tools/author_clone/requirements.txt
```

`native_genagents.py` 只适配输入、生成接口和存储。实际记忆、重要性、检索、反思、人物回答、解析与状态存取来自 genagents。原版提示词未改写；忠实重建要求作为用户约束随每次调用传入。唯一的原生包装错误修复及向量接口更换已逐项披露。

## 输入与运行

原文属于用户附件，保存在数据包中，不随公开代码重复发布。将数据包解压到工作目录。用当前路径重新准备输入，不使用旧机器的绝对路径：

```sh
PYTHONPATH=.runtime/author-clone python tools/author_clone/native_genagents.py prepare \
  --archive /当前数据包/articles.zip --output /当前工作目录/author-inputs \
  --batch-chars 120000
```

`120000` 只是输入路由的字符预算示例，不是模型上下文容量声明，也不是固定篇数。正式派工前应计入原文、原版请求展开及响应余量；完整超长文章可独立分批。该命令只路由原文，`learned_article_count` 仍为零。不得把准备完成当作学习完成。

原生生成请求另有显式 `--prompt-char-budget` 执行预算（默认 150000 字符，同样不是模型容量声明）。展开超过预算时直接报告实际长度并停止，不删文字。全库合入时，原生检索默认取 120 个记忆，取回整篇长文可能超预算；必须实际解决输入粒度/检索容量后继续，不能仅凭两批运行宣布全库规模已验证。

可保留原版 OpenAI 向量接口（需已有有效 API 密钥）；本轮无密钥运行采用以下明确适配：

```sh
python tools/author_clone/download_bge.py /当前工作目录/bge-small-zh
```

模型文件下载完成后，BGE 运行路径会在进程级禁止联网，并关闭 ONNX Runtime 遥测；需要 Linux `libseccomp`。隔离无法生效时不启动该运行。生成仍通过本地文件请求由真实 Work 子代理承接，不在这个原生子进程中发网络请求。

每批由一个新子代理完整执行（本例仅说明参数，具体编号取实际批次）：

```sh
PYTHONPATH=.runtime/author-clone python tools/author_clone/native_genagents.py run-batch \
  --manifest /当前工作目录/author-inputs/manifest.json --ids 0036,0145,0202 \
  --output /当前工作目录/batches/batch-001 --model gpt-6-astra --mode formal \
  --bge-model-dir /当前工作目录/bge-small-zh \
  --anchor '这批原文中作者形成认识与判断的方式' \
  --question '依据本批材料，回答一个需要实际运用这些认识的新问题'
```

程序产生 `requests/*.request.json` 后等待模型。该批真实子代理读取完整原版 `native_prompt` 及用户忠实重建要求，按请求原版格式生成回答，把原版回答作为 JSON 字符串写入同名 `.response.json`：

```json
{"request_id":"请求中的真实ID","model":"gpt-6-astra","agent_id":"实际批次子代理ID","text":"原版要求的JSON回答字符串"}
```

循环承接新请求，直到进程成功退出并产生 `DONE`。不得用规则、虚构结果或预先写好的分数替代真实模型。记录中的模型字段本身不能证明平台实际用了该模型；主代理必须同时保存真实 `spawn_agent` 的模型配置和代理身份。

正式子代理模型为 `gpt-6-astra`、`reasoning_effort=max`；测试为 `gpt-6-sol`。每批换新代理。原文不删，原生 reflection 仍通过来源节点回到原文。批次的整个原生状态位于 `private/native_state/`，公开回执可与该状态核对。

`join-and-answer --states <多个原生状态目录> --output ... --model ... --mode ... --anchor ... --question ...` 只合入已有节点并继续原生反思和回答。其生成请求也由新的子代理承接。它不会把所有笔记扩写后塞进一份巨长文本。

## 交给 Pro 的任务

1. 恢复精确版本源码及原文；读取逐项要求、原始方法和真实进度。
2. 先核清采用项目怎样覆盖目标，保留其必经阶段。不要把本目录的 genagents 试运行称作已经复现 ThinkPersona 或 Second Me。
3. 按实际输入和上下文安排完整文章批次；正式学习每批新建 Astra Max 子代理，实际走完原版链并保存状态。当前的 Sol 测试不抵作正式全库学习。
4. 合入真实状态，实际用于新的分析和回答；回查来源。按用户要求比对学习是否忠实，不外查作者观点真假。
5. 对照全部要求继续补齐；全量作者学习、可反复使用的作者上下文、观点随时间变化、原文笔记本和实际回答效果均须有内容。某个目标尚未由所采用项目覆盖就明确保留为未完成，不能自行设计替代方法再沿用上游名称。
6. 只有真正完成的范围才更新完成状态。遇到不可执行的上游必经步骤，保存精确断点与具体原因；不要删掉步骤、伪造运行，或在提示词里宣称已经克隆。

本目录给出可继续执行的原生调用入口，不提供“Pro 一定不犯错”的保证。
