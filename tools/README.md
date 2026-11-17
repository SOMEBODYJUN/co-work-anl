# 运行工具

当前运行入口是仓库根 `work.py`。研究只依赖现行运行模块、研究 RUN、唯一 registry、正式超边和必要计算资源。

```sh
python work.py --repo <clone> start --actor BossN --save <archive> --token-file <external-token>
python work.py --repo <clone> research search <query>
python work.py --repo <clone> research frontier <object-id>
python work.py --repo <clone> research check
python work.py --repo <clone> checkpoint <paths...> -m '保存研究断点'
```

旧阶段的 board、cleanup、curation、registration-task、map-task 和全仓 final 验收不再存在。新增对象和超边按当前研究 RUN 的回流合同写入，准确绑定正文、证据、版本和剩余义务后再 checkpoint。
