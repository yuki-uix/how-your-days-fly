# 英文字体与拉丁字形：候选家族精读

核对日期：2026-10-30。八条来源记录见 [latin-type-research.json](latin-type-research.json)。这里记录原设计者和官方分发平台实际公开的设计说明，面向日历的用法是本项目假设。厂商陈述、字形文件实测、研究图观察及用户评价分别保留。

## 先扩展问题的维度

“英文”是内容语言；候选通常使用拉丁字形，但不会因此覆盖所有拉丁文字语言的字符、重音与排版约定。字体也不能只按 serif／sans 二分：骨架、衬线、粗细对比、宽度、x-height、开口、数字、原生意大利体、光学尺寸和目标任务可同时成为选择依据。

`display` 主要描述用途，`condensed` 描述宽度，`mono` 描述字宽组织；不宜把这些与所有历史风格排成一个互斥菜单。具体历史分类词汇应保留来源和边界。分类帮助找到可比较差异，不对审美高低计分。

## 家族阅读与分类补充

| 来源／候选 | 实际读到的设计信息 | 面向日历的待验证用途与取舍 |
| --- | --- | --- |
| [Source Serif Readme](https://github.com/adobe-fonts/source-serif/wiki/Source-Serif-Readme) | 与 Source Sans 通过字母比例、文字色调协调，同时保留不同作者与历史参考；说明原生样式和软件合成的区别 | 把 Source Serif 4 + Source Sans 3 作为有设计依据的候选，再比较单一家族或其他配对；原生意大利体与简单倾斜分别记录 |
| [Newsreader / Production Type](https://productiontype.com/font/newsreader/newsreader-text) | 为屏幕长文设计，提供 Caption／Text／Display 及意大利体层级；页面分别列数字特性 | 尝试书名、说明、附注的同族组织；不能从厂商的“bookish”定位推断用户必然喜欢 |
| [Bodoni Moda / 官方家族说明](https://raw.githubusercontent.com/google/fonts/main/ofl/bodonimoda/DESCRIPTION.en_us.html)及[元数据](https://raw.githubusercontent.com/google/fonts/main/ofl/bodonimoda/METADATA.pb) | 明确对应家族名、Roman／Italic 文件、光学与字重轴；与同一上游的 Bodoni* 产品叙述分开 | 作为高对比方向的候选，检查细笔画在尺寸、距离和输出中的效果；不用 Bodoni* 的定价或尺寸承诺解释 Moda |
| [Source Sans 3 / Paul D. Hunt](https://blog.adobe.com/en/publish/2020/11/30/whats-new-in-source-sans-3) | 更新时修订末端、加入中间主字型以控制中间字重过细的横画／斜画；语言替换单独处理 | 日期和较小文字要看具体笔画分布，不用 400／500 数字替代比较；UI 来源不限制其进入印刷品 |
| [Inter / Rasmus Andersson](https://rsms.me/inter/) | Text／Display 有不同设计目标；等宽数字、斜线零、近似字形区分分别提供 | 无衬线字体也有光学尺寸问题。数字对齐和辨识是不同任务，不必启用全部功能；网站已有开关不证明本项目导出执行了它 |
| [Space Grotesk / Florian Karsten](https://github.com/floriankarsten/space-grotesk) | 从 Space Mono 演变，但本身是比例宽；保留部分独特细节；README 列旧式／等宽数字 | 用于有辨识度的标签或标题，也可与正文候选比较；不因来源于 Mono 而当作等宽字体，不补写未承诺的 italic |
| [Instrument Serif / Instrument](https://github.com/Instrument/instrument-serif) | 品牌用的窄体展示衬线，主要面向大尺寸，参考 old style 衬线 | 已有资产可继续比较长月名、短书名和展示数字；小字效果另外验证，不能因“serif”就默认承担全文 |

本次没有打开厂商 PDF 样本册、下载第三方使用案例或操作网页字样开关；上述网站文字和图注不冒充视觉验证。Newsreader 厂商静态套装的样式数量也没有记成已留存的可变字体文件数。

## 日历字样要问什么

后续原创建议字样：

- 月份与星期：`January / September / Wednesday / Sunday`。观察不同词长、大小写与空间需求。
- 标题与书名：`A Week of Reading`、`The Shape of Days`。先用原创中性文字，不借用厂商宣传字样。
- 数字：`01 08 11 28 31 / 2027`。默认比例宽、等宽功能、行列对齐分别比较。
- 近似形与附标：`Il1 / 0O / Émile / naïve / Å`。这些只验证选定样本，不表示完整语言覆盖。
- 风格：对保留的原生 Roman／Italic 文件作同词比较；不要把合成倾斜叫作原生意大利体。

先比较同一名义字号，再比较明确计算的 cap／x-height 或墨迹尺度，记录数值；任何一种匹配都不等于所有字体已达相同视觉大小。若改变光学轴，固定字重、内容与画布以查看其差异，再回到实际标题和全页关系。

## 对素材库与 skill 的建议

1. 候选卡保存描述维度与阅读任务，不预置“经典／高级／年轻”等用户感受。来源中的营销词保留为作者设计意图。
2. 每个候选分别记录可变轴、原生样式、默认数字、可选数字功能、字符样本和渲染支持。文件有某个标签不等于导出应用了它。
3. 年历的小数字、月历的月份标题、周历的图文叙事、单日历的大日号允许分别选择；同一家族也可承担多个角色。
4. 挂墙／桌面以目标距离验证，对印刷和屏幕分别查看。没有一个类别或字重数值天然保证可读或美观。
5. 区分目录里的候选、已保留文件、研究字样采用字体和用户最后选中字体，避免把研究新增字体追写成旧样张的实际材料。

资料阅读可支撑选择理由；本轮不宣称这些理由已得到用户偏好、阅读实验或最终视觉质量的验证。

## 分类词汇的独立依据

补读 [Monotype 的分类指南](https://www.monotype.com/resources/guide-type-styles)导论及指定 serif／sans 正文：历史、形态分类并存，当代设计常跨越类别。取其骨架、对比、衬线等描述词汇；display 是用途、condensed 是宽度、mono 是字宽组织，分别检索。本文没有据分类推断阅读性能或用户喜好，也不采用原文对某一类别“更适合阅读”的概括为通用规则。来源图样未复制或用于视觉验证。
