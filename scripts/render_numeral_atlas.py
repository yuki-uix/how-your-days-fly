#!/usr/bin/env python3
"""Original calendar-numeral specimens, real feature switches and task studies."""
from datetime import date
from pathlib import Path
import argparse,hashlib,importlib.util,json
import uharfbuzz as hb
import design_scene as ds
from glyph_study import GlyphStudy,shape,glyph
from prepare_numeral_study_fonts import prepare

ROOT=Path(__file__).resolve().parents[1]
PROFILES=ROOT/'assets/fonts/numeral-study/profiles.json'
PAPER='#F4F1E9'; INK='#21323A'; MUTED='#657176'; RULE='#D0D2CB'; WHITE='#FFFEFA'
LABEL='num-source-sans'
spec=importlib.util.spec_from_file_location('numeral_dates',ROOT/'.agents/skills/calendar-design-lab/scripts/calendar_data.py')
dates=importlib.util.module_from_spec(spec); spec.loader.exec_module(dates)
FORMS=[('Lining / proportional',{'lnum':True,'onum':False,'pnum':True,'tnum':False,'kern':False}),
       ('Lining / tabular',{'lnum':True,'onum':False,'pnum':False,'tnum':True,'kern':False}),
       ('Oldstyle / proportional',{'lnum':False,'onum':True,'pnum':True,'tnum':False,'kern':False}),
       ('Oldstyle / tabular',{'lnum':False,'onum':True,'pnum':False,'tnum':True,'kern':False})]


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def text(s,x,y,value,size=20,font=LABEL,color=INK,align='start',features=None,role='label'):
    s.text(x,y,value,size,font,color,align,features=features,role=role)


def box(alias,value,size=1,features=None):
    s=GlyphStudy('measure','measure',1800,1000,PAPER,{})
    text(s,0,0,value,size,alias,features=features)
    return s.text_bounds()[0][1]


def measure(alias,features=None):
    requested={'kern':True,'liga':True}; requested.update(features or {})
    digits={}; gids={}; bounds={}
    for c in '0123456789':
        run,units=shape(alias,c,tuple(sorted(requested.items())))
        digits[c]=sum(g[2] for g in run); gids[c]=[g[0] for g in run]
        bounds[c]=box(alias,c,1,features)
    return {'features_requested':requested,'individual_digit_advances':digits,'glyph_ids':gids,'ink_bounds_em':bounds,
            'units_per_em':units,'default_or_requested_digits_tabular':len(set(digits.values()))==1}


def family_board(profiles):
    s=GlyphStudy('numeral-families','Calendar numerals: sixteen starting points',1800,1840,PAPER,{})
    text(s,60,76,'Calendar numerals / sixteen starting points',44)
    text(s,60,121,'Large 28: same ink height (70 units). Other samples: same em size. Descriptions are candidates, not rankings.',20,color=MUTED)
    measures=[]
    for i,p in enumerate(profiles):
        row,col=divmod(i,4); x=60+427*col; y=180+400*row
        s.rect(x,y,399,378,WHITE)
        text(s,x+22,y+37,p['family'],23)
        text(s,x+22,y+66,p['visual_dimension'],16,color=MUTED)
        b=box(p['alias'],'28'); size=70/(b[3]-b[1])
        text(s,x+22,y+181-b[3]*size,'28',size,p['alias'],role='numeral-specimen')
        m=measure(p['alias']); flag='tabular' if m['default_or_requested_digits_tabular'] else 'proportional'
        text(s,x+208,y+119,'Latn/en digits',16,color=MUTED)
        text(s,x+208,y+148,flag,18)
        text(s,x+22,y+237,'0123456789',27,p['alias'],role='numeral-specimen')
        text(s,x+22,y+287,'01 08 11 28 31',24,p['alias'],role='numeral-specimen')
        s.line(x+22,y+314,x+377,y+314,RULE,.8)
        text(s,x+22,y+345,p['coordinate_label'],15,color=MUTED)
        measures.append({'font_id':p['font_id'],'alias':p['alias'],'measurements':m,'matched_28_size':size,'matched_28_ink_height':70})
    text(s,60,1812,'Western digits 0-9 only. Actual files, licenses, axes and measured alternatives are retained; no private calendar art.',20,color=MUTED)
    return s,measures


