#!/usr/bin/env python3
"""Render eight original, editable calendar studies (stdlib SVG; optional PDF).

Examples:
    python3 scripts/render_pattern_atlas.py
    python3 scripts/render_pattern_atlas.py --year 2028 --out-dir tmp/leap-studies
    python3 scripts/render_pattern_atlas.py --pdf output/pdf/calendar-pattern-atlas.pdf

PDF export additionally requires reportlab. The SVGs contain no third-party art,
embedded fonts, external assets, holiday data, or inferred personal preferences.
"""

from __future__ import annotations

import argparse
import calendar
from contextlib import contextmanager
from datetime import date, timedelta
import hashlib
from html import escape
import importlib.util
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CALENDAR_TOOL = ROOT / '.agents/skills/calendar-design-lab/scripts/calendar_data.py'
spec = importlib.util.spec_from_file_location('calendar_data', CALENDAR_TOOL)
dates = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dates)

WIDTH, HEIGHT = 800, 1100
INK, SECONDARY, RULE, PAPER = '#17191C', '#626970', '#D7DADD', '#FFFFFF'
BLUE, PALE = '#2157EA', '#F0F2F4'
MONTHS = list(calendar.month_name)
SHORT = list(calendar.month_abbr)
FONT_FAMILY = {
    'Helvetica': 'Arial, Helvetica, sans-serif',
    'Helvetica-Bold': 'Arial, Helvetica, sans-serif',
    'Times-Roman': 'Times New Roman, Times, serif',
    'Times-Italic': 'Times New Roman, Times, serif',
    'Courier': 'Courier New, Courier, monospace',
}
STUDY_AXES = {
    'A': {'time_structure':'month-matrix','scale':'year','content_role':'date-led','medium':'single-year-poster'},
    'B': {'time_structure':'continuous-weeks','scale':'year','content_role':'date-led','medium':'single-year-poster'},
    'C': {'time_structure':'month-strips','scale':'year','content_role':'date-led','medium':'single-year-poster'},
    'D': {'time_structure':'radial-cycle','scale':'year','content_role':'date-led','medium':'single-year-poster'},
    'E': {'time_structure':'equal-day-field','scale':'year','content_role':'day-count-led','medium':'single-year-poster'},
    'F': {'time_structure':'month-matrix','scale':'month','content_role':'image-led','medium':'monthly-sheet'},
    'G': {'time_structure':'agenda-matrix','scale':'week','content_role':'writing-led','medium':'weekly-sheet'},
    'H': {'time_structure':'serial-units','scale':'day','content_role':'date-led','medium':'single-page-of-daily-sequence'},
}


