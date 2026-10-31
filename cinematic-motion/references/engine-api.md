# REEL 引擎 API

模板内置的确定性时间轴引擎。“确定性”是指：任何时刻 t 的画面只由 t 决定，与播放历史无关。所以它可以随意暂停、拖动、跳到 `?t=12.5`，也能逐帧导出视频。这也是禁止 `@keyframes`、`transition`、`setTimeout`、`Math.random` 的原因——它们都会破坏这一点。

## 目录
1. 画布与 DOM 结构
2. STORYBOARD 与时间轴
3. 场景作用域 `s`
4. `fromTo` 与属性规则
5. 其他方法：set / call / draw / count / scramble / type / flash / shake / glitch
6. 工具：REEL.split / rand / rng / $
7. HUD 与特效令牌
8. 完整最小示例
9. 常见坑

---

## 1. 画布与 DOM 结构

- 画布尺寸由 `:root` 的 `--w` / `--h` 决定（默认 1920×1080）。**所有尺寸都按这块画布的 px 写**，引擎负责整体缩放适配窗口。
- 时间单位是秒。用 `B`（1 拍的秒数）的倍数书写，保证动作落在拍点上。

```
.stage                      画布（引擎缩放）
  .rig                      shake / glitch 作用在这一层
    section.scene#sN        引擎按 STORYBOARD 切换显示（加 .on 类）
      .cam                  引擎自动施加镜头运动 —— 不要对 .cam 做动画
        .layer.bg / .main / .detail   你的内容（.layer 默认 absolute 铺满）
    .tx                     全局转场元素（擦除面板等），在所有场景之上
    .fx-flash               闪白 / 黑场层，由 flash() 控制
  .fx-grain                 胶片颗粒（--grain 控制强度，引擎每 1/24 秒抖动一次）
  .fx-vignette              暗角（--vignette）
  .letterbox                遮幅黑边（--lb，单位 px，不写单位）
  .hud                      不随镜头运动的信息层（时间码、编号等）
```

`.scene`、`.cam`、`.layer`、`.tx` 都是 `position:absolute; inset:0`。场景内元素用绝对定位或 flex/grid 布局均可。

## 2. STORYBOARD 与时间轴

```js
const BPM = 120;
const B = 60 / BPM;            // 1 拍 = 0.5s；1 小节 = 4*B
const STORYBOARD = [
  { id:'s1', start: 0*B,  end: 8*B,  title:'开场', technique:'T10 Line Draw', transition:'X04 Shutter', cam:'push' },
  { id:'s2', start: 8*B,  end: 16*B, title:'宣言', technique:'T03 Scale Slam', transition:'X05 Iris', cam:'pull' },
  // ...
];
const tl = REEL.timeline({ duration: 60*B, bpm: BPM, fps: 30, loop: true });
tl.storyboard(STORYBOARD);
tl.scene('s1', s => { /* 场景动画 */ });
tl.start();
```

| 字段 | 说明 |
|---|---|
| `id` | 对应 `<section class="scene" id="…">` |
| `start` / `end` | 场景可见区间 [start, end)。start 必须在拍点上 |
| `title` | 可显示在 HUD 的 `data-reel="title"` 中 |
| `technique` | 以技法编号开头，如 `'T03 Scale Slam'`（check.py 据此检查多样性） |
| `transition` | 以转场编号开头，如 `'X05 Iris'`；最后一场写 `'END'` |
| `cam` | 镜头运动：`push`（默认，缓推 1→1.06）· `pull`（缓拉 1.08→1）· `left` / `right`（横移 80px）· `rise` / `fall`（竖移 60px）· `none` |

- 场景**可以重叠**：需要两场同时可见的转场（X05 / X07 / X11 / X13 / X14 / X15）把前一场的 `end` 延长转场的时长，后一场的 `start` 仍然落在拍点上。
- 重叠时，DOM 中靠后的 section 在上层——所以 section 的顺序必须与 STORYBOARD 一致。
- `duration` 必须等于最后一场的 `end`。`loop: true` 时播放到结尾自动回到 0。

## 3. 场景作用域 `s`

`tl.scene(id, s => {...})` 里的 `s`：

| 成员 | 含义 |
|---|---|
| `s.id` `s.el` | 场景 id 与 section 元素 |
| `s.start` `s.end` `s.dur` | 场景的绝对起止时间与时长（秒） |
| `s.beat(n)` `s.bar(n)` | n 拍 / n 小节的秒数（直接用 `B*n` 也行） |
| `s.q(sel)` | 在本场景内查询元素，返回数组 |

