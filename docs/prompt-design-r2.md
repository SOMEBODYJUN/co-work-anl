# 笔记工作提示词 R2

目标是让执行者从输入原稿走到两份完整成稿，并能马上判断当前该做哪一步。

## 采用的写法

- 开头直接给成果：保真转写和可复习学习稿，随后给当前开工动作。
- 把泛泛的禁止改成处理办法：疑字列候选、数学检验、回图比较；未决项触发模型自己的高分辨率恢复循环，不转成人工任务，也不调用 `notes block`。
- 启动词负责开工，总协调词负责阶段推进，单份词负责角色交付，工具合同负责台账字段。
- 以具体成果驱动推进：写完整数学单元，保存，修订，验收，再接下一份。异常按实际影响安排工作。只有缺页、损坏原件或视觉工具不可用才阻塞，内容疑点继续自动恢复。
- 保留用户的完整内容、原序/学习双正文、颜色约定、两遍页区检查、新身份独立复核、三轮同快照和修改后重计规则。

## 参考

- [OpenAI：提示词编写实践](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-the-openai-api)：清楚说明任务、输出和格式，用应做的具体行动替代单纯禁止。
- [OpenAI：推理模型提示实践](https://developers.openai.com/api/docs/guides/reasoning-best-practices)：简洁直接、明确目标和成功标准，用清晰分隔组织上下文。
- [OpenAI：任务结果与停止条件](https://github.com/openai/skills/blob/main/skills/.system/openai-docs/references/prompting-guide.md)：明确目标、约束、上下文与停止条件，为判断提供决策规则。

## 核对

命令已对照实际 work.py 的 CLI；新认领、接续、容量已满、当前批次未结束、真实阻塞后推进等情形已用实际队列状态转移函数核对。来源、待办、程序和技能保持原版本。本次是提示词与执行程序的一致性检查，不是模型效果 A/B 测试。结果见 `validation/prompt-r2-check.json`。

正式入口 `prompts/launch-prompt.md` 与单独交付的 `prompts/notes-pro-launch-r3.md` 内容一致。
