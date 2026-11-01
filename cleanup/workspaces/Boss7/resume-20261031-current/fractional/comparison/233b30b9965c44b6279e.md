# Fractional rematching / robust-menu：rank独立Exact-first审查 v3

审查者：rank_deficiency_fee，2026-10-18。仅clone外scratch，不改repo、Work/Git、statement或旧审查字节。

## 1. 实际对象、独立路线和总裁定

实际全文读取：

`/workspace/scratch/038d9dcc4cac/fractional_rematching_extension_statement_only_v3.md`

whole SHA256：`ee80af544eaa5f133efb426a38e8007f21c0ee85594c48e7feaacd5caacc5697`。

未读取作者Proof、general/rainbow新推导或root的证明文件。独立访问primary DLRV PDF arXiv:2309.04656v1，实际读取Sections 2.1–2.5、Theorems 1/10/11、Appendix A的concave extension/solver/Corollary 15、Appendix B Lemma 9完整证明及Appendix C Theorem 20的陈述与证明必要段。本文下方保守链是本次实际数学重构，不把v1/v2的conditional PASS当作v3 unconditional PASS。

原记录：

- v1独立审查 `/workspace/scratch/038d9dcc4cac/fractional_rematching_extension_rank_exact_first_review_v1.md`，SHA256 `b7f8fe124eed85643dda4e48251da3a794b2869b7b22128c55f899198774d5fa`。
- v2增量审查 `/workspace/scratch/038d9dcc4cac/fractional_rematching_extension_rank_exact_review_v2.md`，SHA256 `63c9e78d49c4a0eee967c24a8cc535e5cbcaa3fa149cf4f8e6bde2f8be3235fc`。

本次实际比较A对应段落，v3与v1逐byte相同。

**总裁定：v3不得按全部无条件数值合同PASS。A完整成立；B1的fractional量词可从Appendix A闭合；B2的60000及其后1125000/2250000/3000000常数不能照给定source链认证。另有Lemma6对非reciprocal sampling及对shifted f直接套Theorem20的适用步骤需修正。下方给可核的保守替代乘积，但不把它倒填为v3已述常数。C的unit证书/LP/floor数学、D的shared-singleton组合论和E的全部原jobs转换均成立；C3–C5及D3的无条件源应用依赖backend修订，当前不由旧conditional记录自动升级。未找到反驳A或物理转换的实例。**

Root在本次审查期间获知我指出的μ代回数值问题，随后提醒shifted f的Theorem20适用问题并明确允许下一版放大常数。本记录保留这些疑点与来源，不声称本v3原source数值已经完整认证，不硬救60000。未读取root另交其它reviewer的XOS替代lemma。

## 2. A：独立证明继续有效，包括真实bit算法

A原字节完全相同，故v1记录的自足证明直接适用。其核心是：把y投影至B取得(A2)确实量化到的fractional residual family；其normalized residual预算≤cn，H出现项预算≤n。对每entry设

    m_i(S)=max(V_i,max_{h∈S∩H}v_i({h}))，
    w_i(S)=v_i(S∩B)/V_i+|S∩H|，

inactive比值项另定义0且由v_i(B)=0保证残余值0。Subadditivity给v_i(S)≤m_i(S)w_i(S)，正benchmark使m,w均positive，weighted Jensen给总log额外损失≤n ln(c+1)。选择m的singleton或Vi outside option形成partial fractional matching；只可能在Vi>0的行出现outside质量。因此可把n×n的行列deficits补成正边doubly stochastic匹配，matching整数性给所需log-product。

Vi0、zero singleton、B空、A空、重复配置均无需log0或除0。给定Vi和n² singleton factors的真正最大乘积matching可用有理product的2^(−poly)对数间隙和poly精度log权求出：每matching的rational product分子分母位长受输入多项式控制，distinct products有2^(−poly)的relative/log gap。不会精确比较任意transcendental sums，也不求irrational benchmark。A既不寻找Vi，也不验证全域(A2)。

## 3. B1：为什么Appendix A给的是所有fractional residual families

Primary定义f_i=v_i^+，即在item边际x_i下最大化配置期望utility的concave extension。Corollary 15（α=1）给一份可行x，使对所有可行边际x*均有

    Σ_{i∈A} f_i(x_i*)/f_i(x_i) ≤ 2|A|。

