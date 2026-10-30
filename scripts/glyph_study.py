"""Horizontal LTR glyph-outline SVG studies with explicit HarfBuzz features.

This separate study path does not change design_scene's SVG/PDF behavior or
provide paragraph breaking, vertical typography, font fallback or bidi layout.
"""
from functools import lru_cache
from html import escape
import json,re
import uharfbuzz as hb
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
import design_scene as ds


@lru_cache(maxsize=None)
def font(alias):
    face=hb.Face(hb.Blob.from_file_path(str(ds.FONT_FILES[alias])))
    shaped=hb.Font(face); shaped.scale=(face.upem,face.upem); hb.ot_font_set_funcs(shaped)
    tt,_,glyphs,units=ds.font_info(alias)
    if units!=face.upem: raise ValueError('Font units disagree')
    return shaped,tt,glyphs,tt.getGlyphOrder(),units


@lru_cache(maxsize=None)
def shape(alias,value,features=(),language='en',script='Latn'):
    if not value: return (),font(alias)[4]
    f,*_=font(alias)
    b=hb.Buffer(); b.add_str(value); b.guess_segment_properties()
    if str(b.direction)!='ltr': raise ValueError('Glyph study handles horizontal LTR only')
    b.language=language; b.script=script
    hb.shape(f,b,dict(features))
    records=tuple((i.codepoint,i.cluster,p.x_advance,p.y_advance,p.x_offset,p.y_offset) for i,p in zip(b.glyph_infos,b.glyph_positions))
    if any(v[0]==0 for v in records): raise ValueError(f'{alias} has missing glyphs in {value!r}')
    return records,font(alias)[4]


@lru_cache(maxsize=None)
def glyph(alias,gid):
    _,_,glyphs,order,_=font(alias)
    g=glyphs[order[gid]]
    box=BoundsPen(glyphs); g.draw(box)
    path=SVGPathPen(glyphs); g.draw(path)
    return box.bounds,path.getCommands()


def safe(value): return re.sub(r'[^a-zA-Z0-9_-]','_',value)


class GlyphStudy(ds.Scene):
    def text(self,x,y,value,size=18,font='sans',color='#222222',align='start',tracking=0,rotate=0,role='label',features=None,language='en',script='Latn'):
        if rotate: raise ValueError('Rotation is outside this study path')
        if align not in ('start','middle','end'): raise ValueError('Unsupported alignment')
        requested={'kern':True,'liga':True}; requested.update(features or {})
        records,units=shape(font,str(value),tuple(sorted(requested.items())),language,script)
        positions=[]; penx=peny=extra=0.0; scale=size/units
        for index,(gid,cluster,xa,ya,xo,yo) in enumerate(records):
            positions.append((gid,(penx+xo)*scale+extra,(peny+yo)*scale))
            penx+=xa; peny+=ya
            if index+1<len(records) and records[index+1][1]!=cluster: extra+=tracking
        self.ops.append(('text',{'x':x,'y':y,'value':str(value),'size':size,'font':font,'color':color,'align':align,'role':role,
                                'features':requested,'language':language,'script':script,'positions':positions,'advance':penx*scale+extra,'units':units}))

    def _text_x(self,p): return p['x']-{'start':0,'middle':.5,'end':1}[p['align']]*p['advance']

    def text_bounds(self):
        result=[]
        for kind,p in self.ops:
            if kind!='text': continue
            start=self._text_x(p); scale=p['size']/p['units']; boxes=[]
            for gid,x,y in p['positions']:
                b,_=glyph(p['font'],gid)
                if b: boxes.append((start+x+b[0]*scale,p['y']-y-b[3]*scale,start+x+b[2]*scale,p['y']-y-b[1]*scale))
            if boxes: result.append((p['value'],(min(b[0] for b in boxes),min(b[1] for b in boxes),max(b[2] for b in boxes),max(b[3] for b in boxes)),p['role']))
        return result

    def svg(self):
        prefix=safe(self.key); out=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {self.height}" role="img" aria-labelledby="{prefix}-title">',f'<title id="{prefix}-title">{escape(self.title)}</title>','<defs>']
        used=sorted({(p['font'],gid) for kind,p in self.ops if kind=='text' for gid,_,_ in p['positions']})
        for alias,gid in used: out.append(f'<path id="{prefix}-{safe(alias)}-g{gid}" d="{glyph(alias,gid)[1]}"/>')
        out.append('</defs>')
        for kind,p in self.ops:
            if kind=='text':
                label=escape(p['value'],quote=True); feature_text=escape(json.dumps(p['features'],sort_keys=True),quote=True)
                out.append(f'<g aria-label="{label}" data-text="{label}" data-role="{escape(p["role"],quote=True)}" data-font="{safe(p["font"])}" data-features="{feature_text}" fill="{p["color"]}">')
                start=self._text_x(p); scale=p['size']/p['units']
                for gid,x,y in p['positions']:
                    out.append(f'<use href="#{prefix}-{safe(p["font"])}-g{gid}" transform="translate({start+x:.6f} {p["y"]-y:.6f}) scale({scale:.9f} {-scale:.9f})"/>')
                out.append('</g>')
            else:
                child=ds.Scene.__new__(ds.Scene); child.key=prefix+'-aux'; child.title=''; child.width=self.width; child.height=self.height; child.ops=[(kind,p)]
                source=ds.Scene.svg(child)
                out.append(source[source.index('</defs>')+7:source.rfind('</svg>')])
        return '\n'.join(out+['</svg>'])+'\n'

    def pdf(self,*args,**kwargs):
        raise NotImplementedError('This explicit-feature study path exports SVG only.')