def feature_board():
    s=GlyphStudy('numeral-features','One family: independent numeral width and height choices',1800,1320,PAPER,{})
    text(s,60,76,'One family / four numeral forms',44)
    text(s,60,121,'Source Serif 4, weight 400, opsz 20. Same em size; actual OpenType substitutions and advances.',22,color=MUTED)
    measurements=[]
    for i,(label,features) in enumerate(FORMS):
        row,col=divmod(i,2); x=60+880*col; y=180+360*row
        s.rect(x,y,800,310,WHITE)
        text(s,x+25,y+45,label,27)
        s.line(x+25,y+147,x+770,y+147,RULE,.8)
        text(s,x+25,y+147,'0123456789',72,'num-source-serif',features=features,role='numeral-form')
        text(s,x+25,y+227,'01 08 11 28 31',34,'num-source-serif',features=features,role='numeral-form')
        text(s,x+510,y+218,'111111',32,'num-source-serif',features=features,role='width-test')
        text(s,x+510,y+267,'888888',32,'num-source-serif',features=features,role='width-test')
        s.line(x+505,y+186,x+505,y+273,RULE,.8)
        m=measure('num-source-serif',features); measurements.append({'label':label,**m})
        text(s,x+25,y+279,'tnum' if features['tnum'] else 'pnum',17,color=MUTED)
    text(s,60,946,'Leading zero / a separate content choice',31)
    text(s,60,1027,'1   7   10   28   31',52,'num-source-serif',features=FORMS[1][1],role='date-content')
    text(s,940,1027,'01   07   10   28   31',52,'num-source-serif',features=FORMS[1][1],role='date-content')
    text(s,60,1081,'Same font and numeral features; the strings differ.',22,color=MUTED)
    text(s,60,1181,'A font family can supply several numeral styles. Choosing date typography need not add another family.',24)
    text(s,60,1252,'These are shaped SVG proofs, not a claim that the older shared renderer or a future browser already applies these features.',20,color=MUTED)
    return s,measurements


def contexts():
    s=GlyphStudy('numeral-contexts','Calendar numeral roles across time scales',1800,1390,PAPER,{})
    text(s,60,76,'Year / month / week / day',44)
    text(s,60,121,'Four task studies with different typography proposals. Exact Gregorian dates; physical-size reading tests remain open.',21,color=MUTED)
    for x,y in [(60,180),(930,180),(60,770),(930,770)]: s.rect(x,y,810,530,WHITE)
    records=[]
    text(s,90,230,'Year / a quarter fragment',29)
    text(s,90,271,'Barlow Condensed / small numerals',18,color=MUTED)
    year_model=dates.calendar_data('year',date(2028,1,1)); represented=[]
    for m,month in enumerate(year_model['months'][:3]):
        left=90+m*252; text(s,left,324,['JAN','FEB','MAR'][m],20)
        for i,day in enumerate(['M','T','W','T','F','S','S']): text(s,left+i*32+14,360,day,12,color=MUTED,align='middle')
        for row,week in enumerate(month['weeks']):
            for col,d in enumerate(week):
                if d['in_month']:
                    value=date.fromisoformat(d['date']); represented.append(d['date'])
                    with s.day(value,study='quarter',month=m+1,row=row,column=col): text(s,left+col*32+14,397+row*40,str(d['day']),24,'num-barlow',align='middle',role='date')
    records.append({'id':'quarter','represented_dates':represented})
    text(s,960,230,'Month / February 2028',29)
    text(s,960,271,'Zilla Slab / calendar grid',18,color=MUTED)
    model=dates.calendar_data('month',date(2028,2,1)); represented=[]
    for i,label in enumerate(['Mon','Tue','Wed','Thu','Fri','Sat','Sun']): text(s,1035+i*100,324,label,17,color=MUTED,align='middle')
    for row,week in enumerate(model['months'][0]['weeks']):
        for col,d in enumerate(week):
            if d['in_month']:
                value=date.fromisoformat(d['date']); represented.append(d['date'])
                with s.day(value,study='month',row=row,column=col): text(s,1035+col*100,390+row*65,str(d['day']),40,'num-slab',align='middle',role='date')
    records.append({'id':'month','represented_dates':represented})
    text(s,90,825,'Week / a cross-month span',29)
    text(s,90,868,'Fraunces / expressive seven-day rhythm',18,color=MUTED)
    model=dates.calendar_data('week',date(2028,2,28)); represented=[]
    text(s,90,918,'2028 / 02.28 - 03.05',20,color=MUTED)
    for i,d in enumerate(model['days']):
        value=date.fromisoformat(d['date']); represented.append(d['date']); x=153+i*104
        text(s,x,984,['Mon','Tue','Wed','Thu','Fri','Sat','Sun'][i],16,color=MUTED,align='middle')
        with s.day(value,study='week',column=i): text(s,x,1085,f'{d["day"]:02}',66,'num-fraunces',align='middle',role='date')
    text(s,90,1211,'Wide cells allow proportional figures; compare the actual page.',19,color=MUTED)
    records.append({'id':'week','represented_dates':represented})
    text(s,960,825,'Day / February 29',29)
    text(s,960,868,'DSEG7 Classic / display digits only',18,color=MUTED)
    model=dates.calendar_data('day',date(2028,2,29)); d=model['days'][0]
    with s.day(date(2028,2,29),study='day'): text(s,960,1137,'29',220,'num-dseg',role='date')
    text(s,1370,1043,'Tuesday',29)
    text(s,1370,1097,d['date'],23)
    text(s,960,1211,'Supporting words use Source Sans 3, not the segment face.',19,color=MUTED)
    records.append({'id':'day','represented_dates':[d['date']]})
    text(s,60,1350,'Content, numeral features and placement are independent choices; these studies are not approved calendar templates.',21,color=MUTED)
    return s,records


