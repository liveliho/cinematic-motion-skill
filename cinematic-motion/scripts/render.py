#!/usr/bin/env python3
"""
把 cinematic-motion 影片 HTML 逐帧渲染成 MP4（只在用户要视频文件时使用）。

用法:
    python render.py <film.html> [--out film.mp4] [--fps 30] [--scale 1] [--start 0] [--end 秒]

依赖: playwright（可直接用系统 Edge/Chrome）+ ffmpeg（PATH 里的，或 pip install imageio-ffmpeg）。
原理: 以 ?render=1 打开页面，逐帧调用 window.__reel.seek(t) 截图，管道送进 ffmpeg 编码 H.264。
画面是确定性的，所以导出结果与浏览器播放一致，不受机器性能影响。
"""
import argparse
import shutil
import subprocess
import sys
import time
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def find_ffmpeg():
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return None


def launch(p):
    last = None
    for kw in ({"channel": "msedge"}, {"channel": "chrome"}, {}):
        try:
            return p.chromium.launch(**kw)
        except Exception as e:  # noqa: BLE001
            last = e
    raise RuntimeError(f"无法启动浏览器: {last}")


def main():
    ap = argparse.ArgumentParser(description="REEL 影片 → MP4")
    ap.add_argument("html")
    ap.add_argument("--out")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--scale", type=float, default=1.0, help="分辨率倍数，2 = 4K（16:9 时）")
    ap.add_argument("--start", type=float, default=0.0)
    ap.add_argument("--end", type=float)
    ap.add_argument("--crf", type=int, default=16)
    a = ap.parse_args()

    src = Path(a.html).resolve()
    out = Path(a.out).resolve() if a.out else src.with_suffix(".mp4")
    ffmpeg = find_ffmpeg()
    if not ffmpeg:
        print("找不到 ffmpeg。请安装 ffmpeg，或运行: pip install imageio-ffmpeg")
        sys.exit(2)
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("需要 Playwright: pip install playwright")
        sys.exit(2)

    with sync_playwright() as p:
        browser = launch(p)
        page = browser.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=a.scale)
        page.goto(src.as_uri() + "?render=1")
        page.wait_for_function("window.__reel && window.__reel.ready", timeout=20000)
        page.evaluate("window.__reel.ready")
        w, h = page.evaluate("[document.querySelector('.stage').offsetWidth, document.querySelector('.stage').offsetHeight]")
        page.set_viewport_size({"width": w, "height": h})
        dur = page.evaluate("window.__reel.duration")
        end = min(a.end if a.end is not None else dur, dur)
        frames = int(round((end - a.start) * a.fps))
        W, H = int(w * a.scale) // 2 * 2, int(h * a.scale) // 2 * 2

        cmd = [ffmpeg, "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(a.fps), "-i", "-",
               "-vf", f"scale={W}:{H}:out_range=tv,format=yuv420p", "-c:v", "libx264", "-preset", "medium", "-crf", str(a.crf),
               "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)]
        enc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        t0 = time.time()
        print(f"渲染 {src.name}: {W}×{H} · {a.fps}fps · {frames} 帧 → {out}")
        for i in range(frames):
            t = a.start + i / a.fps
            page.evaluate(f"window.__reel.seek({t})")
            enc.stdin.write(page.screenshot(type="jpeg", quality=95))
            if i % (a.fps * 2) == 0 or i == frames - 1:
                el = time.time() - t0
                eta = el / (i + 1) * (frames - i - 1)
                print(f"  {i + 1}/{frames} 帧 · {t:6.2f}s · 剩余约 {eta:4.0f}s", flush=True)
        enc.stdin.close()
        code = enc.wait()
        browser.close()
    if code != 0:
        print("ffmpeg 编码失败")
        sys.exit(code)
    print(f"完成: {out}（{out.stat().st_size / 1e6:.1f} MB，用时 {time.time() - t0:.0f}s）")


if __name__ == "__main__":
    main()