任意残余fractional family z均产生可行边际x*，且

    f_i(x_i*) ≥ Σ_T z_{i,T}v_i(T)。

取Vi=f_i(x_i)，并用concave-extension primal的poly-support配置解达到该值，立即得到(A2)的全fractional界≤2|A|。不能把Theorem1正文较弱的integral welfare描述单独当作这一步；真正强量词在Appendix A。

Active集合v_i(B)>0可以用value query识别。Active时把整个B配置给每agent质量1/|A|、其余空配置，可作positive可行基线；inactive全部设Vi0且v_i(B)=0。B空/A空分别直接分支，不做空EG目标或log0。原τ要求full-U positive singleton最大乘积匹配，源Lemma9确需其全局最优性，A本身不需。

Generic backend使用primary demand-oracle模型及concave-extension LP/support recovery；不能解释成对任意value-only general subadditive输入的无条件poly算法。B3的total-bit应用域仅是后述显式XOS。Source说近似EG可给所需robust界与poly support，但精确rational数值如何落实应在后续最终Proof明示，不能只写“optimal point”后假定它有理。

## 4. Source迭代舍入的实际对象和共同事件

Source先对A''={i:Vi≥6nu_i}作SetSplitting，其中nu_i是residual最大singleton。配置support值在[Vi/3−nu_i,Vi]⊆[Vi/6,Vi]；新平均Vi'∈[Vi/6,Vi]。一轮welfare rounding只给各agent其某个support配置的子集，normalized utility≤6；若总normalized welfare≥|At|/d，则δ=1/(7d)保证每轮至少δ比例agents达到δVi'。

NSW-ROUND每轮的candidate sets和At变化只依赖该轮welfare rounding，不依赖预先独立抽的item几何标签r_j。真实执行T_i=S_i∩R_t；同轮S_i不交，不同轮R_t不交，故所有T_i是实际disjoint residual subsets，而非独立标签拼装。至多n轮，每轮至少一agent离开；实际上是O(log n)轮。

这套对象/进度与A的fractional benchmark y无关；source随后比较任意π不必输入unknown integral optimum。A''空时不运行Lemma7除以|A''|，T全部空，后续直接用V_i≤6nu_i的界。Inactive nu_i0无需以0分母取log。

## 5. 第一项明确数值objection：μ代回缺因子3

Primary Lemma6实际定义

    μ_i=(1/3) δ² t_i Vi， t_i=1−(i−1)/a。

其证明末尾先得到

    E ln[Vi/(v_i(T_i)+nu_i)] ≤ ln(60 Vi/μ_i)，

随后把它写成ln[60/(δ²t_i)]。按μ定义实际应为

    ln[180/(δ²t_i)]。

因此只纠正这一项后，原Lemma7的165及后文事件200/δ²均不能直接沿用。这里只是source证明链的数值缺口，未提供反例说明最佳backend一定达不到60000；但v3声称已核的那条source列式不足以认证它。v2仍是“若E2成立则…”的条件命题，不因本缺口回溯变成错误。

## 6. 任意Bernoulli参数与shifted f：不能省的适用检查

Primary Lemma16只直接证明sampling概率1/k的期望界。General monotone subadditive v并不总有对任意p的E[v(R_p)]≥p v(S)：三item取v(empty)=0、proper nonempty sets值1、全集值2，p=3/5时E v=144/125<150/125=pv(S)。该反例不直接反驳source加了nu的f，但说明不能无证明把原Lemma16换成任意p版。

一个通用保守替代是k=ceil(1/p)，由monotonicity和1/k版得到

    E[f(R_p)] ≥ (1/k)f(S) ≥ (p/2)f(S)。

对source f=v+nu仍是monotone subadditive，故可用这个half bound。结合f(S)≥δVi/3，通用可证μ改为

    μ_i=(1/6) δ² t_i Vi。                      (S1)

若另有XOS/additive witness，可以对v逐集合证明任意p的exact期望界；那是需明写的更窄route，不当作v3一般subadditive前件。

此外source用f(T)=v(T)+nu，但Theorem20所列singleton上界f({j})≤nu不成立，实际≤2nu。Lipschitz仍≤nu不足以逐字调用那个陈述。可不扩大定理而改为直接对原v应用Theorem20：令μ≤E[v(T)+nu]，在nu<μ/30分支取

    k+1=floor(μ/(10nu))，q=2。

