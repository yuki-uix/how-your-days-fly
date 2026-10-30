# 英文日历的数字、字距与观看尺度

核对日期：2026-10-30。这里新增 6 个一手页面的定向阅读，范围与局限见 [latin-calendar-reading.json](latin-calendar-reading.json)。已有 `font-numerals`、`font-optical-size`、`font-pairing`、`font-jaf-optical` 延续使用，不再算新来源。以下迁移是本项目的待验证设计假设；来源页面及其图像保持 `research-only`，未下载第三方字样或 SF 字体。

## 数字宽度和字形高度分别选择

[OpenType p–t](https://learn.microsoft.com/en-us/typography/opentype/spec/features_pt) 的 `pnum`／`tnum` 分别处理比例宽／等宽；[k–o](https://learn.microsoft.com/en-us/typography/opentype/spec/features_ko) 的 `lnum`／`onum` 处理等高／旧式。二者是独立选择，因此旧式数字也可能等宽。默认字形也不必与特性名称相同。

**日历迁移**：全年列式数字、七天边注、单日大数字分别比较。前者可重视对齐，后者可重视字形节奏；不能只因“日历有数字”就统一选等宽字体。用 `01 08 11 28 31` 及 `111111`／`888888` 测试实际 advance，并看默认墨迹和基线。

**边界**：`hmtx` 的等宽实测只能说明指定实例的默认宽度；它不证明启用了 `tnum`，也不能判断数字是否等高。规范还列出 `kern` 与固定宽度功能的交互，需要在真实塑形环境检查。

## Kerning、tracking、opsz 是三件事

[Adobe InDesign 的官方正文](https://helpx.adobe.com/indesign/desktop/format-and-style-text/tabs-indents-and-spacing/about-kerning-and-tracking.html)区分特定字对、整段字符间距，以及 Metrics／Optical 两种 kerning。InDesign 的 Optical 根据相邻形状调整间距，不能与字体 `opsz` 轴混为一谈。其间距单位为 1/1000 em，随字号改变实际距离。

**日历迁移**：`JANUARY` 等大写标签可以试 tracking 的变化，再检查 `To`、`Wa`、`AV` 等字对；不能把整体加宽视为每个间隙都已恰当。保留原始间距、调整量和单位，便于在 CSS、SVG 或排版应用中重建。

**边界**：官方帮助说明的是 InDesign 的行为，不代表本项目当前逐码点轮廓输出已经自动 kerning。也没有“一切全大写都必须加某个固定字距”的结论。

## Italic 需要对应设计

[OpenType `ital` 轴定义](https://learn.microsoft.com/en-us/typography/opentype/spec/dvaraxistag_ital)把正体／意大利体与 `slnt` 斜度区分；字体也可能用两个独立文件提供 Roman 和 Italic。

**日历迁移**：书名、作者和注释采用斜体时，比较所选字体真正提供的 `a g f` 与整句形态，并说明该角色需要的语气；同族 Roman／Italic 可以形成分工，不预设额外配一个家族才精致。

**边界**：没有 Italic 文件或 `ital` 轴，不以简单倾斜代称原设计。技术轴定义也不独自证明某套字体的历史分类或“书籍感”。

## 光学尺寸需要读者的位置

[OpenType `opsz` 定义](https://learn.microsoft.com/en-us/typography/opentype/spec/dvaraxistag_opsz)指出，轴值选择应尽量考虑读者感知到的大小，包含设备、单位和观看距离。原文的 point 定义与默认建议有具体技术语境，不能变成全部日历的字号配方。

**日历迁移**：桌面近看与挂墙远看分别记录物理尺寸和距离。对有 `opsz` 的候选，固定字重、文本及最终字号，只改变实际光学实例；将实际大小字样和放大局部并排。

**边界**：没有光学轴的字体可以做视觉尺度校正，但不叫启用了光学尺寸。缩略图也不能替代实体观看距离验证。

## 小尺寸研究要看输出和间距

[Apple WWDC20 官方文字稿](https://developer.apple.com/videos/play/wwdc2020/10175/)中，设计者把 SF 的小尺寸细节、side bearings、tracking 与输出分辨率联系起来，并讨论 tracking 和连字的相互作用。本轮只读指定文字稿，没有声称观看视频或研究了画面中的字样。

**日历迁移**：以月份、星期、`Il1 O0` 等真实串观察小尺寸，逐项控制字重、opsz 与 tracking，再回整页。字体内置间隔、整体字距和逐对调整分别记录。

**边界**：这是 2020 年 Apple 系统设计的说明，不把 SF 的切换阈值、tracking 表或平台 API 承诺推广到其他字体与当前网页。

## 可由代码生成的研究板

这是一份尚未渲染的研究建议，实际脚本应记录采用的项：

| 研究区 | 真实字样 | 控制与观察 |
| --- | --- | --- |
| 同字号／同墨迹高度 | `Days in view`、`January · Wednesday` | 明确字重、opsz，记录 em、墨迹框及实际字号；墨迹框相同不保证视觉大小相同 |
| 角色关系 | `A week of reading`、`MON TUE WED THU FRI SAT SUN` | 保留内容、网格与颜色，对比同族 Roman／Italic、衬线／无衬线、展示／查读分工 |
| 数字和间距 | `01 08 11 28 31`、`111111`、`888888`、`JANUARY`、`To Wa AV` | 默认字形测量与显式 tracking 可以由现有轮廓路径完成；没有塑形时不伪造功能开启效果 |
| 光学与 Italic | `January`、`Reading the days`、`agf` | 使用实际可用的轴／文件；固定其他变量；标出当前导出路径的 GSUB/GPOS 局限 |

保留实际文件哈希、许可、轴值、缺字、渲染器、真实启用特性、字号与字距单位。原字体、静态实例、转曲图和用户选择分别记录，避免从“有此特性”跳到“此输出已正确使用”。
