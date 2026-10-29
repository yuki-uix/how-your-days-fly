# How Your Days Fly

让每个人借助 AI，设计自己愿意使用的年历、月历、周历和日历。

最终目标是一个公众可访问的网站：访客可以表达对时间与视觉的偏好，生成和修改日历，保存作品，并复用站内原创或获授权的设计配方。名称暂定。

## 当前阶段

先验证日历设计能力，再把验证有效的方法开放到网站。

- 已有：项目专用的 `calendar-design-lab` skill 初稿、支持年/月/周/日的公历数据工具，以及 8 份可重放 SVG 源码的原创模式样本。
- 正在开始：[第一个真实设计实验](docs/first-experiment.md)。
- 尚未验证：设计满意度、反馈后的改进、跨用户效果、完整设计配方的重放。
- 尚未实现：通用视觉设计引擎、网站、在线 AI 生成、分享与导出服务。当前样本渲染器是实验工具。

```mermaid
flowchart TD
    A[真实需求与审美参考] --> B[设计 Skill：分析与提出方案]
    B --> C[可编辑的设计规格]
    C --> D[日期数据与视觉渲染]
    D --> E[预览与用户反馈]
    E --> C
    E --> F[保存认可的设计配方]
    F --> G[后续网站：生成、修改、分享与复用]
```

上图是拟建流程。当前日期数据工具只负责计算，不负责产生视觉设计。

## 第一轮设计模式样本

先以相近的中性视觉语言比较全年结构，再用月、周、日样本比较内容角色。样本均为原创研究，尚未获得用户的审美认可；它们不是封闭的产品模板清单。

![八份原创日历模式样本](studies/pattern-atlas/overview.svg)

[查看设计语法、样本映射与一手参考](.agents/skills/calendar-design-lab/references/patterns.md)。A–E 比较月份分区、连续周、月份条带、年轮和等日单元；F/G/H 分别展示图像主导月历、书写主导周历与单日日历。点击 SVG 可以查看源文件或完整尺寸。

[公开学习资料与练习路线](.agents/skills/calendar-design-lab/references/learning-guide.md)包括时间可视化开放教材、设计空间研究、排版指南和日历案例；逐项区分公开阅读范围与复用许可。

```sh
python3 scripts/render_pattern_atlas.py
python3 scripts/render_pattern_atlas.py --year 2028 --out-dir tmp/leap-studies
python3 scripts/render_pattern_atlas.py --pdf output/pdf/calendar-pattern-atlas.pdf
```

SVG 生成只用标准库；可选 PDF 导出需要 `reportlab`。SVG 源码可确定性重放，浏览器字形依赖本机字体；后续正式配方需固定字体版本。原图形与 `manifest.json` 保存在 `studies/pattern-atlas/`，PDF 和本地预览保存在忽略的 `output/`。

## 使用当前能力

需要 Python 3.10 或以上；日期工具与测试不依赖第三方 Python 包。

在支持项目 skills 的 agent 中使用 `.agents/skills/calendar-design-lab/SKILL.md`。其他环境可直接读取该文件及其按需引用的资源。

生成日期数据：

```sh
python3 .agents/skills/calendar-design-lab/scripts/calendar_data.py --view year --date 2027-01-01 > calendar.json
python3 .agents/skills/calendar-design-lab/scripts/calendar_data.py --view month --date 2028-02-01
python3 .agents/skills/calendar-design-lab/scripts/calendar_data.py --view week --date 2027-01-01 --week-start sunday
python3 .agents/skills/calendar-design-lab/scripts/calendar_data.py --view day --date 2027-01-01
python3 -m unittest discover -s tests -v
```

输出包含连续日期及月份网格；月份网格保留相邻月份的真实日期，以 `in_month` 区分。日期工具采用公历，支持 2–9998 年，暂不计算农历、节气、法定假日或调休。

## 我们怎样判断进展

技术检查与用户的设计评价单独记录。日期正确、没有溢出，不等于用户愿意使用。

第一阶段需要完成：

1. 一份真实用户愿意使用的日历，记录具体满意和不满意的地方。
2. 一次根据反馈进行的定向修改，保留用户已经喜欢的部分。
3. 保存选定的设计规格、实现版本与素材后，再次渲染；随后验证换年份和另一位用户的需求。

年、月、周、日可以共享字体、素材和设计规则；各自的时间组织与使用场景仍需分别验证。

## 参考作品与素材

参考分析与可分发资产分开管理。只把自有或取得相应许可的字体、图片和模板纳入共享配方，并保留来源、版本及允许用途。AI 生成的内容也需要检查其来源与可分享范围。

原始参考上传、个人资料、密钥和本地输出默认不进入 Git。仓库暂未选择项目整体的开源许可证；公开可读不代表授予所有再利用权利。
