#!/usr/bin/env python3
"""Reproducible English glyph studies, not a complete shaped typography engine."""
import argparse
import hashlib
import json
from pathlib import Path

import design_scene as ds
from prepare_latin_study_fonts import prepare

ROOT=Path(__file__).resolve().parents[1]
PAPER='#F4F1E9'; INK='#242A30'; MUTED='#636A71'; RULE='#D1CEC7'; ACCENT='#AE492D'
FAMILIES=[
    ('ss4','Source Serif 4','Text / display serif','400; opsz 20'),
    ('news','Newsreader','Editorial reading serif','400; opsz 16'),
    ('bodoni','Bodoni Moda','High-contrast serif','400; opsz 24'),
    ('sourcesans','Source Sans 3','Sans / weight and terminal detail','400'),
    ('inter','Inter','Interface / display sans','400; opsz 14'),
    ('space','Space Grotesk','Proportional sans; mono ancestry','400'),
    ('display','Instrument Serif','Display serif','Regular; static'),
    ('sans','IBM Plex Sans Condensed','Condensed sans','Regular; static'),
    ('mono','IBM Plex Mono','Monospaced family','Regular; static'),
]


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def metrics(alias):
    font,cmap,_,units=ds.font_info(alias)
    widths={c:font['hmtx'][cmap[ord(c)]][0] for c in '0123456789'}
    box=ds.glyph_bounds(alias,'x')
    return {'units_per_em':units,'default_digit_advances':widths,'default_digits_tabular':len(set(widths.values()))==1,
            'x_ink_height_em':(box[3]-box[1])/units}


def text(s,x,y,value,size=20,font='sourcesans',color=INK,tracking=0):
    s.text(x,y,value,size,font,color,tracking=tracking)


def families_board():
    s=ds.Scene('latin-families','English type: nine starting points',1800,1770,PAPER,{})
    text(s,60,80,'English type / nine starting points',48)
    text(s,60,124,'Same text at 52 units. Compare shape, width and rhythm; categories are search aids, not rankings.',22,color=MUTED)
    for i,(alias,name,role,coordinates) in enumerate(FAMILIES):
        row,col=divmod(i,3); x=60+570*col; y=180+500*row
        s.rect(x,y,540,465,'#FFFEFA')
        text(s,x+24,y+39,f'{i+1:02} / {name}',22)
        text(s,x+24,y+69,role,17,color=MUTED)
        text(s,x+24,y+148,'Days in view',52,alias)
        text(s,x+24,y+205,'September 2027',32,alias)
        text(s,x+24,y+251,'Mon Tue Wed Thu Fri Sat Sun',20,alias)
        text(s,x+24,y+306,'01 08 11 28 31',36,alias)
        text(s,x+24,y+355,'Il1 O0 ag &',32,alias)
        m=metrics(alias)
        s.line(x+24,y+380,x+516,y+380,RULE,1)
        text(s,x+24,y+407,coordinates,16,color=MUTED)
        default='tabular' if m['default_digits_tabular'] else 'proportional'
        text(s,x+24,y+438,f"x ink {m['x_ink_height_em']:.3f} em / default digits: {default}",16,color=MUTED)
    text(s,60,1736,'Default cmap outlines + advances. No GSUB/GPOS, automatic kerning, ligatures or feature switching.',20,color=MUTED)
    return s


