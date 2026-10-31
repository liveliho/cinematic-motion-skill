# 视觉技法库 T01–T26

每个技法都写了：效果、何时用、要点、可直接改写的代码。代码里的 `#sX` 换成实际场景 id；`s` 是 `tl.scene('sX', s => {...})` 里的场景作用域；`B` 是 1 拍的秒数。

在 STORYBOARD 的 `technique` 字段写**编号 + 英文名**，例如 `'T03 Scale Slam'`。

## 目录

**A. 文字类**
- T01 Mask Rise 遮罩升起
- T02 Char Cascade 逐字瀑布
- T03 Scale Slam 重拍砸字
- T04 Giant Type Pan 巨字横移
- T05 Outline Fill 描边填充
- T06 Marquee Wall 文字墙
- T07 Word Beats 一拍一词
- T08 Decode Scramble 乱码解码
- T09 Counter Roll 数字滚动
- T23 Typewriter 打字机
- T24 Echo Trail 残影回声
- T25 Vertical Brush 竖排书法
- T26 Kinetic Weight 字重呼吸

**B. 形状类**
- T10 Line Draw 描线
- T11 Shape Burst 形状爆发
- T12 Grid Build 网格生成
- T13 Bars Rhythm 律动条
- T14 Split Screen 分屏
- T17 3D Flip 3D 翻转
- T18 Orbit HUD 轨道仪表

**C. 空间与质感类**
- T15 Light Sweep 光扫
- T16 RGB Glitch 色散故障
- T19 Zoom-Through 放大穿越
- T20 Parallax Depth 视差纵深
- T21 Gradient Aura 流光氛围
- T22 Particle Field 粒子场

---

## A. 文字类

### T01 Mask Rise 遮罩升起
**能量** 2–3 · **适合** 全部预设，P1 / P5 / P7 的主力
文字从一条看不见的基线下方升起，像从缝里钻出来。这是最“干净、高级”的文字入场。
要点：每行包一层 `.line`（已带 overflow:hidden）；加一点旋转更有韵味；出场继续向上消失，而不是原路返回。

```html
<h1 class="rise"><span class="line"><span>MAKE IT</span></span><span class="line"><span>MOVE.</span></span></h1>
```
```css
#sX .rise{position:absolute;left:120px;bottom:160px;font:900 240px/.86 var(--font-display);letter-spacing:-.04em}
```
```js
s.fromTo('.rise .line > span', { y: '110%', rotate: 4 }, { y: '0%', rotate: 0 }, { at: B*.5, dur: 1, ease: 'expo.out', stagger: .12 });
s.fromTo('.rise .line > span', { y: '0%' }, { y: '-110%' }, { at: s.dur - B, dur: .5, ease: 'expo.in', stagger: .06 });
// 逐字版：
// const ch = REEL.split(s.q('.rise2'), { mask: true });
// s.fromTo(ch, { y: '110%' }, { y: '0%' }, { at: 0, dur: .8, ease: 'expo.out', stagger: .03 });
```

### T02 Char Cascade 逐字瀑布
**能量** 3–4 · **适合** P3 / P6（`back.out`），P2 / P4（`expo.out`）
每个字带着随机角度依次落下就位。
要点：随机角度用 `REEL.rand(i)`；3D 版给父元素加 `perspective`，字用 `rotateX`。

```html
<div class="cascade">BREAK THE GRID</div>
```
```css
#sX .cascade{position:absolute;left:0;right:0;top:420px;text-align:center;font:800 170px/1 var(--font-display)}
#sX .cascade .ch{transform-origin:50% 100%}
```
```js
const ch = REEL.split(s.q('.cascade'));
s.fromTo(ch, { y: -160, rotate: i => (REEL.rand(i) - .5) * 70, opacity: 0 }, { y: 0, rotate: 0, opacity: 1 },
  { at: 0, dur: .8, ease: 'back.out', stagger: { each: .035, from: 'start' } });
// 3D 翻落版：父元素 CSS 加 perspective:1000px，然后
// s.fromTo(ch, { rotateX: -90, opacity: 0 }, { rotateX: 0, opacity: 1 }, { at: 0, dur: .7, ease: 'expo.out', stagger: .04 });
```

### T03 Scale Slam 重拍砸字
**能量** 5 · **适合** P3 / P2 / P4；P7 只用于印章
一个词从巨大、模糊、透明的状态砸到画面上，同时闪白 + 抖动 + 底色反转。这是标准的“重拍”。
要点：冲击时刻 `hit` 必须落在小节第 1 拍；`expo.out` 让 80% 的位移发生在前 20% 的时间里，所以动画开始的那一刻就是冲击点；砸完后继续极慢放大，避免死帧。

