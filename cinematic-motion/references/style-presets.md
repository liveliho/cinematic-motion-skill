# 风格预设

每支片子**只选一个**预设。预设是一套完整的设计系统（色板 + 字体 + 节奏 + 运动性格 + 质感 + 禁忌），混搭会让片子失去统一感。用户给了品牌色时，只替换色板：品牌主色 → `--accent`，再按预设的明暗关系配 `--bg` / `--fg`；其余规则不变。

## 选择表

| 用户提到的关键词 / 用途 | 预设 |
|---|---|
| 电影、剧集、悬疑、纪录片、作品集开场、高级、暗黑、预告片 | **P1 NOIR TITLE 黑色片头** |
| 设计、建筑、展览、品牌发布、简约、理性、国际主义、信息 | **P2 SWISS KINETIC 瑞士动势** |
| 潮流、音乐、街头、运动、游戏、年轻、炸、燃、派对、电音 | **P3 ACID BRUTAL 酸性野兽派** |
| 科技、AI、芯片、数据、未来、SaaS、产品发布、太空 | **P4 TECH HUD 科技界面** |
| 时尚、奢侈品、美妆、杂志、珠宝、酒店、优雅、艺术 | **P5 EDITORIAL LUXE 杂志奢华** |
| 儿童、食品饮料、电商促销、活泼、可爱、社交媒体、节日 | **P6 POP KINETIC 波普活力** |
| 国潮、新中式、茶、书法、传统节日、文化、东方、诗词 | **P7 INK & SEAL 新中式墨韵** |
| 没有任何线索（纯创意探索） | P2 或 P3（P2 更理性高级，P3 更有冲击力）；中文主题可选 P7 |

所有预设的字体回退栈都已包含中文系统字体。中文文案用预设里的「中文」字体作为 display 或 text。

---

## P1 · NOIR TITLE 黑色片头

- **气质**：克制、悬疑、昂贵。像 HBO 剧集片头或 A24 预告片。
- **色板**：`--bg #0A0A0A` · `--fg #EDE6DA`（象牙白）· `--accent #C8102E`（血红）· `--accent-2 #5E5A55`（暖灰）
  - 备选：金色版 `--accent #C9A45C`；冷蓝版 `--accent #4F7CAC`
- **字体**：
  - display：`'Bodoni Moda', 'Noto Serif SC', 'Songti SC', 'SimSun', serif`（大量使用 italic）
  - text：`'Inter Tight', 'PingFang SC', 'Microsoft YaHei', sans-serif`（300 / 500，全大写小字，宽字距）
  - mono：`'JetBrains Mono', ui-monospace, Consolas, monospace`
  - 中文：Noto Serif SC 900（标题）/ 300（副文）
  - 链接：`https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,wght@0,400..900;1,400..900&family=Inter+Tight:wght@300;500;700&family=JetBrains+Mono:wght@400;600&family=Noto+Serif+SC:wght@300;900&display=swap`
- **BPM**：72–90。场景偏长（2–3 小节），留出大量停顿。
- **运动性格**：慢进、精确停。入场 `glide` / `expo.out` 1.2–1.8s；出场 `expo.in` 0.6s；几乎不用过冲。动作少而准，静止本身就是张力。
- **构图**：大面积黑色负空间；文字小而精确，或巨大而只露一部分；水平细线、居中对称与极端偏置交替。
- **招牌技法**：T01 遮罩升起 · T15 光扫 · T05 描边填充 · T19 放大穿越 · T20 视差纵深 · T10 描线
- **推荐转场**：X12 黑场过渡（全片最多 1 次）· X05 圆形扩张 · X02 色块擦除（用 accent-2）· X08 匹配剪辑 · X10 闪白（克制，peak .5）
- **质感**：`--grain .14` · `--vignette .7` · `--lb 138`（2.39:1 遮幅，开场时让黑边滑入）
- **细节层**：罗马数字场景编号（I / II / III）、极细 1px 线、片厂式小字（"A FILM BY"、"IN ASSOCIATION WITH"）
- **禁忌**：弹性 / 回弹缓动；三种以上颜色；快速频闪；圆角。

## P2 · SWISS KINETIC 瑞士动势

