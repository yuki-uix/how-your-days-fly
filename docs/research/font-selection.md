# 字体选择、搭配、数字与光学尺寸：精读记录

核对日期：2026-10-30。本页保存一手原文的阅读范围与原创分析；对应结构化记录见 [font-selection.json](font-selection.json)。公开文章、图示和品牌版式保持 `research-only`，没有把它们的图片或长文复制进素材库。字体文件的 OFL 范围另见[原始字体清单](../../assets/fonts/type-study/manifest.json)。

## 先区分三种判断

- **设计判断**：某个字形、对比和配对是否表达本案想要的关系，要在真实内容中比较。
- **使用条件**：字符、字重、数字形式、尺寸和阅读距离是否合适，需要具体文件与实际输出支持。
- **品牌规定**：IBM 等体系中的尺寸、行高和用途要求有自己的上下文；可研究其组织方法，不能当成所有日历的统一比例。

下面的迁移方法是本项目提案，不是来源作者为日历设定的规则，也不表示任何用户已认可某种审美。

## 逐项精读

### font-checklist · 用途、表现力与可靠性要一起检查

来源：[Google Fonts Knowledge · A checklist for choosing type](https://fonts.google.com/knowledge/choosing_type/a_checklist_for_choosing_type)，[官方源正文](https://github.com/google/fonts/blob/main/cc-by-sa/knowledge/modules/choosing_type/lessons/a_checklist_for_choosing_type/content.md)。已读完整正文，包括用途、语言、近似字符、字重／宽度／光学尺寸、真实文件、间距和许可各节。

作者把情感反应与实际使用条件并列；个人与文化经验会影响感受。文件版本或子集还可能缺少我们以为存在的字符、样式和功能。

**迁移**：先用真实书名、作者、星期和日期分别试标题／查读／附注角色，再检查实际文件；“有宋体”“已装字体”不构成完整选择理由。

**代价与反例**：一个适合短标题的单字重字体可能足够；长期可编辑系列需要更多内容与角色覆盖。不要把“选项越多”作为选得更好的依据。

### font-pairing · 先说明第二字体增加什么

来源：[Google Fonts Knowledge · Pairing typefaces](https://fonts.google.com/knowledge/choosing_type/pairing_typefaces)，[官方源正文](https://github.com/google/fonts/blob/main/cc-by-sa/knowledge/modules/choosing_type/lessons/pairing_typefaces/content.md)。已读完整正文与图注，包括单字体内部变化、上下文／语气变化和缺失功能。

文章先问主字体的字重、样式、宽度和尺寸是否已经足够，再讨论第二字体。相近 x-height、笔画对比、宽度或气质可以成为连接点，角色差异也可以支持明显对比。

**迁移**：比较“同一家族完成全部角色”与“另加一个有明确任务的字体”。标出它补充的是语言覆盖、数据查读、语气还是样式。

**代价与反例**：衬线＋无衬线是可试路径，不能保证美感；x-height 也不是所有配对都必须相等的硬条件。日号字体若只因习惯而另加，可能制造新的视觉入口。

### font-matrix · 分类标签之后，还要看骨架

来源：[Google Fonts Knowledge · Pairing typefaces based on their construction using the font matrix](https://fonts.google.com/knowledge/choosing_type/pairing_typefaces_based_on_their_construction_using_the_font_matrix)，[官方源正文](https://github.com/google/fonts/blob/main/cc-by-sa/knowledge/modules/choosing_type/lessons/pairing_typefaces_based_on_their_construction_using_the_font_matrix/content.md)。已读三层描述、三条配对路径、完整实例和限制段。

这套方法区分骨架、对比／衬线、表层细节；同为 sans 或 serif 的字形仍可能有明显不同的构造。文章同时把矩阵明确作为辅助判断的方法，保留中间类型和例外。

**迁移**：在候选字样上指出真正共享或相反的形态，再说明它怎样服务标题与日期关系。用一条真实混排语句验证，不能只摆两个字体名称。

**代价与反例**：矩阵以文中西文字形为分析对象，不强行用它分类汉字、楷体或全部展示字。表面相似而底层不同可能产生摩擦，也可能成为刻意表达；结果仍需看整体。

### font-optical-size · 尺寸适配是字形变化

来源：[Google Fonts Knowledge · Choosing typefaces that have optical sizes](https://fonts.google.com/knowledge/choosing_type/choosing_typefaces_that_have_optical_sizes)，[官方源正文](https://github.com/google/fonts/blob/main/cc-by-sa/knowledge/modules/choosing_type/lessons/choosing_typefaces_that_have_optical_sizes/content.md)。已读完整正文及观看距离讨论。

小尺寸设计可能调整字宽、x-height、对比和间距；大尺寸设计可采用不同细节。观看距离会改变实际感知，画布物理尺寸不能直接决定应使用 display 版本。

**迁移**：字体真有 `opsz` 或尺寸专用样式时，在目标尺寸与距离下做对照；再以同尺寸放大看差别。没有该轴时，把墨迹高度匹配称为手动视觉尺度校正。

**代价与反例**：A3 页面上的远看小字不自动适合纤细展示样式。新增 Noto 两份文件只有 `wght`，不能把它们的字重变化叫作光学尺寸功能。

### font-numerals · 数字的高度与宽度是两条轴

来源：[Google Fonts Knowledge · Understanding numerals](https://fonts.google.com/knowledge/introducing_type/understanding_numerals)，[官方源正文](https://github.com/google/fonts/blob/main/cc-by-sa/knowledge/modules/introducing_type/lessons/understanding_numerals/content.md)。已读全文四类数字及适用情境。

等高／旧式与等宽／比例宽可以组合。表格和持续变化的数字常需要对齐；正文与较松散的短数字还可保留不同节奏。每个字体不一定包含全部变体。

**迁移**：分别研究密集全年网格、七日边注和单日大数字，比较默认数字，并检查文件和渲染器是否真正支持所选 OpenType 功能。

**代价与反例**：整套等宽字体不是获得等宽数字的唯一方式；在字体中发现 `tnum` 不表示导出的日历已经使用它。当前实测 Noto Serif SC 400 的默认数字宽度不同，Noto Sans SC 400 相同。

### font-ibm-scale · 一套品牌怎样组织字号与语言

来源：[IBM Design Language · Type scale](https://www.ibm.com/design/language/typography/type-scale/)。选读 `Type scale equation`、`Adjusted scale` 与 `Large formats` 的导论；没有把全部模板或示例下载为素材。

IBM 将字号、行高、不同文字体系和大幅观看距离纳入一套关系；其 CJK 等文字的 95% 调整是针对自己的体系提出。

**迁移**：记录标题、日期与附注之间的关系及不同载体的调整方法；做中西文的实际字面比较后再校正。

**代价与反例**：不能把 95% 或 IBM 的字号序列写成日历通用数值。换字体、语言、观看距离后，需要重新验证行高、可读性与构图。

### font-ibm-family · 家族范围不等于某个文件的范围

来源：[IBM Design Language · Typeface](https://www.ibm.com/design/language/typography/typeface/)。选读 subfamilies、type tester、features、mono versus sans、language support 与 license 各节。

设计者把不同子家族放在品牌任务中使用，也鼓励用实际词句测试。Plex Mono 的 600 单位宽度有具体设计来源与品牌用途。

**迁移**：跨角色可先比较同一家族的不同分支，但逐文件核验字符和功能。本库已有 Plex Mono / Sans Condensed 的 Regular 文件未覆盖本次通用中文字样。

**代价与反例**：官网说整个 Plex 覆盖多种文字，不能据此让本地英文字体承担中文；代码场景的 mono 用法也不是所有日期的默认审美。

### font-jaf-optical · 光学尺寸研究的原设计者语境

来源：[Tim Ahrens、Shoko Mugikura / Just Another Foundry · Size-specific adjustments to type designs](https://justanotherfoundry.com/size-specific-adjustments-to-type-designs)。读作者公开介绍、尺寸设计定义、研究方法与目录；**没有声称读完收费书籍**。

作者以历史字样、设计师访谈与形态比较研究不同尺寸的设计调整，目录把字形、对比、宽度、间距和替代方案分别讨论。

**迁移**：在短字样中分别控制字重、间距和尺寸样式，记录哪种调整回应了哪个观看问题，再回到整页。

**代价与反例**：公开介绍支持研究路径，不能替代书内完整论证，也不授权其书页、字样图片或商业字体进入模板。不要从“存在 optical sizes”推出所有字号都有唯一正确版本。

## 已保存的字体与实测

[字体来源与使用说明](../../assets/fonts/type-study/README.md)列出两份原始 Noto 可变 TTF；没有公开真实案例的图像、请求、反馈或改名工作副本。清单还审核已有三个家族的指定 Regular 文件。

- 指定字重后，先核验通用日历字样；缺字列表只说明这个样本，不代表覆盖所有中文。
- `wght=400` 的内存实例测量默认 cmap 数字的 advance 与墨迹框；这不等于启用了 `tnum`、`pnum`、`lnum` 或 `onum`。
- 当前 `design_scene.py` 的逐码点 cmap／advance 路径没有完整 GSUB/GPOS 处理。资产提供了字体，不等于项目已经具备全部字距调整、中西文塑形或字体功能选择。
- 原始 CJK 字体约 43 MB，作为可复用源资产保存。网页加载、字形子集及导出实例应另行设计并保留相应许可与来源。
