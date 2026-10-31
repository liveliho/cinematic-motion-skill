# 转场库 X01–X16

转场不是“两个场景之间的空隙”，而是一个设计动作。观众记住一支片子，常常是因为它的转场。

在 STORYBOARD 的 `transition` 字段写**出场转场**的编号 + 英文名（如 `'X04 Shutter'`），最后一场写 `'END'`。全片至少 4 种，相邻不重复。

## 目录
- 三种实现方式
- X01 Hard Cut 硬切 · X02 Panel Wipe 色块擦除 · X03 Stacked Wipe 多层色块 · X04 Shutter 快门百叶
- X05 Iris 圆形扩张 · X06 Zoom-Through 放大穿越 · X07 Whip Pan 甩镜 · X08 Match Cut 匹配剪辑
- X09 Glitch Cut 故障切 · X10 Flash Cut 闪切 · X11 Push 推挤 · X12 Fade Through Black 黑场过渡
- X13 Slash 斜切 · X14 Card Shrink 卡片收缩 · X15 Ink Wipe 墨迹晕染 · X16 Type Wipe 巨字擦除
- 按预设推荐

---

## 三种实现方式

| 方式 | 转场 | 怎么写 |
|---|---|---|
| **A. 切点上的事件** | X01 X06 X08 X09 X10 X12 | 场景首尾相接（前一场 end = 后一场 start = 拍点），在切点上加闪白 / 故障 / 放大等事件 |
| **B. 覆盖层** | X02 X03 X04 X16 | 在 `.tx` 里放面板，面板在切点前盖住画面、切点后揭开；写在 `tl` 上，用绝对时间 |
| **C. 场景重叠** | X05 X07 X11 X13 X14 X15 | 两场要同时可见：**前一场的 end 延长转场时长**，后一场 start 仍在拍点；对 `s.el`（section 本身）做动画 |

方式 C 的 STORYBOARD 写法：

```js
{ id:'s3', start: 16*B, end: 24*B + .7, technique:'T12 Grid Build', transition:'X05 Iris', cam:'push' },
{ id:'s4', start: 24*B, end: 32*B,      technique:'T03 Scale Slam', transition:'X10 Flash', cam:'pull' },
```

通用原则：
- **切点永远在拍点上**，最好是小节第 1 拍。
- **带着动作切**（cut on action）：新场景第一帧就已经在动，不要从静止开始。
- 前一场的主体元素在切点前 1 拍开始出场，或者让转场盖住它——不要让观众看到元素“等着被切掉”。

---

### X01 Hard Cut 硬切
最强、最干净的转场。前一场 end = 后一场 start。
让它有意义：两场之间形成强对比——黑底 ↔ 强调色底、巨字 ↔ 小字、满屏 ↔ 留白；新场景的第一个动画 `at: 0`。

### X02 Panel Wipe 色块擦除
一块强调色面板扫过画面：先盖住，切点后揭开。

```html
<!-- 放在 .tx 里 -->
<i class="wipe" id="w1"></i>
```
```css
.tx .wipe{position:absolute;inset:0;background:var(--accent)}
```
```js
const cut = 16*B;   // 前一场结束 = 后一场开始
tl.fromTo('#w1', { x: '-100%' }, { x: '0%' },   { at: cut - .35, dur: .35, ease: 'expo.in' });
tl.fromTo('#w1', { x: '0%' },    { x: '100%' }, { at: cut,       dur: .45, ease: 'expo.out' });
```
同一块面板可以在之后的切点重复使用（再写一对 fromTo）。竖向擦除把 `x` 换成 `y`。

### X03 Stacked Wipe 多层色块
三块不同颜色的面板错开扫过，层次感强。揭开时从最上层开始（`from: 'end'`）。

```html
<i class="wipe c1"></i><i class="wipe c2"></i><i class="wipe c3"></i>
```
```css
.tx .c1{background:var(--accent)} .tx .c2{background:var(--accent-2)} .tx .c3{background:var(--fg)}
```
```js
const cut = 24*B, panels = REEL.$('.tx .c1, .tx .c2, .tx .c3');
tl.fromTo(panels, { y: '100%' }, { y: '0%' },   { at: cut - .5, dur: .4, ease: 'expo.in', stagger: .05 });
tl.fromTo(panels, { y: '0%' },   { y: '-100%' }, { at: cut + .05, dur: .5, ease: 'expo.inOut', stagger: { each: .06, from: 'end' } });
```

### X04 Shutter 快门百叶
8 条竖向百叶从中间向两侧依次合上，切点后再依次打开。
要点：合上动画必须在切点前全部完成——起点 = 切点 − 时长 − stagger 总跨度。

