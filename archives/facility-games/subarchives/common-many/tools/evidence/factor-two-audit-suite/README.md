# 因子二核心构造与三类审计的固定复现入口

本目录服务于[有限构造算法](../../../state/算法/站点字典序搜索与完整续局有限构造--算法.md)及[三类验证职责](../../../state/计算/因子二构造审计与交付检查的验证边界--计算.md)。source 下保留本批全文清洗的六份冻结原字节源码：包说明、CLI、构造核心，以及构造审计、布局障碍审计和交付检查。各文件来源和指纹见 [source_provenance.json](source_provenance.json)；未改写源程序以适配新路径。

## 依赖范围与已完成的重建

[snapshot_manifest.json](snapshot_manifest.json) 固定提交 68fad804ec5946cb296f77dc5b336308a66abf12 中的19个文件，逐项列出原相对路径、清点源ID、SHA-256及字节数：

| 类型 | 文件数 | 用途 |
| --- | ---: | --- |
| Python程序 | 8 | 三核心及五个检查/审计模块 |
| 保存证书 | 4 | growing-k-12、heavy-three-sites、orphan-overlap、rational 的历史lexmax输出 |
| 示例输入 | 4 | 与四证书对应的规范JSON实例 |
| 冻结审计输出 | 3 | exact、reverse、lexmax-barrier 的全内容比较基准 |

这是依赖闭合的**核心审计快照**，共1,306,048字节，并非完整当前冻结仓库。它支持默认lexmax CLI和manifest列出的三项审计入口；不支持另两种CLI方法所需的greedy/equal-flow实现。交付脚本按目录glob扫描，因此在本树中是8程序和4证书；在增添其他模块/证书的树中运行将具有不同检查范围。

本批实际执行了 [reconstruct_snapshot.py](reconstruct_snapshot.py)，成功形成全部19文件的原相对路径树，并逐文件核对长度与SHA-256；[reconstruction_check.json](reconstruction_check.json)记录此次实测。该辅助程序只调用根 work.py clean show 导出，再核固定指纹。它不运行这些程序，不执行认领、done、提交或推送；目标已有相同字节可复用，已有不同字节则拒绝覆盖。源读取仍需本结果仓库的冻结清点及正常读取权限，首次取回未缓存源可能访问网络。

从结果仓库根执行：

~~~sh
python3 archives/facility-games/subarchives/common-many/tools/evidence/factor-two-audit-suite/reconstruct_snapshot.py --work-py work.py --destination cleanup/workspaces/reproduce-facility-core
~~~

该目录形成后，可按需运行：

~~~sh
python3 cleanup/workspaces/reproduce-facility-core/tests/multi_facility/run_exact_audit.py --output /tmp/facility_exact_new.json
python3 cleanup/workspaces/reproduce-facility-core/tests/multi_facility/run_lexmax_barrier_audit.py --output /tmp/facility_barrier_new.json
python3 cleanup/workspaces/reproduce-facility-core/tests/multi_facility/verify_delivery.py --output /tmp/facility_delivery_new.json
python3 -m multi_facility_spe --help
~~~

前三项使用脚本原位置定位依赖；最后一项CLI须在重建根目录运行，或把重建根加入PYTHONPATH。实际生成证书可在重建根运行：

~~~sh
python3 -m multi_facility_spe examples/multi_facility/rational.json --output /tmp/facility_rational_new.json
~~~

均应使用普通Python模式，不能以 -O 关闭承重assert。exact的输出会覆盖指定已有文件；barrier、delivery和CLI预先拒绝已有输出。请选新路径。delivery会自行运行三项审计，并真实求值小证书全部布局，不只是编译或检查文件是否存在。上述命令是可复现接口，不能当作本批全部执行日志。

## 本批实际执行和未执行的边界

本批首次运行布局障碍程序，使用这里的原字节脚本和已保留的原字节定义检查器、逆向枚举函数：

~~~sh
PYTHONPATH=archives/facility-games/subarchives/common-many/tools/evidence/factor-two-reverse-review python3 archives/facility-games/subarchives/common-many/tools/evidence/factor-two-audit-suite/source/tests/multi_facility/run_lexmax_barrier_audit.py --output archives/facility-games/subarchives/common-many/tools/evidence/factor-two-audit-suite/replayed_lexmax_barrier.json
~~~

这条是已执行命令；其输出已存在，原样再次运行会按程序设计拒绝覆盖。重跑时请另取输出文件名。

[replayed_lexmax_barrier.json](replayed_lexmax_barrier.json)包含20个参数实例、1552个坏/好布局实际偏离纯见证，另有6次全部标签字典序枚举。与manifest指定的原冻结barrier记录相比，仅Python版本从3.13.5变为3.12.14；其余整个JSON相等，见[barrier_replay_comparison.json](barrier_replay_comparison.json)。这验证给定纯见证及小域全局枚举；对任意混合在轨策略的下界仍来自数学证明。

本批未运行完整exact构造审计、整套delivery、CLI或原仓库回归。先前[逆向审计](../factor-two-reverse-review/README.md)的612输入实测继续复用，本批没有重复运行。重建19文件和核hash不等于执行数学审计，v2历史报告的旧依赖哈希也不替代当前版本验证。

## 来源处置边界

六份本批源码与此前已清洗的定义检查器、逆向程序共同组成八程序。manifest中的示例、保存证书及尚未逐源处置的大输出在这里仅为可核验的固定依赖；引用、导出和hash核验均不自动将其清点状态变为done。原reverse输出已有单独清洗回执，其实际证据和版本归属另见[历史审计资源](../factor-two-historical-audits/README.md)。
