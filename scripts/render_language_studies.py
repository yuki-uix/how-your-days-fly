#!/usr/bin/env python3
"""Generate the second calendar study set from retained semantic/design cards.

Install requirements-design.txt, then run:
  python3 scripts/render_language_studies.py --pdf output/pdf/learned-calendar-studies.pdf
  python3 scripts/render_language_studies.py --year 2028 --out-dir tmp/learned-2028

This is a study renderer, not a general AI design engine. J2/J3 are a controlled
mapping pair; J1/J4/J5/J6 explore whole art directions and should not be ranked
as if only one variable changed. The chosen art plate is retained, not rerolled.
"""
from __future__ import annotations

import argparse
import calendar
from datetime import date,timedelta
import hashlib
import importlib.util
import json
import math
from pathlib import Path

from design_scene import Scene,ROOT,FONT_FILES,register_pdf_fonts,font_info

spec=importlib.util.spec_from_file_location('calendar_data',ROOT/'.agents/skills/calendar-design-lab/scripts/calendar_data.py')
dates=importlib.util.module_from_spec(spec); spec.loader.exec_module(dates)
IMAGE=ROOT/'assets/images/paper-light/paper-light-j4-v1.png'
FONT_PROVENANCE=ROOT/'assets/fonts/provenance.json'
RING_STYLE={'paper':'#17342E','ink':'#E9EDCF','muted':'#9EAEA1','quiet':'#70877B','accent':'#D8E598','cx':500,'cy':730,'tick_inner':322,'tick_outer':352,'arc_radius':374,'label_radius':414,'start_degrees':-90,'direction':'clockwise','display_font':'display','lookup_font':'mono','day_label_size':12}
STUDY_CAPTIONS=['The long view','Equal day steps','Equal month sectors','Paper and light','A week with room','One day, one page']


def card(task,view,start,end,mapping,layout,roles,whitespace,source_rules,hypothesis,**extra):
    return {'reading_task':task,'display_extent':{'view':view,'start':start.isoformat(),'end':end.isoformat()},'temporal_unit':'civil-date','temporal_mapping':mapping,'spatial_layout':layout,'typographic_roles':roles,'whitespace_role':whitespace,'source_rules':source_rules,'hypothesis':hypothesis,'user_preference_status':'unconfirmed','study_language':'en',**extra}


def colophon(s,label,ink,rule):
    y=s.height-65
    s.line(65,y-24,s.width-65,y-24,rule,.8)
    s.text(65,y,f'{s.key} / {label}',11,'mono',ink)
    s.text(s.width-65,y,'HOW YOUR DAYS FLY',11,'mono',ink,'end')