class Drawing:
    def __init__(self, key, title, subtitle):
        self.key, self.title, self.subtitle = key, title, subtitle
        self.ops = []
        self.marked_dates = []
        self.rect(0, 0, WIDTH, HEIGHT, PAPER)

    def text(self, x, y, value, size=12, font='Helvetica', color=INK, align='start', rotate=0):
        self.ops.append(('text', dict(x=x, y=y, value=str(value), size=size, font=font, color=color, align=align, rotate=rotate)))

    def line(self, x1, y1, x2, y2, color=RULE, width=1):
        self.ops.append(('line', dict(x1=x1, y1=y1, x2=x2, y2=y2, color=color, width=width)))

    def rect(self, x, y, w, h, fill=None, stroke=None, width=1):
        self.ops.append(('rect', dict(x=x, y=y, w=w, h=h, fill=fill, stroke=stroke, width=width)))

    def circle(self, cx, cy, r, fill=None, stroke=None, width=1):
        self.ops.append(('circle', dict(cx=cx, cy=cy, r=r, fill=fill, stroke=stroke, width=width)))

    def path(self, points, fill=None, stroke=None, width=1):
        self.ops.append(('path', dict(points=points, fill=fill, stroke=stroke, width=width)))

    @contextmanager
    def day(self, value):
        self.marked_dates.append(value.isoformat())
        self.ops.append(('day-start', value.isoformat()))
        yield
        self.ops.append(('group-end', None))

    @contextmanager
    def circle_clip(self, cx, cy, r):
        self.ops.append(('clip-start', dict(cx=cx, cy=cy, r=r)))
        yield
        self.ops.append(('clip-end', None))

    def svg(self):
        output = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title desc">',
                  f'<title id="title">{escape(self.title)}</title>', f'<desc id="desc">{escape(self.subtitle)}</desc>']
        clip = 0
        for kind, p in self.ops:
            if kind == 'day-start':
                output.append(f'<g data-date="{p}">')
            elif kind in ('group-end', 'clip-end'):
                output.append('</g>')
            elif kind == 'clip-start':
                clip += 1
                output.append(f'<defs><clipPath id="clip-{clip}"><circle cx="{p["cx"]}" cy="{p["cy"]}" r="{p["r"]}"/></clipPath></defs><g clip-path="url(#clip-{clip})">')
            elif kind == 'text':
                weight = '700' if p['font'].endswith('Bold') else '400'
                italic = 'italic' if p['font'].endswith('Italic') else 'normal'
                output.append(f'<text x="{p["x"]:.3f}" y="{p["y"]:.3f}" font-family="{FONT_FAMILY[p["font"]]}" font-size="{p["size"]}" font-weight="{weight}" font-style="{italic}" fill="{p["color"]}" text-anchor="{p["align"]}" transform="rotate({p["rotate"]} {p["x"]:.3f} {p["y"]:.3f})">{escape(p["value"])}</text>')
            elif kind == 'line':
                output.append(f'<line x1="{p["x1"]:.3f}" y1="{p["y1"]:.3f}" x2="{p["x2"]:.3f}" y2="{p["y2"]:.3f}" stroke="{p["color"]}" stroke-width="{p["width"]}"/>')
            elif kind in ('rect', 'circle'):
                coords = f'x="{p["x"]:.3f}" y="{p["y"]:.3f}" width="{p["w"]:.3f}" height="{p["h"]:.3f}"' if kind == 'rect' else f'cx="{p["cx"]:.3f}" cy="{p["cy"]:.3f}" r="{p["r"]:.3f}"'
                output.append(f'<{kind} {coords} fill="{p["fill"] or "none"}" stroke="{p["stroke"] or "none"}" stroke-width="{p["width"]}"/>')
            elif kind == 'path':
                values = ' '.join(v[0] + ' '.join(f'{n:.3f}' for n in v[1:]) for v in p['points'])
                output.append(f'<path d="{values}" fill="{p["fill"] or "none"}" stroke="{p["stroke"] or "none"}" stroke-width="{p["width"]}"/>')
        return '\n'.join(output + ['</svg>']) + '\n'

    def pdf(self, c):
        from reportlab.lib.colors import HexColor
        for kind, p in self.ops:
            if kind in ('day-start', 'group-end'):
                continue
            if kind == 'clip-start':
                c.saveState()
                clip = c.beginPath()
                clip.circle(p['cx'], HEIGHT-p['cy'], p['r'])
                c.clipPath(clip, stroke=0, fill=0)
            elif kind == 'clip-end':
                c.restoreState()
            elif kind == 'text':
                c.saveState()
                c.setFillColor(HexColor(p['color']))
                c.setFont(p['font'], p['size'])
                c.translate(p['x'], HEIGHT-p['y'])
                c.rotate(-p['rotate'])
                {'start': c.drawString, 'middle': c.drawCentredString, 'end': c.drawRightString}[p['align']](0, 0, p['value'])
                c.restoreState()
            elif kind == 'line':
                c.setStrokeColor(HexColor(p['color']))
                c.setLineWidth(p['width'])
                c.line(p['x1'], HEIGHT-p['y1'], p['x2'], HEIGHT-p['y2'])
            else:
                if p['fill']: c.setFillColor(HexColor(p['fill']))
                if p['stroke']: c.setStrokeColor(HexColor(p['stroke']))
                c.setLineWidth(p['width'])
                flags = dict(fill=bool(p['fill']), stroke=bool(p['stroke']))
                if kind == 'rect': c.rect(p['x'], HEIGHT-p['y']-p['h'], p['w'], p['h'], **flags)
                elif kind == 'circle': c.circle(p['cx'], HEIGHT-p['cy'], p['r'], **flags)
                elif kind == 'path':
                    path = c.beginPath()
                    for v in p['points']:
                        if v[0] == 'M': path.moveTo(v[1], HEIGHT-v[2])
                        elif v[0] == 'L': path.lineTo(v[1], HEIGHT-v[2])
                        elif v[0] == 'C': path.curveTo(v[1], HEIGHT-v[2], v[3], HEIGHT-v[4], v[5], HEIGHT-v[6])
                        elif v[0] == 'Z': path.close()
                    c.drawPath(path, **flags)


