# L3遗漏量接口的代数勘误

2026-10-24，general_exchange；经root授权仅修改原route5a稿局部。未新增一般half证明。

原文件：`research/workspaces/customer-attraction/R-1740705e79f14baba6326b951a52152f/route5a/sequential_deviation_share_lemma.md`。

原§4写：若排列偏离份额和至少`(|C|-|C intersect U|)/2`，则`W >= (OPT_m-W)/2`，即`2W>=OPT_m`。最后的“即”为错误代数：它只给`3W>=OPT_m`。

正确充分条件是份额和至少`L=|C\U|`。因为`W>=L`且`|C intersect U|<=W`，有`OPT_m=|C intersect U|+L<=2W`。如只要求份额和至少`L/2`，可保留的结论是`OPT_m<=3W`。

原§2的模板诊断也相应统一改为`H_m<m`（m>=2），不再以`H_m<m/2`作为half的比较阈值。该段是形式支付模板的不足说明，不能将m个完全遗漏的不交主题场景冒称同一实例SPE反例。

L1、L2、L2*、L3、L4及其证明没有改动。原§4动态共同信用文字未给出独立完备桥，仍保持候选身份。CLAIMS中CA-SEQUENTIAL-DEVIATION-SHARES-v1没有引用错误充分条件，故该行无需因本勘误改变。

导航复核：current README和CLAIMS的实际markdown链接正确指向R-174；先前口头称错链已撤回。RESEARCH_STATE的两个code-span短文件名本身不是链接，不属于本次修复。
