# 可复用馆藏图像：第一组

这 8 张图像分别通过官方单件记录及开放政策核验，保留官方 web-sized JPEG 原字节，用于日历设计研究和屏幕预览。它们不是完整的 12 月或 365 日图像系列，也不代表用户已经选择这种美术方向。

| ID | 内容 | 来源 | 可尝试的时间尺度 |
| --- | --- | --- | --- |
| `met-wave` | 葛饰北斋《神奈川冲浪里》 | [The Met](https://www.metmuseum.org/art/collection/search/45434) | 年、月、日 |
| `met-roses` | 梵高《玫瑰》 | [The Met](https://www.metmuseum.org/art/collection/search/436534) | 月、日 |
| `cma-tulip` | Pieter Holsteyn II 的一枝郁金香 | [CMA](https://www.clevelandart.org/art/2020.133) | 月、周、日 |
| `cma-lily` | Sydenham Edwards 百合植物图版 | [CMA](https://www.clevelandart.org/art/1955.142) | 月、周、日 |
| `cma-bird` | 南宋《白梅与禽》，作者未详 | [CMA](https://www.clevelandart.org/art/1985.371) | 年、月、周、日 |
| `cma-snow` | 与谢芜村《雪中山水》 | [CMA](https://www.clevelandart.org/art/1997.111) | 年、月、日 |
| `cma-lace` | 花藤与几何纹样蕾丝片段 | [CMA](https://www.clevelandart.org/art/1920.1267) | 年、月、周、日 |
| `cma-moon` | 歌川广重《名所江户百景·月之岬》 | [CMA](https://www.clevelandart.org/art/1985.320) | 月、周、日 |

`manifest.json` 保存标题、作者与角色、馆方 credit line、来源、官方 API、下载地址、权利状态、核验日期、像素尺寸、SHA-256、适用尺度与组合建议。`evidence/` 保存最小必要的官方单件元数据快照。下载日期为 2026-10-29。没有重绘、裁切、去底或调色这些馆藏原图。

## 权利范围

- The Met 两件作品的单件页标明 Public Domain，API `isPublicDomain=true`；馆方以 [CC0](https://www.metmuseum.org/hubs/open-access) 提供对应公共领域图像。
- Cleveland 六件作品的单件页允许复制、修改和分发，API `share_license_status=CC0`；适用 [CMA Open Access](https://www.clevelandart.org/open-access) 和 [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/)。CMA 全部元数据开放，不意味着所有藏品图像都开放；以后新增仍需逐件核验。
- 清单保留完整推荐出处，便于查回作品和核对信息；CC0 不把署名作为使用条件。这些图片的 CC0 状态不改变本项目其他文件的授权范围。
- API 的 `creators` 有角色与归属限定：例如百合图版的 Sydenham Edwards 是 artist，Thomas Curtis 是 publisher；不把出版社角色合并误写为共同绘画作者。《白梅与禽》作者未详，不擅自归给具体画家。

## 使用与输出

画作原有满月、花卉、雪景是内容主题。实际日期、月相、当地花期和季节必须另取确定数据；它们不能从画面推定。蕾丝是有破损边缘的实物片段，不能直接当作无缝平铺纹理。

保留版长边约 600–900 像素，适合网页预览和小尺寸图块。`print_use.maximum_mm_at_300ppi` 给出对应 300ppi 尺寸，不能把这些文件直接称为 A3 打印素材。需要更大成品时，从每项 `high_resolution_url` 获取官方高分辨率版本，重新记录字节、尺寸和哈希，再把它写入最终日历 recipe；不依赖未来远程 URL 内容永远不变。
