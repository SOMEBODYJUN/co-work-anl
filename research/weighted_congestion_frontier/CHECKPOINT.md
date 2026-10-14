# 直接保存阶段成果

首次以 `work.py start` 固定角色号与当前会话凭据路径，之后直接保存：

```sh
python3 /本地程序/work.py --repo /本地目录/co-work-anl checkpoint
```

仓库内等价入口：

```sh
bash research/weighted_congestion_frontier/tools/work.sh checkpoint
```

用户已授权研究资产的日常保存。文件有真实可复用增量、身份与证据层级准确、对应核验完成时立即执行。候选、精确障碍、反例与失败回收都可以按实际层级保存。

## 范围和标题

默认保存 `research/weighted_congestion_frontier/` 的当前工作树。其他路径一起列入：

```sh
python3 /本地程序/work.py --repo /本地目录/co-work-anl checkpoint research/weighted_congestion_frontier README.md RESEARCH_STATE.md -m 'C1：保存精确边界与仍待证明的比较'
```

路径相对仓库根，带空格时加引号。工具检查已暂存文件的范围，重新暂存范围内的当前内容，并记录删除。

## 程序完成的操作

程序串行执行本 clone 的 Git 写入：核对分支和文件范围，检查 diff，`git add`，有变化时 commit，普通 push，再读取远端确认 checkpoint 可达。结果 JSON 给出 `status: pushed`、branch、commit、remote_tip、files 与 assets。

每个仍存在的修改文件都有冻结 commit、SHA-256 和 `descriptor` 路径；删除项列在 files。回执与 descriptor 放在 Git 的本地缓存。用所需文件的 descriptor 分享成果：

```sh
python3 /本地程序/work.py --repo /本地目录/co-work-anl send --text '这个引理已保存，剩余义务是……' --asset-json /checkpoint/返回的文件descriptor.json
```

首次凭据配置详见 RUNBOOK.md。后续保存、公屏和同步共用同一外部凭据路径与角色号。

## 重试与冲突

重复执行会恢复已有 checkpoint 的推送，空改动保持原提交。远端有可安全合入的修改时自动同步再推送；具体冲突时保留本地成果并列出受影响文件，处理后重跑同一命令。程序只有在远端确认成功后返回 `status: pushed`。

每个独立对话使用专属工作目录和分支；共享目录的 Git 写入由一个入口串行处理。checkpoint 保存研究资产，公屏由 `send` 更新。

## 对应核验

数学文件运行相应精确核验，协作程序修改运行对应 tests。重要数学状态提升依据 ACCEPTANCE.md 的证明与独立攻击；普通 checkpoint 按当前证据层级完成保存。正式交付运行根地图、来源映射和资产检查。
