# query-witness-originals 三源交付

完整external overlay在 `/workspace/scratch/37f0f9248cfc/boss4-next-cache/query-witness-originals-staging/`，各文件保持最终repo相对路径。子agent未执行Git、认证、claim、done、checkpoint。`semantic-receipts.json`三源均为integrated，须由Boss完成自己的审阅及正常发布步骤。

新增正式计算对象：`archives/unrelated-machines/state/计算/双见证查询染色与固定矩阵证书的原程序核验--计算.md`。证据入口：`archives/unrelated-machines/tools/evidence/query-witness-originals/README.md`，含原字节、全文比较依赖、恢复的首次实际原入口运行、可复现包装器和新保存见证检查。

已有成功的两个原入口各首次run已恢复到 `runs/original-replay-001`，Python3.12.14、均exit0、stderr空，不再次执行。新检查因现有摘要误把a_j当流入权而进行一次保存输出算术核对，未调用原入口或replay、未重新枚举32或5184；48保存分配记录、284任务归属、314机器负载、10格a/b差异，全通过。精确命令及stdout/stderr在证据runs和本工作区都保留。不能将恢复记录冒称本续轮新run，不能把48记录称不同调度数。

`editorial-corrections.json`给三个已交付正文的精确old/new及before/after SHA，stage内有对应全文纠正副本。拷入前核before SHA防止覆盖并发正文：匿名令牌三源审查目标b_j；向量贪心/累计路径3groups5states；对称重置/双见证v3正T、正分母、≤η、η0分支。原冻结源和旧证据字节未改。

`source-read-manifest.json`保三源完整inventory与原字节核对、全文实读比较路径及指纹。`relation-notes.md`已作关系判断；本批不重复done已完成的数学正文/三个fixed证书JSON/旧运行JSON，阶段三正式图仍待建。

后续候选（未认领，需Boss复核实时状态）：

| ID | 路径 | 字节 | 继续用途 |
| --- | --- | --- | --- |
| ba9c71e2bc6052c4f3c0 | tests/audits/unrelated_machines/single_home_cascade_query_separation.py | 16781 | 唯一home强域全部子集实际实现 |
| a6f3780bd6fb78eeece6 | research/reviews/unrelated_machines/single_home_cascade_query_separation_review.md | 3035 | v2全部子集合同与独立性历史 |
| 2a4e61a6d5dcbe202dce | research/reviews/unrelated_machines/two_witness_query_separation_review.md | 3561 | 本批作为依赖已全文实读，尚未登记其done；审查顺序/实际运行归属 |
| 7fb54f095857efa3804e | history/source/notes/unrelated_machines/two_witness_query_separation_v2_author_proof.md | 3238 | v2目标时间阈值的作者原证明 |

`delivery-paths.json`记录overlay各交付文件的相对路径、字节、SHA，供Boss拷入后逐项复核；它自身不递归记录自身。