```html
<div class="layer bg"></div>
<div class="layer main"><div class="slam">LOUD</div></div>
```
```css
#sX .slam{position:absolute;inset:0;display:grid;place-items:center;font:400 520px/1 var(--font-display);text-transform:uppercase}
```
```js
const hit = B*4;
s.fromTo('.slam', { scale: 3.2, opacity: 0, filter: 'blur(30px)' }, { scale: 1, opacity: 1, filter: 'blur(0px)' }, { at: hit, dur: .45, ease: 'expo.out' });
s.fromTo('.slam', { scale: 1 }, { scale: 1.06 }, { at: hit + .45, dur: s.dur - hit - .45, ease: 'linear' });
s.flash({ at: hit, peak: .7, out: .2 });
s.shake({ at: hit + .04, amp: 22, dur: .45 });
s.set('.bg', { background: 'var(--accent)' }, hit);   // 底色反转
s.set('.slam', { color: 'var(--bg)' }, hit);
```

### T04 Giant Type Pan 巨字横移
**能量** 4–5 · **适合** P2 / P3 / P1（慢速）· **英雄时刻常用**
一个 700px 以上的巨大单词横穿画面，字母边缘被画框裁切。观众看到的是“字的局部”，形成强烈的图形感。
要点：加 `data-bleed`（告诉质检这是刻意出血）；用 `calc()` 让它从右侧画外完全穿到左侧画外，不需要知道单词宽度；持续运动用 `linear`；上面叠一行小字形成尺度对比。

```html
<div class="giant" data-bleed>INFINITE</div>
<div class="giant ol" data-bleed>INFINITE</div>
<div class="note">CHAPTER 03 — SCALE</div>
```
```css
#sX .giant{position:absolute;top:50%;left:100%;margin-top:-.5em;font:900 820px/1 var(--font-display);white-space:nowrap;letter-spacing:-.05em}
#sX .giant.ol{top:8%;color:transparent;-webkit-text-stroke:2px var(--accent);font-size:420px}
#sX .note{position:absolute;left:120px;bottom:110px;font:500 22px var(--font-mono);letter-spacing:.3em}
```
```js
s.fromTo('.giant:not(.ol)', { x: 'calc(0% + -600px)' }, { x: 'calc(-100% + -1320px)' }, { at: 0, dur: s.dur, ease: 'linear' });
s.fromTo('.giant.ol', { x: 'calc(-100% + -1920px)' }, { x: 'calc(0% + -2400px)' }, { at: 0, dur: s.dur, ease: 'linear' }); // 反向，制造纵深
s.fromTo('.note', { opacity: 0, x: -30 }, { opacity: 1, x: 0 }, { at: B, dur: .8, ease: 'expo.out' });
```

### T05 Outline Fill 描边填充
**能量** 2–3 · **适合** P1 / P2 / P5 / P3
先出现空心描边字，再被颜色从左到右灌满。
要点：填充层是同一个词的覆盖副本；两次 clip-path 揭示错开 1–2 拍。

```html
<div class="ol">BOLD<span class="fill" aria-hidden="true">BOLD</span></div>
```
```css
#sX .ol{position:absolute;left:120px;top:300px;font:900 340px/1 var(--font-display);color:transparent;-webkit-text-stroke:3px var(--fg)}
#sX .ol .fill{position:absolute;left:0;top:0;color:var(--accent);-webkit-text-stroke:0}
```
```js
s.fromTo('.ol', { clipPath: 'inset(0 100% 0 0)' }, { clipPath: 'inset(0 0% 0 0)' }, { at: 0, dur: .9, ease: 'snap' });
s.fromTo('.ol .fill', { clipPath: 'inset(0 100% 0 0)' }, { clipPath: 'inset(0 0% 0 0)' }, { at: B*2, dur: .8, ease: 'snap' });
```

### T06 Marquee Wall 文字墙
**能量** 4–5 · **适合** P3 / P2 / P6 · **英雄时刻常用**
6–8 行重复文字铺满并溢出画面，奇偶行反向移动，实心与描边交替，整体倾斜。
要点：行在搭建时用 JS 生成；每行文字长度至少是画面宽度的 2 倍；整面墙的倾斜写在 CSS（不被引擎动画的容器上）。

```html
<div class="wall" data-bleed></div>
```
```css
#sX .wall{position:absolute;inset:-80px -300px;display:flex;flex-direction:column;justify-content:center;transform:rotate(-6deg)}
#sX .row{font:400 170px/.92 var(--font-display);white-space:nowrap;text-transform:uppercase}
#sX .row.ol{color:transparent;-webkit-text-stroke:2px var(--fg)}
#sX .row:nth-child(4){color:var(--accent)}
```
```js
const wall = s.q('.wall')[0];
for (let i = 0; i < 7; i++) {
  const r = document.createElement('div');
  r.className = 'row' + (i % 2 ? ' ol' : '');
  r.textContent = 'STAY LOUD ✱ '.repeat(8);
  wall.appendChild(r);
}
const rows = s.q('.row');
s.fromTo(rows, { x: i => i % 2 ? -1400 : 0 }, { x: i => i % 2 ? 0 : -1400 }, { at: 0, dur: s.dur, ease: 'linear' });
s.fromTo(rows, { opacity: 0, y: 90 }, { opacity: 1, y: 0 }, { at: 0, dur: .6, ease: 'expo.out', stagger: { each: .05, from: 'center' } });
```

