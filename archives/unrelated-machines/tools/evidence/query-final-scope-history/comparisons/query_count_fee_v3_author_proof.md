# 合格查询计数和费用的证明v3

对象与ID见独立Exact。采用一般双见证分离v2的同一单调染色。该算法每机标至多一query色；未标q机器负荷≤1.5T，标q机器负荷≤T+Σ_{r∈Q\{q}:σ0r=i}p_ir。

令G为构造的τq实际全机负荷≤βT者（可直接精确扫描验证）。若q不合格，则某超载机器i必须标q（β≥1.5），而其其它query初态总量>cT，从而LQ_i>cT。为每个坏q选最小编号这样的i。每机仅一色，故该选择是坏query到Rβ机器的单射。坏数≤Rβ，|G|≥d−Rβ。Aq仍两两不交，因此合格query的fee总和≤W，给费用平均。

η=0时LQ_i=0、Rβ=0，正确结论是全部d合格，不能严格超过d。η>0时令M=Σq p_sigma0q,q≤ηTd。如果Rβ>0，所有重机的质量严格大于Rβ cT，所以Rβ<M/(cT)≤ηd/c；若Rβ=0，因ηd/c>0同一严格不等式也成立。故|G|≥d−Rβ>(1−η/c)d，得到所列整数下界和非严格费用界。W=0时平均仍为0，无额外严格费用断言。

更强分组计数：每个重机若有k枚queries，质量≤kηT；LQ_i>cT强迫k>c/η，即k≥s=floor(c/η)+1。不同源机的queries集合不交，故Rβ s≤d，从而Rβ≤floor(d/s)。η<c给s≥2，所以d−floor(d/s)≥ceil(d/2)>0。只作整数除法，不按s数值循环。

若物理fee合同要求全部singletons在βT内≥F，则G中的实际τq各费≥F，总支持费≤W；故W≥|G|F≥(d−Rβ)F，并有分组加强。此结论保持原改派费定义；并不把σ0旧unit背景费退款视作负权，也不把源NO解码或两strict见证生成当免费能力。

复杂度只增加计算LQ、Rβ、η比率整数除法和逐q全机回算，均为总输入位长的确定性多项式。T>0使除法合法；T=0仍由原分离v2处理，不放进本正T质量比合同。


## v3的heavy query必要条件

记c=β−1≥1/2，H为单件初态query>cT的个数，S=d−H。每台rich machine若含heavy query，就把它收费给一枚heavy；每query仅一源，所以这样的机器至多H台。没有heavy的rich机每枚query旧端≤cT，严格总量>cT至少要2枚非heavy queries。各机源query组不交，故其数≤floor(S/2)。因此Rβ≤H+floor(S/2)，原坏色单射给good≥d−Rβ≥S−floor(S/2)=ceil(S/2)。原不交fee求和给W≥ceil(S/2)F。

若W≤κF、F>0，则整数ceil(S/2)≤κ，故≤floorκ；因此S≤2floorκ，H≥d−2floorκ。κ<1时条件可能仅给平凡必要形状，不保证构造存在；本结论无充分性。新增heavy阈值是严格>cT，等于cT的job属于非heavy，rich总量严格>cT仍需要至少2枚，等号无漏洞。使用的费必须是原非负改派费，不能扣background退款。
