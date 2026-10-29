"""Small retained scene for editable calendar studies with pinned typography.

SVG proofs use font outlines; the scene source retains text/font/layout values.
PDF export embeds the original licensed fonts. No system font fallback is used.
"""
from __future__ import annotations

import base64
from contextlib import contextmanager
from functools import lru_cache
from html import escape
import math
from pathlib import Path

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

ROOT=Path(__file__).resolve().parents[1]
FONT_FILES={
    'display': ROOT/'assets/fonts/instrumentserif/InstrumentSerif-Regular.ttf',
    'display-italic': ROOT/'assets/fonts/instrumentserif/InstrumentSerif-Italic.ttf',
    'sans': ROOT/'assets/fonts/ibmplexsanscondensed/IBMPlexSansCondensed-Regular.ttf',
    'sans-medium': ROOT/'assets/fonts/ibmplexsanscondensed/IBMPlexSansCondensed-Medium.ttf',
    'sans-bold': ROOT/'assets/fonts/ibmplexsanscondensed/IBMPlexSansCondensed-SemiBold.ttf',
    'mono': ROOT/'assets/fonts/ibmplexmono/IBMPlexMono-Regular.ttf',
    'mono-medium': ROOT/'assets/fonts/ibmplexmono/IBMPlexMono-Medium.ttf',
}


@lru_cache(maxsize=None)
def font_info(name):
    f=TTFont(FONT_FILES[name])
    return f,f.getBestCmap(),f.getGlyphSet(),f['head'].unitsPerEm


def advance(name,text,size):
    f,cmap,_,units=font_info(name)
    missing=[c for c in text if ord(c) not in cmap]
    if missing: raise ValueError(f'{name} lacks glyphs: {missing}')
    return sum(f['hmtx'][cmap[ord(c)]][0] for c in text)*size/units


@lru_cache(maxsize=None)
def glyph_path(name,char):
    _,cmap,glyphs,_=font_info(name)
    pen=SVGPathPen(glyphs)
    glyphs[cmap[ord(char)]].draw(pen)
    return pen.getCommands()


@lru_cache(maxsize=None)
def glyph_bounds(name,char):
    _,cmap,glyphs,_=font_info(name)
    pen=BoundsPen(glyphs)
    glyphs[cmap[ord(char)]].draw(pen)
    return pen.bounds


def register_pdf_fonts():
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont as PDFTTFont
    for name,path in FONT_FILES.items():
        key='DaysFly-'+name
        if key not in pdfmetrics.getRegisteredFontNames():
            pdfmetrics.registerFont(PDFTTFont(key,str(path)))


