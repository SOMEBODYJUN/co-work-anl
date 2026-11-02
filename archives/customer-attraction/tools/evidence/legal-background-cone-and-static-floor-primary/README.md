# 合法背景策略锥与静态floor探针原始证据

## 正式对象

- [合法背景数值策略锥的利润归一与四份探索](../../../state/程序/合法背景数值策略锥的利润归一与四份探索--程序.md)：8226B Game/数值优化与四报告，保count-target、合法过去剩余利润、Fenchel目标、全部近等号/浮点残差和真实证据缺口。
- [静态跟随者门槛保护的受限终局探针与三份数值记录](../../../state/程序/静态跟随者门槛保护的受限终局探针与三份数值记录--程序.md)：2839B探针和三报告，288客户/6叶的精确固定收益、数值门槛范围及解析非SPE障碍的接续。
- [关系及自查](relations-and-self-review.md)：逐关系参与者、前提、证据、未付义务及旧共享页建议。

九个primary总2703135B，完整来源[manifest](source-manifest.json)保大小/SHA/blob/双冻结commit，source-root依原路径逐字节复制，没有缩减银行或矩阵。原两个Python及七JSON都完整保存；没有将report重新格式化冒原件。最初父方clean show导出并逐份校验，当前复制再次核size/SHA；不做Git或网络操作。

## 来源逐项

| primary ID | 文件 | 大小B | 完整处置 |
|---|---|---:|---|
|58a94235d2f076f30a7d|background_cone_attack.py|8226|全文全部函数/原导入与CLI，背景与LCM/BI容差、count-target行、数值KKT/Fenchel、剩余利润归一、停止/失败/写入合同|
|4de96e86af0302610c7c|background_floor_r3_p10000.json|478772|best+10bank全部31维权/query/q、21态policy/行、两轮trace、原1665 trials/elapsed/failures及重复点|
|bc6f6f4d2f2396b20ff6|background_floor_r3_p11000.json|436859|全部11记录，保负mask23/22态历史记忆、原1770 trials/一次failure及所有数值边界|
|d51eb5ffe110489d9f32|background_floor_r4_p10000.json|1029655|全部11记录及56态/最多190行，保932 trials及单mask等号，不升总人数五到六|
|ff5d72762e6815f63f72|background_local_r3_p10000.json|519403|全部11记录，保根/下一背景local合同、三点附近残差/负权、1278 trials；缺child证书不补猜|
|126b24a08489938822a0|probe_floor_protection.py|2839|全文不重复根的eligible/min/score、未占用列、T/q语义、随机bank及提前停止，不是SPE扫描|
|dad95955aba1ce5bc3d4|static_floor_r3_bg0.json|74328|全部21记录、288最佳权与六坏叶/原q值；8个不同输入和重复bank全保，不把float阈值称精确|
|9b520456a10a69135655|static_floor_r3_bg1.json|75653|全部21记录，429最佳/427/423/418邻点、六根收益、负score及q原误差|
|ae4da314bfd8b7a4b8e6|static_floor_r4_bg0.json|77400|全部21重复记录、337权/六叶/数值值和负score；非21独立实例或一般阴性证明|

全部source locator以`source:<40commit>:research/workspaces/customer-attraction/R-ab183d14fb74403091d09db766b05f73/security2/<filename>`记于正式页和manifest。每源另有父方接收的逐源receipts，当前此stage不自行done。

## 必要运行闭包与相关成果

source-root还复制已发表、完整实读的2386B `security/fractional_minmax_probe.py`，SHA `fd6b132e59441ff7ec5592d47c10647e44ab03c955e70ef0eac090b0cdeab0bb`。它与security2同父目录，原路径sys.path/import可恢复，未修改原程序。原报告未存helper指纹；这里只认证当前取得的冻结闭包，不冒历史实际进程使用证明。若运行原程序仍需numpy/scipy，原材料没有版本锁；本批没有安装、导入或调用它们。

[依赖指纹](dependency-fingerprints.json)仅列本批实际比较的共同模型、背景定理、原零根Fenchel程序、两份背景资源、银行完整反族及helper。既有静态证明、五客户解析障碍、银行全参数证明和旧标量有限审计直接复用，0重复执行，related不额外primarydone。它们与当前七大JSON的数学对象/证据层级逐条比较，详见relations-and-self-review.md。

## 唯一新增固定保存记录执行

[review_saved_records.py](review_saved_records.py)只用标准库。完整加载七JSON，并遍历每个字典/列表/数字叶，保全原record/权/行/policy的哈希与语义摘要。一次执行命令（在本包目录也可用相对路径）：

```sh
python review_saved_records.py --output saved-record-review.json
```

实际本轮仅调用一次，退出0，stdout的汇总在[执行事件](execution-events.json)。程序内部elapsed为1.9269526990001395秒，工具报告wall_time为1.99487747秒；未捕获UTC起止，未造时间戳。输出[保存点回代报告](saved-record-review.json)自带checker与manifest的SHA，原件与依赖另有逐字节sha。

| 新执行范围 | 数量/性质 |
|---|---|
| JSON原文 | 7份；107条best/bank（含重复） |
| cone数据 | 44条，3947个保存行，1311个(q,target)态，88条trace |
| cone行算术 | 对保存float解析后`Fraction(str(v))`的十进制字面有理化计算G w，未clip、未limit_denominator |
| cone利润/leader | 用同一十进制权和确切背景/终局整数重新求收益和剩余总利润，未重新BI或重建偏离边 |
| static数据 | 63条，378给定终局；确切整数客户/计数的2268个列收益 |
| static门槛 | 原保存value按十进制有理化，只检查给定占用跟随者相对该数和原score/relative，**不认证真实t** |
| utility显示误差 | 全部≤1e−11；报告保每项精确分数、原float、最大差，不改原文件 |
| 新原入口、LP/SLSQP、SPE求解、终局扫描 | 全0 |

新报告状态`PASSED_FIXED_SAVED_RECORD_ARITHMETIC_AND_SCHEMA_ONLY`仅声称上述固定检查通过。数据保留3条负权cone记录、几个极小负字面行积、概率字面和/归一偏差，不用PASS抹平它们。原min_spe_margin是浮点G@w，本次字面有理行积不是底层精确分数矩阵重建，也没有独立核验rows确实来自每条完整策略边。

静态精确公式对未占用标签仍只是固定分母代数列；本报告不把它当真实偏离收益。没有验证给定bads在未保存全部eligible里最小，没核value双边最优/所有实际历史IC，没有生成新的完整反例或普遍正面证书。

## 原执行与此次执行分开

原四cone报告自存trials 1665/1770/932/1278、failures 0/1/0/0及elapsed约48秒；原static自存trials 5002/12916/12425、elapsed约19.9/47.56/48秒。它们是历史数值搜索报告，不是本批重放结果。旧argv、seed、seconds预算、源码/依赖实际指纹和历史stdout均未存，当前不凭相同字段补写。

原报告各有同模型数值用途；清洗结果不需要先证明所有原候选。有限未成功搜索的边界与后来floor-only解析失败/真SPE银行反族已分别说明。父方负责正式复制、checkpoint和done，完成状态以父方回执为准。
