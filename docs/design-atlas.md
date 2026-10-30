# 日历设计总览

从这里一起调用项目已有的结构、设计语言、样本和素材。它们回答不同问题：**怎样组织时间、怎样建立阅读关系、用什么内容实现、已有作品证明了什么**。详细规则和资产记录仍保存在各自原文件，本页与[统一索引](../design/catalog.json)负责连接它们。

实际开始一轮设计时，使用[基础 skill](../.agents/skills/calendar-design-lab/SKILL.md)：[渐进澄清](../.agents/skills/calendar-design-lab/references/discovery.md) → [方向探索与定向修改](../.agents/skills/calendar-design-lab/references/design-exploration.md) → [案例与证据留档](../.agents/skills/calendar-design-lab/references/case-record.md)。这些流程引用本总览；统一查询也返回对应 workflow 路径。

[字体与排版专题](type-layout-library.md)已接入同一索引，区分规范、设计立场与实现边界。查某尺度时可加 `--domain typography` 或 `--domain layout`，条件条目会连同字体和来源返回。

```mermaid
flowchart LR
    A[用途与时间尺度] --> B[选择时间结构]
    B --> C[确定阅读与构图规则]
    C --> D[选择字体、图像和部件]
    D --> E[对照已有样本或编排新配方]
    E --> F[日期与输出检查]
    F --> G[用户评价与修改]
    G --> E
```

结构、规则、素材和已有样本已经可查。上图是使用它们的设计流程；新配方和用户评价须逐项执行，不因关联建立就自动完成。

## 按要做的日历一起查

| 时间尺度与任务 | 可选时间结构 | 优先检查的设计关系 | 已有样本 | 可组合素材举例 |
| --- | --- | --- | --- | --- |
| **年历**：看全年、查日期、看跨月跨度或总量 | 月份矩阵、月份长条、连续周流、环形周期、等日单元场 | 连续顺序、月界索引、等日／等月语义；展示年份与查读数字分工 | [A](../studies/pattern-atlas/a-month-blocks.svg)／[B](../studies/pattern-atlas/b-continuous-weeks.svg)／[C](../studies/pattern-atlas/c-month-strips.svg)／[D](../studies/pattern-atlas/d-radial-year.svg)／[E](../studies/pattern-atlas/e-equal-day-field.svg)；[J1](../studies/learned-language/j1.svg)／[J2](../studies/learned-language/j2.svg)／[J3](../studies/learned-language/j3.svg) | `y-ribbon` 月份带、`y-tabs` 侧签、织线与环形边饰；海浪横图、蕾丝片段、Plex Mono。见[年历素材板](../studies/material-library/year.jpg) |
| **月历**：查当月、观看主图、形成翻月系列 | 月份矩阵；多页时用单位序列连接月份 | 主图与日期共用锚点、展示与查询分层；月格容纳四至六行；系列固定什么、变化什么 | [F](../studies/pattern-atlas/f-image-led-month.svg)／[J4](../studies/learned-language/j4.svg) | `m-mat` 图像框、`m-specimen` 标本签、`m-dock` 日期底座；植物图版、原创光影图、开放字体。见[月历素材板](../studies/material-library/month.jpg) |
| **周历**：安排与记录、比较七天、给自由笔记留位置 | 时间／议程矩阵；也可截取连续周流 | 留白对应实际书写；日期与星期完整；七天面积、时间刻度与开放区按用途选择 | [G](../studies/pattern-atlas/g-writing-led-week.svg)／[J5](../studies/learned-language/j5.svg) | `w-hours` 时间梯或 `w-notes` 日记条、`w-habit` 习惯矩阵、`w-margin` 回顾边栏；可配一张观察主图。见[周历素材板](../studies/material-library/week.jpg) |
| **日历**：识别今天、逐日揭示内容、留下短记录 | 单位序列；模块式日期组合可作另一方向 | 展示日号与完整日期分工；相邻／年度定位；内容顺序、裁切和日期映射固定 | [H](../studies/pattern-atlas/h-date-led-daily-page.svg)／[J6](../studies/learned-language/j6.svg)；模块式方向目前只有研究参考 | `d-number` 日号、`d-perforation` 边饰、`d-detail` 连载窗口、`d-observe` 观察笺；雪景、月景或原图细节。见[日历素材板](../studies/material-library/day.jpg) |

这些是组合入口，不是封闭模板或互斥分类。月份矩阵既能用于全年海报，也能用于单月；`y-tabs` 可以进入每日系列，`w-habit` 可以扩展到月度。换尺度时重新检查日期数、信息密度和阅读面积，不能只缩放原版。

## 选择时各层负责什么