def footer(d, year, label):
    d.line(42, 1045, 758, 1045, INK, .8)
    d.text(42, 1066, f'{d.key} / {label}', 9, color=SECONDARY)
    d.text(758, 1066, f'HOW YOUR DAYS FLY / {year}', 9, color=SECONDARY, align='end')


def month_grid(d, year, month, x, y, width, row_height=25, size=12, headings=True):
    step = width/7
    if headings:
        for wd, name in enumerate(['M', 'T', 'W', 'T', 'F', 'S', 'S']):
            d.text(x+(wd+.5)*step, y, name, 8, color=SECONDARY, align='middle')
        y += row_height
    for row, week in enumerate(dates.month_record(year, month, 'monday')['weeks']):
        for col, cell in enumerate(week):
            if not cell['in_month']: continue
            value = date.fromisoformat(cell['date'])
            with d.day(value):
                d.text(x+(col+.5)*step, y+row*row_height, cell['day'], size, color=SECONDARY if col>=5 else INK, align='middle')


def month_blocks(year):
    d = Drawing('A', 'Month blocks', 'Annual overview. Twelve familiar monthly grids; Monday first.')
    d.text(42, 75, 'YEAR', 12, 'Helvetica-Bold')
    d.text(36, 184, year, 124, 'Helvetica-Bold')
    d.text(758, 72, 'TWELVE MONTHS', 11, align='end')
    d.text(758, 91, 'ONE PAGE', 11, align='end')
    d.line(42, 224, 758, 224, INK, 1.6)
    w, gap = 220, 28
    for month in range(1, 13):
        row, col = divmod(month-1, 3)
        x, y = 42+col*(w+gap), 265+row*186
        d.text(x, y, f'{month:02d}', 24, 'Helvetica-Bold')
        d.text(x+w, y-2, SHORT[month].upper(), 10, align='end')
        month_grid(d, year, month, x, y+30, w, 20, 12)
    footer(d, year, 'MONTH BLOCKS / YEAR')
    return d


def continuous_weeks(year):
    d = Drawing('B', 'Continuous weeks', 'Annual overview. Weeks continue across month boundaries; outside-year days are pale.')
    d.text(42, 80, 'ONE', 58, 'Helvetica-Bold')
    d.text(42, 138, 'CONTINUOUS', 58, 'Helvetica-Bold')
    d.text(42, 196, 'YEAR.', 58, 'Helvetica-Bold')
    start = date(year, 1, 1)
    start -= timedelta(days=start.weekday())
    end = date(year, 12, 31)
    end += timedelta(days=6-end.weekday())
    rows = ((end-start).days+1)//7
    d.text(758, 77, str(year), 34, align='end')
    d.text(758, 103, f'{rows} DISPLAY ROWS', 9, color=SECONDARY, align='end')
    x, step, top, rh = 258, 71, 245, 14.45
    for col, name in enumerate(['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']):
        d.text(x+(col+.5)*step, top, name, 8, color=SECONDARY, align='middle')
    for row in range(rows):
        row_start = start+timedelta(days=row*7)
        y = top+20+row*rh
        entering = [row_start+timedelta(days=i) for i in range(7) if (row_start+timedelta(days=i)).day == 1 and (row_start+timedelta(days=i)).year == year]
        if entering:
            d.text(42, y, SHORT[entering[0].month].upper(), 12, 'Helvetica-Bold')
            d.line(93, y-4, 224, y-4, RULE, .7)
        for col in range(7):
            value = row_start+timedelta(days=col)
            px = x+col*step
            if value.year == year:
                if value.month % 2 == 0: d.rect(px+1, y-10, step-2, rh-.6, PALE)
                with d.day(value): d.text(px+step/2, y, value.day, 10.5, color=SECONDARY if col>=5 else INK, align='middle')
            else:
                d.text(px+step/2, y, value.day, 10.5, color='#B9BFC5', align='middle')
    footer(d, year, 'CONTINUOUS WEEKS / YEAR')
    return d