- **气质**：理性、锋利、节奏精确。国际主义平面设计会动起来的样子。
- **色板**：`--bg #F1EFEA`（纸白）· `--fg #111111` · `--accent #FF3B00`（国际橙）· `--accent-2 #1F3BFF`（克莱因蓝，少量）
  - 备选：反色版 `--bg #111111` `--fg #F1EFEA`
- **字体**：
  - display：`'Archivo', 'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', sans-serif`（可变字体：字宽 62–125、字重 100–900，适合做 T26 字重呼吸）
  - text：同 display
  - mono：`'JetBrains Mono', ui-monospace, Consolas, monospace`
  - 中文：Noto Sans SC 900 / 300
  - 链接：`https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&family=JetBrains+Mono:wght@400;700&family=Noto+Sans+SC:wght@300;900&display=swap`
- **BPM**：116–128。每个剪切点都卡在拍上。
- **运动性格**：硬朗、果断。`snap` 和 `expo.out` 为主，0.4–0.7s；大量硬切；动作像被网格吸附。
- **构图**：12 栏网格；左对齐；巨大的数字编号；文字与色块形成严格的几何关系；常用分屏。
- **招牌技法**：T12 网格生成 · T13 律动条 · T09 数字滚动 · T07 一拍一词 · T14 分屏 · T26 字重呼吸 · T04 巨字横移
- **推荐转场**：X01 硬切 · X04 快门百叶 · X02 色块擦除 · X11 推挤 · X16 巨字擦除
- **质感**：`--grain .04` · `--vignette 0` · `--lb 0`
- **细节层**：栏线、坐标（N 47°22′）、编号 01–08、时间码、注册标记 ⊕、小号图注
- **禁忌**：斜体衬线；柔和渐变；居中堆叠的大段文字；模糊滤镜（除甩镜外）。

## P3 · ACID BRUTAL 酸性野兽派

- **气质**：大声、粗粝、过载。音乐节海报、球鞋发布、电子乐视觉。
- **色板**：`--bg #0B0B0B` · `--fg #F4F4F0` · `--accent #D4FF00`（酸性绿）· `--accent-2 #FF2E88`（荧光粉）
  - 备选：`--accent #FF4D00` + `--accent-2 #00E0FF`
- **字体**：
  - display：`'Anton', 'ZCOOL QingKe HuangYou', 'Noto Sans SC', 'Microsoft YaHei', sans-serif`（窄而极粗，全大写）
  - text：`'Space Grotesk', 'PingFang SC', 'Microsoft YaHei', sans-serif`
  - mono：`'Space Mono', ui-monospace, Consolas, monospace`
  - 中文：ZCOOL QingKe HuangYou（站酷庆科黄油体）或 Noto Sans SC 900
  - 链接：`https://fonts.googleapis.com/css2?family=Anton&family=Space+Grotesk:wght@400;700&family=Space+Mono:wght@400;700&family=ZCOOL+QingKe+HuangYou&family=Noto+Sans+SC:wght@900&display=swap`
- **BPM**：128–150。快切、重拍密集。
- **运动性格**：暴力而精准。砸字 0.35–0.5s `expo.out` + `shake`；`whip` 甩镜；偶尔 `punch` 过冲；每小节第 1 拍都有冲击。
- **构图**：文字撑满甚至溢出画面；描边字与实心字叠加；倾斜 -6° 的文字带；跑马灯铺满。
- **招牌技法**：T03 重拍砸字 · T06 文字墙 · T16 色散故障 · T24 残影回声 · T11 形状爆发 · T04 巨字横移 · T07 一拍一词
- **推荐转场**：X09 故障切 · X10 闪白 · X03 多层色块 · X07 甩镜 · X13 斜切
- **质感**：`--grain .12` · `--vignette .35` · `--lb 0`；可以加横向扫描线细节
- **细节层**：警告条纹、条形码、"VOL.03"、星号 ✱、箭头 →、大号序号
- **禁忌**：细字重；优雅的衬线；慢速淡入淡出；大面积留白超过 2 秒。

## P4 · TECH HUD 科技界面

- **气质**：精密、冷静、未来感。发布会主 KV、AI 产品片、航天任务画面。
- **色板**：`--bg #05070D`（深空黑蓝）· `--fg #E6F1FF` · `--accent #00E5FF`（电光青）· `--accent-2 #7C5CFF`（紫）
  - 备选：`--accent #3DFF9A`（终端绿）；`--accent #FF6A00`（警示橙）