def details_board():
    s=ds.Scene('latin-details','Optical size, native italics, tracking and numeral width',1800,1560,PAPER,{})
    text(s,60,77,'English type / inspect the decisions',46)
    text(s,60,119,'Controlled glyph studies; output scale and viewing distance still need a final-use proof.',22,color=MUTED)
    text(s,60,185,'01 / Optical design: Source Serif 4, weight 400, same 64-unit size',27)
    for i,(alias,opsz) in enumerate([('ss4small',8),('ss4',20),('ss4display',60)]):
        x=60+580*i
        text(s,x,231,f'opsz {opsz}',19,color=MUTED)
        text(s,x,317,'Reading days',64,alias)
        text(s,x,375,'January / Il1 O0',27,alias)
    text(s,60,430,'The glyph design changes. Scaling letters or changing weight does not activate optical sizing.',21,color=MUTED)
    s.line(60,466,1740,466,RULE,1)
    text(s,60,520,'02 / Native italic: separately designed glyphs, not a skew transform',27)
    for x,roman,italic,name in [(60,'ss4','ss4italic','Source Serif 4 / opsz 20'),(940,'news','newsitalic','Newsreader / opsz 16')]:
        text(s,x,560,name,19,color=MUTED)
        text(s,x,628,'Days in view / ag',51,roman)
        text(s,x,704,'Days in view / ag',51,italic)
        text(s,x,749,'Roman above / native italic below; weight 400.',18,color=MUTED)
    s.line(60,784,1740,784,RULE,1)
    text(s,60,837,'03 / Letterspacing: one variable, two uppercase labels',27)
    for x,tracking,label in [(60,0,'Tracking 0'),(940,4.32,'Tracking 0.12 em')]:
        text(s,x,878,label,19,color=MUTED)
        text(s,x,945,'SEPTEMBER',36,'inter',tracking=tracking)
    text(s,60,1002,'0.12 em is a study coordinate, not a calendar preset. Pair kerning is a separate operation.',21,color=MUTED)
    s.line(60,1038,1740,1038,RULE,1)
    text(s,60,1092,'04 / Default numeral advances: measure the actual pinned file',27)
    for i,(alias,label) in enumerate([('sourcesans','Source Sans 3'),('inter','Inter'),('mono','IBM Plex Mono')]):
        x=60+580*i; m=metrics(alias); text(s,x,1135,label,21)
        cursor=x
        for char in '180':
            width=m['default_digit_advances'][char]*72/m['units_per_em']
            s.rect(cursor,1160,width,100,None,RULE,1)
            text(s,cursor,1240,char,72,alias)
            cursor+=width
        ratios=[m['default_digit_advances'][c]/m['units_per_em'] for c in '180']
        text(s,x,1302,'1 / 8 / 0: '+' / '.join(f'{v:.3f}' for v in ratios)+' em',18,color=MUTED)
        text(s,x,1340,'Default cmap; no tnum or pnum applied.',17,color=MUTED)
    text(s,60,1420,'Width is not figure height: lining / oldstyle and proportional / tabular are independent choices.',21,color=MUTED)
    text(s,60,1505,'These are research specimens. Font features require a verified shaping engine in the final product.',20,color=ACCENT)
    return s


def build(out_dir=ROOT/'studies/latin-type-atlas',cache_dir=ROOT/'tmp/latin-study-fonts'):
    source=json.loads((ROOT/'assets/fonts/latin-study/manifest.json').read_text())
    original={f['path']:f['sha256'] for a in source['assets'] for f in a['local_files']}
    for path,expected in original.items():
        if sha(ROOT/path)!=expected: raise ValueError('Retained source changed: '+path)
    cache=cache_dir/'manifest.json'
    if not cache.exists(): prepare(cache_dir)
    working=json.loads(cache.read_text())
    for f in working['fonts']:
        path=cache_dir/f['file']
        if f['source_sha256']!=original[f['source_file']] or sha(path)!=f['sha256']:
            raise ValueError('Working font changed; rebuild cache from originals.')
        ds.FONT_FILES[f['alias']]=path
    boards=[families_board(),details_board()]
    for board in boards:
        overflow=[(t,b) for t,b,_ in board.text_bounds() if b[0]<-.01 or b[1]<-.01 or b[2]>board.width+.01 or b[3]>board.height+.01]
        if overflow: raise ValueError(f'{board.key} overflow: {overflow}')
    out_dir.mkdir(parents=True,exist_ok=True)
    for board in boards: (out_dir/(board.key+'.svg')).write_text(board.svg())
    record={'source_fonts':'assets/fonts/latin-study/manifest.json','working_fonts':working,
            'existing_fonts':'assets/fonts/provenance.json',
            'family_studies':[{'alias':a,'family':f,'coordinates':c,'measurements':metrics(a)} for a,f,_,c in FAMILIES],
            'method':'Same em-size family board; separate one-variable optical-size and tracking comparisons; original generic English text.',
            'limits':'cmap/hmtx outlines and explicit tracking only. No automatic GSUB/GPOS, kerning, feature substitution, paragraph breaking or user approval.',
            'original_content':'Project-authored generic text and comparison diagrams; no private case content or third-party specimen art.',
            'implementation_sha256':sha(Path(__file__)),'preparer_sha256':sha(ROOT/'scripts/prepare_latin_study_fonts.py'),
            'svg_sha256':{p.name:sha(p) for p in sorted(out_dir.glob('*.svg'))}}
    (out_dir/'manifest.json').write_text(json.dumps(record,indent=2)+'\n')
    print('Built two English type study boards; nine candidate families, no shaping claim.')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out-dir',type=Path,default=ROOT/'studies/latin-type-atlas')
    parser.add_argument('--cache-dir',type=Path,default=ROOT/'tmp/latin-study-fonts')
    args=parser.parse_args(); build(args.out_dir,args.cache_dir)
