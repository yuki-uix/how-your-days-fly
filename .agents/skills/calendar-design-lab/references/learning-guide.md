# 日历设计语言：公开学习资料

核对日期：2026-10-29。这里整理一手公开资料与针对本项目的练习，只保留链接和原创笔记，不镜像原书、论文或作品图。

当前 A–H 样本和八种结构家族是本项目的工作分类。下面的研究可以帮助我们完善它，而不应被倒写成这些分类已经获得学界或用户验证。

## 先分清要学习什么

| 学习问题 | 资料方向 | 希望沉淀的能力 |
| --- | --- | --- |
| 时间可以怎样被组织？ | 时间可视化与时间模型 | 明确单位、连续性、周期、顺序及映射 |
| 排版怎样服务阅读与表达？ | 网格、字体、数字、层次与留白 | 按用途选择视觉关系，解释取舍 |
| 一份日历怎样形成独特体验？ | 设计师说明、实物与出版物档案 | 分析阅读距离、翻页、书写及更新行为 |
| 怎样将设计做成可组合的工具？ | 日历坐标与图形语法研究 | 将已验证的规则落实为数据和渲染能力 |

```mermaid
flowchart LR
    A[时间研究与排版资料] --> C[提炼变量、依据和适用条件]
    B[日历实物与设计师说明] --> C
    C --> D[制作只改变一个因素的样本]
    D --> E[技术检查与用户评价]
    E --> F[完善设计语言与 Skill]
```

这是建议的学习与验证路径；本轮完成资料整理，尚未执行下面的受控实验。

## 优先阅读

### 1. Visualization of Time-Oriented Data，第二版，2023

Wolfgang Aigner、Silvia Miksch、Heidrun Schumann、Christian Tominski。

- [作者官网与章节入口](https://timeviz.net/)；[出版社全书](https://link.springer.com/book/10.1007/978-1-4471-7527-8)。第二版为开放获取全书。
- 先选读第 3、4 章，理解时间模型与视觉映射；第 5、7 章分别用于交互与方法选择问题。附录可按需查阅，不必先读完整本书。
- 访问与许可：作者明确采用 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)，部分第三方插图例外以图注为准。书的许可不自动覆盖所有外链资产。
- 本项目练习：给 A/B/D 各写一张时间模型卡，说明保留什么关系、强调什么任务、查找什么信息较困难。

### 2. TimeViz Browser 2.0，2023

Christian Tominski、Wolfgang Aigner；University of Rostock 团队维护。

