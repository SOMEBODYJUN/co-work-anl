# 报告优先的实际研究入口

当前主任务是调查、经济思维学习、机制研究和新闻式深度报告。计算器另作普通编码任务。
旧周期的17/20保留原记录；本入口通过显式profile切换报告交付，不把旧缺项改成通过。

## 从真实输入开始

`research/program/questions.json`已有48个研究问题，分12组争议。每题有真正竞争的解释、
能区分解释的观察、原始资料路线、与其他问题的接口及产物路径。它们是任务种子，
不是48项已完成研究；新材料可以继续拆题、增加问题，不能把48当研究范围上限。

`research/program/article_selection.json`保存实际甄别结果，给文章名、原发URL、作者、
时间、采用范围与理由。正文在研究工作区cache，和短摘要分开，附真实段落定位与哈希。
官方数据按观测用途使用，政策文本按制度/承诺用途使用；思想教材按实际论证选，
不依作者身份、赞成人数或措辞强硬程度入选。

在同一完整身份的原工作区运行：

```sh
python work.py session start --actor "<完整身份>" --profile report-first
python work.py session next --actor "<完整身份>"
```

显式profile用` s18_editorial `替换计算器阶段，并把思维上下文、文章甄别、问题图纳入
交付。正文、机制和数据工作仍须完成；旧默认profile保留兼容，不能混用完成声明。
附带的旧数学版work.py默认指向数学清理分支，不用它恢复经济任务。先取得经济分支，
然后始终使用仓库根目录入口。

## 1．取得原文与段落

准备`articles.json`：

```json
{"articles":[{"id":"B20","author":"Andrew Batson","published_at":"2020-05-03","title":"Why China isn't sending money to everyone","url":"https://andrewbatson.com/2020/05/03/why-china-isnt-sending-money-to-everyone/","fetch_urls":["https://public-api.wordpress.com/rest/v1.1/sites/andrewbatson.com/posts/slug:why-china-isnt-sending-money-to-everyone/"]}]}
```

```sh
python work.py analysts fetch-bodies --manifest articles.json --cache work/<身份>/cache/bodies
```

工具取得公开HTML/WordPress正文/PDF文字并形成段落；只有短摘要、元数据或登录页时
留为`retry_queued`。取得正文仍不是实读完成，读者须检查范围。

原生网页/PDF阅读器补得正文时，用`import-bodies --manifest <capture.json> --cache ...`
桥接。每文必须有原字节路径、正文路径、匹配的text_sha256及paragraphs；不能把模型
摘要伪装成原文。原始全文不随公开代码提交，分享研究笔记与精确原文链接。

## 2．装配任意模型可以执行的任务

```sh
python work.py analysts reading-packet --corpus work/<身份>/cache/bodies/manifest.json \
  --articles B20,B23P,P15,P26,S24,W25,Z24,Z26 \
  --question "融资承接能力、实际政策选择和损失分配怎样影响私人收入修复？" \
  --guidance docs/THINKING_EXTRACTION.md --output work/<身份>/cache/packet-01
```

任务包真实包含：完整段落、作者/时间/URL/哈希、已填问题、来源明确的提炼合同、
输出结构与真实命令。缺文章直接列明，不让模型填`analyst_context`空白后自行脑补。
按实际并发席位把`TASK.txt`交给阅读者；CLI不自行调用付费模型。

## 3．实际阅读与提炼

阅读者分段读取全篇，交result.json：精确命题；世界认识；主体模型；问题优先级；
由线索推解释的动作；跨作者分歧；有向ALL候选机制；主判断；下一项调查。
每个有分量主张用article_id和paragraph_ids回原文。作者明确观点、项目重构和观测
分别标注。多篇支持不足的认识保留暂定，不能只因模型写得流畅就升级。

```sh
python work.py analysts check-result --packet <任务包> --result <任务包>/result.json
python work.py analysts compile-result --packet <任务包> --result <任务包>/result.json --output <任务包>/thinking_context.txt
python work.py analysts build-reading-graph --packet <任务包> --result <任务包>/result.json --output <任务包>/reading_graph.json
python work.py analysts query-reading-graph --graph <任务包>/reading_graph.json --node <机制ID> --output <任务包>/query.json
```

`check-result`失败返回3并指出具体字段，修该项后继续。它核定位、引用和结构，不代替
经济语义复核。查询返回整条共同前提与来源。阅读者写graph_use.txt，说明查询到底
指向了哪项区分观察和调查；再写一份有明确判断的局部分析，不能只有JSON文件。

## 4．扩展主题与真正搜索

按问题表领取具体问题，材料角色分观测、制度文本、思维、机制线索与反证。当前已有
WordPress目录盘点、给定URL批量取正文、Crossref论文发现；原生搜索负责新来源与争议。
RSS/网站地图的通用解析器尚未接入，不把它算成现有能力。沿思维提炼及图查询产生的
缺口定向搜索，连续修订问题与解释。

500—600篇是实读覆盖目标；元数据、下载、实读、思想归纳、机制裁决分别记账。
普通候选立即保存，不逐条做最终报告式终审。承重关系由相邻研究者和独立读者核实。

本轮13篇直接批取实测为9篇取得正文、4篇进入重试（P15、P26、Z24、Z26）；这4篇
通过实际原站阅读捕获与import-bodies进入完整语料。不能把桥接获取说成CLI
单独全部成功。当前13篇原文复读与新观点覆盖见甄别记录，其中多篇属于旧文重新取正文。

## 5．持续研究与发布

报告profile只按实际产物和明确依赖判断阶段失效；不再因每次新增来源删除所有后续
阶段。原文变化与受影响图节点仍须处理，最终复核与发布仍绑定当前版本。
拒审保留已审文件范围，不能把一次拒审扩展成几百条“从未审过”的噪声。

暂时来源失败进入重试，其他题和正文继续；每批回查失败项。两席通常用于实质取证/
推理，一席综合或写作，按问题更换职责。计算器和浏览器不占报告停止条件。

报告以主判断、决定性事实、主体选择、机制和后果为主线。后台记录另存。取得新认识
后继续修报告；实际完成委托的报告与承重核对后才停止，不因保存、节点数或测试数结束。
