# 已保留字体的数字特性：实际塑形审计

测量日期：2026-10-30。覆盖素材库现有 **16个家族、19份Roman／Italic文件**，包含基础11家族与数字专项新增5家族，原字体没有改写。完整逐字数据见 [numeral-feature-audit.json](numeral-feature-audit.json)，可重跑脚本为 [audit_numeral_features.py](../../scripts/audit_numeral_features.py)。

## 测量范围

输入固定为西方数字串`0123456789`；方向`ltr`、脚本`Latn`、语言`en`。所有可变字体固定`wght=400`，其余轴为该原始文件默认值。HarfBuzz实际执行默认塑形与所列功能，不只查看字体标签。另为Noto Serif SC增加`zh-Hans`语言和关闭`locl`的诊断对照。

运行时：FontTools 4.68.0、uharfbuzz 0.57.0；底层HarfBuzz版本保存在JSON中。每份原字体单独保留路径、SHA-256、版本、轴坐标及GSUB／GPOS标签。每个测量设置保留实际请求、glyph ID、advance、偏移、墨迹框，以及相对默认的字形替代、轮廓与占位变化。

**这些数值属于指定文件、坐标、文字脚本和语言。** 不外推整个家族、其他版本、其他轴坐标或全部语言，也不证明日历可读性或用户偏好。

## 直接可用的发现

| 家族／指定样式 | 本次实际结果与使用边界 |
| --- | --- |
| Instrument Serif Roman／Italic | 默认数字比例宽；没有本轮关注的五个数字功能标签。这里未据此断言字体不存在其他替代设计。 |
| IBM Plex Mono／Sans Condensed Regular | 默认数字等宽。`zero`改变0的轮廓、保留本串advance；等宽数字并不要求整套字体都是mono。 |
| Noto Serif SC | **原始cmap／hmtx与真实塑形可能不同**，见下节。en与zh-Hans在同一文件、同一字重下得到不同数字字形和宽度。 |
| Noto Sans SC | 该指定实例在本轮en／Latn默认塑形中数字advance相等；本轮没有五个数字特性标签的显式切换。 |
| Source Serif 4 Roman／Italic | 四组`tnum/pnum × lnum/onum`都实际测量，有不同轮廓或位置；两个等宽设置均严格等宽。默认已等宽等高，因此再开`tnum+lnum`可没有可见变化。 |
| Newsreader Roman | 默认等宽，`pnum`产生比例宽替代；`tnum`可与默认相同。本文件没有本轮的`lnum/onum`标签。 |
| Newsreader Italic | **本次保留文件**在400／默认opsz18下，默认及显式`tnum`都是7的advance1300、其他数字1100（UPM2000）；`pnum`切换有效。不能把Roman指标转给Italic，也不据此裁决全家族。 |
| Bodoni Moda Roman | 默认比例宽；四组数字功能的实际结果不同，两个等宽设置均严格等宽。这里固定400／原文件默认opsz11，不能把这些指标移用到500／opsz48的展示实例。 |
| Source Sans 3 Roman | 默认等宽；开启`pnum`、`onum`或二者同时，得到比例等高、等宽旧式、比例旧式的不同轮廓／宽度。虽无显式`tnum/lnum`标签，默认仍有相应数字形式。`zero`让0比其他数字宽1字体单位，见精度边界。 |
| Inter Roman | 默认比例宽；`tnum`真实替代并变成等宽，`pnum`可与默认相同。当前文件没有`lnum/onum`标签；不能凭`tnum`推断已选旧式或等高形式。 |
| Space Grotesk Roman | 四组显式设置产生不同结果。`tnum+lnum`严格等宽；`tnum+onum`中1宽621，其余620（UPM1000），保存这一微差，不将其简化成“功能失败”。 |
| Fraunces Roman | 固定400／opsz9／SOFT0／WONK1时默认比例宽，没有本轮关注的五个数字功能标签。不据此否定其可变轴的字形变化；轴坐标研究与数字功能切换分开。 |
| Zilla Slab Regular | 默认与显式`pnum+onum`的比例旧式结果相同。四组数字功能实际不同，两个等宽设置均为每数字600单位；适合补充粗衬线及默认旧式方向。 |
| Barlow Condensed Regular | 默认比例宽；`tnum`实际替代为每数字434单位，`pnum`与默认相同。这份文件的数字特性标签仅包含本轮的`pnum/tnum`。 |
| Azeret Mono Roman | 固定400，默认及`tnum`均每数字650单位，但`tnum`真实改变1–9的轮廓；**宽度不变也可能有可见字形变化**。`zero`改变0而保持等宽。 |
| DSEG7 Classic Regular | 输入0–9默认每数字816单位，未含本轮五个数字功能标签。本审计只检验数字串，不验证点号、冒号、换行或其他字符的显示语义。 |