因E v≥μ−nu，有

    E v/15−(k+1)nu/3 ≥ μ/30−nu/15 ≥ μ/30−nu。

故{v+nu≤μ/30}包含于Theorem20对原v的合法低尾事件。再由k+1≥μ/(15nu)，得到

    Pr[v+nu≤μ/30] ≤ sqrt(2/2^k)
                         ≤ 2·2^(−μ/(30nu))。  (S2)

这里对Theorem20的singleton前件确为v({j})≤nu，无偷换shifted f。nu0另分支；对active A''而言nu>0，因为finite subadditive v(B)>0不可能所有singleton0。

## 7. 从合法tail到一个可核的保守Lemma6–7链

记f=v(T)+nu。若nu≥μ/30，直接f≥nu给E ln(Vi/f)≤ln(30Vi/μ)。否则x=μ/(30nu)>1，按f<μ/30分解并用(S2)，得到

    E ln(Vi/f)
      ≤ ln(30Vi/μ)+(2/2^x)ln x
      ≤ ln(60Vi/μ)。                          (S3)

最后的函数上界≤ln2可按x所在整数区间核；x∈[1,2]直接成立，x∈[h,h+1]、h≥2时用h+1≤2^h及h≤2^(h−1)。这也避开原证明在ln x负时替换概率方向的潜在问题。

代入通用(S1)，得到每agent

    E ln[Vi/(w_i+nu_i)] ≤ ln[360/(δ² t_i)]。

对a=|A''|的顺序平均，阶乘估计−a^(−1)Σ_i ln t_i≤1，故

    E Y ≤ ln(360/δ²)+1 < ln(1000/δ²)，
    Y=(1/a)Σ_i ln[Vi/(w_i+nu_i)]。             (S4)

这里w_i=v_i(T_i)≤Vi，nu_i≤Vi/6，所以Y≥−ln(7/6)。对非负Y+ln(7/6)作Markov即可在一个绝对正概率事件得到

    GM_{A''} Vi/(w_i+nu_i) < 1200/δ²。         (S5)

δ=2/35为固定常数；该成功概率有绝对positive lower bound。不是从E log有界直接无条件宣称所需常数，也不依赖π或未知benchmark allocation。

## 8. Lemma9和任意comparison π：无integral benchmark依赖

Lemma9完整proof仅用原τ是full-U positive singleton最大乘积matching。对任意π:H和Wi≥0，以τ/π交替有向图分组，切在需要outside最大singleton nu的agent，形成不交路径。若某路径τ乘积小于终点nu乘其余π值，替换该一条路径并使用一枚原H外item会改进τ，矛盾。每条路径单独分析，即便不同终点的outside最佳item相同也无冲突；最终ρ只使用H的τ/π边。补全未激活agents后，得到

    GM max(Wi,v_i({ρ(i)}))
      ≥ GM max(Wi,v_i({π(i)}),nu_i)。

当图有cycle且包含nu端时，在nu端切开；不含nu的closed cycle不会进入这组可达路径。Zero π值只使相关乘积比较平凡，不需log0。B空时nu0，亦无outside positive路径。

最终source算法在Ti之上重选H匹配，故至少达到上述ρ的真实utility。取Wi=w_i，source同一个rounding成功事件对任何π都可给

    Π_i (Vi+s_i)/(w_i+nu_i+s_i)
      ≤ ( max( 2·1200/δ²,6) )^n，

其中s_i=v_i({π(i)})。A''用w_i+nu_i≤2Vi，非A''用Ti空和Vi≤6nu_i。若Π(Vi+s_i)=0，目标本来平凡；否则分母均positive，合法作比值。

再用max(w_i,nu_i,s_i)≥(w_i+nu_i+s_i)/3，得到可核的保守比较factor

    3·2·1200/δ² = 352800 d² ≤ 400000 d²，
    δ=1/(7d)。                                (S6)

它对全部π在同一事件同时成立，post-Lemma8部分没有用S_i*或integral OPT。与A的c+1相乘，c2、d5/2时factor可取7500000；若另预留2倍实现slack，取15000000。Unit benchmark内部floor为3/4时，原actual NSW至少1/20000000，因而rho=2^30足够。这是供新版本明写的保守链，**不是v3的60000 / 1/3000000链**。