def month_strips(year):
    d = Drawing('C', 'Month strips', 'Annual overview. Twelve parallel month strips, aligned by day of month.')
    d.text(42, 86, str(year), 66, 'Helvetica-Bold')
    d.text(758, 65, 'MONTHS AS STRIPS', 12, align='end')
    d.text(758, 87, 'DAYS AS A MEASURE', 12, align='end')
    d.line(42, 129, 758, 129, INK, 1.6)
    step = 716/12
    for month in range(1, 13):
        x = 42+(month-1)*step
        d.text(x+step/2, 174, f'{month:02d}', 21, 'Helvetica-Bold', align='middle')
        d.text(x+step/2, 197, SHORT[month].upper(), 8, color=SECONDARY, align='middle')
        d.line(x, 214, x, 1001, RULE, .7)
        for day in range(1, calendar.monthrange(year, month)[1]+1):
            value = date(year, month, day)
            y = 240+(day-1)*24.4
            if value.weekday() >= 5: d.rect(x+3, y-13, step-6, 20, PALE)
            with d.day(value):
                d.text(x+12, y, f'{day:02d}', 10.5)
                d.text(x+step-11, y, ['Mo','Tu','We','Th','Fr','Sa','Su'][value.weekday()], 7.5, color=SECONDARY, align='end')
    d.line(758, 214, 758, 1001, RULE, .7)
    footer(d, year, 'MONTH STRIPS / YEAR')
    return d


def polar(cx, cy, r, degrees):
    a = math.radians(degrees)
    return cx+r*math.cos(a), cy+r*math.sin(a)


def arc(d, cx, cy, r, start, end, color=INK, width=1):
    count = max(2, math.ceil(abs(end-start)))
    points = [polar(cx, cy, r, start+(end-start)*i/count) for i in range(count+1)]
    d.path([('M', *points[0])] + [('L', *p) for p in points[1:]], stroke=color, width=width)


def radial_year(year):
    d = Drawing('D', 'Radial year', 'A cyclical annual calendar. Every day has the same angular interval; month arcs follow real day counts.')
    d.text(42, 79, 'THE YEAR', 37, 'Helvetica-Bold')
    d.text(42, 121, 'COMES AROUND.', 37, 'Helvetica-Bold')
    cx, cy = 400, 590
    model = dates.calendar_data('year', date(year, 1, 1))
    count = len(model['days'])
    for i, cell in enumerate(model['days']):
        value = date.fromisoformat(cell['date'])
        angle = -90+i*360/count
        a = polar(cx, cy, 266 if value.day==1 else 278, angle)
        b = polar(cx, cy, 296, angle)
        with d.day(value): d.line(*a, *b, color=INK if value.weekday()<5 else '#A5ADB4', width=1.5 if value.day==1 else .9)
        if value.day in (1, 8, 15, 22):
            px, py = polar(cx, cy, 254, angle)
            d.text(px, py+2.5, f'{value.day:02d}', 7.5, color=SECONDARY, align='middle')
    day_index=0
    for month in range(1, 13):
        days_in_month=calendar.monthrange(year,month)[1]
        a0=-90+day_index*360/count
        a1=-90+(day_index+days_in_month)*360/count
        arc(d,cx,cy,313,a0+1,a1-1,INK if month%2 else '#8D959C',4)
        px,py=polar(cx,cy,345,(a0+a1)/2)
        d.text(px,py+4,SHORT[month].upper(),11,'Helvetica-Bold',align='middle')
        day_index+=days_in_month
    d.text(cx,cy+20,str(year),86,'Helvetica-Bold',align='middle')
    d.text(cx,cy+52,f'{count} DAYS / ONE CYCLE',10,color=SECONDARY,align='middle')
    d.text(42,1004,'Equal angle per day. Month arcs follow their actual duration.',11,color=SECONDARY)
    footer(d,year,'RADIAL CYCLE / YEAR')
    return d


def equal_day_field(year):
    d=Drawing('E','Equal-day field','Annual day field, chronological left-to-right reading. Equal circles represent days, not weekdays or weeks.')
    model=dates.calendar_data('year',date(year,1,1))
    d.text(42,80,'EVERY DAY',55,'Helvetica-Bold')
    d.text(42,140,'COUNTS THE SAME.',55,'Helvetica-Bold')
    d.text(42,205,str(year),28)
    d.text(758,202,f'{len(model["days"])} EQUAL DAYS',10,color=SECONDARY,align='end')
    cols=20
    for i,cell in enumerate(model['days']):
        value=date.fromisoformat(cell['date'])
        row,col=divmod(i,cols)
        cx,cy=60+col*35.8,285+row*36.2
        with d.day(value):
            d.circle(cx,cy,12,INK if value.day==1 else (PALE if value.month%2==0 else PAPER),RULE,.8)
            d.text(cx,cy+2.8,f'{value.day:02d}',7.5,color=PAPER if value.day==1 else SECONDARY,align='middle')
    d.text(42,1004,'Left to right, then down. A dark circle begins a new month.',11,color=SECONDARY)
    footer(d,year,'EQUAL-DAY FIELD / YEAR')
    return d


