#!/usr/bin/env python3
"""Original type/layout research proofs with no third-party art or private cases.

Glyph-outline studies use cmap/hmtx plus explicit tracking. They do not claim
OpenType shaping, kerning, ligatures, language substitutions or line breaking.
"""
import argparse
from datetime import date
import hashlib
import importlib.util
import json
from pathlib import Path

import design_scene as ds
from prepare_type_study_fonts import prepare

ROOT=Path(__file__).resolve().parents[1]
CACHE=ROOT/'tmp/type-layout-fonts'
OUTPUT=ROOT/'studies/type-layout-atlas'
INK='#233C39'; MUTED='#6B7970'; PAPER='#F5F5ED'; BLUE='#345C72'; RULE='#C7CFC3'; ORANGE='#BD6948'
NS=['一','二','三','四','五','六','日']
spec=importlib.util.spec_from_file_location('atlas_dates',ROOT/'.agents/skills/calendar-design-lab/scripts/calendar_data.py')
dates=importlib.util.module_from_spec(spec); spec.loader.exec_module(dates)


def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def ink_scale(font,text,height):
    *_,units=ds.font_info(font)
    boxes=[ds.glyph_bounds(font,c) for c in text if ds.glyph_bounds(font,c)]
    low=min(b[1] for b in boxes); high=max(b[3] for b in boxes)
    size=height*units/(high-low)
    return size,high*size/units


def text_board():
    s=ds.Scene('type-proof','字体、角色与数字研究',1800,1480,PAPER,{})
    s.text(60,77,'字体选择：从字形到角色',40,'sans500',INK)
    s.text(60,120,'原创字样研究 / 不以字体类别或极简程度判定审美高低',21,'sans400',MUTED)
    for i,(font,label) in enumerate([('serif400','Noto Serif SC / 400'),('sans400','Noto Sans SC / 400')]):
        x=60+i*890
        s.text(x,197,label,21,'sans400',MUTED)
        s.text(x,308,'日子的形状',92,font,INK)
        s.text(x,370,'Days in view / 一月 · January',29,font,INK)
        s.text(x,426,'01 08 11 28 31',38,font,INK)
        s.text(x,472,'周一 · Monday，标点与字面一起看。',25,font,MUTED)
    s.line(60,520,1740,520,RULE,1)
    s.text(60,579,'相近视觉尺度：墨迹高度 56',28,'sans500',INK)
    for i,(font,label) in enumerate([('serif400','宋体'),('sans400','黑体')]):
        x=60+i*890; size,baseline=ink_scale(font,'日子的形状',56)
        s.text(x,620+baseline,'日子的形状',size,font,INK)
        s.text(x,732,f'{label} / 补偿后的字号 {size:.1f}',21,'sans400',MUTED)
    s.text(60,785,'墨迹框相同不等于看起来同样大；内部空间与笔画分布仍需观看。',23,'sans400',MUTED)
    s.line(60,828,1740,828,RULE,1)
    s.text(60,888,'角色配对：三个可检验的选择',28,'sans500',INK)
    pairs=[('serif400','serif400','同族关系'),('serif600','sans400','互补角色'),('sans500','mono','展示与索引')]
    for i,(title,lookup,label) in enumerate(pairs):
        x=60+i*580
        s.text(x,945,label,21,'sans400',MUTED)
        s.text(x,1024,'日子的形状',62,title,INK)
        s.text(x,1082,'01 08 11 28 31',29,lookup,INK)
        s.text(x,1127,'一月 / January',21,'sans400',MUTED)
    s.line(60,1180,1740,1180,RULE,1)
    s.text(60,1240,'数字宽度是实测，不由家族名称推断',28,'sans500',INK)
    for i,(font,label) in enumerate([('serif400','宋体 / 比例 advance'),('sans400','黑体 / 等宽 advance'),('mono','Plex Mono / 等宽 advance')]):
        x=60+i*580
        s.text(x,1312,'01112831',42,font,INK)
        s.text(x,1355,label,20,'sans400',MUTED)
    s.text(60,1420,'本证明未执行 GSUB/GPOS；特性启用、段落排版及导出效果须在目标环境另验。',22,'sans400',MUTED)
    return s


def art(s,x,y,w,h):
    # Original code-native geometric field used as a neutral image-role module.
    s.rect(x,y,w,h,BLUE)
    s.circle(x+w*.67,y+h*.43,min(w,h)*.30,'#D8DFB3')
    s.path([('M',x,y+h*.86),('L',x+w*.35,y+h*.38),('L',x+w*.62,y+h*.86),('L',x+w,y+h*.59),('L',x+w,y+h),('L',x,y+h),('Z',)],ORANGE)


def date_row(s,model,x,y,step,size=24):
    for i,item in enumerate(model['days']):
        value=date.fromisoformat(item['date'])
        with s.day(value,column=i): s.text(x+i*step,y,f'{value.day:02}',size,'sans400',INK)
        s.text(x+i*step,y+27,NS[value.weekday()],14,'sans400',MUTED)


