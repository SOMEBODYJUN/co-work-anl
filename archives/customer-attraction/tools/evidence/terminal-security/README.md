# 末两主题与静态安全值：精确证据

对应[计算对象](../../../state/计算/末两主题条件与安全值代换的精确核验--计算.md)。`original/`按冻结来源原路径保留三个本批代码/证书来源与五个已处置的规范依赖；文件身份和SHA256在[PROVENANCE.json](PROVENANCE.json)。`replay/`是本轮实际运行结果，原证书不被重写。

## 固定四客户的独立全历史检查

从仓库根运行，结果输出到stdout：

~~~bash
python3 -B archives/customer-attraction/tools/evidence/terminal-security/original/research/workspaces/customer-attraction/R-a13b93880118462581808cbd7231863e/parent_review/terminal_pair_review.py
~~~

该脚本只用标准库，从相邻`credible_attack/`读取原JSON动作表；它自行固定四主题并逐定义检查全部85个有序历史的255次真正偏离，重算(C,D,A,B)、四个利润1、θ=1及W=OPT=4。完整stdout已保存为`replay/independent_pair.json`。它核固定输入，不提供任意JSON的通用schema验证。

## 重新生成完整四客户证书

原生成程序会写自己旁边的JSON，因此不要直接在`original/`运行它的主入口来覆盖冻结件。以下同一次运行仅把`OUT`改为一个新的输出目录，保持原源码和断言不变；若目录已存在会停止，先另选目录名即可：

~~~bash
python3 -B - <<'PY'
from pathlib import Path
import runpy

base = Path('archives/customer-attraction/tools/evidence/terminal-security').resolve()
fresh = base / 'fresh-replay'
fresh.mkdir(exist_ok=False)
source = base / 'original/research/workspaces/customer-attraction/R-a13b93880118462581808cbd7231863e/credible_attack/load_dominance_witness.py'
namespace = runpy.run_path(str(source), run_name='frozen_generation_replay')
namespace['main'].__globals__['OUT'] = fresh
namespace['main']()
PY
~~~

原程序使用所保存的五个`customer_attraction`模块，无第三方包；其固定相对根解析依赖于这里保留的完整原路径。规范验证报告255次真正偏离，附加递归核验报告340次含自身比较，其中220次严格。所有85个有序节点动作、输入和三个行动计数结果均在生成JSON，不只是stdout摘要。

本轮实际使用单独`replay/`作为`OUT`；新JSON与原文件逐字节相同，SHA256均为`4bb93707e105b2ea63e22ff14243681be8f033c19747bfc5c48d61ea905f13f7`。两份JSON和[witness_comparison.json](replay/witness_comparison.json)均保留。`root_outcomes`是计数向量，不能当作有序路径列表。

## 从26个客户核验静态分离

~~~bash
python3 -B archives/customer-attraction/tools/evidence/terminal-security/verify_quadratic_gap.py
~~~

脚本使用标准库Fraction，重建26个客户与f/H/K，核正定主子式及p、q、λ的有理证书，无优化器或完整SPE搜索。结果为M=19/2、自响应135/14、差1/7，本轮输出在`replay/quadratic_gap.json`。若要额外保存一份，可传`--output 新路径`；程序以独占新建方式写文件，拒绝覆盖已有结果。

所有核验均须保留Python断言，不使用`-O`或`-OO`；`-B`仅禁止生成pycache，不移除断言。新版26客户脚本也显式拒绝断言关闭的运行。原四客户脚本没有同一守卫，调用者须遵守普通运行条件。

四客户证据证明一个真实SPE满足更广的负载支配条件；26客户证据反驳一个静态安全值代换。二者都不是六人半覆盖的反例，均不能完成LAST所缺的早期收益聚合。
