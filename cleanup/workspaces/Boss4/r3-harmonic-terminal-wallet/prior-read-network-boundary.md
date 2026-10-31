# 前批非秘密只读检索错误及阶段

此记录只说明上一批r3-fresh-source-attack的一次不必要的大范围读取，不是本批必要源缺失。

当时对冻结commit的整个`research`（未限制扩展名）做只读`git grep`。partial-clone缺少某些blob，Git尝试按已有配置从原远端读取。该进程长时间无结果，收到Ctrl-C中断后工具输出的完整非秘密错误是：

```text
fatal: unable to access 'https://github.com/SOMEBODYJUN/co-work-anl.git/': Proxy CONNECT aborted
```

随后该进程exit130。这个消息定位于建立代理CONNECT隧道时被中断；没有观察到目标站点HTTP401/403、认证挑战、登录提示或凭据提交。因尚未观察到目标HTTP连接建立，不能将它叫作已发生的目标Git认证失败；也无法从该消息推断代理内部是否使用既有认证。没有更换/查找凭据或重复该读取。

随后限定`research/**/*.md`的只读相关引用检索成功。本批必要五源及四运行依赖都从本地冻结对象取得并核SHA；为防无关lazy-fetch，原件提取设置`GIT_NO_LAZY_FETCH=1`。如果必要本地对象缺失，将保真实错误并报告缺口，不重试认证、不找备用凭据。没有Git写、同步、认领、完成或认证操作。
