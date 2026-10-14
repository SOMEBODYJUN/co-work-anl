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

实施提交和迁移后的真实远端验证将在完成后记录。当前公屏的旧部署测试与控制记录由显式迁移删除；新收发测试使用临时分支，结束后清理。
