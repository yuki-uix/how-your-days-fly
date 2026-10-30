# 数字角色的新增字体源资产

2026-10-30。保留五个新增候选家族的**原始文件和完整原始OFL**，各一份Roman字体与一份许可；源文件合计884,368 bytes。这里是可用资产记录，不代表所有候选都适合所有日历或用户已认可其视觉效果。[manifest.json](manifest.json)逐文件保存来源、字节数、SHA-256、Git blob／发行包成员、轴值、版本、原始许可头和实测。

## 来源与保留范围

| 家族／文件 | 一手设计说明与用途研究 | 实际保留 |
| --- | --- | --- |
| Fraunces | [原设计仓库](https://github.com/undercasetype/Fraunces)把它描述为表现性Old Style soft-serif；“Old Style”是字体风格，不能据此推定数字已开启旧式功能 | Roman VF，`opsz`／`wght`／`SOFT`／`WONK`；不收Italic |
| Zilla Slab | [Mozilla官方仓库](https://github.com/mozilla/zilla-slab)说明它是Typotheque为Mozilla制作的家族，并列Google Fonts为分发渠道 | Regular静态TTF，作为粗衬线形态候选 |
| Barlow Condensed | [原设计仓库](https://github.com/jpt/barlow)说明其低对比、略圆且有三种宽度；本库只收其中Condensed Regular | 原生窄体静态TTF，不是将普通字体横向压缩 |
| Azeret Mono | [原设计仓库](https://github.com/displaay/Azeret)说明其等线性、连接细节与替代字形，并明确免费开放的是mono子家族 | Roman VF，仅`wght`；不收其他商业子家族 |
| DSEG7 Classic | [作者官方仓库](https://github.com/keshikan/DSEG)说明七段／十四段LCD语汇、空格／冒号及句点的特殊行为 | 仅官方稳定v0.46发行包中的Classic Regular七段TTF；不收Mini、Italic、14段或beta |

前四套从官方Google Fonts固定提交 `6157dfaa640ca5738b4d1a7070fe389c3036d7fc` 取得并校验Git blob；DSEG固定[官方v0.46发行版](https://github.com/keshikan/DSEG/releases/tag/v0.46)，保留发行包SHA-256、字节数与两个成员的原始字节。没有镜像整个发行包。DSEG原许可成员名为`DSEG-LICENSE.txt`，本库保存为`OFL.txt`，内容字节未改。

Roboto Slab在固定Google Fonts提交中位于`apache/robotoslab`，[原许可为Apache License 2.0](https://github.com/google/fonts/blob/6157dfaa640ca5738b4d1a7070fe389c3036d7fc/apache/robotoslab/LICENSE.txt)，未纳入本轮。采用OFL Zilla Slab补足粗衬线形态，保持本轮资产筛选逻辑一致；这不表示Apache字体不能用于日历。

## 指定文件的实测

FontTools 4.68.0，在内存固定`wght=400`，其他轴使用文件原始默认值；静态Regular不作变形。默认`cmap`／`hmtx`与字形墨迹框直接测量；只列GSUB／GPOS特性标签，没有执行替代、字距或塑形。

| 家族 | 本轮测量坐标 | 默认0–9 advance |
| --- | --- | --- |
| Fraunces | `opsz=9, wght=400, SOFT=0, WONK=1` | 比例宽；例如0=1300、1=902、8=1165（UPM2000） |
| Zilla Slab | 静态Regular／400 | 比例宽；0=576、1=385、8=538（UPM1000） |
| Barlow Condensed | 静态Regular／400 | 比例宽；0=444、1=256、8=422（UPM1000） |
| Azeret Mono | `wght=400` | 0–9全部650（UPM1000） |
| DSEG7 Classic | 静态Regular／400 | 0–9全部816（UPM1000） |

- 五份文件都覆盖`01 08 11 28 31`，并保留十个数字各自墨迹框。此样本不是完整字符／语言覆盖认证。
- Fraunces原文件默认`wght=900`、`opsz=9`、`SOFT=0`、`WONK=1`；Azeret Mono默认`wght=100`。默认轴值不能当作已选择的400。作者README的部分默认值与本文件不同，因此资产事实以实际`fvar`为准。
- Fraunces有`rvrn`，`WONK`涉及替换；只实例化轮廓、逐码点取字，不等于所有替换已执行。`opsz`、softness与数字实际变化需在目标塑形／渲染路径另验。
- Zilla Slab有`onum`／`lnum`／`pnum`／`tnum`，Barlow有`pnum`／`tnum`；这里只列发现的标签，未把“包含标签”记成“导出已启用”。数字宽度和高度分类分开检查。
- DSEG虽为一些拉丁字母分配codepoint，七段形态不等于普通正文字形；它缺少斜杠`/`和中文。完整日期若使用`/`、星期或月份，须明确另选字体，不能静默回退。其空格／冒号与零宽句点也不能照普通正文标点推断。

## 选择条件与代价

Fraunces可探索表现性大日号；Zilla Slab可比较粗衬线的印刷节奏；Barlow Condensed可比较有限宽度内的查读；Azeret Mono可比较固定宽度与辨识细节；DSEG7 Classic只在刻意采用电子显示语气时进入候选。这些是任务假设，不是品质或可读性排名。

日历小字需要另看输出尺寸、字重、数字开口、段间隙、像素／纸面和观看距离。窄体可能节省宽度，也可能让近似数字更难辨；等宽有利于特定对齐，却不自动比比例宽更美；七段字体的大尺寸表现不能外推到全年密集网格。

## 许可与修改

五套均保留各自OFL 1.1、版权和原始来源。DSEG原许可明确保留名称`DSEG`；其余四份原始头没有声明保留名称。完整条件以各原文件为准；实例化、子集化、转换或改名时仍须另留修改与来源记录，不能将字体替换为项目整体许可证，也不能单独售卖字体。

本轮没有发布修改字体、网页子集、Woff2或个人样张。原字体、工作实例、功能启用和最终输出分开保留；网站加载方案与印刷制作条件另选。