- `s` 上所有方法的 `at` 都是**相对场景起点**的时间；选择器字符串只在本场景内查找。
- `tl` 本身有同样的方法，只是 `at` 为绝对时间、选择器在整个文档查找——全局转场元素（`.tx` 里的东西）写在 `tl` 上。
- 想在场景作用域里操作场景外的元素，传元素本身：`s.fromTo(REEL.$('.tx .w1'), …)`。

## 4. `fromTo` 与属性规则

```js
s.fromTo(targets, fromProps, toProps, { at, dur, ease, stagger })
```

| 参数 | 默认 | 说明 |
|---|---|---|
| `targets` | — | 选择器字符串 / 元素 / 数组（如 `REEL.split` 的结果） |
| `at` | 0 | 开始时间（秒） |
| `dur` | 0.8 | 时长（秒） |
| `ease` | `'expo.out'` | 见下表 |
| `stagger` | 0 | 数字（每个元素依次延迟）或 `{ each, from, seed }` / `{ amount, from }`；`from` 可取 `'start'` `'end'` `'center'` `'edges'` `'random'` 或索引数字 |

**ease 可选值**：`linear` · `sine/quad/cubic/quart/quint/expo/circ/back/elastic` + `.in` / `.out` / `.inOut`（如 `expo.out`）· `power1–4.*`（GSAP 别名）· 招牌缓动 `snap`（锐利的 inOut，用于位移和擦除）· `glide`（顺滑减速入场）· `whip`（甩镜，几乎瞬移）· `punch`（轻微过冲弹出）· 自定义 `'cb(.7,0,.2,1)'`。

### 变换简写（同一元素上组合成一个 transform）

| 键 | 默认单位 | 说明 |
|---|---|---|
| `x` `y` `z` | px | 也可以写字符串 `'110%'`（相对自身尺寸）或 `'calc(-100% + -1920px)'` |
| `scale` `scaleX` `scaleY` | 无 | |
| `rotate` `rotateX` `rotateY` `skewX` `skewY` | deg | 3D 旋转需要父元素有 `perspective` |

组合顺序固定为：translate → rotateX → rotateY → rotate → skew → scale。**在同一个元素上使用这些简写时，不要在 CSS 里写 transform**（会被覆盖）。

### 任意 CSS 属性

- 驼峰或短横线写法都可以：`opacity` `clipPath` `filter` `color` `backgroundColor` `letterSpacing` `width` `borderRadius` `strokeDashoffset` `maskPosition` `backgroundPosition` `fontVariationSettings`……
- CSS 变量：`'--p': 0 → 1`（不带单位）。
- 以 `@` 开头的键设置 **属性** 而非样式：`'@d'`（路径变形，两端点数和命令结构要一致）、`'@r'`、`'@stroke-width'`。
- 纯数字：`opacity`、`z-index`、`font-weight`、`line-height`、CSS 变量、`@属性` 不加单位；其他 CSS 属性自动补 `px`。
- **字符串按数字逐个插值**，两端结构必须一致：`'inset(0 100% 0 0)'` → `'inset(0 0% 0 0)'`。单独的 `0` 会自动沿用另一端的单位。颜色请用 hex 或 rgb（不要用 `white` 这类名称）。
- 结构不一致的值无法补间，会在结束时跳变，引擎会给出警告（check.py 会把它报为 ERROR）。
- `display` 不能补间——用 `opacity` / `visibility` / `clipPath`，或用 `set`。

### 函数值（每个元素不同）

```js
s.fromTo(chars, { y: (i, el, n) => (i % 2 ? -1 : 1) * 200 }, { y: 0 }, { dur: .8, stagger: .03 });
```

函数在搭建时调用一次，参数为（索引, 元素, 总数）。此时场景还未显示，**不要在函数里测量尺寸**（offsetWidth 等会是 0）。

### 时间语义（重要）

1. 在元素某属性的第一个补间开始之前，会应用这个补间的 **from 值**——所以入场元素从 0 秒起就处在隐藏状态，不需要额外 set。
2. 同一属性有多个补间时，**最近一个已开始的补间生效**。连续动作的写法：下一个的 from = 上一个的 to。
3. 出场动画就是之后的另一个 `fromTo`：

