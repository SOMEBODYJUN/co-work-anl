# 开源 OCR 候选与能力边界

项目内已包含 JiangZhexin/handwritten-math-notes-to-latex 的原始完整源码及 MIT 许可证。它提供转写、数学核验、记号管理和 LaTeX 检查规程，不是一个新的 OCR 模型。

可选第二识读来源：

| 项目 | 可辅助的工作 | 本项目采用方式 |
| --- | --- | --- |
| [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) | 中文文字、文档版面及公式识别；其公式流水线说明支持手写公式 | 对困难裁图生成第二候选，与原图和视觉模型比较 |
| [Pix2Text](https://github.com/breezedeus/Pix2Text) | 混合文字/公式到 Markdown；文档说明支持中文识别 | 作为另一种读法，保存原始输出与差异 |

未在本包安装上述模型或下载权重，也未测得它们在用户整批中文手写笔记上的准确率。不要把论文/项目的印刷体或通用数据集指标当作这批手稿的指标。依赖和模型许可需按实际下载版本检查。可先选小字、中文、公式、旁注、跨页证明等代表区域做试验，再决定是否值得加入；不是工具越多就越可靠。

安装额外 OCR 仅在实际环境允许、资源合适时进行。优先本地推理；未经用户明确授权不要把私有手记发送到第三方在线演示站。无可选 OCR 时可以使用视觉模型逐区识读，但不能伪称做过第二 OCR 引擎验证。

官方视觉模型说明提醒小字、旋转、非拉丁文字和图形等仍可能出错，图像也可能被缩放。因此采用“全页定位 + 局部高分辨率 + 符号上下文 + 新审阅者盲读 + 回图”组合。单纯多次调用同一模型不构成正确性的保证。

核查来源：

- [OpenAI Images and vision](https://developers.openai.com/api/docs/guides/images-vision)
- [PaddleOCR 公式识别流水线](https://github.com/PaddlePaddle/PaddleOCR/blob/main/docs/version3.x/pipeline_usage/formula_recognition.en.md)
- [Pix2Text 官方仓库](https://github.com/breezedeus/Pix2Text)