def panorama(year):
    paper,ink,muted,accent,rule='#F1EFE8','#262923','#666E63','#A64532','#D6D7CB'
    start=date(year,1,1); end=date(year,12,31)
    c=card('Locate a civil date within a continuous annual span','year',start,end,'equal-civil-day-units','53-or-54 continuous week columns x seven weekday rows',{'year':'display','lookup_dates':'mono','month_index':'sans-medium'},'Separate the annual overview from its date index',['temporal:continuous-order','type:display-versus-lookup','type:shared-anchors'],'A horizontal span may communicate continuity while month markers preserve lookup.',comparison_kind='whole-direction')
    s=Scene('J1','The long view',1400,1000,paper,c)
    s.text(60,202,str(year),216,'display',ink,role='display')
    s.text(1335,107,'THE LONG VIEW',17,'mono-medium',ink,'end')
    s.text(1335,145,'January to December',28,'display-italic',ink,'end')
    s.line(65,251,1335,251,ink,1.1)
    first=start-timedelta(days=start.weekday()); last=end+timedelta(days=6-end.weekday())
    count=((last-first).days+1)//7
    x0,y0,grid_w,row_h=120,386,1215,61
    col_w=grid_w/count
    s.card['spatial_layout']=f'{count} continuous week columns x seven weekday rows'
    s.card['style']={'paper':paper,'ink':ink,'accent':accent,'lookup_font':'mono','display_font':'display'}
    for wd,name in enumerate(['Mo','Tu','We','Th','Fr','Sa','Su']):
        s.text(65,y0+wd*row_h+6,name,14,'mono',muted,role='index')
    for i in range(count):
        x=x0+i*col_w
        s.line(x,y0-25,x,y0+6*row_h+25,rule,.55)
        for wd in range(7):
            value=first+timedelta(days=i*7+wd); px=x+col_w/2; py=y0+wd*row_h+6
            if value.year!=year:
                s.text(px,py,str(value.day),12,'mono','#A9AFA3','middle',role='context')
                continue
            if value.day==1:
                s.rect(x+1,y0+wd*row_h-17,col_w-2,32,accent)
                s.text(px,y0-58,calendar.month_abbr[value.month].upper(),12,'sans-medium',ink,'middle',role='index')
                s.line(px,y0-46,px,y0-29,accent,1)
            with s.day(value,column=i,row=wd):
                s.text(px,py,f'{value.day:02d}',14,'mono',paper if value.day==1 else (accent if wd>=5 else ink),'middle',role='lookup')
    s.text(65,864,'One position for each civil date.',25,'display-italic',ink)
    s.text(1335,862,f'{len(dates.calendar_data("year",start)["days"])} DAYS / {count} DISPLAY WEEKS',12,'mono',muted,'end')
    colophon(s,'CONTINUOUS YEAR',muted,rule)
    return s


def point(cx,cy,r,angle):
    rad=math.radians(angle)
    return cx+r*math.cos(rad),cy+r*math.sin(rad)


def arc(s,cx,cy,r,a,b,color,width):
    n=max(2,math.ceil(abs(b-a)*1.2)); pts=[point(cx,cy,r,a+(b-a)*i/n) for i in range(n+1)]
    s.path([('M',*pts[0])]+[('L',*p) for p in pts[1:]],stroke=color,width=width)


def ring_angle(value,mapping):
    year_start=date(value.year,1,1)
    if mapping=='equal-civil-day':
        n=366 if calendar.isleap(value.year) else 365
        return -90+(value-year_start).days*360/n
    if mapping=='equal-month':
        return -90+(value.month-1)*30+(value.day-1)/calendar.monthrange(value.year,value.month)[1]*30
    raise ValueError('Unknown ring mapping')


def ring(year,mapping):
    key='J2' if mapping=='equal-civil-day' else 'J3'
    style=dict(RING_STYLE); start,end=date(year,1,1),date(year,12,31)
    c=card('Read the annual cycle and compare the weight assigned to days and months','year',start,end,mapping,'one clockwise radial year',{'year':'display','month_index':'mono-medium','selected_day_labels':'mono'},'Keep the central year distinct from the date ring',['temporal:declared-normalization','type:nested-hierarchy'],'Equal-day and equal-month views may support different senses of annual rhythm.',comparison_kind='controlled',changed_variable='temporal_mapping',control_group='annual-ring',style=style)
    s=Scene(key,'A year in the round',1000,1400,style['paper'],c)
    ink,muted=style['ink'],style['muted']; cx,cy=style['cx'],style['cy']
    s.text(65,102,'A year',76,'display',ink,role='display')
    s.text(65,176,'in the round.',76,'display-italic',ink,role='display')
    s.text(935,98,str(year),18,'mono',ink,'end',role='index')
    s.text(935,132,'A CONTROLLED PAIR',11,'mono',muted,'end')
    total=366 if calendar.isleap(year) else 365
    values=[start+timedelta(days=i) for i in range(total)]
    for value in values:
        a=ring_angle(value,mapping)
        inner=306 if value.day==1 else style['tick_inner']
        with s.day(value,angle_degrees=a):
            s.line(*point(cx,cy,inner,a),*point(cx,cy,style['tick_outer'],a),ink if value.weekday()<5 else style['quiet'],1.4 if value.day==1 else .8)
        if value.day in [1,8,15,22]:
            px,py=point(cx,cy,286,a)
            s.text(px,py+3,f'{value.day:02d}',style['day_label_size'],'mono',muted,'middle',role='lookup')
    for month in range(1,13):
        first=date(year,month,1)
        a=ring_angle(first,mapping)
        next_first=date(year+1,1,1) if month==12 else date(year,month+1,1)
        b=270 if month==12 else ring_angle(next_first,mapping)
        arc(s,cx,cy,style['arc_radius'],a+.55,b-.55,ink if month%2 else style['accent'],3)
        px,py=point(cx,cy,style['label_radius'],(a+b)/2)
        s.text(px,py+4,calendar.month_abbr[month].upper(),13,'mono-medium',ink,'middle',role='index')
    s.text(cx,cy+27,str(year),152,'display',ink,'middle',role='display')
    s.text(cx,cy+66,f'{total} CIVIL DATES',12,'mono',muted,'middle')
    s.text(65,1227,'Equal day steps' if mapping=='equal-civil-day' else 'Equal month sectors',38,'display-italic',ink)
    s.text(65,1260,'Every civil date receives the same angle.' if mapping=='equal-civil-day' else 'Each month receives 1/12 of the circle; day spacing varies.',14,'sans',muted)
    colophon(s,'ANNUAL CYCLE',muted,style['quiet'])
    return s