class Scene:
    def __init__(self,key,title,width,height,paper,card):
        self.key,self.title,self.width,self.height=key,title,width,height
        self.ops=[]
        self.dates=[]
        self.card=card
        self.rect(0,0,width,height,paper)

    def text(self,x,y,value,size=18,font='sans',color='#222222',align='start',tracking=0,rotate=0,role='label'):
        value=str(value)
        advance(font,value,size)  # Fail early on missing glyphs.
        self.ops.append(('text',dict(x=x,y=y,value=value,size=size,font=font,color=color,align=align,tracking=tracking,rotate=rotate,role=role)))

    def line(self,x1,y1,x2,y2,color='#CCCCCC',width=1):
        self.ops.append(('line',dict(x1=x1,y1=y1,x2=x2,y2=y2,color=color,width=width)))

    def rect(self,x,y,w,h,fill=None,stroke=None,width=1):
        self.ops.append(('rect',dict(x=x,y=y,w=w,h=h,fill=fill,stroke=stroke,width=width)))

    def circle(self,cx,cy,r,fill=None,stroke=None,width=1):
        self.ops.append(('circle',dict(cx=cx,cy=cy,r=r,fill=fill,stroke=stroke,width=width)))

    def path(self,points,fill=None,stroke=None,width=1):
        self.ops.append(('path',dict(points=points,fill=fill,stroke=stroke,width=width)))

    def image(self,path,x,y,w,h):
        self.ops.append(('image',dict(path=str(Path(path).relative_to(ROOT)),x=x,y=y,w=w,h=h)))

    @contextmanager
    def day(self,value,**encoding):
        self.dates.append({'date':value.isoformat(),'weekday_monday0':value.weekday(),**encoding})
        self.ops.append(('day-start',value.isoformat()))
        yield
        self.ops.append(('group-end',None))

    def _text_x(self,p):
        width=advance(p['font'],p['value'],p['size'])+max(0,len(p['value'])-1)*p['tracking']
        return p['x']-({'start':0,'middle':.5,'end':1}[p['align']])*width

    def text_bounds(self):
        found=[]
        for kind,p in self.ops:
            if kind!='text': continue
            f,cmap,_,units=font_info(p['font'])
            scale=p['size']/units
            cursor=self._text_x(p)
            boxes=[]
            for char in p['value']:
                box=glyph_bounds(p['font'],char)
                if box:
                    x0,y0,x1,y1=box
                    boxes.append((cursor+x0*scale,p['y']-y1*scale,cursor+x1*scale,p['y']-y0*scale))
                cursor+=f['hmtx'][cmap[ord(char)]][0]*scale+p['tracking']
            if not boxes: continue
            x0=min(v[0] for v in boxes); y0=min(v[1] for v in boxes)
            x1=max(v[2] for v in boxes); y1=max(v[3] for v in boxes)
            if p['rotate']:
                a=math.radians(p['rotate']); cx,cy=p['x'],p['y']
                points=[(cx+(x-cx)*math.cos(a)-(y-cy)*math.sin(a),cy+(x-cx)*math.sin(a)+(y-cy)*math.cos(a)) for x,y in [(x0,y0),(x0,y1),(x1,y0),(x1,y1)]]
                x0,y0,x1,y1=min(v[0] for v in points),min(v[1] for v in points),max(v[0] for v in points),max(v[1] for v in points)
            found.append((p['value'],(x0,y0,x1,y1),p['role']))
        return found

    def svg(self):
        used=sorted({(p['font'],c) for kind,p in self.ops if kind=='text' for c in p['value']})
        out=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {self.height}" role="img" aria-labelledby="{self.key}-title">',f'<title id="{self.key}-title">{escape(self.title)}</title>','<defs>']
        for name,char in used:
            out.append(f'<path id="{self.key}-{name}-{ord(char)}" d="{glyph_path(name,char)}"/>')
        out.append('</defs>')
        for kind,p in self.ops:
            if kind=='day-start': out.append(f'<g data-date="{p}">')
            elif kind=='group-end': out.append('</g>')
            elif kind=='text':
                f,cmap,_,units=font_info(p['font']); scale=p['size']/units
                cursor=self._text_x(p)
                out.append(f'<g aria-label="{escape(p["value"],quote=True)}" data-text="{escape(p["value"],quote=True)}" data-role="{p["role"]}" fill="{p["color"]}" transform="rotate({p["rotate"]} {p["x"]:.4f} {p["y"]:.4f})">')
                for char in p['value']:
                    out.append(f'<use href="#{self.key}-{p["font"]}-{ord(char)}" transform="translate({cursor:.4f} {p["y"]:.4f}) scale({scale:.6f} {-scale:.6f})"/>')
                    cursor+=f['hmtx'][cmap[ord(char)]][0]*scale+p['tracking']
                out.append('</g>')
            elif kind=='line':
                out.append(f'<line x1="{p["x1"]:.4f}" y1="{p["y1"]:.4f}" x2="{p["x2"]:.4f}" y2="{p["y2"]:.4f}" stroke="{p["color"]}" stroke-width="{p["width"]}"/>')
            elif kind in ('rect','circle'):
                coords=f'x="{p["x"]:.4f}" y="{p["y"]:.4f}" width="{p["w"]:.4f}" height="{p["h"]:.4f}"' if kind=='rect' else f'cx="{p["cx"]:.4f}" cy="{p["cy"]:.4f}" r="{p["r"]:.4f}"'
                out.append(f'<{kind} {coords} fill="{p["fill"] or "none"}" stroke="{p["stroke"] or "none"}" stroke-width="{p["width"]}"/>')
            elif kind=='path':
                path=' '.join(v[0]+' '.join(f'{n:.4f}' for n in v[1:]) for v in p['points'])
                out.append(f'<path d="{path}" fill="{p["fill"] or "none"}" stroke="{p["stroke"] or "none"}" stroke-width="{p["width"]}"/>')
            elif kind=='image':
                data=base64.b64encode((ROOT/p['path']).read_bytes()).decode()
                out.append(f'<image x="{p["x"]}" y="{p["y"]}" width="{p["w"]}" height="{p["h"]}" preserveAspectRatio="xMidYMid meet" href="data:image/png;base64,{data}"/>')
        return '\n'.join(out+['</svg>'])+'\n'

    def pdf(self,c):
        from reportlab.lib.colors import HexColor
        for kind,p in self.ops:
            if kind in ('day-start','group-end'): continue
            if kind=='text':
                c.saveState(); c.setFillColor(HexColor(p['color']))
                c.translate(p['x'],self.height-p['y']); c.rotate(-p['rotate'])
                x=self._text_x(p)-p['x']
                obj=c.beginText(x,0); obj.setFont('DaysFly-'+p['font'],p['size']); obj.setCharSpace(p['tracking']); obj.textOut(p['value']); c.drawText(obj); c.restoreState()
            elif kind=='line':
                c.setStrokeColor(HexColor(p['color'])); c.setLineWidth(p['width'])
                c.line(p['x1'],self.height-p['y1'],p['x2'],self.height-p['y2'])
            elif kind=='image':
                c.drawImage(str(ROOT/p['path']),p['x'],self.height-p['y']-p['h'],p['w'],p['h'],preserveAspectRatio=True,anchor='c')
            else:
                if p['fill']: c.setFillColor(HexColor(p['fill']))
                if p['stroke']: c.setStrokeColor(HexColor(p['stroke']))
                c.setLineWidth(p['width']); flags=dict(fill=bool(p['fill']),stroke=bool(p['stroke']))
                if kind=='rect': c.rect(p['x'],self.height-p['y']-p['h'],p['w'],p['h'],**flags)
                elif kind=='circle': c.circle(p['cx'],self.height-p['cy'],p['r'],**flags)
                elif kind=='path':
                    path=c.beginPath()
                    for v in p['points']:
                        if v[0]=='M': path.moveTo(v[1],self.height-v[2])
                        elif v[0]=='L': path.lineTo(v[1],self.height-v[2])
                        elif v[0]=='C': path.curveTo(v[1],self.height-v[2],v[3],self.height-v[4],v[5],self.height-v[6])
                        elif v[0]=='Z': path.close()
                    c.drawPath(path,**flags)
