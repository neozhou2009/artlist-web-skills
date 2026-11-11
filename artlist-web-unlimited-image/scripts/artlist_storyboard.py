#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Artlist 网页 Unlimited 故事板生成（CDP + Playwright）

用法:
  python artlist_storyboard.py --name SC002 --prompt-file prompt.txt \
      --refs "a.png;b.png;c.png" --out out.png [--project URL]

前提:
  1. 用独立 profile 启动 Chrome（登录过一次 Artlist）:
     chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\\chrome-cdp-profile"
  2. 该窗口已登录 Artlist，账号 Unlimited 可用。

流程: 设置 Nano Banana 2.1 / 16:9 / 1K / Medium / 1 张 / Unlimited
      -> set_input_files 直接上传本次参考图（不弹文件选择框）
      -> 填提示词 -> Generate -> 等完成 -> 打开详情 -> Download -> 存到 --out
"""
import argparse
import json
import os
from pathlib import Path
import subprocess
import time
import urllib.request

from playwright.sync_api import sync_playwright

CDP = "http://127.0.0.1:9222"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PROFILE = r"C:\chrome-cdp-profile"
# 默认进 Artlist 生成页；需要把素材落在指定项目/文件夹时用 --project 传该文件夹 URL。
DEFAULT_PROJECT = "https://toolkit.artlist.io/new?mode=image"


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def ensure_chrome(url, timeout=45):
    """9222 没响应就用独立 profile 拉起 Chrome；已登录态保存在 PROFILE 里。"""
    def alive():
        try:
            with urllib.request.urlopen(CDP + "/json/version", timeout=2) as r:
                return r.status == 200
        except Exception:
            return False

    if alive():
        log("cdp chrome: already running")
        return
    if not os.path.exists(CHROME):
        raise SystemExit(f"Chrome not found: {CHROME}")
    log("cdp chrome: starting")
    subprocess.Popen(
        [CHROME, "--remote-debugging-port=9222", f"--user-data-dir={PROFILE}",
         "--no-first-run", "--no-default-browser-check", "--new-window", url],
        creationflags=getattr(subprocess, "DETACHED_PROCESS", 0)
        | getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0),
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    deadline = time.time() + timeout
    while time.time() < deadline:
        if alive():
            log("cdp chrome: ready")
            return
        time.sleep(1)
    raise SystemExit("cdp chrome did not come up; check the profile and login state")


def connect():
    pw = sync_playwright().start()
    browser = pw.chromium.connect_over_cdp(CDP)
    ctx = browser.contexts[0]
    pages = [p for p in ctx.pages if "artlist.io" in p.url]
    page = pages[-1] if pages else (ctx.pages[0] if ctx.pages else ctx.new_page())
    return pw, browser, page


def ensure_settings(page, ratio="16:9"):
    # 模型 -> Nano Banana 2.1
    page.get_by_role("button", name="Select model").click()
    page.get_by_role("menuitem", name="Nano Banana 2.1").click()
    log("model: Nano Banana 2.1")

    # 画幅/画质/思考档/张数
    page.get_by_role("button", name="Open generation settings").click()
    page.wait_for_timeout(400)
    for radio, label in ((ratio, ratio), ("1K", "1K"), ("Medium", "Medium"), ("1", "1 image")):
        try:
            page.get_by_role("radio", name=radio, exact=True).click()
            page.wait_for_timeout(200)
        except Exception as exc:
            raise SystemExit(f"Cannot confirm setting {label}; generation stopped: {exc}")
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)

    # Unlimited 开关
    sw = page.get_by_role("switch", name="Unlimited")
    checked = sw.get_attribute("aria-checked")
    if checked != "true":
        sw.click()
        page.wait_for_timeout(300)
        checked = sw.get_attribute("aria-checked")
    log(f"unlimited: {checked}")
    if checked != "true":
        raise SystemExit("Unlimited is not enabled; generation stopped")


def attach_refs(page, refs):
    # 只认 multiple 的那个 file input；DOM 顺序会变，不能用 nth()。
    # 有些页面状态下参考图容器还没挂载，先点一下 Image Reference 再试。
    sel = 'input[type=file][multiple]'
    # 上一次失败可能残留参考图，占满 14 个槽位后上传控件会消失：先清空
    cleared = page.evaluate("""() => {
        const b = [...document.querySelectorAll('button[aria-label]')]
            .find(x => x.getAttribute('aria-label') === 'Clear all references');
        if (!b) return 'none';
        b.click();
        return 'cleared';
    }""")
    if cleared == 'cleared':
        page.wait_for_timeout(2500)
        log("cleared leftover references")
    if page.locator('button[aria-label="Remove Image Reference"]').count() != 0:
        raise SystemExit("Old references remain; clear them before retrying")
    if not refs:
        return
    if page.locator(sel).count() == 0:
        try:
            page.get_by_role("button", name="Image Reference").click(timeout=5000)
        except Exception:
            pass
        page.wait_for_timeout(1500)
    if page.locator(sel).count() == 0:
        page.wait_for_timeout(3000)
    if page.locator(sel).count() == 0:
        raise SystemExit("multiple file input not found; check the prompt bar state")
    if page.locator(sel).count() != 1:
        raise SystemExit("Ambiguous file inputs; identify the image reference input first")
    page.locator(sel).set_input_files(refs)
    n = 0
    deadline = time.time() + 25
    while time.time() < deadline:
        page.wait_for_timeout(1500)
        n = page.locator('button[aria-label="Remove Image Reference"]').count()
        if n == len(refs):
            break
    log(f"refs attached: {n} (expect {len(refs)})")
    if n != len(refs):
        raise SystemExit(f"only {n}/{len(refs)} references attached")


def fill_prompt(page, prompt):
    editor = page.locator('[contenteditable="true"]').first
    editor.click()
    page.keyboard.press("Control+A")
    page.keyboard.press("Backspace")
    editor.fill(prompt)
    page.wait_for_timeout(500)
    log(f"prompt filled: {len(prompt)} chars")


def generate(page):
    before = set(page.locator('a[href*="assetId="]').evaluate_all(
        "els => els.map(e => e.getAttribute('href'))"))
    page.get_by_role("button", name="Generate").click()
    log("generate clicked")
    deadline = time.time() + 600
    while time.time() < deadline:
        page.wait_for_timeout(5000)
        try:
            now = set(page.locator('a[href*="assetId="]').evaluate_all(
                "els => els.map(e => e.getAttribute('href'))"))
            fresh = [h for h in now - before if "assetWidth=" in h]
            if fresh:
                log("generation ready")
                return fresh[0]
        except Exception:
            pass
    raise SystemExit("Generation timed out; inspect Artlist tasks before resubmitting (submission may exist)")


def download_asset(page, href, out_path):
    log(f"asset: {href}")
    try:
        page.get_by_role("button", name="Collapse prompt").click(timeout=3000)
        page.wait_for_timeout(600)
    except Exception:
        pass
    link = page.locator(f'a[href*="assetId={href.split("assetId=")[1].split("&")[0]}"]').first
    link.click(timeout=20000)
    page.wait_for_timeout(3000)
    with page.expect_download(timeout=180000) as dl:
        page.get_by_role("button", name="Download").click(timeout=20000)
    dl.value.save_as(out_path)
    log(f"saved: {out_path} ({os.path.getsize(out_path)} bytes)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--prompt-file", required=True)
    ap.add_argument("--refs", default="")
    ap.add_argument("--out", required=True)
    ap.add_argument("--project", default=DEFAULT_PROJECT)
    ap.add_argument("--ratio", default="16:9", choices=["16:9", "9:16", "1:1"])
    ap.add_argument("--prepare-only", action="store_true",
                    help="Set up prompt/references without submitting or downloading; review reference identities and labels in Chrome")
    args = ap.parse_args()

    prompt = open(args.prompt_file, encoding="utf-8").read().strip()
    if not prompt:
        raise SystemExit("Prompt is empty")
    refs = [p.strip() for p in args.refs.split(";") if p.strip()]
    for r in refs:
        if not os.path.isfile(r):
            raise SystemExit(f"missing ref: {r}")
    refs = [str(Path(r).resolve()) for r in refs]
    if len(refs) > 14:
        raise SystemExit("This image workflow supports at most 14 references; confirm current UI limits")
    if Path(args.out).exists():
        raise SystemExit(f"Output already exists; choose a new filename: {args.out}")
    Path(args.out).resolve().parent.mkdir(parents=True, exist_ok=True)

    ensure_chrome(args.project)
    pw, browser, page = connect()
    try:
        page.goto(args.project, wait_until="domcontentloaded")
        page.wait_for_timeout(4000)
        # 页面可能停在素材详情弹层：先关弹层、再展开提示词栏，否则没有 Image Reference 控件
        for _ in range(2):
            try:
                page.get_by_role("button", name="Close modal").click(timeout=1500)
                page.wait_for_timeout(500)
            except Exception:
                pass
            try:
                page.get_by_role("button", name="Expand prompt").click(timeout=1500)
                page.wait_for_timeout(500)
            except Exception:
                pass
        ensure_settings(page, args.ratio)
        attach_refs(page, refs)
        fill_prompt(page, prompt)
        if args.prepare_only:
            log("Prepared only; inspect thumbnails, labels, prompt, settings and Unlimited in Chrome. No generation submitted.")
            return
        href = generate(page)
        download_asset(page, href, args.out)
        meta = {"name": args.name, "asset": href, "out": args.out,
                "refs": [os.path.basename(r) for r in refs],
                "prompt_file": os.path.abspath(args.prompt_file)}
        print("RESULT " + json.dumps(meta, ensure_ascii=False))
    finally:
        pw.stop()


if __name__ == "__main__":
    main()