| 层 | 已整理的内容 | 详细事实与记录放在哪里 |
| --- | --- | --- |
| 结构词汇 | 时间结构、信息层次、内容角色、载体／行为四个维度；八种结构家族 | [结构模式](../.agents/skills/calendar-design-lab/references/patterns.md) |
| 设计判断 | 设计卡、条件性规则、问题定位；时间语义与排版构图的依据 | [设计语言](../.agents/skills/calendar-design-lab/references/design-language.md)、[时间语义](../.agents/skills/calendar-design-lab/references/temporal-semantics.md)、[排版与构图](../.agents/skills/calendar-design-lab/references/typographic-composition.md) |
| 学习与案例证据 | 开放教材、论文、设计者说明，以及按尺度收集的二十个官方案例 | [学习指南](../.agents/skills/calendar-design-lab/references/learning-guide.md)、[年／月案例](research/annual-monthly-materials.md)、[周／日案例](research/weekly-daily-materials.md) |
| 实际素材 | 八张逐件 CC0 图像、十六个原创向量部件、五个 OFL 字体家族、一张原创生成图像和带取舍的字体／构图条目 | [素材使用指南](material-library.md)、[字体排版专题](type-layout-library.md)、[素材总索引](../assets/library/catalog.json)及各资产 provenance |
| 设计证据 | A–H 八份结构／内容研究，J1–J6 六份应用研究；各自保留日期和实现记录 | [A–H manifest](../studies/pattern-atlas/manifest.json)、[J1–J6 说明](../studies/learned-language/README.md)与 [manifest](../studies/learned-language/manifest.json) |
| 修改与保存 | 技术检查、用户反馈、重放与重新参数化的区别、最终选定资产 | [审查](../.agents/skills/calendar-design-lab/references/review.md)、[配方记录](../.agents/skills/calendar-design-lab/references/recipe.md) |

**八种结构家族与十四份样本不是同一套编号。** F 与 A 都使用月份矩阵，只是尺度和内容角色不同；J4 又用该结构研究图像、字体与锚点。模块式日期组合是已整理的家族，但尚无本地成品样本。索引中的关联是工作映射，不能补写成不存在的实验。

## 两条可以追溯的组合路径

### 家中观看的图像月历

已有证据是 [F](../studies/pattern-atlas/f-image-led-month.svg) 的图像主导月历，以及 [J4](../studies/learned-language/j4.svg) 的共边光影图像月历。J4 的设计卡实际使用 `type:image-date-anchors` 与 `type:display-versus-lookup`：图像、月份展示字、查读数字分别承担角色。

下一份配方可选 `m-mat` + `m-dock`，搭配已经留档的 `paper-light-j4` 或逐件 CC0 图像 `cma-tulip`。这是**用现有部件编排新设计的建议**，不表示原 J4 曾使用后来制作的部件，也不是把图片换入就已完成验证。

需要保存主图与裁切、月份和周起始日、字体角色及共用边缘。`m-dock` 现有 SVG 是五月示例；改作其他月份须重新生成真实日期并调整源码，当前 CLI 没有通用的月历换图接口。十二个月还须补足内容序列并检查四至六行月格。图像大幅打印另取高清版本。

### 看见全年连续流动

已有证据是 [B](../studies/pattern-atlas/b-continuous-weeks.svg) 与横向的 [J1](../studies/learned-language/j1.svg)。共同结构是连续周流，J1 的实际规则包括 `temporal:continuous-order`、`type:display-versus-lookup`、`type:shared-anchors`。

新设计可保留连续日期和月界入口，再试用 `y-ribbon` 或 `y-tabs` 辅助定位。若改为环形，应转而参考 [D](../studies/pattern-atlas/d-radial-year.svg) 与 [J2／J3](../studies/learned-language/README.md)：J2 是等日，J3 是等月，两者的时间映射不同。环形边饰 `y-orbit` 则只是装饰，不承载天文或日期数据。

这个例子将结构变化、规则变化和素材变化分开记录。B 与 J1 的整体外观差异不能归因于某一个变量；J2／J3 才是已经保留共同视觉条件的受控比较。

## 一次检索，保留原始记录

在仓库根目录运行：

```sh
python3 scripts/design_catalog.py --scale month --json
```

[统一索引](../design/catalog.json)把该尺度的结构、规则、样本和 material IDs 关联起来，查询时同时展开素材记录。八组学习来源和早期案例也保留入口；与后续二十案例重复的记录通过 ID 对应，早期 Stendig、MUJI 等入口不会丢失。具体许可、哈希、图像尺寸与字体文件仍以[素材索引](../assets/library/catalog.json)及其来源记录为准，详细文献解释以对应规则原文为准，避免在多个入口分别维护相互冲突的副本。

来源或样本记录变更后，运行 `python3 scripts/design_catalog.py --build`，会同时刷新素材索引和统一关系索引。检索遇到过期来源会提示重建。查开放许可素材时仍用 `python3 scripts/material_catalog.py --scale month --shareable-only --json`；统一检索列出研究材料，不把它们标作可分发文件。

参考作品仍为研究材料，不能因被关联就变成模板资产；CC0、OFL、项目原创部件和未实现提案的范围也各不相同。原有样本的重放条件继续保留：A–H 的 SVG 字形依赖本机字体；J1–J6 固定字体与所选图像。两组都不能仅凭日期正确或截图好看，就宣称用户已认可或通用设计能力已验证。

当前完成的是统一知识入口、关系检索与已有实验的保留。公众网站、通用组合渲染器和跨用户设计效果仍需后续实现与验证。