```js
s.fromTo('.title', { y: '110%' }, { y: '0%' }, { at: 0, dur: .9, ease: 'expo.out' });       // 入场
s.fromTo('.title', { y: '0%' }, { y: '-110%' }, { at: s.dur - B, dur: .5, ease: 'expo.in' }); // 出场
```

## 5. 其他方法

| 方法 | 说明 |
|---|---|
| `s.set(targets, props, at)` | 在 `at` 瞬间设值。`at` 之前不施加（保持 CSS 默认值），除非该属性更早还有补间 |
| `s.call(fn, { at, dur })` | 每帧调用 `fn(p, localT)`，p 在 0→1 间线性变化，localT 为距 at 的秒数。区间外只在状态改变时以 p=0 或 1 调用一次。**fn 必须是 p/localT 的纯函数**（不能累加内部状态），因为时间可以跳转。适合 Canvas 绘制、自定义文字 |
| `s.draw(svgShapes, { at, dur, ease, stagger, erase })` | SVG 描线（自动设置 `pathLength=1`）。`erase:true` 为从起点擦除。适用于 path / line / circle / rect / polyline / ellipse，需有 `stroke`、`fill="none"` |
| `s.count(el, { from, to, at, dur, ease, decimals, prefix, suffix, group })` | 数字滚动；`group:false` 关闭千分位（年份必须关） |
| `s.scramble(el, { at, dur, chars, trail, rate, mode, seed })` | 乱码解码。`mode:'decode'`（默认，先全乱码再从左到右解出）或 `'build'`（逐字出现）。中文可传 `chars:'永和九年岁在癸丑暮春之初'` |
| `s.type(el, { at, dur, caret })` | 打字机，默认光标 `▍` |
| `s.flash({ at, in, out, color, peak })` | 闪白：`in`（默认 0）秒内升到 peak，`at` 时达到峰值，`out`（默认 0.18）秒内退去。`color:'#000'` 加 `in` 即黑场过渡 |
| `s.shake({ at, dur, amp, freq })` | 画面冲击抖动（作用在 `.rig`，默认 0.4s、14px），随时间衰减 |
| `s.glitch({ at, dur, amp })` | 故障：错位、斜切、反色、色相跳变（默认 0.3s） |

这些方法都返回 `s`，可以链式调用。

## 6. 工具

```js
const chars = REEL.split(s.q('.title'), { by: 'chars', mask: true });  // 拆字，返回 span 数组
const words = REEL.split(s.q('.sub'), 'words');                         // 拆词
REEL.rand(n)        // 整数 n → [0,1) 的固定伪随机数（同一个 n 永远同一个结果）
const r = REEL.rng(42); r(); r();   // 带种子的序列生成器，用于搭建时生成随机布局
REEL.$('.tx .w1')   // 全文档查询，返回数组
```

- `split`：只对**纯文本元素**使用（内部的子元素会被抹平）；同一元素重复 split 返回缓存结果；空格会保留。`mask:true` 会给每个字包一层 `overflow:hidden` 的 `.mask`，配合 `y:'110%' → '0%'` 实现遮罩升起。
- 按行遮罩：直接在 HTML 里写 `<span class="line"><span>第一行</span></span>`，对 `.line > span` 做动画。
- `split` 产生的 `.ch` / `.w` 是 inline-block，可以自由做 transform。

## 7. HUD 与特效令牌

HUD 里放这些属性的元素，引擎会自动更新内容：

| 属性 | 内容 |
|---|---|
| `data-reel="timecode"` | `00:12:05`（分:秒:帧） |
| `data-reel="scene"` | `03 / 08` |
| `data-reel="title"` | 当前场景的 `title` |
| `data-reel="progress"` | 引擎写入 `transform: scaleX(进度)`；请在 CSS 里给它 `transform-origin: 0 50%` |

特效令牌写在 `:root`，也可以在时间轴里对 `.stage` 做动画来覆盖（`.stage` 是所有层的祖先）：

```js
tl.fromTo('.stage', { '--lb': 0 }, { '--lb': 138 }, { at: 0, dur: 1.2, ease: 'snap' }); // 遮幅黑边滑入
tl.fromTo('.stage', { '--grain': .08 }, { '--grain': .2 }, { at: B*32, dur: .1 });      // 某段颗粒加重
```

## 8. 完整最小示例（一个场景）