### T07 Word Beats 一拍一词
**能量** 4 · **适合** P2 / P3 / P6 · 推进段的主力
每一拍换一个词，底色随拍反转，形成蒙太奇式快切。
要点：最后一个词留住；可以用渐快的时间表制造冲刺感（如 `[0, 1, 2, 2.5, 3, 3.25, 3.5]` 拍）。

```html
<div class="layer bg"></div>
<div class="layer main beats"><b>WE</b><b>DON'T</b><b>MAKE</b><b>ADS.</b></div>
```
```css
#sX .beats b{position:absolute;inset:0;display:grid;place-items:center;font:400 380px/1 var(--font-display);text-transform:uppercase}
```
```js
const words = s.q('.beats b'), bg = s.q('.bg')[0];
words.forEach((w, i) => {
  const t = B * i;
  s.fromTo(w, { opacity: 0, scale: 1.25 }, { opacity: 1, scale: 1 }, { at: t, dur: .3, ease: 'expo.out' });
  if (i < words.length - 1) s.set(w, { opacity: 0 }, t + B);
  s.set(w, { color: i % 2 ? 'var(--bg)' : 'var(--fg)' }, t);
  s.set(bg, { background: i % 2 ? 'var(--accent)' : 'var(--bg)' }, t);
});
```

### T08 Decode Scramble 乱码解码
**能量** 3 · **适合** P4 / P2 / P3
字符先是乱码，再从左到右逐个“解”出真文字。用于标签、坐标、系统信息、副标题。
要点：用等宽字体避免抖动；中文可传一串汉字作乱码字符集。

```html
<div class="code">SIGNAL ACQUIRED</div>
<div class="code cn">正在连接未来</div>
```
```css
#sX .code{position:absolute;left:120px;top:120px;font:500 26px var(--font-mono);letter-spacing:.24em;color:var(--accent)}
#sX .code.cn{top:170px;letter-spacing:.4em}
```
```js
s.scramble('.code:not(.cn)', { at: B*.5, dur: 1.2 });
s.scramble('.code.cn', { at: B*1.5, dur: 1.2, chars: '天地玄黄宇宙洪荒日月盈昃辰宿列张' });
// 逐字生成版：mode:'build'；二进制：chars:'01'
```

### T09 Counter Roll 数字滚动
**能量** 3 · **适合** P4 / P2，所有需要“数据感”的场景
数字从 0 滚到目标值，配一条同步增长的进度线。
要点：`font-variant-numeric: tabular-nums` 防止宽度抖动；年份必须 `group:false`；进度线与计数用同一个 ease 才会同步。

```html
<div class="num">0</div><div class="unit">% FASTER</div><div class="meter"><i></i></div>
```
```css
#sX .num{position:absolute;left:120px;top:260px;font:800 380px/1 var(--font-display);font-variant-numeric:tabular-nums;letter-spacing:-.04em}
#sX .unit{position:absolute;left:130px;top:660px;font:500 34px var(--font-mono);letter-spacing:.2em}
#sX .meter{position:absolute;left:120px;right:120px;top:760px;height:2px;background:rgba(127,127,127,.3)}
#sX .meter i{position:absolute;inset:0;background:var(--accent);transform-origin:0 50%}
```
```js
s.count('.num', { from: 0, to: 98.6, decimals: 1, at: B, dur: B*4, ease: 'expo.out' });
s.fromTo('.meter i', { scaleX: 0 }, { scaleX: .986 }, { at: B, dur: B*4, ease: 'expo.out' });
s.fromTo('.unit', { opacity: 0, y: 20 }, { opacity: 1, y: 0 }, { at: B*2, dur: .6, ease: 'expo.out' });
// 年份：s.count('.year', { from: 1990, to: 2026, at: B, dur: 2, group: false, ease: 'expo.inOut' });
```

### T23 Typewriter 打字机
**能量** 2 · **适合** P4 / P2 / P1（字幕感）
逐字打出，带闪烁光标。
要点：等宽字体；需要更优雅的版本（P5 / P7）用“逐字浮现”代替光标。

```html
<p class="tw">In a world made of pixels, motion is meaning.</p>
```
```css
#sX .tw{position:absolute;left:120px;bottom:140px;max-width:1300px;font:400 44px/1.4 var(--font-mono)}
```
```js
s.type('.tw', { at: B, dur: 2.2 });
// 逐字浮现版：
// const ch = REEL.split(s.q('.tw'));
// s.fromTo(ch, { opacity: 0, filter: 'blur(8px)', y: 10 }, { opacity: 1, filter: 'blur(0px)', y: 0 }, { at: B, dur: .8, ease: 'glide', stagger: .08 });
```

### T24 Echo Trail 残影回声
**能量** 4 · **适合** P3 / P6
同一个词的 6 份副本以错开的时间入场，形成阶梯状残影，再在重拍时收拢成一个。
要点：最后一份是实心主体，其他是描边残影；残影透明度递增。

