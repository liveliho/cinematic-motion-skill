#!/usr/bin/env python3
"""
cinematic-motion 质检脚本。

用法:
    python check.py <film.html>            # 静态检查 + 浏览器检查 + 生成联系表（contact sheet）
    python check.py <film.html> --static   # 只做静态检查（没有 Playwright / 浏览器时）

输出:
    控制台报告：ERROR 必须修；WARN 除非是刻意为之，否则也要修。
    <html 所在目录>/_qa/<文件名>/contact.png   每场 2 帧的缩略图总览
    <html 所在目录>/_qa/<文件名>/frames/*.png   对应的全尺寸帧
退出码: 有 ERROR 时为 1，否则为 0。
"""
import argparse
import base64
import io
import json
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE = SKILL_DIR / "assets" / "template.html"
TECHNIQUES = SKILL_DIR / "references" / "techniques.md"
TRANSITIONS = SKILL_DIR / "references" / "transitions.md"

BLOCKS = [
    ("REEL BASE", r"/\* ══════ REEL BASE v1.*?/\* ══════ /REEL BASE ══════ \*/"),
    ("REEL ENGINE", r"/\* ══════ REEL ENGINE v1.*?/\* ══════ /REEL ENGINE ══════ \*/"),
]
BRIEF_FIELDS = ["片名", "概念", "风格", "色板", "字体", "节奏", "动势", "英雄时刻"]
KNOWN_EASES = {"linear", "none", "snap", "glide", "whip", "punch"} | {
    f"{fam}.{kind}"
    for fam in ["quad", "cubic", "quart", "quint", "power1", "power2", "power3", "power4",
                "sine", "expo", "circ", "back", "elastic"]
    for kind in ["in", "out", "inOut"]
}
FONT_HOSTS = ("https://fonts.googleapis.com", "https://fonts.gstatic.com")


class Report:
    def __init__(self):
        self.errors, self.warns, self.notes = [], [], []

    def error(self, msg):
        self.errors.append(msg)

    def warn(self, msg):
        self.warns.append(msg)

    def note(self, msg):
        self.notes.append(msg)


def line_of(text, idx):
    return text.count("\n", 0, idx) + 1


def user_region(html):
    """去掉引擎和基础样式后的、作者自己写的部分。"""
    out = html
    for _, pat in BLOCKS:
        out = re.sub(pat, "", out, flags=re.S)
    return out