```html
<section class="scene" id="s2"><div class="cam">
  <div class="layer bg"><i class="bar"></i><i class="bar"></i><i class="bar"></i></div>
  <div class="layer main"><h1 class="hero"><span class="line"><span>MAKE IT</span></span><span class="line"><span>MOVE.</span></span></h1></div>
  <div class="layer detail"><span class="tag">02 — MANIFESTO</span><span class="rule"></span></div>
</div></section>
```

```css
/* s2 · 宣言 */
#s2 .bar{position:absolute;top:0;bottom:0;width:6px;background:var(--accent);transform-origin:50% 100%}
#s2 .bar:nth-child(1){left:12%} #s2 .bar:nth-child(2){left:50%} #s2 .bar:nth-child(3){left:88%}
#s2 .hero{position:absolute;left:120px;bottom:180px;font:900 260px/.86 var(--font-display);letter-spacing:-.04em}
#s2 .tag{position:absolute;left:124px;top:110px;font:500 20px var(--font-mono);letter-spacing:.3em}
#s2 .rule{position:absolute;left:124px;right:124px;top:150px;height:1px;background:var(--fg);transform-origin:0 50%}
```

```js
tl.scene('s2', s => {
  s.fromTo('.bar', { scaleY: 0 }, { scaleY: 1 }, { at: 0, dur: B*2, ease: 'expo.out', stagger: { each: B/2, from: 'center' } });
  s.fromTo('.hero .line > span', { y: '110%' }, { y: '0%' }, { at: B, dur: 1, ease: 'expo.out', stagger: .12 });
  s.fromTo('.rule', { scaleX: 0 }, { scaleX: 1 }, { at: B*.5, dur: 1.2, ease: 'snap' });
  s.scramble('.tag', { at: B*.5, dur: .9 });
  s.fromTo('.hero', { letterSpacing: '-0.04em' }, { letterSpacing: '0.02em' }, { at: B, dur: s.dur - B, ease: 'linear' }); // 持续呼吸
  s.fromTo('.hero .line > span', { y: '0%' }, { y: '-110%' }, { at: s.dur - B, dur: .45, ease: 'expo.in', stagger: .06 });
});
```

## 9. 常见坑

1. **居中与变换冲突**：CSS 里用 `transform: translate(-50%,-50%)` 居中的元素一旦被引擎做 x/y/scale 动画，CSS 的 transform 会被覆盖导致跳位。改用 `inset:0; margin:auto`、flex 或 grid 居中。
2. **不要对 `.cam` 做动画**（引擎在用）。转场需要移动整场时，对 `section.scene` 本身（`s.el`）做动画是允许的。
3. **一个元素只属于一个场景**；相同的视觉在两个场景都出现时，各写一份（匹配剪辑就是这么做的）。
4. **SVG 子元素旋转/缩放**：给它们加 `transform-box: fill-box; transform-origin: center;`，否则会绕 SVG 左上角转。
5. **大面积 blur 很贵**：同一时刻带 `filter: blur()` 动画的大元素不超过 3 个；静态模糊的氛围光加 `will-change: transform`。
6. **轨道数量**：拆字很方便，但全片补间元素保持在约 1500 个以内（一段 40 个字 × 3 个属性 = 120 条轨道）。
7. **clip-path / polygon 两端点数必须相同**；`circle()` 两端都写完整：`circle(0% at 50% 50%)` → `circle(75% at 50% 50%)`。
8. **遮罩裁掉字母下沿**：`.mask` 和 `.line` 已预留上下 0.12em / 0.08em；行高极小（<0.85）时要给容器额外加 padding。
9. **字体加载**：引擎最多等待字体 3 秒再开始播放。字体在部分网络下可能加载失败，所以回退字体栈一定要写全。
10. **可变字体动画**（`fontVariationSettings`）需要 Google Fonts 链接里请求轴的范围（如 `wght@100..900`），只请求单个字重时无法动画。
11. **没有动画的元素会直接显示**：引擎只隐藏“有入场补间”的元素。搭建时批量生成元素（格子、粒子、形状）却只给其中一部分做动画，其余的会按 CSS 默认一直可见——要么只生成会出现的那些，要么给每个都写入场。
12. **引擎警告就是 bug**：选择器没匹配到、ease 名写错、值结构不一致、场景没写动画，都会出现在控制台和 check.py 报告里。