def build(out_dir=ROOT/'studies/numeral-atlas',cache_dir=ROOT/'tmp/numeral-study-fonts'):
    profiles=json.loads(PROFILES.read_text())['profiles']; cache=cache_dir/'manifest.json'
    if not cache.exists(): prepare(cache_dir)
    working=json.loads(cache.read_text())
    if working['profiles_sha256']!=sha(PROFILES): raise ValueError('Study profiles changed; rebuild working-font cache.')
    for f in working['fonts']:
        p=cache_dir/f['file']
        if sha(p)!=f['sha256'] or sha(ROOT/f['source_file'])!=f['source_sha256']: raise ValueError('Working/source font changed')
        ds.FONT_FILES[f['alias']]=p
    atlas,measures=family_board(profiles); features,forms=feature_board(); tasks,task_dates=contexts()
    boards=[atlas,features,tasks]
    for s in boards:
        outside=[(v,b) for v,b,_ in s.text_bounds() if b[0]<-.01 or b[1]<-.01 or b[2]>s.width+.01 or b[3]>s.height+.01]
        if outside: raise ValueError(f'{s.key} overflow: {outside}')
    out_dir.mkdir(parents=True,exist_ok=True)
    for s in boards: (out_dir/(s.key+'.svg')).write_text(s.svg())
    record={'profiles':'assets/fonts/numeral-study/profiles.json','working_fonts':working,'family_measurements':measures,'four_forms':forms,
            'calendar_contexts':task_dates,'glyph_shaping':{'uharfbuzz':hb.__version__,'harfbuzz':hb.version_string(),'language':'en','script':'Latn','direction':'ltr'},
            'original_content':'Project-authored generic numeral samples and exact public dates; no real user calendar, illustration or feedback imported.',
            'scope':'Separate SVG study path with actual requested features. No paragraph layout or PDF export; design_scene remains unchanged.',
            'implementation_sha256':sha(Path(__file__)),'glyph_study_sha256':sha(ROOT/'scripts/glyph_study.py'),'preparer_sha256':sha(ROOT/'scripts/prepare_numeral_study_fonts.py'),
            'svg_sha256':{p.name:sha(p) for p in sorted(out_dir.glob('*.svg'))}}
    (out_dir/'manifest.json').write_text(json.dumps(record,indent=2)+'\n')
    print('Built 16 numeral candidates, actual four-form feature proof and four calendar task contexts.')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--out-dir',type=Path,default=ROOT/'studies/numeral-atlas'); p.add_argument('--cache-dir',type=Path,default=ROOT/'tmp/numeral-study-fonts')
    a=p.parse_args(); build(a.out_dir,a.cache_dir)