仅在explicit XOS route另证明E v(R_p)≥p v(S)时，可省(S1)的half：同样修正后每agent常数180、平均小于500/δ²，选择600/δ²事件；(S6)变为176400d²≤180000d²，预留2倍实现slack后floor benchmark给1/9000000，足以保rho=2^24。这也不能认证v3更强的1/3000000显示值；root若改用统一更大rho则不必优化这一点。

## 9. B3有限位义务：已核项与不可一句话跳过的项

C的floor确使所有clause系数、正utility落在1/(4m)网格，缩放后≤4m。Explicit XOS的value/max-clause直接扫描；demand对每clause取p_j−price_j的positive项，再取最佳clause，总位多项式。Initial/final maximum-product matching可由A记录的精确gap算法实现。最终comparison guarantee也可用最佳π的有理product核验，不需读irrational benchmark或unknown OPT。

SetSplitting在A''上产生的份数ki,S=floor(3v_i(S)/Vi)≤m/2，因为v_i(S)≤m nu_i且nu_i≤Vi/6。因此没有按1/Vi展开。每份贪心取item达到Vi/3−nu_i，必要时trim，保持原item子集且support多项式；normalized rational质量的和/差/除法须按bit长度计。

几何item标签可只采前n轮及tail：概率δ(1−δ)^(t−1)与(1−δ)^n均为poly-bit rationals，δ2/35固定。精确有限rational sampling可用common denominator的binary整数区间加rejection，按denominator位长而非其数值或1/probability工作。若要worst-case total-bit界，应给rejection统一cutoff并把极小失败概率吸入overall constant success；不可无说明把unbounded rejection称worst-case poly。

Welfare rounding也需足够概率slack。若直接拿expectation≥|At|/d，不能自动给可测的constant success概率。Explicit XOS可以独立抽每agent support配置并对每item从claimants均匀选一人；给定自身配置，Jensen使被保留概率≥1/2，由其additive witness得expected normalized福利≥|At|/2。准备过的support使每agent值≤6，故达到(2/5)|At|的概率≥1/56；重复并核验即可落实d5/2。General subadditive可把source Theorem11参数先取epsilon1/20，expected≥(9/20)|At|，再接受(2/5)|At|，取得constant slack；不从epsilon1/10的期望正好2/5直接推常数接受率。

这些S_i抽样/接受必须独立于几何过滤标签R_t，以保source Lemma5–7条件化正确。At只按过滤前S_i变化即可满足。至少一agent每轮离开，所以cutoff和union bound只跨poly轮。

还须在最终Proof落实：rational residual targets的精度、poly-support回收、所有计算中间bit长度、sampling cutoffs和最终保留因子的预算。Appendix A提供合适数学接口，但v3只写“固定2倍”而未展示完整实现核算；本记录不因grid存在便把任意未列backend实现全部认证。无需unknown optimal allocation或exponential configuration oracle；explicit XOS可另用poly-size clause/marginal LP来兑现residual支持，但应在后续实现证明明写。

## 10. C的无条件代数部分

Unit-FSLP每positive clause support的原v恰1，故lambda作为有限y给B_v(y)=1；all utilities≤1使log-CONFIG objective≤0，而此y达到0。Item equality可逐item把缺口加到不含它的配置质量上，每item至多拆一条entry，support只增|U|，monotonicity和normalized上界保持值1。没有指数枚举。

同一lambda还能给full positive singleton matching：每正entry选择一个positive clause item，column质量≤FSLP的positive-support容量，行和1，matching整数性给原U的positive injection。n≤m由此自动成立，不输入未知actual allocation。

Floor每坐标损失<1/(4m)，每clause总损失<1/4，tilde总质量∈[3/4,1]，tilde≤原v。原positive支持仍包住全部tilde系数，故同一y在tilde下每entry≥3/4、benchmark≥3/4。Zero/duplicate indexed clauses和unused resources不损这些量词。

