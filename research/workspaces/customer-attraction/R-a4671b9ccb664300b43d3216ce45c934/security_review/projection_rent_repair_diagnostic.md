# 投影外部信用不能自动成为可信rent修复预算

2026-10-25。查重后的接续诊断；只使用已有全参数原模型反例与已审rent编译组件。不认领新原实例、新不可能性范围或half反例。

## 1. 已有rent编译器需要什么

`R-d1dc7a18aded4304a25a87486681fb21/credible_continue/shared_terminal_rent_compiler.md` 的旧目标路径要求**最后一个旧动作已经是旧前缀上的BR**。对其余位置 i 与每个主题 A（含原动作），必须预选真正完整 child-SPE，并用其当前角色收益 d_i(A) 定义可信缺陷。共同终局租金只支付这些真实child缺陷，half代价为 `3(m-1)g`。

`R-3bc48d936f044f12b0fa743482ff5eb0/credible/heterogeneous_prefix_repair.md` 则先要求某一目标尾部已经是真正完整SPE，前缀可信缺陷为

`delta_i=[max_A min_(genuine child-SPE eta) u_i(A,eta)-u_i(target)]_+`。

异质层的half代价 `2 sum_i delta_i+max_i delta_i` 是新Cartesian实例的真实福利稀释；它不是回放策略的actual-node后悔。投影后悔(P4)控制后者，没有控制这些child最小值或所需目标路径尾部的存在性。

## 2. 最末位的直接障碍

设投影计划最后角色当前旧主题不是BR，存在旧主题T给严格增益。任何完整Cartesian目录的辅助保险都不能保留该最后旧动作：最后角色只改旧坐标到T、保持所有辅助坐标不变，其辅助收益完全不变，旧严格改善仍成立。此论证不需要估计保险大小，也不能由root-only或全层rent消除。

这是旧 `R-4ffa8b85fa8847e09e45dcafc8e1326f/deletion/cartesian_terminal_obstruction.md` 的同一终端原理；不把它扩大为非Cartesian或允许改旧尾部后的修复不可能。

## 3. 外部信用小、投影末位后悔小，修复福利变化仍可无界

直接复用 `R-7e9f44beea424d469713364afe7dd180/global_proof/deleting_opt_external_customers_obstruction.md` 的全部参数族：两人、主题A/B/C，类型 `A:Q,B:3,C:2,BC:2Q-4`，Q>=4。唯一最优并集 O=A∪B，O外仅两个C客户。

原完整SPE可取实际 BC。原福利 `2Q+1`、实际外部信用 E=2；投影后保留同一策略/标签，实际内部福利 `I=2Q-1`。原B历史末位选C原得Q；投影后仅得Q-2，而改A得Q，所以最后投影后悔恰为2。根投影后悔为零；故全实际投影后悔恰等于 E，完全吻合旧PATH-REFUND。

投影游戏唯一完整SPE为BA，福利 `3Q-1`。因此

`W_exact_projection-I=Q`，

在外部信用固定 E=2时无界。特别地，不存在独立于实例的常数K，使“投影后找某精确SPE，其福利至多I+K E”对所有原完整SPE都成立。

这里关键是修复福利上升，不能拿投影游戏某个half结论 `OPT<=2W_exact_projection` 反推原 `OPT<=2(I+E)`。换最差投影SPE也无济于事，因为本族投影SPE唯一。该事实已经由旧删除反例承担；本文只明确指出它排除哪一个从外部信用直接接rent/归纳的推断。

## 4. 尚可能的真实接点

SEC-OPT? 不要求换一份投影SPE，所以不被上面的修复障碍否定。但若用rent路线证明它，必须额外给出：可保留目标尾部的真实BR/SPE，或允许改尾后原福利的准确共同修正项；再控制真正child可信缺陷而非仅actual后悔。旧实例表明E单独不能支付这些福利变化。

目前没有得到上述控制。把整个外部信用E当作rent购买力，再在最终福利中照算E，会重复支付同一份信用；把conditional half稳健编译式当作独立预算则是循环。本轮因此停止这一直接修复推断，保留SEC-OPT?为未证、真正强/弱根安全桥和Q-CAG-HALF仍OPEN。