```html
<div class="echo"><b>ECHO</b><b>ECHO</b><b>ECHO</b><b>ECHO</b><b>ECHO</b><b>ECHO</b></div>
```
```css
#sX .echo{position:absolute;inset:0;display:grid;place-items:center}
#sX .echo b{grid-area:1/1;font:400 300px/1 var(--font-display);color:transparent;-webkit-text-stroke:2px var(--fg)}
#sX .echo b:nth-child(-n+3){opacity:.35}
#sX .echo b:last-child{color:var(--accent);-webkit-text-stroke:0}
```
```js
const copies = s.q('.echo b');
s.fromTo(copies, { y: 900 }, { y: (i, el, n) => -(n - 1 - i) * 56 }, { at: 0, dur: 1.1, ease: 'expo.out', stagger: { each: .06, from: 'end' } });
s.fromTo(copies, { y: (i, el, n) => -(n - 1 - i) * 56 }, { y: 0 }, { at: B*4, dur: .4, ease: 'snap' });
s.shake({ at: B*4 + .35, amp: 10, dur: .3 });
```

### T25 Vertical Brush 竖排书法
**能量** 1–3 · **适合** P7（主力）、P5
竖排毛笔字像墨迹一样从上到下洇开，朱红印章在重拍时盖下。
要点：用 `mask-image` 柔边渐变揭示；mask-size 300% 让过渡带足够柔和；印章是全片唯一的强调色块。

```html
<div class="v">山高水长</div>
<div class="seal">墨<br>韵</div>
<div class="sign">丙午年 · 秋</div>
```
```css
#sX .v{position:absolute;right:420px;top:140px;writing-mode:vertical-rl;font:400 200px/1.1 var(--font-display);letter-spacing:.08em;
  -webkit-mask-image:linear-gradient(180deg,#000 45%,transparent 55%);mask-image:linear-gradient(180deg,#000 45%,transparent 55%);
  -webkit-mask-size:100% 300%;mask-size:100% 300%;-webkit-mask-repeat:no-repeat;mask-repeat:no-repeat}
#sX .seal{position:absolute;right:300px;top:640px;width:96px;height:96px;display:grid;place-items:center;background:var(--accent);color:var(--bg);font:400 36px/1 var(--font-display);border-radius:6px}
#sX .sign{position:absolute;right:316px;top:140px;writing-mode:vertical-rl;font:300 24px var(--font-text);letter-spacing:.5em;color:var(--accent-2)}
```
```js
s.fromTo('.v', { maskPosition: '0% 100%' }, { maskPosition: '0% 0%' }, { at: B, dur: 2.4, ease: 'sine.inOut' });
s.fromTo('.sign', { opacity: 0, y: -20 }, { opacity: 1, y: 0 }, { at: B*3, dur: 1.2, ease: 'glide' });
s.fromTo('.seal', { scale: 1.8, opacity: 0, rotate: -8 }, { scale: 1, opacity: 1, rotate: 0 }, { at: B*6, dur: .4, ease: 'expo.out' });
s.shake({ at: B*6 + .03, amp: 6, dur: .3 });
// 一笔横线：SVG path 加 stroke-linecap:round、stroke-width:18，用 s.draw 画出
```

### T26 Kinetic Weight 字重呼吸
**能量** 2–4 · **适合** P2（Archivo）、P5、P4
可变字体的字重 / 字宽像波浪一样在字母间传递，文字在“呼吸”。
要点：Google Fonts 链接必须请求轴范围（如 `Archivo:wdth,wght@62..125,100..900`）；按字 stagger 从中心或两端开始。

```html
<div class="vw">RHYTHM</div>
```
```css
#sX .vw{position:absolute;left:0;right:0;top:360px;text-align:center;font-family:'Archivo',var(--font-display);font-size:300px;line-height:1;font-variation-settings:'wght' 100,'wdth' 62}
```
```js
const ch = REEL.split(s.q('.vw'));
s.fromTo(ch, { fontVariationSettings: "'wght' 100, 'wdth' 62" }, { fontVariationSettings: "'wght' 900, 'wdth' 125" },
  { at: 0, dur: B*2, ease: 'sine.inOut', stagger: { each: .07, from: 'center' } });
s.fromTo(ch, { fontVariationSettings: "'wght' 900, 'wdth' 125" }, { fontVariationSettings: "'wght' 300, 'wdth' 80" },
  { at: B*4, dur: B*2, ease: 'sine.inOut', stagger: { each: .07, from: 'edges' } });
```

---

## B. 形状类

### T10 Line Draw 描线
**能量** 2–3 · **适合** 全部；P1 / P4 / P7 最常用
SVG 线条、圆、框被“画”出来，常用来切开画面、圈出重点、连接标签。
要点：SVG 用与画布一致的 viewBox；元素要 `fill:none` 并有 `stroke`；圆的起笔在 3 点钟方向，想从 12 点开始就旋转 -90°（配合 `transform-box: fill-box`）；**已有虚线样式的元素不要用 draw**（会覆盖虚线）。