```css
.tx .sl{position:absolute;top:0;bottom:0;width:12.6%;background:var(--fg)}
```
```js
const tx = REEL.$('.tx')[0];
for (let i = 0; i < 8; i++) tx.insertAdjacentHTML('beforeend', `<i class="sl" style="left:${i * 12.5}%"></i>`);
const sl = REEL.$('.tx .sl'), cut = 32*B;
tl.fromTo(sl, { clipPath: 'inset(0 0 100% 0)' }, { clipPath: 'inset(0 0 0% 0)' }, { at: cut - .52, dur: .4, ease: 'expo.in', stagger: { amount: .12, from: 'center' } });
tl.fromTo(sl, { clipPath: 'inset(0% 0 0 0)' }, { clipPath: 'inset(100% 0 0 0)' }, { at: cut + .02, dur: .45, ease: 'expo.out', stagger: { amount: .12, from: 'center' } });
```
横向百叶：`style="top:${i * 12.5}%"`，CSS 改为 `left:0;right:0;height:12.6%`，clip-path 改左右方向。

### X05 Iris 圆形扩张
新场景从一个圆里扩张出来。圆心可以对准前一场的某个圆点（与 X08 结合效果最好）。
方式 C：前一场 end 延长 0.7s。

```js
// 写在后一场的 tl.scene 里
s.fromTo(s.el, { clipPath: 'circle(0% at 50% 50%)' }, { clipPath: 'circle(75% at 50% 50%)' }, { at: 0, dur: .7, ease: 'expo.inOut' });
// 圆心对准前一场的点：'circle(0% at 32% 58%)' → 'circle(90% at 32% 58%)'（偏心时半径要更大才能盖满）
```

### X06 Zoom-Through 放大穿越
镜头冲进字母的中空处（见 T19），中空处的颜色填满画面后硬切到下一场；**下一场的底色必须等于填满画面的颜色**。
写法与 T19 相同：前一场最后 0.8s 对字母做 `scale: 1 → 60`、`expo.in`。也可以冲进一个圆、一个方框或一个数字 0。

### X07 Whip Pan 甩镜
两场同时向一侧急速甩动并带运动模糊，像摄影机快速横摇。
方式 C：前一场 end 延长 0.35s。

```js
// 前一场的 tl.scene 里（s.dur 已包含延长部分）
s.fromTo(s.el, { x: 0, skewX: 0, filter: 'blur(0px)' }, { x: -1920, skewX: -8, filter: 'blur(24px)' }, { at: s.dur - .35, dur: .35, ease: 'whip' });
// 后一场的 tl.scene 里
s.fromTo(s.el, { x: 1920, skewX: -8, filter: 'blur(24px)' }, { x: 0, skewX: 0, filter: 'blur(0px)' }, { at: 0, dur: .35, ease: 'whip' });
```
竖版画布把 1920 换成 1080，或直接用 `'-100%'` / `'100%'`。

### X08 Match Cut 匹配剪辑
前一场最后一帧和后一场第一帧共享同一个形状：同样的位置、大小、颜色。硬切时形状保持不动，周围的世界变了。
例：s3 结尾一个 300px 的强调色圆停在 (1320, 540)；s4 开场同一个圆在同一位置，随后它变成单词里的 “O”，或扩大成整个背景。
写法：两场各放一份同样的形状（位置写死成相同的数值），前一场的形状最后停稳，后一场的形状从 `at: 0` 开始变化。这是最“聪明”的转场，P1 / P4 / P7 尤其适合。

### X09 Glitch Cut 故障切
切点附近 0.3 秒的画面撕裂、错位、反色，再加一次强调色闪。

```js
const cut = 40*B;
tl.glitch({ at: cut - .12, dur: .3, amp: 60 });
tl.flash({ at: cut, peak: .5, out: .1, color: '#D4FF00' });
```
P4 用轻量版：`amp: 20, dur: .2`，不加闪。

### X10 Flash Cut 闪切
切点上一次闪白（或强调色闪），配合硬切，冲击力极强。

```js
tl.flash({ at: 32*B, out: .25 });                    // 白闪
tl.flash({ at: 48*B, out: .2, color: '#FF3B00' });   // 强调色闪
```
注意：闪光层的颜色一旦设置过，就会保持到下一次设置——所以全片只要有一次写了 `color`，之后每次闪都要写明 `color`（白色写 `'#FFFFFF'`）。

### X11 Push 推挤
新场景把旧场景推出画面。
方式 C：前一场 end 延长 0.6s。

```js
// 前一场
s.fromTo(s.el, { y: '0%' }, { y: '-100%' }, { at: s.dur - .6, dur: .6, ease: 'snap' });
// 后一场
s.fromTo(s.el, { y: '100%' }, { y: '0%' }, { at: 0, dur: .6, ease: 'snap' });
```

