# 直接共居SAT编译三半锐界：root作者证明

ID: UM-DIRECT-COHABITING-SAT-COMPILER-SHARP-THREE-HALVES-v1。冻结消息陈述先交general，仅本Proof先保root，不给尚未冻结独立记录者。全部对象按statement与weighted完整Exact，未增加资格或假设。

所有Φ的1.5完整上界：全部q_i放Mi（time rho），全部b_i放Ci（time1），每clause u_c任取自己的一个真实Ci（time.5）。每occ只属一clause，故每Ci至多再一u，load<=1.5；每Mi恰一q，load rho。Dummy照同规则，所有原jobs恰一次。空式idle单列0。

若非空actual C<1.5，所有M finite costs至少rho>.75，两件总>1.5，故每M至多一q/b。置E={i:q_i@Ci},R={i:b_i@pin}。真实qiCi=.5与biCi1合1.5不能共居；dummyqiCi1同样排bi，所以E⊆R。N台M上q/b件数N−|E|+|R|<=N，故R=E且每M恰一件。每ucCi=.5不能与bi unit共居，故其所在真实i必须在R=E，即同编号qi外送/bi返回。

每索引有一条有效cycle edge：不在E则是环内qi，在E则是返回bi、端为pin。N条有效edge覆盖全部N台M各一次，所以方向沿每变量环一致；可令z_i0代表Mi、z_i1代表Mi+，由Mi件数(1−z_i)+z_i-=1得全部z相同。每返回bi的polarity s_i等于该变量方向z，按z0为真z1为假取赋值。每clause uc实际所在i返回且同编号，故其文字真。扫描完整σ确定性位多项式。因此UNSAT所有actual C>=1.5，配上界OPT1.5，包含任意未事先规范的全部jobs去向。

SAT上界1：沿满足赋值方向放有效cycle jobs；每clause选一个真文字i，qiCi、bi pin、ucCi共居总.5+.5=1，其余qi环内、biCi，dummy环内。各M一件time rho或1、所有Ci<=1，所有原jobs执行。

非空所有公式OPT>=1需另证，不能仅因某job存在可选unit端就称下界。反设C<1，则每bi不能在Ci unit执行，所以R为全部N索引；M仍每台至多一件，件数N−|E|+N<=N迫E全部索引。至少一clause uc执行于真实Ci，此机同时有qi，处理总.5+.5=1矛盾。若有dummy其qiCi1已更直接矛盾。因此SAT实际OPT恰1。

源空公式OPT0；dummy/重复literal不影响按物理occurrence的计数。构造和解码扫描显式任务与有理比较，位多项式；不需要找未知SAT赋值来输出普遍1.5上界。本页只是具体SAT桥的固定三半锐界、常用matching/方向计数直接重构，不给near2困难性或全球原创性认证。