def static_checks(html, rep):
    tpl = TEMPLATE.read_text(encoding="utf-8")

    # 1. 模板占位符
    for m in re.finditer(r"\{\{[^}]*\}?\}?", html):
        rep.error(f"第 {line_of(html, m.start())} 行仍有模板占位符: {m.group(0)[:60]}")

    # 2. 引擎与基础样式必须与模板逐字一致
    for name, pat in BLOCKS:
        a = re.search(pat, html, flags=re.S)
        b = re.search(pat, tpl, flags=re.S)
        if not a:
            rep.error(f"找不到 {name} 区块（必须从 assets/template.html 原样复制）")
        elif b and a.group(0) != b.group(0):
            rep.error(f"{name} 区块被改动过——它必须与 assets/template.html 完全一致")

    # 3. 导演方案
    brief = re.search(r"DIRECTOR'S BRIEF(.*?)-->", html, flags=re.S)
    if not brief:
        rep.error("缺少 DIRECTOR'S BRIEF 注释块")
    else:
        for f in BRIEF_FIELDS:
            if f not in brief.group(1):
                rep.error(f"DIRECTOR'S BRIEF 缺少字段: {f}")

    # 4. 设计令牌
    for tok in ["--bg", "--fg", "--accent", "--font-display", "--font-text"]:
        if not re.search(re.escape(tok) + r"\s*:", html):
            rep.error(f":root 里缺少设计令牌 {tok}")

    # 5. 外部资源：只允许 Google Fonts
    for m in re.finditer(r"<script[^>]*\ssrc\s*=", html, flags=re.I):
        rep.error(f"第 {line_of(html, m.start())} 行引入了外部脚本——动画只能用内置 REEL 引擎")
    for m in re.finditer(r"""(?:href|src)\s*=\s*["'](https?://[^"']+)""", html, flags=re.I):
        if not m.group(1).startswith(FONT_HOSTS):
            rep.error(f"第 {line_of(html, m.start())} 行引用了外部资源: {m.group(1)[:80]}（只允许 Google Fonts）")
    for m in re.finditer(r"url\(\s*['\"]?(https?://[^'\")]+)", html, flags=re.I):
        if not m.group(1).startswith(FONT_HOSTS):
            rep.error(f"第 {line_of(html, m.start())} 行 CSS 引用了外部资源: {m.group(1)[:80]}")
    for m in re.finditer(r"<(img|video|audio|iframe)\b", html, flags=re.I):
        rep.warn(f"第 {line_of(html, m.start())} 行使用了 <{m.group(1)}>——除非是用户提供的素材，视觉应全部用排版/CSS/SVG/Canvas 生成")

    # 6. 破坏确定性（无法逐帧定位 / 导出）的写法
    ur = re.sub(r"<!--.*?-->", "", user_region(html), flags=re.S)
    css = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", ur, flags=re.S | re.I))
    js = "\n".join(re.findall(r"<script[^>]*>(.*?)</script>", ur, flags=re.S | re.I))
    banned = [
        (css, r"@keyframes|(?<![-\w])animation\s*:", "CSS @keyframes/animation 不受时间轴控制（暂停、拖动、导出都会错位）——改用 s.fromTo"),
        (css, r"(?<![-\w])transition\s*:", "CSS transition 会让引擎写入的值延迟生效、画面错位——删掉"),
        (js, r"\bsetTimeout\b|\bsetInterval\b", "setTimeout/setInterval 不可定位——改用 s.call 或 s.fromTo 的 at"),
        (js, r"\bMath\.random\b", "Math.random 每次播放都不同——改用 REEL.rand(n) / REEL.rng(seed)"),
        (js, r"\bDate\.now\b|\bperformance\.now\b|\brequestAnimationFrame\b", "自建时钟/动画循环会脱离时间轴——改用 s.call"),
        (js, r"\bgsap\b|\banime\s*\(|\bTHREE\.|\bVelocity\b|\bReact\b|\bVue\b", "不允许引入其他动画/框架库"),
    ]
    for src, pat, why in banned:
        m = re.search(pat, src)
        if m:
            rep.error(f"发现 `{m.group(0)}`：{why}")

    # 7. ease 名称
    for m in re.finditer(r"ease\s*:\s*['\"]([^'\"]+)['\"]", js):
        e = m.group(1)
        if e not in KNOWN_EASES and not re.match(r"^(cb|cubic-bezier)\([^)]+\)$", e):
            rep.error(f"未知 ease \"{e}\"（可用: expo.out / glide / snap / whip / punch / back.out / sine.inOut ...）")

    # 8. 结构
    scenes = re.findall(r"<section[^>]*class=\"[^\"]*\bscene\b[^\"]*\"[^>]*id=\"([^\"]+)\"|<section[^>]*id=\"([^\"]+)\"[^>]*class=\"[^\"]*\bscene\b", ur)
    ids = [a or b for a, b in scenes]
    if not ids:
        rep.error("没有找到任何 <section class=\"scene\" id=\"...\">")
    for sid in ids:
        if not re.search(r"tl\.scene\(\s*['\"]" + re.escape(sid) + r"['\"]", js):
            rep.error(f"场景 #{sid} 没有对应的 tl.scene('{sid}', ...) 动画")
    if "tl.start()" not in js:
        rep.error("缺少 tl.start()")
    if "STORYBOARD" not in js:
        rep.error("缺少 STORYBOARD")
    return ids


def known_ids(path, prefix):
    if not path.exists():
        return set()
    return set(re.findall(rf"^###\s+({prefix}\d\d)\b", path.read_text(encoding="utf-8"), flags=re.M))


