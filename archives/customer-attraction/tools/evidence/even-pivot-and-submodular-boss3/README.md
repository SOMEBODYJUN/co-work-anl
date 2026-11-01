# 同枢任意阶恒等式、四阶分离与固定次模探针

五primary全部原字节共14718B，分别是6217B证明、3241B Fraction检查器、368B检查报告、3055B次模探针与1837B浮点报告。source-manifest保来源ID、双冻结commit/path、blob、SHA、大小与保存路径。related-original两稿为关联全读，不在本批新增done。

## 正式对象

- [覆盖同枢恒等式](../../../state/引理/覆盖调和势的任意阶同枢交换恒等式--引理.md)：全k/实背景证明、偶阶正性、同人数效用展开与真实SPE付款缺口。
- [二阶与四阶分离](../../../state/障碍/次模删除势的二阶与四阶覆盖交换分离--障碍.md)：全域次模二阶正性、dummy秩二四阶差1/2、非负客户表示障碍。
- [三人固定探针](../../../state/计算/三人反组次模安全值探针的精确界与原浮点记录--计算.md)：全F模型668行、原完整记录及新解析最优界s/3。

## 实际运行

1. 未改verify_even_pivot_taxes.py的原入口恰一次，4.583秒、exit0、stderr空；stdout/生成报告均与368B原报告逐字节同。exact-replay保实际argv/版本/指纹、完整stdout/stderr及新报告。recorded_original_runner.py是本次组织脚本的原字节副本，含当次工作区/cache路径约定，不冒可任意平移的通用入口。
2. check_submodular_contract.py独立标准库Fraction数学及JSON字面审计恰一次，不import原探针、不调用LP。重建完整43节点/215非自IC、63个F列，六查询恒等式378系数全同；668行逐一保存原小数余量及全1F达到点的精确余量。contract-replay/event.json保脚本SHA/版本/时间，report.json为实际输出对象。工具观测退出码0；stdout在工具结果显示，没有另存为冒充原始捕获的文本文件。NumPy2.3.5仅用来对当前十个默认随机查询作数据对应，匹配j7，不运行优化器。

本轮原submodular main/solve、LP/MIP均0。原浮点报告没有旧源码SHA/argv/版本/对偶/完整轨迹；其数值接近1/3不单独证明任何上界。新界来自正文六查询恒等式、二阶税、末位IC及全1达到例，针对精确数学系数模型；不把它写成历史HiGHS对偶或二进制系数最优证书。

## 复现

原Fraction入口只有标准库依赖。将original/07375b51ff4212cbe2e1/verify_even_pivot_taxes.py复制到新的仓库外目录，开启默认assert后运行它；它会在自身目录写even_pivot_taxes_verified.json，再与original/f65da45c08481ab6448f/中的冻结报告比较。不要在original目录直接运行而覆盖冻结数据。

定义级审计：在另一个新目录复制check_submodular_contract.py及original/目录后运行脚本；它要求contract-replay尚不存在，自动产生全六行系数、全部668余量、完整策略及报告。Fraction数学只用标准库；NumPy若可用则另记录十查询对应，缺少它不删除数学检查。原浮点probe需要NumPy/SciPy，但此包未执行它，也没有把当前版本倒填为历史环境。

related-context-manifest保存五篇全读正式正文及SHA；relation-review写明对象关系和条件，供第三阶段据证据整理，不导入旧图。有限网格、全参数解析、共同次模扩大模型、客户表示和完整SPE分开保留。