- **字体**：
  - display：`'Sora', 'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', sans-serif`
  - text：同 display（200 / 600）
  - mono：`'JetBrains Mono', ui-monospace, Consolas, monospace`（大量使用）
  - 中文：Noto Sans SC 200（大标题用细字更有科技感）/ 700
  - 链接：`https://fonts.googleapis.com/css2?family=Sora:wght@200..800&family=JetBrains+Mono:wght@300..700&family=Noto+Sans+SC:wght@200;700&display=swap`
- **BPM**：100–120。
- **运动性格**：数据驱动、扫描式。入场 `glide`，元素像被系统“加载”出来；持续旋转与扫描线用 `linear`；数字和乱码快速刷新后定格。
- **构图**：中心对称的仪表盘；同心圆轨道；网格背景；四角取景框 ⌜ ⌝ ⌞ ⌟；细线连接标签与目标。
- **招牌技法**：T18 轨道仪表 · T08 乱码解码 · T09 数字滚动 · T10 描线 · T22 粒子场 · T20 视差纵深 · T21 流光氛围
- **推荐转场**：X05 圆形扩张 · X09 故障切（轻，amp 20）· X13 斜切 · X08 匹配剪辑 · X06 放大穿越
- **质感**：`--grain .06` · `--vignette .6` · `--lb 0`；文字可加 `text-shadow: 0 0 24px` 强调色光晕
- **细节层**：坐标、十六进制编号、进度条、百分比、`[ SYS.ONLINE ]`、扫描刻度尺
- **禁忌**：暖色主调；手写或衬线字体；弹性缓动；纸张质感。

## P5 · EDITORIAL LUXE 杂志奢华

- **气质**：优雅、松弛、昂贵。Vogue 封面、奢侈品广告、艺术展预告。
- **色板**：`--bg #F3EEE6`（奶油纸）· `--fg #1A1714`（墨）· `--accent #B08D57`（香槟金）· `--accent-2 #6E1E1E`（酒红）
  - 备选：暗版 `--bg #14110F` `--fg #EFE7DA`
- **字体**：
  - display：`'Cormorant Garamond', 'Noto Serif SC', 'Songti SC', 'SimSun', serif`（大号 italic 300 / 500）
  - text：`'Manrope', 'PingFang SC', 'Microsoft YaHei', sans-serif`（小号全大写，宽字距 0.3em）
  - mono：`'JetBrains Mono', ui-monospace, Consolas, monospace`（几乎不用）
  - 中文：Noto Serif SC 300 / 600
  - 链接：`https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,500;0,700;1,300;1,500&family=Manrope:wght@300;600&family=Noto+Serif+SC:wght@300;600&display=swap`
- **BPM**：60–80。
- **运动性格**：缓慢、流畅、有分寸。`glide` 1.4–2.2s；遮罩揭示比位移多；绝不急促；停顿要长。
- **构图**：大量留白；不对称排版；超大的单个字母或数字作为背景图形；细金线分隔；衬线大字与无衬线小字对比。
- **招牌技法**：T01 遮罩升起 · T05 描边填充 · T15 光扫 · T20 视差纵深 · T21 流光氛围（低饱和）· T17 3D 翻转（慢）· T26 字重呼吸
- **推荐转场**：X02 色块擦除（柔和，用 accent）· X05 圆形扩张 · X14 卡片收缩 · X12 黑场过渡 · X15 墨迹晕染
- **质感**：`--grain .06` · `--vignette .25` · `--lb 0`
- **细节层**：期号 "N°07"、季节 "AUTUMN / WINTER 2026"、页码、细线框；每场 1–2 个即可
- **禁忌**：故障效果；抖动；荧光色；粗黑体；快于 0.5s 的入场。

## P6 · POP KINETIC 波普活力

- **气质**：明亮、跳跃、好玩。快消品广告、App 宣传、社交媒体短片。
- **色板**：`--bg #FFF6E5`（奶油）· `--fg #161616` · `--accent #FF5A36`（番茄红）· `--accent-2 #2D5BFF`（宝蓝）· 额外可用 `#FFD23F`（明黄）、`#00C48C`（薄荷）
  - 本预设允许 4 种强调色，但每场最多出现 2 种