```html
<svg class="lines" viewBox="0 0 1920 1080" width="1920" height="1080">
  <path class="ln" d="M120 540 H1800"/>
  <circle class="ln ring" cx="960" cy="540" r="320"/>
  <path class="ln" d="M960 120 V960"/>
</svg>
```
```css
#sX .lines{position:absolute;inset:0}
#sX .ln{fill:none;stroke:var(--accent);stroke-width:3}
#sX .ring{transform-box:fill-box;transform-origin:center;transform:rotate(-90deg)}
```
```js
s.draw('.ln', { at: 0, dur: 1.2, ease: 'snap', stagger: .15 });
s.draw('.ln', { at: s.dur - B, dur: .6, ease: 'expo.in', erase: true });
```

### T11 Shape Burst 形状爆发
**能量** 4–5 · **适合** P6 / P3 / P4
十几个圆、方块、圆环从随机位置弹出，然后持续漂浮；或冲击波圆环向外扩散。
要点：随机布局在搭建时用 `REEL.rng(种子)` 生成（每次播放都一样）；出现顺序 `from:'random'`。

```html
<div class="burst"></div>
```
```css
#sX .burst{position:absolute;inset:0}
#sX .burst i{position:absolute;border-radius:50%;background:var(--accent)}
#sX .burst i.sq{border-radius:0;background:var(--accent-2)}
#sX .burst i.rg{background:none;border:3px solid var(--fg)}
```
```js
const box = s.q('.burst')[0], r = REEL.rng(11);
for (let i = 0; i < 18; i++) {
  const d = document.createElement('i'), size = 30 + r() * 180;
  d.className = ['', 'sq', 'rg'][i % 3];
  d.style.cssText = `width:${size}px;height:${size}px;left:${960 + (r() - .5) * 1500 - size / 2}px;top:${540 + (r() - .5) * 820 - size / 2}px`;
  box.appendChild(d);
}
const shapes = s.q('.burst i');
s.fromTo(shapes, { scale: 0, rotate: -90 }, { scale: 1, rotate: 0 }, { at: B, dur: .7, ease: 'back.out', stagger: { each: .03, from: 'random' } });
s.fromTo(shapes, { y: 0 }, { y: i => -40 - REEL.rand(i) * 120 }, { at: B, dur: s.dur - B, ease: 'linear' });
// 冲击波：<i class="wave"> 圆环 → s.fromTo('.wave', { scale: 0, opacity: 1 }, { scale: 4, opacity: 0 }, { at: B*4, dur: 1, ease: 'expo.out', stagger: .12 });
```

### T12 Grid Build 网格生成
**能量** 3 · **适合** P2（主力）、P4
栏线依次画出构成网格，再随机点亮若干格子，文字吸附在网格上出现。
要点：线和格子在搭建时生成；竖线 `scaleY`、横线 `scaleX`，变换原点分别在上端和左端；**只生成会被点亮的格子**——没有动画的元素会按 CSS 默认直接显示出来。

```html
<div class="grid"></div>
```
```css
#sX .grid{position:absolute;inset:80px}
#sX .gv{position:absolute;top:0;bottom:0;width:1px;background:var(--fg);opacity:.35;transform-origin:50% 0}
#sX .gh{position:absolute;left:0;right:0;height:1px;background:var(--fg);opacity:.35;transform-origin:0 50%}
#sX .cell{position:absolute;width:12.5%;height:20%;background:var(--accent);transform-origin:0 0}
```
```js
const g = s.q('.grid')[0], cols = 8, rows = 5;
for (let i = 1; i < cols; i++) g.insertAdjacentHTML('beforeend', `<i class="gv" style="left:${i / cols * 100}%"></i>`);
for (let j = 1; j < rows; j++) g.insertAdjacentHTML('beforeend', `<i class="gh" style="top:${j / rows * 100}%"></i>`);
for (let k = 0; k < cols * rows; k++) if (REEL.rand(k * 7) < .22)   // 只生成约 22% 会被点亮的格子
  g.insertAdjacentHTML('beforeend', `<b class="cell" style="left:${k % cols / cols * 100}%;top:${Math.floor(k / cols) / rows * 100}%"></b>`);
s.fromTo(s.q('.gv'), { scaleY: 0 }, { scaleY: 1 }, { at: 0, dur: .9, ease: 'snap', stagger: .05 });
s.fromTo(s.q('.gh'), { scaleX: 0 }, { scaleX: 1 }, { at: .15, dur: .9, ease: 'snap', stagger: .05 });
s.fromTo(s.q('.cell'), { scale: 0 }, { scale: 1 }, { at: B*2, dur: .35, ease: 'expo.out', stagger: { each: .04, from: 'random' } });
```

