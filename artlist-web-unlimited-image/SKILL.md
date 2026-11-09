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

- 使用当前浏览器与 computer-use 文档描述的方式，选择 Image、模型和生成设置。用户未指定时，根据用途选择适当画幅及输出数量；不要假定 1K 或 16:9 对所有需求最合适。
- 本次在 2026-11-05 的已登录网页实测：Image → Nano Banana 2.1 → generation settings → 1K；16:9、1 张图、Medium thinking、Web Search 关闭，页面显示 Unlimited 开启，生成按钮显示无限符号。以上是一次实测，不保证其他账户或未来仍免费。Web Search 开关在当时页面标注会消耗额外积分，按需求谨慎设置。
- 上传本地参考图前读取当前浏览器 file-uploads 文档；在 Image 输入菜单中选择 Image → Upload Image，先监听 filechooser，再点击上传控件并使用返回的 chooser 选择绝对路径。等待上传完成，确认参考图缩略图与标签，并确认生成按钮已启用。用户要求基于特定图片改造时，将该图片作为身份或内容参考，明确只修改哪些特征。
- 提交后跟踪同一任务到完成或明确失败；不要因页面延迟重复提交。完成后打开结果详情，确认模型、尺寸、图像和参考用途，检查主要视觉要求与人物身份是否保留。生成成功只是候选，不代表用户审美确认。

## 交付与记录

- 展示平台原生生成结果；如用户需要文件或项目交付，通过 Artlist 支持的下载功能保存，并核对实际路径、文件类型、像素尺寸及内容。给候选文件使用清晰的新名称，保留源图、提示词和生成信息。不要把网站预览截图冒充原图或用未授权方式绕过下载限制。
- 2026-11-05 生成一张奥利弗造型候选时，Nano Banana 2.1 / 1K / 16:9 / Unlimited 网页显示完成，详情显示 PNG，画面为正面全身单视图；点击下载后 Chrome 报 `ERR_BLOCKED_BY_CLIENT`，本地原图未确认保存。若再次遇到拦截，记录实际错误，保留可访问的生成详情并说明未保存；可检查浏览器提供的正常下载途径，不绕过安全限制。不要把这次错误当作所有 Artlist 下载都失败。
- 用户要求多视图或成套参考时，明确每幅实际视角与身份一致性，区分单张全身概念图与已完成的多视图资产。只有用户确认后，才将候选标为采用或更新项目引用。
