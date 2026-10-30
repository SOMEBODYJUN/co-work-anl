# 逐坐标状态一致性下的 Cartesian 资源配额：作者证明 v1

对应UM-COORDINATE-OBLIVIOUS-CARTESIAN-MENU-QUOTA-v1。root独立推导。证明冻结后不主动交给尚未冻结Exact-first重构的reviewer。

固定任意函数f_i。第i坐标两条线L_i(0)={ (a,b):b=f_i(0)}、L_i(1)={ (a,b):b+a=f_i(1)}各2项且恰交一项c_i；另各有一独占项e_i(0),e_i(1)。三个是彼此不同真实坐标resources。任一selected group state支持是∏_i L_i(g_i)，故所有group的支持并集恰为这些三个坐标符号的全积，大小3^t，独立于函数。

上界：若最小bundle大小k，则Dk<=3^t，故k<=floor(3^t/D)=floor((3/2)^t)。由于每bundle项质量1/D，此给Exact上界，允许任意partial/discard资源。

下界：对并集内每个resource u，把其单位容量在所有兼容groups间均分。若坐标符号为c_i则g_i任意，若为e_i(g_i)则该g_i被固定；因此若u有h个common坐标，兼容degree为2^h，给每兼容group 2^-h。每resource总分配1。

固定group g，它在每坐标支持里有一个common符号和一个own-exclusive符号，故收到的分数总量为∏_i(1/2+1)=(3/2)^t。由此对任意group集合A，总收到 |A|(3/2)^t，来自N(A)的每项总供给<=1，推出|N(A)|>=|A|(3/2)^t>=k|A|，k=floor((3/2)^t)。这是所有子集的Hall配额条件，不只检查全部groups。

将每group拆成k个槽，每槽接该group所有支持resources。任意槽子集X所触及group集合A满足|X|<=k|A|，且N(X)=N(A)；上式给Hall。因此存在覆盖全部槽的整数matching，各group得到恰k枚不同真实资源，跨group不交。

k<=D，故槽总数Dk<=D²，与原显式资源总数D²同阶；显式边数<=DkD<=D³，已有原family全部菜单incidence也是D³。标准增广路二分matchingdeterministic且按这些显式计数poly，所有fraction只用于证明Hall，算法无需展开巨分母。每有限权1/D位长O(t)。t1:k1，valid。

因此对每固定(f_i)与进一步优化f_i，值皆相同。它趋零约(3/4)^t，但ordinary family允许ell_i(g)依赖其它g坐标，故不能把本受限语义冒充ordinary makespanNO。