def launch(p):
    last = None
    for kw in ({"channel": "msedge"}, {"channel": "chrome"}, {}):
        try:
            return p.chromium.launch(**kw)
        except Exception as e:  # noqa: BLE001
            last = e
    raise RuntimeError(f"无法启动浏览器（试过 Edge / Chrome / Playwright Chromium）: {last}")


OVERFLOW_JS = """
() => {
  const st = document.querySelector('.stage');
  const k = st.getBoundingClientRect().width / st.offsetWidth;
  const R = st.getBoundingClientRect();
  const out = [];
  const visible = el => {
    for (let e = el; e && e !== st; e = e.parentElement) {
      const cs = getComputedStyle(e);
      if (cs.display === 'none' || cs.visibility === 'hidden' || parseFloat(cs.opacity) < 0.05) return false;
    }
    return true;
  };
  const pad = 4 * k;
  document.querySelectorAll('.scene.on *').forEach(el => {
    if (el.closest('[data-bleed]')) return;
    const texts = Array.from(el.childNodes).filter(n => n.nodeType === 3 && n.textContent.trim());
    if (!texts.length || !visible(el)) return;
    for (const n of texts) {
      const range = document.createRange();
      range.selectNodeContents(n);
      const r = range.getBoundingClientRect();   // 实际字形范围，而不是元素盒子
      if (!r.width || !r.height) continue;
      const vt = Math.max(pad, r.height * .25);  // 行盒包含字体的上下留白，竖直方向放宽
      if (r.left < R.left - pad || r.right > R.right + pad || r.top < R.top - vt || r.bottom > R.bottom + vt) {
        out.push((el.textContent || '').trim().slice(0, 24));
        break;
      }
    }
  });
  return Array.from(new Set(out)).slice(0, 6);
}
"""