def layout_card(key,model):
    s=ds.Scene('layout-'+key,key,800,520,PAPER,{})
    s.text(40,45,'2028.02.28 - 03.05',14,'sans400',MUTED)
    if key=='axis':
        s.text(400,122,'日子的形状',46,'serif400',INK,'middle')
        art(s,180,160,440,210)
        date_row(s,model,180,427,65,24)
    elif key=='grid':
        art(s,40,90,530,265)
        s.text(40,424,'日子的形状',49,'serif600',INK)
        s.text(40,471,'Days in view',22,'serif400',MUTED)
        for i,item in enumerate(model['days']):
            value=date.fromisoformat(item['date']); y=109+i*45
            s.text(625,y,NS[value.weekday()],15,'sans400',MUTED)
            with s.day(value,row=i): s.text(758,y,f'{value.day:02}',24,'sans400',INK,'end')
    elif key=='dense':
        s.text(40,116,'日子的形状',52,'sans500',INK)
        for i,item in enumerate(model['days']):
            value=date.fromisoformat(item['date']); x=40+i*105
            with s.day(value,column=i): s.text(x,192,f'{value.day:02}',29,'sans400',INK)
            s.text(x,224,'周'+NS[value.weekday()],15,'sans400',MUTED)
            s.line(x,249,x+82,249,RULE,1)
            for row in range(4): s.line(x,279+row*36,x+82,279+row*36,RULE,.8)
        s.text(40,478,'内容区用于记录，并非已填写的个人数据。',18,'sans400',MUTED)
    else:
        s.text(32,365,'日',350,'serif600',BLUE)
        s.text(355,153,'子的形状',70,'serif400',INK)
        s.line(355,190,760,190,ORANGE,5)
        s.text(355,253,'Days in view',35,'display',INK)
        date_row(s,model,355,383,57,24)
        s.text(355,478,'展示字与查读入口分开',18,'sans400',MUTED)
    return s


def embed(child,x,y,w,h):
    svg=child.svg(); body=svg[svg.index('>')+1:svg.rfind('</svg>')]
    return f'<svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="0 0 {child.width} {child.height}">{body}</svg>'


def layout_board(cards):
    s=ds.Scene('layout-proof','构图选择与代价',1800,1350,'#E9ECE4',{})
    s.text(60,77,'构图选择：四种关系，各有用途',40,'sans500',INK)
    s.text(60,122,'同一周日期与原创几何材料；任务、层级与组织方式变化，不作单变量因果比较。',22,'sans400',MUTED)
    parts=[]
    labels=['轴线与居中 / 稳定的观看入口','非对称网格 / 图版与边注','字段组织 / 为记录分配空间','表现性展示 / 另保留查读路径']
    for i,card in enumerate(cards):
        row,col=divmod(i,2); x=60+col*880; y=170+row*580
        parts.append(embed(card,x,y,800,520))
        s.text(x,y+558,labels[i],23,'sans400',INK)
    return s.svg().replace('</svg>','\n'.join(parts)+'</svg>')


def build(out_dir=OUTPUT):
    manifest=CACHE/'manifest.json'
    if not manifest.exists(): prepare(CACHE)
    fonts=json.loads(manifest.read_text())
    source_fonts=json.loads((ROOT/'assets/fonts/type-study/manifest.json').read_text())
    originals={a['id']:next(f for f in a['local_files'] if f['path'].endswith('.ttf'))['sha256'] for a in source_fonts['assets']}
    for asset in source_fonts['assets']:
        for f in asset['local_files']:
            if sha(ROOT/f['path'])!=f['sha256']: raise ValueError('Retained source font/license changed.')
    for item in fonts['fonts']:
        if item['source_sha256']!=originals[item['source_id']]:
            raise ValueError('Working cache belongs to another source; run prepare_type_study_fonts.py again.')
        p=CACHE/item['file']
        if sha(p)!=item['sha256']: raise ValueError('Working font changed; rebuild from retained originals.')
        ds.FONT_FILES[item['alias']]=p
    model=dates.calendar_data('week',date(2028,2,28))
    text=text_board(); layouts=[layout_card(k,model) for k in ['axis','grid','dense','expressive']]
    for s in [text]+layouts:
        overflow=[(t,b) for t,b,_ in s.text_bounds() if min(b[0],b[1])<-.01 or b[2]>s.width+.01 or b[3]>s.height+.01]
        if overflow: raise ValueError(f'{s.key} overflow: {overflow}')
    out_dir.mkdir(parents=True,exist_ok=True)
    (out_dir/'type-specimens.svg').write_text(text.svg())
    (out_dir/'layout-relations.svg').write_text(layout_board(layouts))
    for s in layouts: (out_dir/(s.key+'.svg')).write_text(s.svg())
    records={'font_working_copies':fonts,'source_fonts':'assets/fonts/type-study/manifest.json',
             'original_content':'Project-authored generic study text and native geometric field. No private design case or third-party artwork used.',
             'rendering_limits':'cmap/hmtx glyph outlines with explicit tracking; no automatic shaping, kerning, OpenType substitutions, paragraph breaking or CLREQ implementation.',
             'study_kind':'Comparative questions and compositional hypotheses; not an aesthetic ranking or user approval.',
             'date_model':model,'layout_cards':[{'id':s.key,'represented_dates':s.dates} for s in layouts],
             'implementation_sha256':sha(Path(__file__)),'preparer_sha256':sha(ROOT/'scripts/prepare_type_study_fonts.py'),
             'svg_sha256':{p.name:sha(p) for p in out_dir.glob('*.svg')}}
    (out_dir/'manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
    print('Built public type/layout study boards and four reusable composition proofs.')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out-dir',type=Path,default=OUTPUT)
    args=parser.parse_args(); build(args.out_dir)
