#!/usr/bin/env python3
"""Build scale-grouped calendar material cards and outlined SVG contact sheets.

These are editable components, not finished calendar templates. Decorative
geometry carries no seasonal, astronomical, or measured-data meaning.
"""
from __future__ import annotations

import argparse
import base64
import calendar
from datetime import date
import hashlib
from html import escape
import importlib.util
import json
import math
from pathlib import Path

from design_scene import Scene

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('material_calendar_data', ROOT/'.agents/skills/calendar-design-lab/scripts/calendar_data.py')
dates = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dates)

SCALES = ('year', 'month', 'week', 'day')
SCALE_NAMES = {'year': 'Annual / see the whole', 'month': 'Monthly / build a series', 'week': 'Weekly / make room', 'day': 'Daily / notice one thing'}
PAPER = '#F5F1E8'
INK = '#24312E'
PALETTES = {
    'year': ['#E9EDB2', '#2D453D', '#BC5C3A', '#E8B385'],
    'month': ['#DFE7EF', '#2D4CB1', '#EFB999', '#607A65'],
    'week': ['#E4EBDF', '#3F5B46', '#B6C5DA', '#D8A46C'],
    'day': ['#F5BD91', '#943C2F', '#8B78A0', '#E6DBAE'],
}

# Explicit transfer decisions, rather than a list of vague style names.
DEFINITIONS = [
    ('y-ribbon', 'year', 'Day-weighted ribbon', '等日长度月份带', 'functional',
     '需要看见全年连续性与月份长短时使用；每段宽度由实际公历天数计算。', ['month lengths', 'quarter separators', 'continuity'],
     ['year', 'month'], '年历作长索引；月历缩为当前月份在全年中的定位条。', ['year', 'width', 'palette']),
    ('y-tabs', 'year', 'Twelve edge tabs', '十二月份侧签', 'navigation',
     '多页系列的检索部件；位置编码月份，颜色仅作装饰。', ['tabs', 'month index', 'series'],
     ['year', 'month', 'day'], '年历作目录；月历保留当月签；日页可用侧签标识所在月份。', ['year', 'tab depth', 'palette']),
    ('y-weave', 'year', 'Quarter weave', '四分区织线', 'ornament',
     '用于年历边框、封面或章节分隔的原创线纹；四区不代表季节或观测数据。', ['weave', 'line texture', 'quarters'],
     ['year', 'month'], '年历作四区底纹；月历只选其中一区，控制纹理与数字对比。', ['line spacing', 'stroke', 'palette']),
    ('y-orbit', 'year', 'Orbit ornament', '环形装饰线', 'ornament',
     '给径向构图提供可替换边饰；纯装饰，不是月相、日长或天文轨道。', ['rings', 'border', 'radial'],
     ['year', 'day'], '年历置于日期环之外；日页作低对比图像框，不能冒充天文数据。', ['ring count', 'amplitude', 'palette']),
    ('m-mat', 'month', 'Image mat + caption', '主图卡纸与图注', 'image-frame',
     '为横向主图、作品名与来源留出独立区域；不把文字压在复杂图像上。', ['image', 'caption', 'mat'],
     ['month', 'day'], '月历放整幅作品；日历选一个细节并保留原作身份。', ['image aspect', 'mat width', 'caption depth']),
    ('m-specimen', 'month', 'Specimen label', '博物学标本签', 'content-module',
     '适合植物、鸟类或材料图版的标题与出处；示例字段留空，不虚构物种与地点。', ['botanical', 'caption', 'archive'],
     ['month', 'week', 'day'], '月历形成图版系列；周页记录一次观察；日页形成一日一物。', ['field names', 'rule spacing', 'palette']),
    ('m-overprint', 'month', 'Overprint planes', '叠色几何片', 'ornament',
     '原创不透明色片模拟叠印关系，可替换配色与方向；并非某种真实印刷效果证明。', ['geometric', 'overprint', 'color block'],
     ['month', 'day'], '月序列每月改变位置而保留语法；日序列一次只改变一个参数。', ['plane positions', 'palette', 'scale']),
    ('m-dock', 'month', 'Six-row date dock', '可容纳六行的日期底座', 'date-module',
     '固定六行空间，保留真实月份起点；非本月位置保持空白而非捏造日期。', ['six rows', 'lookup', 'date grid'],
     ['month'], '主图可以自由更换；七列与六行承载不同月份，仍需检查字号与写字面积。', ['year', 'month', 'week start', 'cell size']),
    ('w-hours', 'week', 'Time ladder', '七日时间梯', 'planning-module',
     '适合按时间段安排的一周；标注的小时是坐标，不代表用户真实日程。', ['time budget', 'seven days', 'hours'],
     ['week', 'day'], '周页并列七天；日页扩展一列并增加刻度，其他空间留给记录。', ['anchor date', 'hour range', 'row height']),
    ('w-notes', 'week', 'Seven note stamps', '七张日记条', 'writing-module',
     '七天提供同等书写空间，保留日期与星期，避免把周末默认为不用记录。', ['equal area', 'notes', 'seven units'],
     ['week', 'day'], '周页排七条；日页放大一条，增加需要的字段。', ['anchor date', 'columns', 'rule spacing']),
    ('w-habit', 'week', 'Empty habit weave', '空白习惯矩阵', 'tracking-module',
     '允许用户自己写行名与勾选；未填写是未填写，不是未完成或坏的一天。', ['habit', 'blank state', 'matrix'],
     ['week', 'month'], '周页七列；月页按实际天数扩展，不能沿用七列而省略日期。', ['anchor date', 'row names', 'checkbox size']),
    ('w-margin', 'week', 'Review + next margin', '回顾与下周边栏', 'reflection-module',
     '为周回顾和下一步留出不与时间表混淆的边栏；英文短提示为项目原创。', ['review', 'next', 'margin'],
     ['week', 'month', 'day'], '周/月页作收尾；日页可缩成一个可选问题，不强迫用户填满。', ['prompts', 'rule count', 'width']),
    ('d-number', 'day', 'Expressive day number', '展示型单日数字', 'type-module',
     '数字作为单页视觉主角，查阅信息用另一层级完整标注。', ['display numeral', 'hierarchy', 'date identity'],
     ['day', 'month'], '日页显示日号；月封面显示月号，不能让月号被误读成日期。', ['date', 'font role', 'size', 'palette']),
    ('d-perforation', 'day', 'Perforated edge', '撕页孔线边饰', 'carrier-motif',
     '向撕页形式借用视觉提示；图中孔线仅为平面图形，未验证实体装订和裁切。', ['tear off', 'edge', 'paper'],
     ['day', 'week'], '日页作页首边饰；周历作收尾分隔，不作为真实裁切工程图。', ['hole spacing', 'edge depth', 'palette']),
    ('d-detail', 'day', 'One image, four windows', '单图局部连载窗口', 'sequence-module',
     '预留四个局部观察窗口；衍生裁切仍要保留来源，不能宣称是四件独立作品。', ['detail', 'sequence', 'crop'],
     ['day', 'week', 'month'], '同图跨四天逐步观察，或月历主图搭配周页细节；先确认裁切权限。', ['source image', 'crop positions', 'sequence length']),
    ('d-observe', 'day', 'Observation slip', '一日观察笺', 'writing-module',
     '用少量原创提示支持记录；空白区域保持可用，不预填励志语录。', ['journal', 'observation', 'prompt'],
     ['day', 'week'], '日页三个字段；周页七张短笺，按成品尺寸减少问题数量。', ['prompts', 'rule spacing', 'field count']),
]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_component(key, scale, title, year=2027):
    colors = PALETTES[scale]
    bg, accent, secondary, tertiary = colors
    s = Scene(key, title, 800, 500, PAPER, {'scale': scale, 'year': year, 'status': 'component-study'})
    if key == 'y-ribbon':
        s.text(46, 130, str(year), 107, 'display', accent)
        data = dates.calendar_data('year', date(year, 1, 1))
        total = len(data['days']); x = 46
        for m in range(1, 13):
            count = sum(d['month'] == m for d in data['days'])
            w = 708*count/total
            s.rect(x, 230, w, 98, [accent, secondary, tertiary, bg][(m-1)//3])
            s.text(x+7, 215, f'{m:02}', 16, 'mono', INK)
            for d in data['days']:
                if d['month'] == m:
                    with s.day(date.fromisoformat(d['date']), month=m, width=708/total):
                        if d['day'] > 1:
                            xx = x+(d['day']-1)*708/total
                            s.line(xx, 315, xx, 328, PAPER, .5)
            x += w
        s.text(46, 383, f'{total} civil days / actual month lengths', 19, 'mono', INK)
    elif key == 'y-tabs':
        s.text(48, 138, 'A year, indexed.', 76, 'display', accent)
        for m in range(1, 13):
            x = 48+(m-1)*59
            s.rect(x, 204, 47, 115+(m%3)*32, colors[(m-1)%4])
            s.text(x+23.5, 240, f'{m:02}', 21, 'mono-medium', PAPER if (m-1)%4 == 1 else INK, 'middle')
            s.line(x+23.5, 370, x+23.5, 423, accent, 1)
    elif key == 'y-weave':
        for q in range(4):
            x, y = 42+(q%2)*358, 36+(q//2)*217
            s.rect(x, y, 330, 193, bg)
            for n in range(25):
                xx = x+8+n*13
                yy = y+8+n*7
                s.line(xx, y+6, xx, y+187, colors[1+q%3], 1.3)
                if yy < y+190: s.line(x+6, yy, x+324, yy, colors[1+(q+1)%3], 1.4)
            s.rect(x+18, y+18, 82, 43, PAPER)
            s.text(x+30, y+48, f'{q+1:02}', 25, 'mono', INK)
    elif key == 'y-orbit':
        for ring in range(13):
            pts=[]
            for n in range(181):
                a = n*2*math.pi/180
                r=62+ring*10+7*math.sin(a*6+ring*.31)
                pts.append(('M' if n==0 else 'L', 400+1.6*r*math.cos(a), 250+r*math.sin(a)))
            s.path(pts, stroke=colors[1+ring%3], width=1.2)
        s.text(400, 268, 'TIME', 43, 'display', accent, 'middle')
    elif key == 'm-mat':
        s.rect(74, 38, 652, 424, bg)
        s.rect(110, 72, 580, 275, PAPER, accent, 1)
        s.line(110, 72, 690, 347, accent, .8)
        s.line(690, 72, 110, 347, accent, .8)
        s.rect(291, 186, 218, 42, PAPER)
        s.text(400, 215, 'IMAGE SLOT', 20, 'mono', accent, 'middle')
        s.text(110, 395, 'Title / maker / source', 25, 'display', INK)
        s.text(110, 430, 'A caption has its own space.', 16, 'sans', INK)
    elif key == 'm-specimen':
        s.rect(72, 45, 656, 410, '#E6E7D8', accent, 1)
        s.text(104, 110, 'FIELD NOTES', 19, 'mono', accent, tracking=2)
        s.text(104, 172, 'One specimen', 61, 'display', INK)
        for i, text in enumerate(['Name', 'Observed', 'Source']):
            y = 246+i*67
            s.text(105, y, text, 18, 'mono', INK)
            s.line(260, y+4, 684, y+4, accent, .8)
    elif key == 'm-overprint':
        s.rect(90, 50, 330, 365, bg)
        s.path([('M',270,90),('L',700,150),('L',610,440),('L',190,372),('Z',)], secondary)
        s.rect(360, 145, 160, 265, accent)
        s.circle(270, 257, 105, '#D7A28B')
        s.text(75, 461, 'same grammar / new arrangement', 20, 'mono', INK)
    elif key == 'm-dock':
        month = 5  # Six display rows in 2027, intentionally checked.
        model = dates.calendar_data('month', date(year, month, 1))
        s.text(46, 73, f'{calendar.month_name[month]} {year}', 53, 'display', accent)
        for c, label in enumerate(['M','T','W','T','F','S','S']):
            s.text(92+c*102, 122, label, 17, 'mono', INK, 'middle')
        for row in range(6):
            for col in range(7):
                x, y = 46+col*102, 144+row*50
                s.rect(x, y, 96, 44, bg if col<5 else '#E6DBC8')
                if row < len(model['months'][0]['weeks']):
                    d=model['months'][0]['weeks'][row][col]
                    if d['in_month']:
                        with s.day(date.fromisoformat(d['date']), row=row, column=col):
                            s.text(x+12, y+29, d['day'], 21, 'mono', INK)
    elif key in ('w-hours','w-notes','w-habit'):
        model=dates.calendar_data('week', date(year, 4, 8))
        s.text(137,485,f'{model["period"]["start"]} / {model["period"]["end"]}',15,'mono',INK)
        for col, d in enumerate(model['days']):
            x=137+col*87
            with s.day(date.fromisoformat(d['date']), column=col):
                s.text(x+36, 73, calendar.day_abbr[d['weekday_monday0']].upper(), 17, 'mono', accent, 'middle')
                s.text(x+36, 110, f'{d["day"]:02}', 26, 'mono-medium', INK, 'middle')
            if key == 'w-notes':
                s.rect(x, 140, 75, 300, bg)
                for row in range(7): s.line(x+9, 190+row*33, x+66, 190+row*33, '#95A98D', .7)
        if key == 'w-hours':
            for row, hour in enumerate([6,9,12,15,18,21]):
                y=153+row*58
                s.text(62, y+6, f'{hour:02}', 16, 'mono', INK)
                s.line(128, y, 746, y, '#9AA791', .8)
            for col in range(8): s.line(128+col*87, 136, 128+col*87, 457, '#9AA791', .7)
        elif key == 'w-habit':
            for row in range(4):
                y=180+row*76
                s.line(40, y+18, 113, y+18, '#9AA791', 1)
                for col in range(7): s.rect(157+col*87, y, 35, 35, None, accent, 1)
    elif key == 'w-margin':
        s.rect(43, 38, 344, 420, bg)
        s.rect(413, 38, 344, 420, '#E6DFD1')
        for x, title, prompt in [(70,'Looking back','What stayed with you?'),(440,'Looking ahead','What needs room?')]:
            s.text(x, 118, title, 49, 'display', INK)
            s.text(x, 162, prompt, 20, 'sans', INK)
            for row in range(6): s.line(x, 215+row*39, x+288, 215+row*39, '#9AA791', .8)
    elif key == 'd-number':
        value=date(year,4,18)
        with s.day(value):
            s.rect(0, 0, 800, 500, bg)
            s.text(65, 385, '18', 460, 'display-italic', accent)
            s.text(560, 115, calendar.day_abbr[value.weekday()].upper(), 33, 'mono', accent)
            s.text(560, 164, f'APR {year}', 22, 'mono', accent)
            s.line(560, 197, 736, 197, accent, 1)
            s.text(560, 239, f'{value.timetuple().tm_yday:03}', 27, 'mono', accent)
    elif key == 'd-perforation':
        s.rect(74, 38, 652, 424, '#F9E6CC')
        s.rect(74, 38, 652, 56, accent)
        for n in range(26): s.circle(87+n*25, 95, 4, PAPER)
        s.text(115, 198, 'A fresh page.', 80, 'display', accent)
        s.text(115, 248, 'A visual paper motif.', 23, 'sans', INK)
        for y in range(301,421,39): s.line(115, y, 677, y, '#C5A48E', .9)
    elif key == 'd-detail':
        for n in range(4):
            x, y=48+(n%2)*365, 36+(n//2)*227
            s.rect(x, y, 336, 191, colors[n])
            s.circle(x+167, y+99, 58, None, PAPER, 2)
            s.line(x+167, y+24, x+167, y+174, PAPER, 1)
            s.line(x+92, y+99, x+242, y+99, PAPER, 1)
            s.text(x+15, y+35, f'{n+1:02} / 04', 17, 'mono', INK if n==0 else PAPER)
            s.text(x+168,y+177,'CROP WINDOW',14,'mono',INK if n==0 else PAPER,'middle')
    elif key == 'd-observe':
        s.rect(64, 35, 672, 430, '#EBE2CB')
        s.text(102, 115, 'A small record', 65, 'display', accent)
        for n, prompt in enumerate(['Today', 'I noticed', 'To remember']):
            y=193+n*91
            s.text(103, y, prompt, 20, 'mono', INK)
            s.line(104, y+44, 690, y+44, '#B49984', .9)
    else:
        raise ValueError(key)
    return s


def component_records(year=2027):
    result=[]
    for key, scale, title, zh, role, purpose, tags, other, transfer, params in DEFINITIONS:
        s=build_component(key,scale,title,year)
        source=s.svg()
        result.append((s,source,{
            'id':key,'title':title,'title_zh':zh,'primary_scale':scale,
            'suggested_scales':other,'role':role,'purpose':purpose,'tags':tags,
            'cross_scale_adaptation':transfer,'parameters':params,
            'parameter_scope':'Editable design variables in source. The current CLI exposes year and output directory only.',
            'rights_status':'project-original-no-public-license-selected',
            'sharing_scope':'Retained as original project material; no additional public reuse grant is asserted.',
            'local_path':f'assets/library/components/{key}.svg',
            'sha256':hashlib.sha256(source.encode()).hexdigest(),
            'dimensions':{'width':800,'height':500},
            'calendar_dates':s.dates,'example_year':year,
            'implementation':'scripts/build_material_library.py',
            'note':'Editable code + outlined SVG proof; not a finished calendar or validated user preference.',
        }))
    return result


def embed_svg(svg,x,y,w,h):
    start=svg.index('>')+1
    return f'<svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="0 0 800 500">'+svg[start:svg.rfind('</svg>')]+'</svg>'


def embed_image(asset,x,y,w,h):
    data=base64.b64encode((ROOT/asset['local_path']).read_bytes()).decode()
    title=escape(asset['attribution'])
    return f'<image x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid meet" href="data:image/jpeg;base64,{data}"><title>{title}</title></image>'


IMAGE_GROUPS={
    'year':['met-wave','cma-lace'],
    'month':['met-roses','cma-tulip'],
    'week':['cma-lily','cma-bird'],
    'day':['cma-snow','cma-moon'],
}


def board(scale, records, images):
    s=Scene('board-'+scale, SCALE_NAMES[scale],1800,1130,PAPER,{})
    s.text(50,85,SCALE_NAMES[scale],62,'display',INK)
    s.text(52,124,'4 editable components + 2 CC0 image starting points',24,'sans',INK)
    parts=[]
    own=[r for r in records if r[2]['primary_scale']==scale]
    for i, (_,svg,meta) in enumerate(own):
        x=50+i*430
        parts.append(embed_svg(svg,x,164,410,256.25))
        s.text(x,457,f'{meta["id"]} / {meta["title"]}',21,'sans-medium',INK)
    for i, asset_id in enumerate(IMAGE_GROUPS[scale]):
        a=images[asset_id]; x=50+i*860
        s.rect(x,515,840,420,'#E8E6DE')
        parts.append(embed_image(a,x+18,532,804,386))
        s.text(x,975,f'{a["id"]} / CC0 / {a["dimensions"]["width"]} x {a["dimensions"]["height"]} px',24,'mono',INK)
        s.text(x,1010,'Metropolitan Museum of Art' if a['id'].startswith('met-') else 'Cleveland Museum of Art',23,'sans',INK)
    s.text(50,1080,'Components are studies. Image groups suggest use; a source image can work at more than one scale.',22,'sans',INK)
    return s.svg().replace('</svg>', '\n'.join(parts)+'</svg>')


def overview(records,images):
    s=Scene('material-overview','Calendar material library',1800,1940,PAPER,{})
    s.text(50,83,'How your days fly / material library',67,'display',INK)
    s.text(52,129,'Annual / monthly / weekly / daily - source images, editable parts, different reading tasks',25,'sans',INK)
    parts=[]
    for row,scale in enumerate(SCALES):
        y=174+row*430
        s.text(50,y+48,SCALE_NAMES[scale],43,'display',PALETTES[scale][1])
        own=[r for r in records if r[2]['primary_scale']==scale][:2]
        for col,(_,svg,meta) in enumerate(own):
            x=50+col*430
            parts.append(embed_svg(svg,x,y+78,410,256.25))
            s.text(x,y+366,meta['id']+' / '+meta['title'],21,'sans',INK)
        for col,asset_id in enumerate(IMAGE_GROUPS[scale]):
            x=910+col*430; a=images[asset_id]
            s.rect(x,y+78,410,256.25,'#E8E6DE')
            parts.append(embed_image(a,x+10,y+87,390,237))
            s.text(x,y+366,asset_id+' / CC0 source image',21,'sans',INK)
    s.text(50,1910,'16 retained vector components + 8 CC0 source images / v1 / 2026-10-29',22,'mono',INK)
    return s.svg().replace('</svg>', '\n'.join(parts)+'</svg>')


def build(out_dir=ROOT/'studies/material-library', year=2027):
    if not 2<=year<=9998: raise ValueError('year must be between 2 and 9998')
    for font in json.loads((ROOT/'assets/fonts/provenance.json').read_text())['files']:
        if digest(ROOT/font['path'])!=font['sha256']:
            raise ValueError(f'Font changed: {font["path"]}; revise provenance explicitly before replay.')
    image_manifest=json.loads((ROOT/'assets/library/open-images/manifest.json').read_text())
    images={v['id']:v for v in image_manifest['assets']}
    for a in images.values():
        if a['license']!='CC0-1.0': raise ValueError(f'Image not admitted as CC0: {a["id"]}')
        if digest(ROOT/a['local_path'])!=a['sha256']: raise ValueError(f'Image changed: {a["id"]}')
    components=component_records(year)
    component_dir=ROOT/'assets/library/components'
    component_dir.mkdir(parents=True,exist_ok=True)
    out_dir.mkdir(parents=True,exist_ok=True)
    for _,source,meta in components:
        # Alternate-year runs do not overwrite the retained baseline component assets.
        destination=ROOT/meta['local_path'] if year==2027 else out_dir/Path(meta['local_path']).name
        destination.write_text(source)
    if year==2027:
        (component_dir/'manifest.json').write_text(json.dumps({
            'schema_version':1,'created_on':'2026-10-29','assets':[r[2] for r in components],
            'implementation_sha256':digest(Path(__file__)),
            'font_manifest':'assets/fonts/provenance.json',
        },ensure_ascii=False,indent=2)+'\n')
    for scale in SCALES:
        (out_dir/f'{scale}.svg').write_text(board(scale,components,images))
    (out_dir/'overview.svg').write_text(overview(components,images))
    print(f'Built 16 components and 5 grouped SVG boards for {year}.')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out-dir',type=Path,default=ROOT/'studies/material-library')
    p.add_argument('--year',type=int,default=2027)
    args=p.parse_args()
    build(args.out_dir,args.year)
