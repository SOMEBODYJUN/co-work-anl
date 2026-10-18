# 仿射线逐tuple分组与全局dummy的编译障碍：精确陈述

ID/version：UM-AFFINE-LINE-TUPLE-GROUP-GLOBAL-DUMMY-ESCAPE-v1。

本文件把root此前实际发给rank的精确消息正式冻结；rank的e8eed151…独立记录已先完成，不能倒称其先读了本文件。此前独立输入是消息陈述及已公开source的明示定义，不含新作者Proof。本文件不附证明策略。

对象：prime R≥2、k≥1，有限变量X及indexed relations G，每relation涉及k个不同变量，变量relation-degree≤R；给每变量的incidence注入j_x:G(x)→F_R，变量资源tag分离。显式tuple表A_g允许为空。每allowed indexed tuple e=(g,s)给资源集合S_e=⊔_(x∈X_g){(x,z,s(x)z+j_x(g)):z∈F_R}，大小D=kR。令n=Σ|A_g|，m0为非空表数，给整数q且1≤q≤m0，d=n−q≥0。

完整ordinary UM：每tuple e独立一group，menu有其原S_e state（每资源private1/D）及d个dummy singleton states（各private1），dummy资源δ_1,…,δ_d由所有groups真实共享。全部state不同private，全部资源不同resource机；每group一selector1只可去自己menu的private，每state-resource一件不同incidence仅可去其private以表内权或对应resource机1，余∞。全部未选state jobs保留，无其它jobs/预载。d=0时无dummy资源/states/jobs。

Exact：对每上述输入，无source/OPT/full-set matching witness，可det-bit-poly输出全部原jobs共同实际峰≤2−ceil(kR/2)/(kR)≤3/2。且完整峰≤1可行当且仅当原indexed full sets有大小≥q的两两不交packing；这个equivalence是unit可行性，不是假装该1.5构造会求unit解。

Counts：n(d+1)private，vR²+d resource，原jobs n(D+d+1)，finite n(2D+3d+1)，dense=[n(d+1)+vR²+d]·n(D+d+1)。按完整显式输入/输出总位长多项式，不称poly(logR)的succinct展开。q=n与空relations不换源promise；q>m0或m0=0在域外。空relations不产生groups，不把原source归一化分母改成m0。只排这个具体uniform/dummy计数编译，不排所有tuple grouping/全局guard/其它资源权重归约，不给near2主反面或新颖性认证。