若已给成功actual NSW≥1/rho且原utilities≤1，则m_bad个utility<rho^(−K)会使product<rho^(−K m_bad)，与product≥rho^(−n)合并得m_bad<n/K。K=ceil(1/eta)给严格<eta n。c_eta=q_eta/2使quality≤c_eta确为quality<q_eta，边界严谨。变量eta仅承诺poly(K)，不承诺poly(log 1/eta)。这一代数对任何正确固定rho成立；它不自行验证v3宣称的backend数值。

## 11. D shared singleton REPAIR全部组合论

D1给原至少n−D个unit groups保留其disjoint原资源，对其余至多D个groups分别分配不同repair singleton，得到augmented unit actual；D0及D≥n亦合法。Menu是alternative states，不把原clause与repair加权相加；没有新增agents。

D2取任意augmented actual，删掉所有D新resources后仍是原Q的actual allocation。至多D个groups持有任何repair item；其它groups的augmented utility与原utility完全相同。因此原必有γn个≤δ groups，augmented仍至少γn−D个。一个group持多repair也不增加可获救group数，不允许一repair给多group。

D3 YES经D1得augmented全unit，normalized原state全正support必包含于相应分配集合，可取integral lambda，故FSLP feasible。NO经D2得至少(γ−a)n>eta n个低组；**若**C对相同n组给FSLP feasible⇒存在少于eta n个≤c_eta的actual，便矛盾。因此测试该显式0/1 FSLP即可deterministic promise-decision，无需运行随机finder，也无derandomization。此逻辑只用positive success probability推出存在。

阈值需沿正确backend/rho走；不能先假定C成立再把本D的条件推理说成独立证明C。固定γ−a、same-n计数、D≤a n及nD显式新增states均必要。NP语言若确Karp-reduces至该explicit promise，则P=NP是deterministic LP测试的后果；本记录没有给这样的source reduction。

## 12. E全部原UM jobs、zero与counts

给任何实际disjoint item allocation，按原菜单选达到v_g(T_g)的原indexed state，并令r_g为其原utility。每selector在所选原root执行time1。仅所选state的allocated positive-resource incidence jobs送到其各自原resource time1；该selected state的其它incidences全部在原root；所有unselected-state incidences全部在各自root，包括time0的原jobs。

每original incidence identity与selector恰执行一次。Selected root真实load=1+Σ_all p−Σ_allocated_positive p=2−r_g；unselected roots load1。Disjoint actual sets保证每resource最多一枚exported incidence job，load≤1。未export zero jobs不占resource，但仍在原roottime0执行。并未把internal floor coefficients替换物理处理时间。

于是全矩阵C≤2；successful quality-count保证只能控制同n个selected roots中有多少超过2−q_eta，不能改成所有machines makespan≤2−c_eta。Unit actual时同一构造全load≤1，至少一unit selector给ordinary OPT下界1，所以OPT恰1。D1修复后还包括全部新增repair states jobs，未删除原state。

S states、m originalresources、I explicit incidences时机器S+m、jobs n+I，finite entries为S+2I；m≥1和nonempty menus给合法非空machine集。Repair增加nD roots、D resources、nD positive singleton incidence jobs、nD selector endpoints，selector仍原n枚。若材料化额外zero incidences，须照实加到I并保留；不能把所有implicit零坐标自动算成没有job又宣称逐job完整。Dense (S+m)(n+I)及binary原时间编码规模均按explicit augmented input多项式。

## 13. Final scope与下一步

A独立成立；B1强fractional residual数学量词真实存在于primary concave-extension接口；post-Lemma8 comparison机制确可针对任意π而不用integral benchmark。C的LP/normalization/floor、D的shared-singleton counting及E的实际全job负载账均可核。

但v3的已声明60000与1/3000000不能从本次actual source检查签出：至少必须处理μ代回、任意Bernoulli参数、shifted f theorem前件、常数成功事件与有限位/采样实现。上方(S1)–(S6)是一条可独立核的保守替代数学链，允许下一版放大到400000d²、最终unit NSW1/20000000和rho2^30；不是改写已冻结v3。若下一版缩为explicit XOS并用另外的新lemma，应另读其Exact，不假称本记录先审了它。

没有作者Proof读后、software/finite execution、source hardness、all-group constant minimum、general UM solver或global novelty认证。保留v1/v2/v3真实流程与原字节，等待root实际读本记录后路由正式修订。
