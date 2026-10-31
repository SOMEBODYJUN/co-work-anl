# 仿射线逐tuple与全局dummy：root冻结证明

对应UM-AFFINE-LINE-TUPLE-GROUP-GLOBAL-DUMMY-ESCAPE-v1。完整原对象与位域按statement。rank已仅据root消息及source定义独立冻e8eed151…，本Proof才另冻；不改其原始读取记录。

从m0个非空relations任取q个不同relations，各选其显式表第一tuple，得到q个不同tuple groups。不求源赋值，也不优化full-set packing。取这些选中的任意子族F。对每变量x有r_x≤R条长R的selected lines，来自不同relations，intercepts注入；同slope平行、异slope恰一交，故任两线不重合且交≤1。二阶容斥给union≥r_xR−C(r_x,2)≥(R+1)r_x/2。变量tag分离，Σr_x=k|F|，得每个F的邻域≥k(R+1)|F|/2≥ceil(kR/2)|F|，含odd kR、F空和r0。

普通整数capacitated Hall给每选中group b=ceil(kR/2)枚全局不交真实资源。其余n−q=d个groups与d枚global dummy作确定性bijection，选对应singleton。每selector去选态private，选中原state只外送该b件incidences，选中dummy state外送其唯一incidence。所有其它incidences全留原private，含选real组的全部dummy states、选dummy组的原real state和其它dummy states。每选real机负载2−b/D，其余private≤1，U及dummy资源各至多一unit，全部原jobs一次；共同峰≤1.5。

若原full sets有q个两两不交，选这q个groups的real states，其余groups各一dummy；selected states全部incidences导出，其余states全部park，给完整unit。反向任意完整actual≤1，每selector所在state的private已承unit，因该state每incidence private时间严格正，全部必须导出。每resource至多一unit，所以selected dummy groups≤d，至少q个groups选real，其全部full sets已不交。其它未选state可额外导出只占资源，不妨碍提取。因此unit iff packing≥q，selectors亦给OPT≥1。

q=n时d0且m0=n，表非空部分各一tuple，所有groups都选real，Hall及unit等价原生成立，无除零。空relations不生成groups，j_x注入仍原样；m0只用于域和选择，不偷改source value分母或near-perfect YES。超域q不能引用这个逃逸，不为其补未声明归约。

各state归一质量1。private数n(d+1)，resource数vR²+d；incidences nD+nd、selectors n，故jobs n(D+d+1)。selector有限条目n(d+1)，incidences每件两端共2n(D+d)，合finite n(2D+3d+1)，dense如statement。选q表首项、line枚举、qD边flow、dummy bijection及输出全部原jobs均显式总位多项式；槽数qb≤qD≤nD，不按更大隐藏分母数值展开，不求CSP解或枚举全部子族。固定source k,R时为普通source-polynomial；任意二进制R的vR²展开必须收费。

技术是既有仿射线pair overlap/Hall与flat完整回填。具体增量是关闭此前不由constraint-as-group结论自动覆盖的这一自然tuple-as-group+globaldummy count桥。它并未证明原源全set packing容易，也没有给一般source-to-UM归约不可能或near2主命题反面。