### T13 Bars Rhythm 律动条
**能量** 4 · **适合** P2 / P3 / P6
一排竖条像均衡器一样在每一拍跳到新的高度，可视化“节拍”本身。
要点：入场后从第 2 拍起开始跳动（给入场留时间）；高度用 `REEL.rand` 生成。

```html
<div class="bars"></div>
```
```css
#sX .bars{position:absolute;left:120px;right:120px;bottom:120px;height:600px;display:flex;gap:14px;align-items:flex-end}
#sX .bar{flex:1;height:100%;background:var(--fg);transform-origin:50% 100%}
#sX .bar:nth-child(5n){background:var(--accent)}
```
```js
const row = s.q('.bars')[0];
for (let i = 0; i < 24; i++) row.insertAdjacentHTML('beforeend', '<i class="bar"></i>');
const bars = s.q('.bar');
const h = (i, k) => k <= 1 ? 1 : .15 + REEL.rand(i * 31 + k * 7) * .85;
s.fromTo(bars, { scaleY: 0 }, { scaleY: 1 }, { at: 0, dur: .6, ease: 'expo.out', stagger: { each: .02, from: 'center' } });
for (let k = 2; k < 10; k++)
  s.fromTo(bars, { scaleY: i => h(i, k - 1) }, { scaleY: i => h(i, k) }, { at: B * k, dur: B * .8, ease: 'expo.out' });
```

### T14 Split Screen 分屏
**能量** 3–4 · **适合** P2 / P6 / P3
画面分成 2–4 块，各自从不同方向揭开，里面的文字反向滑入；还可以动画网格比例做“焦点切换”。
要点：每块面板 `overflow:hidden`；`gridTemplateColumns` 也能补间（`'1fr 1fr 1fr'` → `'1fr 2fr 1fr'`），但要确认收窄后的面板仍放得下里面的文字。

```html
<div class="panes"><div class="pane p1"><span>DESIGN</span></div><div class="pane p2"><span>MOTION</span></div><div class="pane p3"><span>CODE</span></div></div>
```
```css
#sX .panes{position:absolute;inset:0;display:grid;grid-template-columns:1fr 1fr 1fr}
#sX .pane{position:relative;overflow:hidden;display:grid;place-items:center}
#sX .p1{background:var(--accent)} #sX .p2{background:var(--fg);color:var(--bg)} #sX .p3{background:var(--accent-2)}
#sX .pane span{font:900 96px var(--font-display);letter-spacing:-.03em}
```
```js
s.fromTo('.pane', { clipPath: i => ['inset(100% 0 0 0)', 'inset(0 0 100% 0)', 'inset(100% 0 0 0)'][i] }, { clipPath: 'inset(0% 0% 0% 0%)' },
  { at: 0, dur: .7, ease: 'snap', stagger: .1 });
s.fromTo('.pane span', { y: i => i % 2 ? -220 : 220, opacity: 0 }, { y: 0, opacity: 1 }, { at: .3, dur: .8, ease: 'expo.out', stagger: .1 });
s.fromTo('.panes', { gridTemplateColumns: '1fr 1fr 1fr' }, { gridTemplateColumns: '1fr 2fr 1fr' }, { at: B*4, dur: .7, ease: 'snap' }); // 收窄后侧栏文字仍要放得下
```

### T17 3D Flip 3D 翻转
**能量** 3 · **适合** P6 / P2 / P5（慢速）
文字卡片绕 X 轴翻转落下，像翻页牌或掀开的卡片。
要点：父元素 `perspective`；卡片 `transform-origin` 在底边；`backface-visibility:hidden`。

```html
<div class="flip"><span class="card">NEW</span><span class="card">ERA</span></div>
```
```css
#sX .flip{position:absolute;inset:0;display:flex;gap:30px;justify-content:center;align-items:center;perspective:1400px}
#sX .card{display:block;padding:10px 50px;background:var(--fg);color:var(--bg);font:900 220px/1 var(--font-display);transform-origin:50% 100%;backface-visibility:hidden}
```
```js
s.fromTo('.card', { rotateX: -95, opacity: 0 }, { rotateX: 0, opacity: 1 }, { at: 0, dur: .9, ease: 'expo.out', stagger: .12 });
s.fromTo('.card', { rotateX: 0 }, { rotateX: 95 }, { at: s.dur - B, dur: .45, ease: 'expo.in', stagger: .06 });
```

### T18 Orbit HUD 轨道仪表
**能量** 3 · **适合** P4（主力）
同心圆轨道以不同速度、方向旋转，配刻度、读数和百分比。
要点：SVG 子元素必须 `transform-box: fill-box; transform-origin: center`；虚线圆用 scale + 旋转入场，实线圆和刻度可以用 draw。