def image_month(year):
    paper,ink,muted,blue,rule='#F9F7F0','#222B32','#687078','#224DB1','#D9DBD2'
    start,end=date(year,4,1),date(year,4,30)
    c=card('Encounter a monthly image while retaining a complete date index','month',start,end,'chronological days segmented into weeks','shared-edge image plus month grid',{'month':'display','lookup_dates':'sans-medium','weekdays':'mono'},'Separate material image, month identity and date lookup',['type:image-date-anchors','type:display-versus-lookup'],'An image-led page may feel like a changing domestic print while remaining useful.',comparison_kind='whole-direction',image_asset=str(IMAGE.relative_to(ROOT)))
    s=Scene('J4','April / paper and light',1000,1400,paper,c)
    s.text(65,167,'April',153,'display',ink,role='display')
    s.text(935,84,str(year),21,'mono',ink,'end',role='index')
    s.text(935,126,'04 / 12',12,'mono',muted,'end')
    s.image(IMAGE,65,211,870,580)
    s.line(65,838,935,838,ink,.8)
    width=870; step=width/7
    for wd,name in enumerate(['MON','TUE','WED','THU','FRI','SAT','SUN']):
        s.text(65+(wd+.5)*step,875,name,12,'mono',muted,'middle',role='index')
    weeks=dates.month_record(year,4,'monday')['weeks']
    for row,week in enumerate(weeks):
        for wd,cell in enumerate(week):
            if not cell['in_month']: continue
            value=date.fromisoformat(cell['date'])
            with s.day(value,row=row,column=wd):
                s.text(65+(wd+.5)*step,937+row*64,f'{value.day:02d}',32,'sans-medium',blue if wd>=5 else ink,'middle',role='lookup')
    s.text(65,1291,'Paper / light / April',22,'display-italic',muted)
    s.text(935,1287,'MONDAY FIRST',11,'mono',muted,'end')
    colophon(s,'IMAGE-LED MONTH',muted,rule)
    return s


