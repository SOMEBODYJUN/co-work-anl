# 笔记工作启动词

本次做笔记识读与工作存档，身份 Boss【填编号】，RUN【填唯一ID】。

我授权你使用本次提供的 githubtoken.txt 对 SOMEBODYJUN/co-work-anl 认证，自行克隆、同步、修改本次笔记工作文件、提交并推送 `work/notes`。凭据只通过仓库外 `--token-file` 使用，禁止输出或提交内容。

使用 `work/notes` 分支的 work.py。已有附件时使用实际路径；否则从 https://raw.githubusercontent.com/SOMEBODYJUN/co-work-anl/work/notes/work.py 取得。执行：

```sh
python <本分支work.py路径> --repo <本Boss独立目录> start --actor BossN --token-file <仓库外凭据路径>
```

进入返回的 clone，只用其根 work.py。阅读 AGENTS.md、START-HERE.md 和 prompts/coordinator-prompt.md，实际检查视觉与子代理能力，运行工具自检。新工作执行 `python work.py notes init RUN`；接续执行 `python work.py notes status RUN`。

只处理本次提供的原稿、旧稿和明确授权的材料。核对课次与页段，原图独立初读后再比较旧稿。原件只读，保留全部有效内容、重复证明和原留白；每份输出保真转写与学习稿，保存疑点、来源映射、真实逐区观察与独立复核记录。最多同时三个笔记任务，每个新审阅者只处理分配的一份，不递归派生；作者不能审自己的稿。锁定版本连续三轮全量独立复核，任何实质修改后重新计数。

主代理统一整合，串行执行 `python work.py checkpoint <实际原件/工作/输出路径> -m "本轮识读及断点"`。确认 `pushed` 才算远端已存；暂时无法推送用 `--local-only` 保全。及时更新本 RUN 检查点，真实中断保存准确页区与下一动作。缺少原稿时保持等待输入；不能把程序自检或样例算作用户笔记已完成。