def picture_month(year):
    d=Drawing('F','Image-led month','An image-led monthly calendar. Original procedural wave artwork paired with an ordinary January month grid.')
    d.text(42,67,'STUDY OF A CURRENT',11,'Helvetica-Bold')
    d.text(758,67,'01',11,align='end')
    # Original vector artwork: bounded sinusoidal paths, no sampled artist asset.
    with d.circle_clip(400,345,225):
        for i in range(68):
            base=110+i*7
            pts=[]
            for j in range(141):
                x=140+j*3.8
                env=math.exp(-((x-405)/175)**2)
                y=base+32*math.sin((x-120)/65+i*.065)*env+18*math.sin(x/112+i*.09)
                pts.append((x,y))
            d.path([('M',*pts[0])]+[('L',*p) for p in pts[1:]],stroke=BLUE,width=1.35)
    d.text(42,660,'JANUARY',48,'Helvetica-Bold')
    d.text(758,658,str(year),25,align='end')
    d.line(42,690,758,690,INK,.8)
    month_grid(d,year,1,42,726,716,49,29)
    footer(d,year,'IMAGE-LED MONTH GRID / MONTH')
    return d


def writing_week(year):
    start=date(year,1,4)
    start-=timedelta(days=start.weekday())
    end=start+timedelta(days=6)
    d=Drawing('G','Writing-led week','A weekly agenda with one lane per day and a separate notes area. Blank writing space is intentional.')
    if start.year == end.year and start.month == end.month:
        d.text(42,78,f'{start.day:02d} - {end.day:02d}',58,'Helvetica-Bold')
        d.text(42,129,f'{SHORT[start.month].upper()} {start.year}',25)
    else:
        d.text(42,78,f'{start.day:02d} {SHORT[start.month].upper()} {start.year}',43,'Helvetica-Bold')
        d.text(42,129,f'TO {end.day:02d} {SHORT[end.month].upper()} {end.year}',25)
    d.text(758,74,'A WEEK',11,align='end')
    d.text(758,95,'WITH ROOM',11,align='end')
    d.line(42,168,758,168,INK,1.4)
    d.text(563,205,'NOTES',10,'Helvetica-Bold')
    d.line(526,190,526,1004,RULE,.8)
    for i in range(7):
        value=start+timedelta(days=i)
        y=205+i*111
        with d.day(value):
            d.text(42,y+14,f'{value.day:02d}',29,'Helvetica-Bold',color=SECONDARY if i>=5 else INK)
            d.text(98,y+9,calendar.day_abbr[value.weekday()].upper(),10,color=SECONDARY)
            d.line(42,y+86,490,y+86,RULE,.8)
    for y in range(251,1005,36): d.line(563,y,758,y,RULE,.6)
    footer(d,year,'WRITING-LED AGENDA / WEEK')
    return d


def daily_page(year):
    value=date(year,1,1)
    d=Drawing('H','Date-led daily page','A single daily page with the date as the main image. One page is a sample of a serial daily calendar.')
    d.text(42,79,calendar.day_name[value.weekday()].upper(),62,'Helvetica-Bold')
    d.line(42,115,758,115,INK,1.5)
    d.text(758,159,str(year),27,align='end')
    d.rect(42,202,716,565,BLUE)
    d.text(400,665,'01',462,'Times-Roman',PAPER,'middle')
    d.text(42,870,'JANUARY',62,'Helvetica-Bold')
    d.text(42,924,calendar.day_name[value.weekday()],28,'Times-Italic')
    total=len(dates.calendar_data('year',value)['days'])
    d.text(758,924,f'DAY 001 / {total}',11,color=SECONDARY,align='end')
    with d.day(value): d.text(42,1004,value.isoformat(),11,color=SECONDARY)
    footer(d,year,'DATE-LED PAGE / DAY')
    return d


def build_studies(year):
    if not 2 <= year <= 9998: raise ValueError('year must be between 2 and 9998')
    return [fn(year) for fn in [month_blocks,continuous_weeks,month_strips,radial_year,equal_day_field,picture_month,writing_week,daily_page]]