```html
<svg class="orbit" viewBox="-500 -500 1000 1000" width="1000" height="1000">
  <circle class="o1" r="460"/><circle class="o2" r="380"/><circle class="o3" r="300"/>
  <path class="tick" d="M0 -490 V-430 M0 430 V490 M-490 0 H-430 M430 0 H490"/>
</svg>
<div class="readout"><b class="pct">0</b><span>% SYNC</span></div>
```
```css
#sX .orbit{position:absolute;left:460px;top:40px}
#sX .orbit *{fill:none;stroke:var(--accent);transform-box:fill-box;transform-origin:center}
#sX .o1{stroke-width:2;stroke-dasharray:4 14}
#sX .o2{stroke-width:1}
#sX .o3{stroke-width:10;stroke-dasharray:60 30 8 30}
#sX .tick{stroke-width:2}
#sX .readout{position:absolute;left:0;right:0;top:470px;text-align:center;font:200 120px/1 var(--font-display)}
#sX .readout span{display:block;font:500 22px var(--font-mono);letter-spacing:.4em;margin-top:16px}
```
```js
s.draw('.o2, .tick', { at: 0, dur: 1.2, ease: 'snap' });
s.fromTo('.o1, .o3', { scale: .6, opacity: 0 }, { scale: 1, opacity: 1 }, { at: .2, dur: 1, ease: 'expo.out', stagger: .15 });
s.fromTo('.o1', { rotate: 0 }, { rotate: 90 }, { at: 0, dur: s.dur, ease: 'linear' });
s.fromTo('.o3', { rotate: 0 }, { rotate: -140 }, { at: 0, dur: s.dur, ease: 'linear' });
s.count('.pct', { from: 0, to: 100, at: B, dur: B*6, ease: 'expo.inOut' });
```

---

## C. 空间与质感类

### T15 Light Sweep 光扫
**能量** 2 · **适合** P1 / P5 / P4
一道高光斜扫过文字表面，像金属或胶片反光。常用于结尾签名。
要点：`background-clip:text`；不要再对同一个元素 split（会破坏背景裁切）；金色版把高光改成 `#FFF3D6`。

```html
<div class="sweep">AURELIA</div>
```
```css
#sX .sweep{position:absolute;left:0;right:0;top:420px;text-align:center;font:500 200px/1 var(--font-display);letter-spacing:.06em;color:transparent;
  background:linear-gradient(100deg,var(--fg) 42%,#ffffff 50%,var(--fg) 58%);background-size:300% 100%;-webkit-background-clip:text;background-clip:text}
```
```js
s.fromTo('.sweep', { opacity: 0, letterSpacing: '0.2em' }, { opacity: 1, letterSpacing: '0.06em' }, { at: 0, dur: 1.6, ease: 'glide' });
s.fromTo('.sweep', { backgroundPosition: '100% 0%' }, { backgroundPosition: '0% 0%' }, { at: B*2, dur: 1.6, ease: 'sine.inOut' });
```

### T16 RGB Glitch 色散故障
**能量** 4–5 · **适合** P3（主力）、P4（轻量）
三份叠加的文字（红、青、白）用 `screen` 混合，在一个短时间窗内随机错位，配合整体 glitch。
要点：错位用一串 `set`（每 1/30 秒一次）实现，数值来自 `REEL.rand`，因此可以精确定位；最后一定要归位。

```html
<div class="rgb"><span>ERROR</span><span>ERROR</span><span>ERROR</span></div>
```
```css
#sX .rgb{position:absolute;inset:0;display:grid;place-items:center}
#sX .rgb span{grid-area:1/1;font:400 360px/1 var(--font-display);mix-blend-mode:screen}
#sX .rgb span:nth-child(1){color:#FF0040} #sX .rgb span:nth-child(2){color:#00FFC8} #sX .rgb span:nth-child(3){color:#FFFFFF}
```
```js
const [r, c] = s.q('.rgb span'), t0 = B*2;
for (let k = 0; k < 16; k++) {
  const t = t0 + k / 30, a = k % 5 === 4 ? 0 : 1;
  s.set(r, { x: a * (REEL.rand(k * 3) - .5) * 60, y: a * (REEL.rand(k * 3 + 1) - .5) * 14 }, t);
  s.set(c, { x: a * (REEL.rand(k * 3 + 2) - .5) * -60 }, t);
}
s.set([r, c], { x: 0, y: 0 }, t0 + 16 / 30);
s.glitch({ at: t0, dur: .25 });
```

### T19 Zoom-Through 放大穿越
**能量** 5 · **适合** P1 / P2 / P4 / P3 · **英雄时刻常用**，也可当转场（X06）
镜头冲进一个字母的中空处（O、D、0、8、口、回），中空处的颜色填满画面，切到下一场。
要点：`transform-origin` 对准字母中空处（百分比相对文字盒子），**必须用 `?t=` 截帧确认对准**；用 `expo.in` 越冲越快；下一场的底色 = 冲进去后看到的颜色。

```html
<div class="zoom"><span class="zw">GO</span></div>
```
```css
#sX .zoom{position:absolute;inset:0;display:grid;place-items:center}
#sX .zw{font:900 520px/1 var(--font-display);transform-origin:71% 53%}  /* 对准 O 的中心，按截帧微调 */
```
```js
s.fromTo('.zw', { scale: .9, opacity: 0 }, { scale: 1, opacity: 1 }, { at: 0, dur: .8, ease: 'expo.out' });
s.fromTo('.zw', { scale: 1 }, { scale: 60 }, { at: s.dur - .8, dur: .8, ease: 'expo.in' });
```

