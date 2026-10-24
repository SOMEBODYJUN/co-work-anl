# 一般半覆盖接续：已付源预算与真正传播债

Q-CAG-HALF仍OPEN。本轮继续同一clone/actor；只研究任意人数、任意有限共同目录、全部有序历史纯SPE。六个原分支已接续，root直接推进一般推导。旧个人区、其他actor临时文件保留不动。

## 1. 从上一轮合法结果出发

详见[上轮一般稿](../round3/GENERAL_PROOF_WORKING.md)：owner势、全J Hall-A/B、完整OPT前缀的联合资金、单行HIT、真实I信用路由均有各自解析证明与独立核对。所有初始owner-source可同时放入eta_i=u_i(I)+gamma_i，总eta=W。真正未付是捕获后重置到actual-prefix的incoming费用；NET逐行充分条件可能强于half，不能默认必须走该路。

本轮既可攻更弱总费用，也可放弃actual-prefix重置或采用全新一般机制。静态maxflow、同核积分、随机角色钟及固定ghost恒等式均不能自动支付原整条IC。

## 2. root新检验的全输入候选：最小调和最优增量

固定一个合法背景b，剩r位单位玩家。定义

    P_k(b)=max_(A_1,...,A_k in catalog) sum_x[H_(b_x+c_x)-H_(b_x)]，P_0=0，
    Delta_k(b)=P_k(b)-P_(k-1)(b)，
    L_r(b)=min_(1<=k<=r+1) Delta_k(b)。

**MIN-PI（本轮随后已由完整SPE反驳，以下保留原候选）**：每份完整r人SPE的当前收益u>=L_r(b)。它弱于已反驳的u>=Delta_(r+1)，后者不能恢复为引理。旧430客户反例本身不决定MIN-PI；必须重新计算所有增量，不能以单个下一步差值替代最小值。

### 静态充分性重构（普遍证明，不依赖MIN-PI为真）

原实例总人数m，背景b由p=m-r个真实旧目录行动给出。取任意k>=1及一个达到P_(k-1)(b)的profileB，写L_x=b_x+c_x(B)、g(A)=sum_(x in A)1/(L_x+1)。对任意合法A，加入它的势增正好g(A)，因此g(A)<=Delta_k(b)。

固定最优m槽比较元组T，覆盖O、覆盖次数a_x。逐客户 1_(a_x>0)<=(a_x+L_x)/(1+L_x)。求和，并把L的p+k-1个合法旧/比较行动展开，同一目录给

    OPT_m <= sum_j g(T_j)+sum_(A in prefix+B)g(A)
          <= (m+p+k-1) Delta_k(b)。

当1<=k<=r+1时m+p+k-1<=2m，故L_r(b)>=OPT_m/(2m)。若MIN-PI成立，则原每个实际前缀均可应用，求和即half。此段只是旧静态插入预算的直接min弱化，没有证明首位保底，也不认领静态代数新颖性。

### 当前一般推导和缺口

将Delta_k减阈值t后，可视为可变人数净调和最优值的严格增长。但纯SPE不是静态NE，不能从全局净势增长推出玩家不会选外部保底。一个孩子中尾部效用高于t，也不能免费推到父节点。要证明MIN-PI，仍须从原全部真实后继IC建立新的总体势或安全值关系，不能用Pk序列凹性（已知可不凹）。

只在既存完整策略锥里检验这一精确一般候选。若分离，仅否定MIN-PI，不否定half；无分离仅表示所选有限诊断没有结论。该计算不变成新固定人数项目。

## 3. 新候选已否定，不继续势增量路线

[冻结证书](parent/min_increment_counterexample.json)与[独立单位审查](global/review_min_pi.md)给MIN-PI的完整SPE反例：首位3481，P0..P4为0,6013,20275/2,27693/2,35111/2，最小增量3709。全部43历史258比较精确通过，主题覆盖不同。W10671、OPT12546，未否定half或EI。有限窗口增量非增仍不足；没有声称计算无限Pk全局凹性。停止该候选，不扩反族。

## 4. root正在接合的正向组件

[可预测激活](relay/predictable_activation_transport.md)给source吸收1/c、nonowner固定state吸收至多1/[c(c+1)]，恰接owner势边际。root从前缀可测性重构该式。多个state各w<=1不能相加成一个role一次预算。

[共同Uniform世界](relay/adaptive_cancellation_priority_world.md)使每R客户每world始终有unit；按U_owner阈值向激活future角色前进。终点事件包含于Ui>U_owner>所有该state future coverer，所以Beta2允许路径观察全world后选择。首个query固定，所有role递增，故质量守恒。每world可在同一actual Hall-A域选gamma(U)，再取常数w=E[rho·1_terminal]/D购买原整条IC，没有条件化原IC。若保原SOURCE-NET，gamma须含固定局部delta；全域greedy不自动保delta。

固定world的最低终端价格可按角色逆序求：每个state无激活future才终止，否则可选一个激活future并重查任意合法含x主题。每个终点的排序witness仍成立。全world期望最低费用是否<=W仍未证明，不能把新合法自由度称支付。

[actual I联合核](mixed/joint_activation_owner_credit.md)在同一优先级世界中先给actual coverer信用，再走query。owner实际未覆盖的客户，每actual coverer得1/(c_actual+1)，query总量kappa。未来J-none泄露激活，故证明用事件包含，不声称未来仍独立。查询携带的这些客户不在当前actual主题中。多客户、多query同role的整行付款仍未合并。

[动态rank](shared/net_dynamic_rank.md)精确消去固定实际Hall取消，费用成为超额价格层Hall缺额；只是完整表示，未证动态cut<=W。NET-FRAC拆证明库存，不改单位客户游戏；不把fractional可行当原INT可行。Hall-A恒定R源的world自适应取消，与Hall-B平均I库存的固定比例取消不可混用；random winner版本另须逐worldcut及source证明。

[真实offhistory桥](credible/incoming_slack_transport.md)给tracked b>=1客户的每recipient收费至多其利润一半，但整个IC还广播fresh R及新outside；不能截掉或把逐recipient半界求和当总收缩。自然action-return有offhistory prescribed行动IC，任意重查不自动有。根继续攻共同预算或更弱总费用，主目标仍OPEN。