def writing_week(year):
    anchor=date(year,4,8); start=anchor-timedelta(days=anchor.weekday()); end=start+timedelta(days=6)
    paper,ink,muted,rule='#F2F0E7','#31392F','#78806D','#CED2C3'
    c=card('Write in seven equal daily areas while keeping the week visible','week',start,end,'chronological seven-day sequence','seven equally sized columns',{'week_title':'display','day_numbers':'display','weekday_index':'sans-medium'},'Writing area is the main content',['type:purposeful-whitespace','type:series-invariants'],'Consistent baselines and equal day areas may make a weekly page more inviting to use.',comparison_kind='whole-direction',daily_writing_width=180)
    s=Scene('J5','A week with room',1400,1000,paper,c)
    s.text(65,87,str(year),18,'mono',muted)
    s.text(65,216,f'Week {start.isocalendar().week:02d}',131,'display',ink,role='display')
    s.text(1335,116,f'{start.day:02d} - {end.day:02d} APRIL',23,'mono',ink,'end',role='index')
    s.text(1335,158,'SEVEN DAYS / EQUAL ROOM',11,'mono',muted,'end')
    s.line(65,263,1335,263,ink,1)
    col_w=180; x0=70
    for wd in range(7):
        value=start+timedelta(days=wd); x=x0+wd*col_w
        if wd: s.line(x,299,x,827,rule,.85)
        s.text(x+13,319,calendar.day_abbr[value.weekday()].upper(),13,'sans-medium',muted,role='index')
        with s.day(value,column=wd,writing_width=col_w):
            s.text(x+13,410,f'{value.day:02d}',82,'display',ink,role='lookup')
        for y in [485,588,691,794]: s.line(x+13,y,x+col_w-14,y,rule,.7)
    s.text(65,885,'Notes',26,'display-italic',ink)
    s.line(150,882,1335,882,rule,.8)
    colophon(s,'WRITING-LED WEEK',muted,rule)
    return s


def daily_page(year):
    value=date(year,4,18); before=value-timedelta(days=1); after=value+timedelta(days=1)
    paper,ink,muted,rule='#E9B9A2','#6B3028','#935B4A','#C38D78'
    total=366 if calendar.isleap(year) else 365
    c=card('Give one civil date a clear identity and a page-turning presence','day',value,value,'one civil date per page','single page with expressive date and stable context',{'day':'display-italic proportional figures','weekday_month_year':'sans/mono'},'Give the numeral silhouette space while preserving contextual anchors',['type:expressive-display-numerals','type:series-invariants'],'A date can carry visual identity through its letterform and scale.',comparison_kind='whole-direction',series_invariants=['month/year anchors','weekday anchor','adjacent-date rail'])
    s=Scene('J6','One day / 18 April',1000,1400,paper,c)
    s.text(65,91,'A DAY',12,'mono',ink)
    s.text(935,91,str(year),22,'mono',ink,'end',role='index')
    s.text(65,239,'APRIL',94,'display',ink,role='index')
    s.text(65,292,calendar.day_name[value.weekday()].upper(),20,'mono',ink,role='index')
    with s.day(value): s.text(483,1102,f'{value.day:02d}',940,'display-italic',ink,'middle',role='display')
    s.text(65,1215,f'{(value-date(year,1,1)).days+1:03d} / {total}',13,'mono',ink)
    s.text(935,1215,value.isoformat(),15,'mono',ink,'end')
    s.line(65,1253,935,1253,rule,1)
    s.text(65,1292,f'{before.day:02d} {calendar.day_abbr[before.weekday()].upper()}',13,'mono',muted)
    s.text(935,1292,f'{after.day:02d} {calendar.day_abbr[after.weekday()].upper()}',13,'mono',muted,'end')
    colophon(s,'DATE-LED DAILY PAGE',muted,rule)
    return s


def build_studies(year):
    if not 2<=year<=9998: raise ValueError('year must be between 2 and 9998')
    return [panorama(year),ring(year,'equal-civil-day'),ring(year,'equal-month'),image_month(year),writing_week(year),daily_page(year)]


