# 异步公屏与一键工作程序验证

本轮验证对象为 schema 3 公屏和自包含 tools/work.py。数学目标 WC-TARGET v1 仍为 OPEN。

## 本地验证

执行：`python -m unittest discover -s research/weighted_congestion_frontier/tests -p 'test_*.py'`。

| 测试文件 | 通过项目 |
| --- | ---: |
| tests/test_board.py | 24 |
| tests/test_board_entry.py | 5 |
| tests/test_checkpoint.py | 22 |
| tests/test_work.py | 14 |

全部 65 项通过。

测试使用隔离的真实 bare Git 与独立 clone，覆盖同题并发消息全部接受、稳定 ID 去重、异步回复、冻结资产、断网重试、丢失确认、显式旧树迁移及迁移期间新消息保全。统一入口覆盖空目录恢复、角色号 001、凭据与程序路径含空格、普通 0644 上传程序认证、已暂存/未暂存/未跟踪文件保留、真实冲突完整备份、冲突后再次同步阻断和共享提交锁。

独立审查补充实跑了程序文件名含单引号、未跟踪文件与远端同名的恢复边界。发现的上传程序认证与参数转发问题已修正。

根 build_map.py --check、build_crosswalk.py --check、check_assets.py 与 git diff --check 通过。MODEL.md、CLAIMS.md 的精确数学身份未修改。

## 远端部署

实施修订已推送至 `main@0d92a5f7d69f4b9eae535b21981f00b331f2741f`，程序重新 fetch 核对 checkpoint 可从远端抵达。

正式 `wcg/board` 已普通快进迁移至 `152824baa601ca38576aeebaaa9daa873ac97122`；metadata 为 schema 3，迁移后消息流为空。原有当前公屏的事件、认领、成员登记和部署测试文件已清除。

真实收发验收在临时分支 `wcg/validation-1ff9423dc93b` 上执行 `tools/live_smoke.py --branch <临时分支> --live`：两个独立 clone 的同题消息均发布成功，跨 clone 同 ID 重试没有重复，延迟回复和冻结资产核验通过。验收后的四条消息 ID 为 `ef21a01e0db54dfa8e449f164bc78a9b`、`f1e43ddef75e407cacaaca7239b09ca8`、`de36388b672942778c2686104ec10626`、`3aa503beddfa4e9ebb605082fdd4a12e`；该测试分支已删除，正式公屏没有测试消息。

另以普通 0644 的独立上传 `work.py`，从空目录对真实仓库执行 start：自动克隆、固定角色号、配置外部凭据并读取正式公屏。之后无需重复给凭据执行 checkpoint，远端确认成功且没有制造空提交；冻结版本为 `0d92a5f7d69f4b9eae535b21981f00b331f2741f`。该次临时工作分支亦已删除。

上述检查针对运行程序与消息传输；数学研究成功仍按 ACCEPTANCE.md 判断。
