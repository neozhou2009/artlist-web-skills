# Artlist Web Unlimited Skills

Artlist 网页生图与视频生成 skills，可供支持 SKILL.md 的 Codex、WorkBuddy 等宿主安装。网页 Unlimited 与 MCP 调用的资格不同，以当前账户和生成面板为准。

## 安装与更新

下载本仓库最新版本，将需要的完整目录安装到宿主的 skills 目录；不要只复制 SKILL.md。已安装旧版时替换整个对应目录，并重新加载 skill 或开启新会话，避免继续使用缓存的旧指令。

- `artlist-web-unlimited-image/`：生图与图片编辑；附带 `scripts/artlist_storyboard.py` 和 `requirements.txt`，可运行 Nano Banana 2.1 CDP 流水线。
- `artlist-web-unlimited-video/`：视频模型设置、参考上传、任务跟踪与下载；没有附带通用视频自动生成脚本。

## 上传修复

旧发布版要求先打开菜单再用 filechooser；菜单重渲染可能使控件失效。现在优先通过真实 Chrome 的独立登录 profile + Playwright CDP，直接对正确的 `input[type=file]` 调用 `set_input_files`，避免系统选文件窗口。上传后仍须核对缩略图、标签、身份与用途。

WorkBuddy 需要具备本地 Python/Playwright 执行及 Chrome CDP 连接能力。仅有截图点击工具时，安装 skill 本身不会增加这些能力；可以先使用 My References 中已入库素材，不要循环重试失效菜单。

在生图 skill 目录安装依赖并先准备、检查素材：

```powershell
python -m pip install -r requirements.txt
python scripts/artlist_storyboard.py --name TEST --prompt-file "C:/素材/prompt.txt" --refs "C:/素材/a.png;C:/素材/b.png" --out "C:/输出/candidate.png" --prepare-only
```

首次在独立 Chrome 窗口登录 Artlist 后重跑。此命令不会提交生成。核对后可在网页手动生成；去掉 `--prepare-only` 才会执行完整生成与下载。详细前置条件、参数、停止条件见各目录 SKILL.md。

## 验证范围

生图脚本源自 2026-11-08 已使用的图片参考上传与生成流程；本次补齐发布文件、参考数量与 Unlimited 停止条件、prepare-only。视频 Start Frame JPG 的 chooser 成功仅是历史单次记录，不代表所有入口都可靠。脚本依赖网页结构，界面或模型变化后须重新核对；本次发布验证不包含新的在线 Artlist 生成。