### X12 Fade Through Black 黑场过渡
渐暗到黑、切换、再渐亮。电影感最强，但最慢——全片最多用 1 次，只用于 P1 / P5 / P7，通常放在呼吸场前后。

```js
tl.flash({ at: 44*B, in: .5, out: .6, color: '#000000' });   // 0.5s 渐黑，切点全黑，0.6s 渐亮
```

### X13 Slash 斜切
新场景沿一条斜线切入，边缘可以跟一条强调色斜条。
方式 C：前一场 end 延长 0.6s。

```js
// 后一场
s.fromTo(s.el, { clipPath: 'polygon(0% 0%, 0% 0%, -30% 100%, -30% 100%)' }, { clipPath: 'polygon(0% 0%, 130% 0%, 100% 100%, -30% 100%)' }, { at: 0, dur: .6, ease: 'snap' });
```
```css
/* 可选：跟随边缘的斜条，放在 .tx 里 <i class="slash"></i> */
.tx .slash{position:absolute;top:-10%;bottom:-10%;left:0;width:56px;background:var(--accent)}
```
```js
tl.fromTo('.tx .slash', { x: -400, skewX: -16 }, { x: 2400, skewX: -16 }, { at: 24*B, dur: .6, ease: 'snap' });
```

### X14 Card Shrink 卡片收缩
旧场景缩成一张圆角卡片并变暗，新场景从下方盖上来。像 App 里的页面切换，干净现代。
方式 C：前一场 end 延长 0.7s。

```js
// 前一场
s.fromTo(s.el, { scale: 1, borderRadius: '0px', filter: 'brightness(1)' }, { scale: .84, borderRadius: '28px', filter: 'brightness(.45)' }, { at: s.dur - .7, dur: .7, ease: 'snap' });
// 后一场
s.fromTo(s.el, { y: '105%' }, { y: '0%' }, { at: 0, dur: .7, ease: 'snap' });
```
```css
#s5{box-shadow:0 -30px 80px rgba(0,0,0,.45)}   /* 后一场加阴影，层次更清楚 */
```

### X15 Ink Wipe 墨迹晕染
新场景像墨迹一样从一侧柔和地洇开（P7 主力，P5 可用）。
方式 C：前一场 end 延长 1.2s。

```css
#s6{-webkit-mask-image:linear-gradient(90deg,#000 45%,transparent 55%);mask-image:linear-gradient(90deg,#000 45%,transparent 55%);
    -webkit-mask-size:300% 100%;mask-size:300% 100%;-webkit-mask-repeat:no-repeat;mask-repeat:no-repeat}
```
```js
// 后一场
s.fromTo(s.el, { maskPosition: '100% 0%' }, { maskPosition: '0% 0%' }, { at: 0, dur: 1.2, ease: 'sine.inOut' });
```
从中心晕开的版本：CSS 改为 `mask-image:radial-gradient(circle,#000 35%,transparent 65%); mask-position:50% 50%`，动画 `maskSize: '0% 0%'` → `'400% 400%'`。

### X16 Type Wipe 巨字擦除
一块印着巨大文字的强调色面板横扫过画面，切点发生在它完全盖住画面的瞬间。适合带品牌名或章节名的转场。

```html
<div class="tw-panel"><span>NEXT</span></div>   <!-- 放在 .tx 里 -->
```
```css
.tx .tw-panel{position:absolute;top:0;bottom:0;left:0;width:220%;background:var(--accent);display:flex;align-items:center;justify-content:center;
  font:900 520px/1 var(--font-display);color:var(--bg);white-space:nowrap;letter-spacing:-.04em}
```
```js
const cut = 28*B;
tl.fromTo('.tx .tw-panel', { x: '100%' }, { x: '-100%' }, { at: cut - .55, dur: 1.1, ease: 'quart.inOut' });   // 对称缓动的中点恰好是切点
```
面板宽 220% 保证有约 0.1 秒完全盖住画面，切点就藏在这段时间里；不要用 `snap`，它中段太快，面板上的字会看不清。

---

## 按预设推荐

| 预设 | 首选 | 可用 | 避免 |
|---|---|---|---|
| P1 NOIR | X12 X05 X08 | X02 X10（克制）X06 | X03 X09 X16 |
| P2 SWISS | X01 X04 X02 | X11 X16 X10 | X12 X15 X09 |
| P3 ACID | X09 X10 X03 | X07 X13 X16 | X12 X15 |
| P4 TECH | X05 X08 X13 | X09（轻）X06 X01 | X15 X03 |
| P5 LUXE | X02 X14 X05 | X12 X15 X08 | X09 X10 X07 |
| P6 POP | X03 X05 X11 | X14 X16 X02 | X12 X09 |
| P7 INK | X15 X12 X08 | X05 X02 | X09 X10 X03 X13 |