def overview_svg(studies):
    parts=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1280" role="img" aria-labelledby="overview-title">',
           '<title id="overview-title">Eight original calendar pattern studies</title>',
           '<rect width="1600" height="1280" fill="#FFFFFF"/>',
           '<text x="36" y="51" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="700" fill="#17191C">Calendar, eight ways.</text>',
           '<text x="36" y="79" font-family="Arial, Helvetica, sans-serif" font-size="14" fill="#626970">A-E: annual structure. F-H: content emphasis and scale. Exploratory studies.</text>']
    for i,d in enumerate(studies):
        row,col=divmod(i,4)
        content=d.svg()
        content=content.replace('id="title"',f'id="{d.key}-title"').replace('id="desc"',f'id="{d.key}-desc"')
        content=content.replace('aria-labelledby="title desc"',f'aria-labelledby="{d.key}-title {d.key}-desc"')
        content=content.replace('id="clip-',f'id="{d.key}-clip-').replace('url(#clip-',f'url(#{d.key}-clip-')
        x,y=35+col*390,115+row*570
        content=content.replace('<svg ',f'<svg x="{x}" y="{y}" width="360" height="495" ',1)
        parts.append(content)
        parts.append(f'<text x="{x}" y="{y+518}" font-family="Arial, Helvetica, sans-serif" font-size="15" fill="#17191C">{d.key} / {escape(d.title)}</text>')
    return '\n'.join(parts+['</svg>'])+'\n'


def export_pdf(studies,path):
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import mm
    from reportlab.lib.colors import HexColor
    path.parent.mkdir(parents=True,exist_ok=True)
    c=canvas.Canvas(str(path),pagesize=(420*mm,297*mm),pageCompression=1,invariant=1)
    c.setTitle('Calendar, eight ways - How Your Days Fly')
    c.setAuthor('How Your Days Fly')
    cover_w,cover_h=420*mm,297*mm
    c.setFillColor(HexColor(INK)); c.setFont('Helvetica-Bold',27)
    c.drawString(35,cover_h-43,'Calendar, eight ways.')
    c.setFont('Helvetica',10)
    c.drawString(35,cover_h-64,'A-E: annual structure studies. F-H: content emphasis and scale. Explorations, not personal preference claims.')
    tile_w=(cover_w-70)/4
    scale=.285
    for i,d in enumerate(studies):
        row,col=divmod(i,4)
        x=35+col*tile_w+(tile_w-WIDTH*scale)/2
        top=cover_h-92-row*360
        c.saveState(); c.translate(x,top-HEIGHT*scale); c.scale(scale,scale); d.pdf(c); c.restoreState()
        c.setFillColor(HexColor(INK)); c.setFont('Helvetica-Bold',10)
        c.drawString(x,top-HEIGHT*scale-16,f'{d.key} / {d.title}')
    c.showPage()
    page_w,page_h=297*mm,420*mm
    for d in studies:
        c.setPageSize((page_w,page_h))
        scale=min(page_w/WIDTH,page_h/HEIGHT)
        c.saveState(); c.translate((page_w-WIDTH*scale)/2,(page_h-HEIGHT*scale)/2); c.scale(scale,scale); d.pdf(c); c.restoreState()
        c.showPage()
    c.save()


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--year',type=int,default=2027)
    parser.add_argument('--out-dir',type=Path,default=ROOT/'studies/pattern-atlas')
    parser.add_argument('--pdf',type=Path)
    args=parser.parse_args(argv)
    try: studies=build_studies(args.year)
    except ValueError as exc: parser.error(str(exc))
    args.out_dir.mkdir(parents=True,exist_ok=True)
    records=[]
    for d in studies:
        filename=f'{d.key.lower()}-{d.title.lower().replace(" ","-")}.svg'
        content=d.svg()
        (args.out_dir/filename).write_text(content,encoding='utf-8')
        records.append({'id':d.key,'title':d.title,'description':d.subtitle,'design_axes':STUDY_AXES[d.key],'file':filename,'sha256':hashlib.sha256(content.encode()).hexdigest(),'represented_dates':d.marked_dates,'review_status':'exploration-unreviewed'})
    (args.out_dir/'overview.svg').write_text(overview_svg(studies),encoding='utf-8')
    manifest={'recipe_version':1,'year':args.year,'renderer':'scripts/render_pattern_atlas.py','artwork':'original procedural vector graphics','fonts':'PDF standard fonts; SVG uses system fallback fonts, not embedded','replay_scope':'Deterministic SVG source. Browser glyph rendering depends on installed fonts; production typography needs pinned font versions.','personal_preferences_inferred':False,'studies':records}
    (args.out_dir/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if args.pdf: export_pdf(studies,args.pdf)
    print(f'Wrote {len(studies)} original studies to {args.out_dir}')
    if args.pdf: print(f'PDF: {args.pdf}')


if __name__=='__main__': main()
