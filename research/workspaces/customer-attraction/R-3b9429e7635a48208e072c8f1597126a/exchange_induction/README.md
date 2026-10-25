# 冻结前缀与净差交换：本轮精确停界

2026-10-25。Q-CAG-HALF 原模型，一般人数、任意有限共同目录、全部有序历史纯 SPE。
本目录是未完成探索的个人备份；**没有新增已证关系，没有新 half 范围，一般目标仍 OPEN。**
未运行新的有限实例扫描，未修改 git 或向外发送消息。

## 1. 已撤回的冻结前缀加强

固定旧负载 b、旧覆盖 P，剩余 r 人。令实际新增覆盖为 D、剩余玩家最终利润之和为 V，
R_r(P) 是 r 个目录主题在 P 外的最大覆盖。曾试候选

    R_r(P) <= D+V.

空背景时 D=V=W，因此该式足以给 half，但它对实际根 SPE 的实际前缀也为假。
独立审查者指出并重读的既有来源：

- `../../R-5c4f6385eec046eb9a20052facacba11/background/global_actual_prefix_counterexample.md`；
- 同 actor 的 `parent/actual_prefix_independent_review.md`。

52 单位客户、四人完整 SPE 的实际路径 A,B,A,B，在实际前缀 A,B 后，r=2、D=0、V=17、R_2(P)=18。
故加入任意 D 系数仍不能修复这一点。它与一般总税 GT 的比较目标不同，不能用 GT 反例替代此真实反证。

## 2. 精确递推及它为何没有闭合

定义 G=F_r(P)、H=F_(r-1)(P union S)、delta=G-H，其中 S 是当前真实动作。
令当前终局利润 u、当前新覆盖 a=|S\P|；令尾部真实新增覆盖 D_tail、尾利润 V_tail，
以及相对 P union S 的尾部最佳新增覆盖 R_tail=H-|P union S|。
若以

    slack(h)=D+V-R_r(P)

计冻结前缀候选的余额，则无条件精确有

    slack(h)=slack(h,S)+u-delta.

这来自同一真实路径的 D=a+D_tail、V=u+V_tail 及覆盖补全的定义，不搬运离轨后继。
它不提供支付：已知负首步余额族可有 delta>u；52 客户实际前缀更直接说明任意背景 slack 非负本身错误。
因此不能把较少剩余人数的任意背景假设作为 induction hypothesis。

## 3. 也已撤回的纯遗漏并集加强

曾检查 root 充分加强 W>=max_(T_1,...,T_m)|union_j T_j\U_actual|。
仓库查重及父方指出它已有严格反例，故未作任何新扫描：

- `../../R-171cd7d518434f36a48cd50df29c9303/global/optimal_omission_exchange_counterexample.md`；
- `../../R-171cd7d518434f36a48cd50df29c9303/coupling/optimal_omission_independent_review.md`。

71 客户完整二人 SPE 有 W=35、唯一最优覆盖 O=38，但最优遗漏 L=36>W。
一般净差的正确对象始终是 O-W=L-E，其中 E=|U_actual\O|，不能删掉比较并集之外的实际覆盖信用。

## 4. 删除与换根的剩余真实义务

已完整读一般稿 BG、旧利润修正后的 cross-branch relay 接口、多槽最优补全交换，
以及全人数保险族任意删位上漂稿。它们的可用范围保持原身份，不在此重新认领：

- 任意历史真实分支比较须保留旧玩家最终利润变化；非根不可只比较尾利润。
- 删除原玩家后，投影福利是 W-e_i，不是 W-u_i。
- 若真正删后 SPE 福利 W'=W-e_i+d_i，记 Delta=OPT_m-OPT_(m-1)、L=alpha W'-OPT_(m-1)，则

      OPT_m-2W=Delta+alpha*d_i-alpha*e_i-(2-alpha)W-L.

  这是精确代数；删去真实 child slack L 后，保险族会同时令全部删位的单份局部 coupon 付款失败。
- 多槽 ME/MM 只给静态补全可行性；不同强制动作产生互斥真实尾部，不能自动耦合。

同一删除式代 m=5：

    OPT_5-2W=Delta_5+(1499/750)d_i-(1499/750)e_i-W/750-L.

若没有新增不等式共同支付右侧净差，则该式只是条件接口，不能宣布一般五人 half。
本轮没有找到这种新增全输入支付关系，故在此准确停界；不继续调残余/背景系数或制造近似旧障碍。