### T20 Parallax Depth 视差纵深
**能量** 1–3 · **适合** 全部；呼吸场的首选
3 层以不同速度横移：远景慢、中景中、近景快且虚化（景深）。可以再做一次“变焦”：近景变虚、中景变实。
要点：速度比约 1 : 3 : 8；近景放大并模糊；全部用 `linear`。

```html
<div class="layer far"><div class="far-grid"></div></div>
<div class="layer mid"><h2 class="quiet">silence is a frame too</h2></div>
<div class="layer near" data-bleed><i class="blob"></i></div>
```
```css
#sX .far-grid{position:absolute;inset:-100px;background-image:linear-gradient(var(--accent-2) 1px,transparent 1px),linear-gradient(90deg,var(--accent-2) 1px,transparent 1px);background-size:120px 120px;opacity:.25}
#sX .quiet{position:absolute;left:0;right:0;top:500px;text-align:center;font:italic 300 72px var(--font-display)}
#sX .blob{position:absolute;left:1200px;top:600px;width:700px;height:700px;border-radius:50%;background:var(--accent);filter:blur(14px);opacity:.9}
```
```js
s.fromTo('.far', { x: 0 }, { x: -60 }, { at: 0, dur: s.dur, ease: 'linear' });
s.fromTo('.mid', { x: 0 }, { x: -180 }, { at: 0, dur: s.dur, ease: 'linear' });
s.fromTo('.near', { x: 0 }, { x: -520 }, { at: 0, dur: s.dur, ease: 'linear' });
s.fromTo('.quiet', { filter: 'blur(12px)', opacity: 0 }, { filter: 'blur(0px)', opacity: 1 }, { at: B, dur: 1.6, ease: 'glide' }); // 对焦
```

### T21 Gradient Aura 流光氛围
**能量** 1–2 · **适合** P4 / P5 / P1 / P7（低饱和墨晕）
2–3 个巨大的模糊色团在文字后方缓慢游移，营造“网格渐变”般的氛围光。
要点：模糊是静态的，只动 transform（性能好）；加 `will-change:transform`；这是背景层，前面要有清晰的主体。

```html
<div class="layer bg"><i class="aura a1"></i><i class="aura a2"></i><i class="aura a3"></i></div>
```
```css
#sX .aura{position:absolute;width:900px;height:900px;border-radius:50%;filter:blur(140px);opacity:.75;will-change:transform}
#sX .a1{background:var(--accent);left:-200px;top:-200px}
#sX .a2{background:var(--accent-2);right:-250px;top:200px}
#sX .a3{background:#ffffff;left:600px;bottom:-500px;opacity:.25}
```
```js
s.fromTo('.aura', { x: 0, y: 0, scale: .8 }, { x: i => [380, -420, 160][i], y: i => [220, -160, -260][i], scale: 1.15 }, { at: 0, dur: s.dur, ease: 'sine.inOut' });
```

### T22 Particle Field 粒子场
**能量** 2–5 · **适合** P4（主力）、P1（漂浮尘埃）
Canvas 绘制数百个粒子：曲速星空（由中心向外加速飞出）或漂浮尘埃。
要点：粒子属性在搭建时由 `REEL.rand` 决定；`s.call` 里的位置**只由 lt 计算**，不能累加——这样拖动时间轴也正确。

```html
<canvas class="pf" width="1920" height="1080"></canvas>
```
```css
#sX .pf{position:absolute;inset:0}
```
```js
const cv = s.q('.pf')[0], ctx = cv.getContext('2d'), N = 500;
const P = Array.from({ length: N }, (_, i) => ({ a: REEL.rand(i * 3) * Math.PI * 2, d: REEL.rand(i * 3 + 1), z: .3 + REEL.rand(i * 3 + 2) * .7 }));
s.call((p, lt) => {
  ctx.clearRect(0, 0, 1920, 1080);
  const speed = .12 + p * .5;                       // 越来越快
  P.forEach(q => {
    const k = (q.d + lt * speed * q.z) % 1, r = k * k * 1300;
    const x = 960 + Math.cos(q.a) * r, y = 540 + Math.sin(q.a) * r, len = 4 + r * .25 * speed;
    ctx.strokeStyle = `rgba(230,241,255,${Math.min(1, r / 400)})`;
    ctx.lineWidth = q.z * 2.2;
    ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + Math.cos(q.a) * len, y + Math.sin(q.a) * len); ctx.stroke();
  });
}, { at: 0, dur: s.dur });
// 漂浮尘埃版：x = (q.d * 1920 + lt * 30 * q.z) % 1920，y 用 Math.sin(lt * q.z + q.a) 小幅摆动，画小圆点
```