def overview(studies):
    year=date.fromisoformat(studies[0].card['display_extent']['start']).year
    out=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1800 1510" role="img" aria-label="Six new calendar studies">','<rect width="1800" height="1510" fill="#E8E6E0"/>']
    # Cover uses the same pinned outline pipeline as the studies.
    cover=Scene('cover','Learned calendar studies',1800,1510,'#E8E6E0',{})
    cover.text(55,85,f'Calendar studies / {year}',62,'display','#303731')
    cover.text(55,124,'TIME / TYPE / IMAGE / SPACE',14,'mono','#667064')
    cover_svg=cover.svg(); inside=cover_svg[cover_svg.index('>')+1:cover_svg.rfind('</svg>')]
    out.append(inside)
    for i,(s,label) in enumerate(zip(studies,STUDY_CAPTIONS)):
        row,col=divmod(i,3); bx,by=55+col*582,180+row*635
        max_w,max_h=525,540; scale=min(max_w/s.width,max_h/s.height)
        x=bx+(max_w-s.width*scale)/2; y=by+(max_h-s.height*scale)/2
        source=s.svg().replace('<svg ',f'<svg x="{x:.3f}" y="{y:.3f}" width="{s.width*scale:.3f}" height="{s.height*scale:.3f}" ',1)
        out.append(source)
        caption=Scene(f'caption-{s.key}','Caption',1800,1510,'#E8E6E0',{})
        caption.ops=[]; caption.text(bx,by+575,f'{s.key} / {label}',18,'sans-medium','#303731')
        raw=caption.svg(); out.append(raw[raw.index('>')+1:raw.rfind('</svg>')])
    return '\n'.join(out+['</svg>'])+'\n'


def export_pdf(studies,path):
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import mm
    year=date.fromisoformat(studies[0].card['display_extent']['start']).year
    register_pdf_fonts(); path.parent.mkdir(parents=True,exist_ok=True)
    c=canvas.Canvas(str(path),pagesize=(420*mm,297*mm),invariant=1,pageCompression=1)
    c.setTitle('Calendar studies / time, type, image and space'); c.setAuthor('How Your Days Fly')
    cover=Scene('book-cover','Calendar studies',1800,1273,'#E8E6E0',{})
    cover.text(62,97,f'Calendar studies / {year}',68,'display','#303731')
    cover.text(62,139,'SIX ORIGINAL STUDIES AFTER SOURCE READING',16,'mono','#667064')
    factor=420*mm/1800
    c.saveState(); c.scale(factor,factor); cover.pdf(c); c.restoreState()
    for i,s in enumerate(studies):
        row,col=divmod(i,3); bx,by=62+col*580,180+row*528
        scale=min(510/s.width,445/s.height)
        x=bx+(510-s.width*scale)/2; y=by+(445-s.height*scale)/2
        c.saveState(); c.scale(factor,factor); c.translate(x,1273-y-s.height*scale); c.scale(scale,scale); s.pdf(c); c.restoreState()
        label=Scene(f'caption{s.key}','Caption',1800,1273,'#E8E6E0',{})
        label.ops=[]; label.text(bx,by+477,f'{s.key} / {STUDY_CAPTIONS[i]}',18,'sans-medium','#303731')
        c.saveState(); c.scale(factor,factor); label.pdf(c); c.restoreState()
    c.showPage()
    for s in studies:
        w,h=(420*mm,297*mm) if s.width>s.height else (297*mm,420*mm)
        c.setPageSize((w,h)); scale=min(w/s.width,h/s.height)
        c.saveState(); c.translate((w-s.width*scale)/2,(h-s.height*scale)/2); c.scale(scale,scale); s.pdf(c); c.restoreState(); c.showPage()
    # Human-readable proof notes connect principles and actual study operations.
    notes=Scene('notes','Reading notes',1000,1400,'#F4F1E8',{})
    notes.text(65,132,'From sources',87,'display','#26342B')
    notes.text(65,219,'to design decisions.',87,'display-italic','#26342B')
    entries=[('J1','Continuity with an index','A full date sequence remains visible across month boundaries.'),('J2 / J3','One changed mapping','Equal civil-day steps and normalized months preserve different relations.'),('J4','Image and date roles','One retained art plate; a complete month grid with shared edges.'),('J5','Whitespace for a task','Seven equal daily writing areas and recurring baselines.'),('J6','Lookup and display type','Proportional display numerals retain a separate date context.')]
    for i,(key,title,body) in enumerate(entries):
        y=330+i*161; notes.line(65,y-26,935,y-26,'#C7CCBF',.8)
        notes.text(65,y,key,13,'mono','#657460'); notes.text(65,y+49,title,36,'display','#26342B'); notes.text(65,y+85,body,17,'sans','#657460')
    notes.text(65,1216,'Sources read: TimeViz chapters3-4; Timelines Revisited;',15,'mono','#657460')
    notes.text(65,1242,'The Vignelli Canon; Datawrapper; Google Design; ggtime.',15,'mono','#657460')
    notes.text(65,1305,'These are design hypotheses; personal preference awaits user review.',17,'display-italic','#26342B')
    c.setPageSize((297*mm,420*mm)); scale=min(297*mm/1000,420*mm/1400)
    c.saveState(); c.scale(scale,scale); notes.pdf(c); c.restoreState(); c.showPage(); c.save()