- **字体**：
  - display：`'Bricolage Grotesque', 'ZCOOL KuaiLe', 'Noto Sans SC', 'PingFang SC', sans-serif`（800）
  - text：`'Bricolage Grotesque', 'PingFang SC', 'Microsoft YaHei', sans-serif`（400）
  - mono：`'DM Mono', ui-monospace, Consolas, monospace`
  - 中文：ZCOOL KuaiLe（站酷快乐体）或 Noto Sans SC 900
  - 链接：`https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@200..800&family=DM+Mono:wght@400;500&family=ZCOOL+KuaiLe&family=Noto+Sans+SC:wght@500;900&display=swap`
- **BPM**：110–130。
- **运动性格**：弹性、有重量。入场 `back.out` / `punch`（过冲 10–20%）；形状像橡皮一样挤压拉伸（scaleX/scaleY 交替）；`elastic.out` 每支片子最多用 2 次。
- **构图**：大色块拼贴；圆形、胶囊、星形、波浪线；文字放在色块上；元素从画面四周弹入。
- **招牌技法**：T11 形状爆发 · T02 逐字瀑布 · T14 分屏 · T07 一拍一词 · T17 3D 翻转 · T13 律动条 · T24 残影回声
- **推荐转场**：X03 多层色块 · X05 圆形扩张 · X11 推挤 · X14 卡片收缩 · X16 巨字擦除
- **质感**：`--grain .05` · `--vignette 0` · `--lb 0`
- **细节层**：贴纸式标签、星星 ★、对话气泡、"NEW!"、手绘感箭头（SVG 描线）
- **禁忌**：黑底；胶片颗粒过重；悬疑式慢节奏；细线 HUD。

## P7 · INK & SEAL 新中式墨韵

- **气质**：留白、气韵、当代东方。国潮品牌、茶饮、传统节日、文化纪录片。
- **色板**：`--bg #F1ECE2`（宣纸）· `--fg #161412`（墨）· `--accent #B7352A`（朱砂红，用于印章）· `--accent-2 #8A8172`（淡墨灰）
  - 备选：夜版 `--bg #12100E` `--fg #EDE6D8`，朱砂不变；青绿版 `--accent #2F6F62`
- **字体**：
  - display：`'Ma Shan Zheng', 'ZCOOL XiaoWei', 'Noto Serif SC', 'KaiTi', 'STKaiti', serif`（马善政毛笔楷书）
  - text：`'Noto Serif SC', 'Songti SC', 'SimSun', serif`（200 / 400）
  - 英文点缀：`'Cormorant Garamond'` italic
  - 链接：`https://fonts.googleapis.com/css2?family=Ma+Shan+Zheng&family=ZCOOL+XiaoWei&family=Noto+Serif+SC:wght@200;400;900&family=Cormorant+Garamond:ital,wght@1,400&display=swap`
- **BPM**：60–76。
- **运动性格**：如笔走墨。揭示用柔边遮罩（mask-image 渐变，像墨迹洇开），1.2–2s `glide` / `sine.inOut`；印章用一次 `expo.out` 重拍（scale 1.6 → 1）配轻微 shake；其余运动极慢。
- **构图**：竖排文字（`writing-mode: vertical-rl`）；大片留白；远山 / 圆月 / 一笔横线等极简图形；朱红印章是唯一的强调色块。
- **招牌技法**：T25 竖排书法 · T01 遮罩升起 · T20 视差纵深（远山层叠）· T21 流光氛围（墨晕，低饱和）· T10 描线（一笔线条）· T23 打字机（逐字浮现）· T03 重拍砸字（仅用于印章）
- **推荐转场**：X15 墨迹晕染 · X12 黑场过渡 · X05 圆形扩张（圆月）· X08 匹配剪辑 · X02 色块擦除（淡墨）
- **质感**：`--grain .1`（纸纹）· `--vignette .3` · `--lb 0`
- **细节层**：小号竖排落款、篆刻印章、节气名、干支纪年、细竖线；每场 1–2 个
- **禁忌**：霓虹色；故障与频闪；科技 HUD；超过两种红色；拼音式的英文硬译。
