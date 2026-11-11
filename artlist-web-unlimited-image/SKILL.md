---
name: artlist-web-unlimited-image
description: Generate or edit images through Artlist's website using Unlimited mode, including Nano Banana 2.1 at 1K, image references, result review, and delivery. Use when the user requests Artlist web image generation or asks to use its Unlimited option; use artlist-web-unlimited-video for video generation.
---

# Artlist 网页 Unlimited 生图

用于 Artlist 网页图像生成与图片编辑。尊重用户指定的模型、画幅、分辨率、参考图、用途和计费条件。优先使用已有的 Artlist 插件能力；当用户明确要求网页 Unlimited，或者插件不能验证网页的 Unlimited 资格时，使用已登录的 Artlist 网页，并遵循当前 computer-use 工具说明。不要假设插件调用享有网页 Unlimited 资格。

## 准备

1. 找到并查看用户指定的原图及其上下文；区分身份、服装、道具、风格和构图等参考用途。保留原文件，不覆盖或擅自替换已采用资产。根据任务写明变更与需要保持的内容；人物一致性生成后必须实际对照。
2. 核对网页账户、生成模式、目标模型、图像尺寸、数量和 Unlimited 状态。不同账户、模型、分辨率和设置的可用性可能变化，以提交时页面为准。若用户要求免费或 Unlimited，确认当前设置显示 Unlimited 已开启，再提交；不可用时说明具体状态，不擅自换成付费生成。用户已授权本次生成及普通费用提示时，按会话授权操作；如工具明确要求用户在看到报价后再次确认，遵守该工具要求。
3. 生成前清空上一次任务的无关提示词和参考，核对素材缩略图、用途、实际引用标签及最终提示词。网页可能在切换模型或模式后保留旧内容；不要根据编号推测素材。记录实际模型、设置、提示词和来源。

## 网页操作

- **图片参考上传的首选路径是已验证的 CDP + Playwright 脚本**：使用真实 Chrome 的独立登录 profile，通过 `set_input_files` 写入隐藏的 `<input type=file>`，再确认缩略图/参考标签后生成。此方法不会打开系统文件选择框。本 skill 附带 [scripts/artlist_storyboard.py](scripts/artlist_storyboard.py)，这是已使用的 Nano Banana 2.1 生图流水线；安装与运行见下方。其他模型按实际页面适配，不擅自切换用户指定模型。
- **遇到菜单重渲染时，不要继续使用两步式 `filechooser` 流程操作 Artlist Image → Upload Image**。此前该路由出现过菜单收起导致 `observed page or control state changed`、隐藏输入框 `element not visible`。失败时不要反复重试或回到系统文件选择框；改用 CDP 脚本。若 CDP 暂不可用，优先在 Artlist 网页用 `My References` 选择已入库素材；否则说明阻碍并停下。
- 仅当 CDP 脚本不可用且用户明确要求探索其他浏览器上传路径时，才按当前浏览器工具文档尝试 chooser 流程；把它视为未验证替代路径，先做单张小范围验证，确认页面缩略图和参考标签后才继续。
- 使用当前浏览器与 computer-use 文档描述的方式，选择 Image、模型和生成设置。用户未指定时，根据用途选择适当画幅及输出数量；不要假定 1K 或 16:9 对所有需求最合适。
- 本次在 2026-11-05 的已登录网页实测：Image → Nano Banana 2.1 → generation settings → 1K；16:9、1 张图、Medium thinking、Web Search 关闭，页面显示 Unlimited 开启，生成按钮显示无限符号。以上是一次实测，不保证其他账户或未来仍免费。Web Search 开关在当时页面标注会消耗额外积分，按需求谨慎设置。
- 使用 CDP 脚本上传本地参考图后，等待上传完成并确认缩略图与 `@imgN` 标签数量、顺序和用途都正确；用户要求基于特定图片改造时，将该图片作为身份或内容参考，明确只修改哪些特征。任何上传路线都必须先核对实际引用，禁止在没有确认参考图已挂载时提交生成。
- 提交后跟踪同一任务到完成或明确失败；不要因页面延迟重复提交。完成后打开结果详情，确认模型、尺寸、图像和参考用途，检查主要视觉要求与人物身份是否保留。生成成功只是候选，不代表用户审美确认。

## 附带脚本与安装

整目录安装，保留 `scripts/` 与 `requirements.txt`；适用于能运行 Python、Playwright 并连接本机 Chrome CDP 的宿主。仅有截图/点击能力的 WorkBuddy 环境不能直接运行此方案；先检查执行能力，不声称已切换成功。

在本 skill 目录执行：

```powershell
python -m pip install -r requirements.txt
python scripts/artlist_storyboard.py --name TEST --prompt-file "C:/素材/prompt.txt" --refs "C:/素材/a.png;C:/素材/b.png" --out "C:/输出/candidate.png" --prepare-only
```

- 脚本默认连接 `127.0.0.1:9222`，未启动时使用 Windows Chrome 和独立 profile `C:/chrome-cdp-profile` 自动启动。跨机器需调整脚本顶部 `CHROME`、`PROFILE`；CDP 地址与启动端口必须一致。本机调试端口不要暴露到公网。
- 首次在这个独立 Chrome 窗口登录 Artlist，然后重新运行。无需安装 Playwright 自带 Chromium，脚本连接已安装的 Chrome。
- `--prepare-only` 只设置 Nano Banana 2.1 / 1K / Medium / 单张 / 默认 16:9、上传参考与填写提示词，**不会点击 Generate**。在 Chrome 核对素材身份、实际标签和顺序、提示词、模型设置、Unlimited 后，可手动生成；需要完整流水线时去掉该选项。`--ratio` 可选 16:9、9:16、1:1；`--project` 可指定 Artlist 文件夹 URL。
- 脚本会清空旧图片参考，限定唯一的 `input[type=file][multiple]`，直接 `set_input_files`，等待参考数量完全匹配。数量匹配不能证明身份与顺序正确，必须实际核对。选择器不存在、有多个匹配、旧参考清不掉或 Unlimited 未开启时停止，不退回循环点击上传菜单。
- 完整流水线会点击 Generate，等待新素材并用网页 Download 保存；同一页面不要并发运行其他生成，以免新素材匹配混淆。超时或中断后先查网页任务，不能直接重跑造成重复提交。输出文件存在时停止，保留原件。
- 该脚本来自 2026-11-08 的生图实用版本，本次发布补了停止条件与 prepare-only。历史成功不等于当前每个模型、账户、页面均已验证。页面变化时检查选择器后再运行。

## 交付与记录

- 展示平台原生生成结果；如用户需要文件或项目交付，通过 Artlist 支持的下载功能保存，并核对实际路径、文件类型、像素尺寸及内容。给候选文件使用清晰的新名称，保留源图、提示词和生成信息。不要把网站预览截图冒充原图或用未授权方式绕过下载限制。
- 2026-11-05 生成一张奥利弗造型候选时，Nano Banana 2.1 / 1K / 16:9 / Unlimited 网页显示完成，详情显示 PNG，画面为正面全身单视图；点击下载后 Chrome 报 `ERR_BLOCKED_BY_CLIENT`，本地原图未确认保存。若再次遇到拦截，记录实际错误，保留可访问的生成详情并说明未保存；可检查浏览器提供的正常下载途径，不绕过安全限制。不要把这次错误当作所有 Artlist 下载都失败。
- 用户要求多视图或成套参考时，明确每幅实际视角与身份一致性，区分单张全身概念图与已完成的多视图资产。只有用户确认后，才将候选标为采用或更新项目引用。