def browser_checks(path, rep, techniques_known, transitions_known):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        rep.warn("未安装 Playwright，跳过浏览器检查（pip install playwright）。请改用浏览器工具按 ?t=秒 截图人工检查。")
        return

    qa = path.parent / "_qa" / path.stem
    frames_dir = qa / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    for old in frames_dir.glob("*.png"):
        old.unlink()

    try:
        from PIL import Image, ImageStat  # noqa: F401
        have_pil = True
    except ImportError:
        have_pil = False

    with sync_playwright() as p:
        browser = launch(p)
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        console_errors = []
        page.on("pageerror", lambda e: console_errors.append(f"JS 运行错误: {e}"))
        page.on("console", lambda m: console_errors.append(f"console.error: {m.text}") if m.type == "error" else None)
        page.goto(path.resolve().as_uri() + "?render=1")
        try:
            page.wait_for_function("window.__reel && window.__reel.ready", timeout=15000)
            page.evaluate("window.__reel.ready")
        except Exception:
            rep.error("页面没有初始化 REEL（脚本报错，或没有调用 tl.start()）")
            for c in console_errors:
                rep.error(c)
            browser.close()
            return
        w, h = page.evaluate("[document.querySelector('.stage').offsetWidth, document.querySelector('.stage').offsetHeight]")
        page.set_viewport_size({"width": w, "height": h})
        data = page.evaluate("window.__reel.report()")
        for c in console_errors:
            rep.error(c)
        for m in data["log"]:
            rep.error(f"引擎警告: {m}")

        D, bpm = data["duration"], data["bpm"]
        beat = 60.0 / bpm
        sc = sorted(data["scenes"], key=lambda s: s["start"])
        n = len(sc)
        rep.note(f"画幅 {w}×{h} · 时长 {D:.2f}s · {bpm} BPM（1 拍 {beat:.3f}s）· {n} 个场景 · {data['tracks']} 条动画轨道")

        # ── 结构规则 ──
        if n < 4:
            rep.error(f"只有 {n} 个场景——至少需要 6 个（15 秒短片至少 5 个）")
        elif n < 6 or n > 12:
            rep.warn(f"{n} 个场景——建议 6–12 个")
        if not (12 <= D <= 90):
            rep.warn(f"总时长 {D:.1f}s 超出常规范围（15–60s）")
        if sc and abs(sc[0]["start"]) > 0.01:
            rep.error("第一个场景必须从 0 秒开始")
        covered = 0.0
        for s in sc:
            if s["start"] > covered + 0.02:
                rep.error(f"{covered:.2f}s – {s['start']:.2f}s 之间没有任何场景（画面空白）")
            covered = max(covered, s["end"])
        if covered < D - 0.02:
            rep.error(f"{covered:.2f}s 之后到结尾 {D:.2f}s 没有场景")
        for s in sc:
            d = s["end"] - s["start"]
            if d < beat - 1e-3:
                rep.error(f"场景 {s['id']} 只有 {d:.2f}s（短于 1 拍）")
            elif d < 1.0:
                rep.warn(f"场景 {s['id']} 只有 {d:.2f}s，观众来不及读")
            r = (s["start"] / beat) % 1
            if min(r, 1 - r) * beat > 0.02:
                rep.warn(f"场景 {s['id']} 的起点 {s['start']:.3f}s 没有落在拍点上（请用 n*B 表示）")
            if s["animated"] <= 1:
                rep.error(f"场景 {s['id']} 几乎是静态的（只有 {s['animated']} 个动画对象）")
            elif s["animated"] < 3:
                rep.warn(f"场景 {s['id']} 只有 {s['animated']} 个动画对象——加入细节层/背景层运动")
        if sum(1 for s in sc if s["cam"] == "none") > 2:
            rep.warn("超过 2 个场景关闭了镜头运动（cam:'none'）——画面容易显得死板")

        # ── 技法与转场多样性 ──
        tech_ids, trans_ids = [], []
        for i, s in enumerate(sc):
            tm = re.match(r"\s*(T\d\d)", s["technique"] or "")
            if not tm:
                rep.error(f"场景 {s['id']} 的 technique 必须以技法编号开头（如 'T03 Scale Slam'）")
            else:
                tech_ids.append(tm.group(1))
                if techniques_known and tm.group(1) not in techniques_known:
                    rep.warn(f"场景 {s['id']} 的技法 {tm.group(1)} 不在 references/techniques.md 中")
            xm = re.match(r"\s*(X\d\d|END)", s["transition"] or "")
            if not xm:
                rep.error(f"场景 {s['id']} 的 transition 必须以转场编号开头（如 'X04 Shutter'；最后一场可写 'END'）")
            elif xm.group(1) != "END":
                trans_ids.append(xm.group(1))
                if transitions_known and xm.group(1) not in transitions_known:
                    rep.warn(f"场景 {s['id']} 的转场 {xm.group(1)} 不在 references/transitions.md 中")
        if tech_ids and len(set(tech_ids)) < 0.7 * len(tech_ids):
            rep.error(f"主技法重复太多：{len(tech_ids)} 个场景只用了 {len(set(tech_ids))} 种（需 ≥70% 不同）")
        need = min(4, max(1, n - 1))
        if trans_ids and len(set(trans_ids)) < need:
            rep.error(f"转场只用了 {len(set(trans_ids))} 种——至少需要 {need} 种")
        for a, b in zip(trans_ids, trans_ids[1:]):
            if a == b:
                rep.warn(f"相邻两次转场都是 {a}——换一个")

        # ── 抽帧：每场 entry + hold 两帧，外加首尾 ──
        shots = [(0.05, "open")]
        for s in sc:
            d = s["end"] - s["start"]
            shots.append((s["start"] + min(0.9, d * 0.35), f"{s['id']}·入"))
            shots.append((s["start"] + d * 0.82, f"{s['id']}·定"))
        shots.append((D - 0.04, "end"))
        thumbs = []
        for i, (t, label) in enumerate(shots):
            page.evaluate(f"window.__reel.seek({t})")
            png = page.screenshot()
            fp = frames_dir / f"{i:02d}_{t:06.2f}s.png"
            fp.write_bytes(png)
            thumbs.append((label, t, png))
            if label.endswith("定"):
                over = page.evaluate(OVERFLOW_JS)
                if over:
                    rep.warn(f"{label} @ {t:.2f}s 文字超出画面: {over}（刻意出血的元素请加 data-bleed）")

        # ── 空白帧检测（每 0.5s 采样） ──
        if have_pil:
            from PIL import Image, ImageStat
            blank_run, t = [], 0.0
            runs = []
            while t < D:
                page.evaluate(f"window.__reel.seek({t})")
                img = Image.open(io.BytesIO(page.screenshot(type="jpeg", quality=60))).convert("L").resize((192, 108))
                if ImageStat.Stat(img).stddev[0] < 4:
                    blank_run.append(t)
                else:
                    if len(blank_run) >= 2:
                        runs.append((blank_run[0], blank_run[-1]))
                    blank_run = []
                t += 0.5
            if len(blank_run) >= 2:
                runs.append((blank_run[0], blank_run[-1]))
            for a, b in runs:
                rep.warn(f"{a:.1f}s – {b:.1f}s 画面接近纯色（≥1 秒没有内容）——除非是刻意的呼吸/黑场")

        # ── 联系表 ──
        cells = "".join(
            f'<figure><img src="data:image/png;base64,{base64.b64encode(png).decode()}"><figcaption>{label} · {t:.2f}s</figcaption></figure>'
            for label, t, png in thumbs
        )
        cols = 4 if w >= h else 6
        tw = 480 if w >= h else 300
        sheet = f"""<html><body style="margin:0;background:#111;color:#ddd;font:14px monospace">
<div style="display:grid;grid-template-columns:repeat({cols},{tw}px);gap:10px;padding:10px">{cells}</div>
<style>figure{{margin:0}}img{{width:{tw}px;display:block;border:1px solid #333}}figcaption{{padding:4px 2px}}</style></body></html>"""
        sp = browser.new_page(viewport={"width": cols * (tw + 10) + 10, "height": 400})
        sp.set_content(sheet)
        (qa / "contact.png").write_bytes(sp.screenshot(full_page=True))
        rep.note(f"联系表: {qa / 'contact.png'}")
        rep.note(f"全尺寸帧: {frames_dir}")
        (qa / "report.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        browser.close()


def main():
    ap = argparse.ArgumentParser(description="cinematic-motion 质检")
    ap.add_argument("html")
    ap.add_argument("--static", action="store_true", help="只做静态检查")
    a = ap.parse_args()
    path = Path(a.html)
    if not path.exists():
        print(f"找不到文件: {path}")
        sys.exit(2)
    html = path.read_text(encoding="utf-8")
    rep = Report()
    static_checks(html, rep)
    if not a.static:
        try:
            browser_checks(path, rep, known_ids(TECHNIQUES, "T"), known_ids(TRANSITIONS, "X"))
        except RuntimeError as e:
            rep.warn(str(e) + " —— 已跳过浏览器检查")

    print("═" * 64)
    print(f" cinematic-motion 质检 · {path.name}")
    print("═" * 64)
    for m in rep.notes:
        print(f"  ·  {m}")
    for m in rep.errors:
        print(f"  ✗ ERROR  {m}")
    for m in rep.warns:
        print(f"  ! WARN   {m}")
    print("─" * 64)
    if rep.errors:
        print(f" FAIL · {len(rep.errors)} 个错误，{len(rep.warns)} 个警告 —— 修复后重新运行")
        sys.exit(1)
    print(f" PASS · 0 个错误，{len(rep.warns)} 个警告" + ("（逐条确认是否刻意为之）" if rep.warns else ""))
    print(" 下一步：打开联系表 contact.png，按 SKILL.md 的「视觉自检」逐条检查。")


if __name__ == "__main__":
    main()