“四组显式组合不同”与“四组结果都严格符合所请求的宽度”分别记录。JSON使用 `four_explicit_combinations_measured_distinct` 与 `four_explicit_combinations_match_widths_strictly`，避免把不同glyph ID当成所有语义都已满足。

DSEG7的等宽测量不授权把它当通用正文字体。实际年月日分隔符、星期和书名应另选经过字符及语义检查的字体；七段数字是否适合小日号也不能从本次覆盖测试推断。所有新增测量与基础14文件的记录使用同一上下文；基础14条逐对象校验保持不变。

## Noto Serif SC：语言与默认局部字形会改变结果

同一保留VF、`wght=400`、`script=Latn`，得到：

| 路径／语言 | 默认0–9的glyph ID | advance（UPM1000） |
| --- | --- | --- |
| 原始cmap／hmtx（不塑形） | 17–26 | 557、471、558、557、555、558、558、549、558、562 |
| HarfBuzz，`en`，默认`locl` | 30584–30593 | 全部550 |
| HarfBuzz，`zh-Hans`，默认`locl` | 17–26 | 557、471、558、557、555、558、558、549、558、562 |
| HarfBuzz，`en`，仅关闭`locl`诊断 | 17–26 | 回到上述比例宽 |

因此，原素材库记录的**raw-cmap比例宽**并没有错；它与本次**指定语言下的实际塑形结果**是不同测量路径。关闭`locl`只用来确认差异来源，不是给所有日历关闭本地化字形的建议。排版配方应保留语言／脚本和实际渲染器。

## 四个不能省略的区分

1. **标签、请求与结果**：文件包含某个标签、代码请求它、实际发生替代分别留证。请求无变化可能是默认已采用，不等于功能失效。
2. **数字宽度与高度**：`pnum/tnum`和`lnum/onum`是两个选择维度。不能只凭advance判定旧式／等高，也不能把墨迹高度相同当作同一数字形式。
3. **严格相等与微小误差**：保留`advance_spread_units`与em值。Space Grotesk的旧式等宽和Source Sans的斜线0出现1单位级差异，与Newsreader指定Italic文件中7差200单位的事实不同；本审计不把任一差异自动归因于字体缺陷。
4. **轮廓与ID**：不同glyph ID可能保留同样轮廓；本次额外比较实际矢量绘制内容，`outline_changed_digits`与`glyph_substituted_digits`独立。字形坐标发生改变也不等于人眼已认可其美感。

## 适合下一步实际字样研究的三组

- **Source Serif 4 Roman**：四种数字形式的完整对照，可固定字重、光学轴、名义字号、基线与字串，再解释宽度和高度各自改变什么。
- **Inter Roman**：默认比例宽和真正启用`tnum`的对照，适合说明同一家族内也能独立选择数字表现；不必为了等宽另换mono家族。
- **Noto Serif SC**：同文件、同坐标下的语言／`locl`对照，用于解释字体文件指标与实际中英排版为何不同。诊断关闭功能不作为默认推荐。

这些均为可验证的技术问题，不预设大日号、七日横栏或全年网格必须采用某一种数字风格。实际日历还须回到1–31、前导零、星期字体、单元锚点、观看距离和整体图文关系。
