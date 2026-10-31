# 直接共居 SAT 编译三半锐界：作者 statement / Proof 实际 read-after

审查者：general_query_response_review。2026-10-18。

## 实际顺序与正式范围

先仅据原P的定义/结论陈述及root消息中的新fixed-half Claim独立构证、冻结初稿与final，并独立枚举指定8机10job小矩阵。Root实际通读独立final后，本轮才首次实际全文读取：

- direct_cohabiting_sat_compiler_sharp_three_halves_statement_v1.md，SHA 9de253ea49c94f265d9306cde8d45f9207911500cb5ad0c858bacf91dad6b72e。
- direct_cohabiting_sat_compiler_sharp_three_halves_proof_v1.md，SHA 941faba582073dbfd7342f8479bd3817f4cb51dca34813c1578dcab668256f16。

**正式只认证新Claim C：UM-DIRECT-COHABITING-SAT-COMPILER-SHARP-THREE-HALVES-v1，真实x_i=y_i=1/2、dummy x_i=1、3/4<rho<1。作者statement与先行新陈述一致，Proof通过，无fatal。**

不认证Claim B的任意异权active分支或其共同matching，也未读该异权作者Proof、其它agent输出或新canonical。本次仅scratch新增，初稿/final独立记录与枚举证书保原字节，未改repo/Work/Git。

## 作者Proof实际核对

1. Universal三半完整上界正确：q_i全部M_i，b_i全部C_i，每clause u_c任选本clause实际C_i。不同clauses不共用同一occurrence，因此每C最多一件u，load至多1+1/2。所有M一件q、load rho，dummy原jobs也完整保留。非空时峰恰3/2，不需要未知SAT赋值。
2. C<3/2时M上每件q/b至少rho>3/4，所以每M至多一件。作者设E={q_i@C_i}、R={b_i@pin(i)}，由C_i的q_i+b_i至少3/2得到E⊆R；dummy pair总2也被排除。
3. 全部q/b实际在M上的件数精确N−|E|+|R|，至多N迫|R|≤|E|，结合包含得R=E、每M恰一件。这是我先行“每M/C各恰一件q/b”容量论证的等价写法，未预设同编号返回，覆盖任何合法额外exports。
4. u_c真实C_i时间1/2不能与b_i unit共居，因此所在i必须属于R=E。它是同编号q_i导出、b_i返回的真实occurrence，不能借dummy或不属于该clause的occurrence。
5. 每索引恰一个有效q或b在其M_i/M_(i+)边上。每台M恰一件给(1−z_i)+z_(i−)=1，故每变量环方向一致；返回b的pin给s_i=z。z0取True、z1取False，每clause的actual u目的地提供真literal，SAT解码正确。Padding、重复变量/文字及任意dummy polarity不破坏这件数恒等式。
6. 解码逐实际job扫描、读环端并输出变量位，确定性总位多项式；无需规范化未选的额外exports、匹配求解或搜索SAT。所有原q/b/u任务都在计数中。
7. SAT完整unit上界正确：各clause选一真occurrence，q_i放C_i、b_i放与truth方向一致的pin，u_c与q_i在C_i合计1；其它q沿环统一方向、b_i停C_i，dummy不选。每M一件rho或1、各C负载1，全部原jobs恰一次。
8. 作者另证非空OPT≥1，未错误地因job存在unit可选端就宣称下界：若C<1，全部b不能C，所以R全体；M容量与件数迫E全体。任一clause的u_c便与真实q_i在C_i合计1矛盾；dummy q_i若也在C_i unit更直接矛盾。因此非空SAT精确OPT1。
9. UNSAT无任何C<3/2调度，结合universal完整等号上界给OPT3/2；空式idle零jobs OPT0单列。严格阈值不可扩为≤3/2，既有完整UNSAT等号witness使其sharp。
10. Statement的rho4/5、正正负负四环UNSAT例与我独立原矩阵一致：8 machines、10 jobs、24 finite entries、5184 eligible assignments，整数10单位最优15；有限枚举只是checks，不承担一般证明。作者Proof未宣称软件实现或依赖此穷举。
11. 所有复杂度按显式N/L/二进制rho及padding计量，不按分母数值展开。没有将fixed三半gap包装near2反面、新hardness或全球新颖性认证。

## 冻结状态

先行final：
/workspace/scratch/038d9dcc4cac/direct_cohabiting_sat_compiler_sharp_three_halves_exact_only_review_v1_final.md

SHA 5118de136df42fd69d6630b21a4290e33cd18f41de29e3d54c6bed0d9906630f。

其初稿7f9caf5f91d72a512f983c9b887e10e5adf64d5eaefd88ac7d53096489bacf5f与独立枚举d7fb60f5c1857174868efe7366c3506ca6cacb2cf2710bfe37586113a3d2cad4均已核hash保留。本轮不重写历史措辞或first/final字节。

**最终读后判断：仅fixed-half Claim C statement/Proof通过，无standing fatal；B的异权active matching不纳本认证。等待最终canonical后另作指定范围实际阅读。**