def export(studies,target,year):
    font_records,asset_record=verify_assets()
    target.mkdir(parents=True,exist_ok=True); records=[]
    for s in studies:
        outside=[(text,box) for text,box,_ in s.text_bounds() if box[0]<-.01 or box[1]<-.01 or box[2]>s.width+.01 or box[3]>s.height+.01]
        if outside: raise ValueError(f'{s.key} has text outside scene: {outside}')
        filename=f'{s.key.lower()}.svg'; source=s.svg(); (target/filename).write_text(source,encoding='utf-8')
        records.append({'id':s.key,'title':s.title,'source':filename,'sha256':hashlib.sha256(source.encode()).hexdigest(),'dimensions':{'width':s.width,'height':s.height},'design_card':s.card,'represented_dates':s.dates,'user_review':'pending'})
    (target/'overview.svg').write_text(overview(studies),encoding='utf-8')
    implementation={'entrypoint':'scripts/render_language_studies.py','entrypoint_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scene_renderer':'scripts/design_scene.py','scene_renderer_sha256':hashlib.sha256((ROOT/'scripts/design_scene.py').read_bytes()).hexdigest(),'requirements':'requirements-design.txt','requirements_sha256':hashlib.sha256((ROOT/'requirements-design.txt').read_bytes()).hexdigest()}
    manifest={'recipe_version':2,'year':year,'implementation':implementation,'fonts':font_records,'image_asset':asset_record,'replay_scope':'Pinned fonts and retained art; SVG uses outlines and embeds the chosen image. Editable text and layout remain in source.','studies':records,'evidence':{'source_reading':['.agents/skills/calendar-design-lab/references/temporal-semantics.md','.agents/skills/calendar-design-lab/references/typographic-composition.md'],'personal_preference':'not-established','cross_user_validation':'not-run'}}
    (target/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def verify_assets():
    font_records=json.loads(FONT_PROVENANCE.read_text())
    for entry in font_records['files']:
        if hashlib.sha256((ROOT/entry['path']).read_bytes()).hexdigest()!=entry['sha256']:
            raise ValueError(f'Font asset changed; revise provenance and recipe before replay: {entry["path"]}')
    asset_record=json.loads((IMAGE.parent/'provenance.json').read_text())
    if hashlib.sha256(IMAGE.read_bytes()).hexdigest()!=asset_record['sha256']:
        raise ValueError('Selected image changed; revise provenance and recipe before replay')
    return font_records,asset_record


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--year',type=int,default=2027)
    parser.add_argument('--out-dir',type=Path,default=ROOT/'studies/learned-language')
    parser.add_argument('--pdf',type=Path)
    args=parser.parse_args(argv)
    try: studies=build_studies(args.year); export(studies,args.out_dir,args.year)
    except ValueError as exc: parser.error(str(exc))
    if args.pdf: export_pdf(studies,args.pdf)
    print(f'Wrote {len(studies)} studies and retained design cards to {args.out_dir}')
    if args.pdf: print(f'PDF: {args.pdf}')


if __name__=='__main__': main()
