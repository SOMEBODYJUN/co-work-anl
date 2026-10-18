# 逐坐标状态一致性下的 Cartesian 资源配额：冻结 Exact v1

ID：UM-COORDINATE-OBLIVIOUS-CARTESIAN-MENU-QUOTA-v1。
2026-10-18，boss11 root。不同于无条件普通UM对象；本页额外限制全体group的状态选择，仅量化此语义子问题。reviewer先只据本Exact独立重构，再实际读作者证明。

整数t>=1，D=2^t。groups g∈F_2^t、resources(a,b)∈F_2^t×F_2^t、每group indexed states ell∈F_2^t。每state支持S(g,ell)={ (a,b): b_i+g_i a_i=ell_i 对每i}，每项质量1/D，恰D项。

额外限制：必须存在t个函数 f_i:F_2→F_2，给每个group选的完整state同时满足ell_i(g)=f_i(g_i)。f_i可任意选，但不能依赖g的其它坐标。给每group任意子集B_g⊆S(g,ell(g))，不同groups的B_g不交；允许资源不用。最大化min_g |B_g|/D，记V_obl(t)。

Exact Statement：每整数t>=1、每一组固定(f_i)，上述部分子集最优值都恰为

V_obl(t)=floor((3/2)^t)/2^t。

上界量化任意partial subsets；下界输出各group恰floor((3/2)^t)项的disjoint真实资源bundle，可用显式大小bit-polynomial的二分图b-matching构造。t1为1/2。floor不能省掉，不称连续分数分配即实际bundle。

范围：这是额外state-consistency语义下的精确配额，不是普通无约束UM的OPT，也不提供将这些函数约束编码成机器负载的gadget。与同一无约束flat family的V_t=1−2^-t对照，仅定位产品解码需要阻止何种跨坐标重选；并不排除其它产品/一致性归约，也不创建hardness源。复杂度按groups/resources/菜单的显式输入总长度，不称poly(t)。