- [公开案例浏览器](https://browser.timeviz.net/)。与上书配套，作者说明收录超过 150 种方法。
- 可按时点／区间、线性／周期、静态／动态等维度筛选，适合先直观浏览，再回书中找解释。
- 访问与许可：公开浏览；每个案例图像及外链材料的复用范围应分别核对。
- 本项目练习：先限定“静态、二维、周期时间”，比较不同结果，而非仅搜索“好看的日历”。

### 3. Timelines Revisited，2017

Matthew Brehmer、Bongshin Lee、Benjamin Bach、Nathalie Henry Riche、Tamara Munzner。发表于 IEEE TVCG 23(9)。

- [作者项目站与预印本](https://timelinesrevisited.github.io/)、[带讲解的幻灯片](https://timelinesrevisited.github.io/slides/)、[案例画廊](https://timelinesrevisited.github.io/supplemental/gallery/)。
- 先看设计空间图和讲座中的比较：representation、scale、layout 是不同选择。同样的事件可以讲出不同时间关系。
- 访问与许可：作者提供公开预印本、讲座和例子；公开访问不等于取得再出版所有图像的许可。
- 本项目练习：固定一组纪念日，对照按实际时间间距和只按事件顺序排列的结果，再比较直线与环形。

### 4. The Vignelli Canon

Massimo Vignelli。

- [RIT Vignelli Center 的出版物入口](https://www.rit.edu/vignellicenter/vignelli-legacy-0)；[机构公开 PDF](https://www.rit.edu/vignellicenter/sites/rit.edu.vignellicenter/files/documents/The%20Vignelli%20Canon.pdf)。
- 重点关注网格、字号关系、留白与设计的一致性。它呈现一位设计师的方法和立场，适合与其他表达方式对照。
- 访问与许可：机构提供完整 PDF 阅读，本轮未核实到可自由再分发全文或图像的开放许可。
- 本项目练习：固定 A 的日期结构，分别只改变字号比例、月间距和对齐关系，观察阅读与表达怎样改变。

### 5. Which fonts to use for your charts and tables，2022

Lisa Charlotte Muth，Datawrapper。

- [作者在 Datawrapper 的完整公开文章](https://www.datawrapper.de/blog/fonts-for-data-visualization)。
- 重点学习数字等高／旧式、等宽／比例宽，以及字重、大小和对比度。它针对图表和表格，不能把所有建议直接当成艺术日历的统一要求。
- 访问与许可：完整网页可读；正文和示例图片未在本轮核实开放再分发许可。字体本身另有许可。
- 本项目练习：固定日期位置，比较不同数字形式在远距离查阅和单日主视觉中的效果。

### 6. Choosing Web Fonts: A Beginner’s Guide

Google Design。

- [官方公开指南](https://design.google/library/choosing-web-fonts-beginners-guide)。
- 关注字体选择怎样与项目用途、文本量、字符覆盖及字体家族范围相关，补足未来网页多语言显示的问题。
- 访问与许可：完整网页可读；阅读指南不授予其推荐的所有字体统一许可。
- 本项目练习：为同一份中英双语日历检查实际需要的字形、数字和符号，并记录字体角色与回退策略。

## 按问题选读的实现研究

### 7. Calendar-based graphics for visualizing people’s daily schedules，2020

Earo Wang、Dianne Cook、Rob J Hyndman。发表于 Journal of Computational and Graphical Statistics 29(3), 490–502。

- [作者介绍与公开 PDF 入口](https://robjhyndman.com/publications/calendar-vis/)。
- 研究怎样把日期重组为日历坐标，以及怎样在日期单元中放其他图形。适合开始实现“个人内容进入日历”时阅读；不要求项目改用 R。
- 访问与许可：作者全文可读；论文图像的共享范围与相关软件许可分别核对。
- 本项目练习：在 F 的同一日期结构中放入原创图形或有权限的个人内容，保持日期坐标不变。

### 8. ggtime: A Grammar of Temporal Graphics，2025 提交的 arXiv 预印本

Cynthia A. Huang、Mitchell O’Hara-Wild、Rob J. Hyndman、Matthew Kay。

- [arXiv 记录](https://arxiv.org/abs/2510.25656)、[全文 HTML](https://arxiv.org/html/2510.25656v1)。本指南引用预印本，不将其标为已核实的同行评审论文。
- 关注可组合的时间语义，尤其是不等长月份、粒度对齐和坐标转换。
- 访问与许可：所查 HTML 标明论文为 CC BY 4.0；软件代码的许可需要另查。
- 本项目练习：将 D 分别做成“每天等角度”和“每月等角度”，明确各自的编码含义与取舍。

## 日历作品怎样读

这些是案例研究入口，不是已经授权的素材库。

| 案例与一手入口 | 分析的问题 |
| --- | --- |
| [Vignelli Center 的 Stendig 档案](https://artsandculture.google.com/asset/stendig-calendar-vignelli-massimo/aQHwHqYgKY7K0w?hl=en) | 阅读距离怎样影响数字比例与信息层次？ |
| [Anaptár 设计师说明](https://anaptar.com/about/) | 个人的周期时间观怎样与径向结构和数据联系起来？ |
| [Danese 的 Timor 产品资料](https://www.danesemilano.com/contents/files/products/timor_files_mari_timor_481.pdf) | 永久历怎样通过部件呈现日期，更新动作怎样参与体验？ |

先写自己观察到的关系，再对照设计师的原文。将观察、作者说明和我们的设计假设分开记录。不要从一个案例推出人人适用的风格规则。

## 给项目补上的术语

| 术语 | 示例 | 要避免的混淆 |
| --- | --- | --- |
| 展示范围／视图 | 一年、一月、一周、一天 | 年历仍可能以一天为最小单元 |
| 时间粒度 | 小时、日、周、月 | 粒度不是纸张或屏幕尺寸 |
| 时间映射 | 按实际时长、按顺序、相对一个起点 | Timelines Revisited 的 scale 主要涉及这一层，不只是年／月／周／日 |
| 空间结构／布局 | 直线、环形、网格、分面、分段 | 同一时间映射可以有不同形状；形状也不会自动保证原有关系保持 |

这是本项目对术语的工作约定；不同文献的定义应保留原语境。当前样本 manifest 中的 `design_axes.scale` 指展示范围，不应与论文中的 scale 直接对应；通用配方形成前需明确映射。

## 学完之后留下什么

每份资料只提炼少量可验证的知识卡：

1. 来源与证据：作者明确说了什么？我们的观察是什么？
2. 设计变量：具体可以改变哪一项？
3. 适用条件与代价：它支持什么阅读任务，会弱化什么？
4. 原创实验：固定哪些条件，只改变哪一个因素？
5. 结果：技术检查与用户评价分别怎样？

经过实验和反馈后，再将有效方法写进 skill 或代码。资料链接与概念整理本身不构成已验证的设计能力。

建议的首轮顺序：先浏览 TimeViz 案例与 Timelines 讲座，再选读主教材第 3、4 章；并行读 Vignelli 与数字排版文章。每读一段就回到 A–H 做一个小对照。两篇实现研究放到需要相应能力时深入。
