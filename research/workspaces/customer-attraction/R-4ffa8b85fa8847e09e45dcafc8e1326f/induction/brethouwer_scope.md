# Brethouwer 2018 primary PDF 范围核验

2026-10-24。本页是文献适用范围检查，不是重证其数值下界。

Primary source: Jan-Tino Brethouwer, *The quality of equilibria in generalized market sharing games*, University of Twente master thesis, December 3, 2018.

- Landing: https://essay.utwente.nl/essays/76986
- PDF: https://essay.utwente.nl/fileshare/file/76986/Brethouwer_MA_EEMCS.pdf
- 本轮 browser source `turn4view0`；Root 若要最终引用，需自行 open 此 URL 后取得自己的有效引用。

## Source scope (concise)

Definitions 3.4/3.8/3.12 (printed pp. 8–10) use full preceding-action observation and SPE in every subgame; the criterion is worst SPE. Definition 4.2 (p. 13) additionally requires downward-closed strategy sets. Section 6.2 removes downward closure: Definition 6.15 (p. 33) permits a separate arbitrary strategy family S_i for each player and equal resource sharing.

Theorem 6.22 (p. 38; PDF page index 37) states a four-player covering-game lower bound 2.0558498235 from an integer program, with 28 valued items. The preceding paragraph uses 4 and 5 actions for players 3 and 4. It does not assert common strategy families and does not print the four-player values, incidence table, or full strategy certificate. Thus the displayed numerical result cannot be treated here as an independently verified Q-CAG-HALF counterexample.

Definition 7.2 (pp. 39–40), equation (60), imposes shared misery: whenever a later entrant decreases an earlier payoff, the entrant's instantaneous payoff cannot exceed the earlier player's resulting payoff. Lemma 7.4 requires this condition. Theorem 7.6 and Corollary 8.2 concern symmetric singleton games, not arbitrary common catalogs.

## Independent model check

一般 CAG 不满足 equation (60)。取两个共同目录主题 A={x}, B={x,y}。玩家先选 A 得即时收益 1；后来玩家加入 B 后，早者降为 1/2，而后来者收益 3/2。因此 shared-misery 的必要蕴涵已失败。这个直接计算只是否定工具的普遍适用性，不是否定主目标。

PDF 印页38还明确报告其三人例6.21在添加向下闭包后改变了 SPE。因此不能凭静态子主题支配，在顺序模型中免费完成向下闭包、删子主题或角色对称化。

## Exact remaining obligation

若要使用其四人 >2 数值，需要先取得原始四人客户值、各 S_i 和完整策略，并做定义级精确验证；再另证如何保留全部离轨理性地转为一个共同目录。原论文的现有陈述没有执行这一步，也没有证明本题一般 half。
