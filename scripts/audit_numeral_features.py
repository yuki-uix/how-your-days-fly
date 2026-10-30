"""Measure retained ASCII numeral feature behavior with actual HarfBuzz shaping.

No font is modified. Coordinates are wght 400 and other VF axes at their
source defaults. Bounds are font-unit glyph ink relative to each pen origin,
including shaped offsets; they do not certify visual size or readability.
"""
import argparse
from functools import lru_cache
import hashlib
import json
from pathlib import Path

import fontTools
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont
import uharfbuzz as hb

DIGITS='0123456789'
INTERESTING={'tnum','pnum','lnum','onum','zero'}


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def selected_sources(repo):
    selections=[
      ('font-instrumentserif','Instrument Serif','assets/fonts/instrumentserif/InstrumentSerif-Regular.ttf','Roman'),
      ('font-instrumentserif','Instrument Serif','assets/fonts/instrumentserif/InstrumentSerif-Italic.ttf','Italic'),
      ('font-ibmplexmono','IBM Plex Mono','assets/fonts/ibmplexmono/IBMPlexMono-Regular.ttf','Roman'),
      ('font-ibmplexsanscondensed','IBM Plex Sans Condensed','assets/fonts/ibmplexsanscondensed/IBMPlexSansCondensed-Regular.ttf','Roman'),
    ]
    for manifest in ['assets/fonts/type-study/manifest.json','assets/fonts/latin-study/manifest.json','assets/fonts/numeral-study/manifest.json']:
        for asset in json.loads((repo/manifest).read_text())['assets']:
            for f in asset['local_files']:
                if f['path'].endswith('.ttf'):
                    selections.append((asset['id'],asset.get('family') or asset['title'],f['path'],f.get('style') or ('Italic' if 'Italic' in f['path'] else 'Roman')))
    return selections


def measure_file(repo,family_id,family,relative,style):
    path=repo/relative
    tt=TTFont(path)
    units=tt['head'].unitsPerEm
    coords={a.axisTag:a.defaultValue for a in tt['fvar'].axes} if 'fvar' in tt else {}
    if 'wght' in coords: coords['wght']=400
    tables={t:sorted({r.FeatureTag for r in tt[t].table.FeatureList.FeatureRecord}) if t in tt and tt[t].table.FeatureList else [] for t in ['GSUB','GPOS']}
    tags=set(tables['GSUB'])|set(tables['GPOS'])
    blob=hb.Blob.from_file_path(str(path)); face=hb.Face(blob); font=hb.Font(face)
    font.scale=(units,units); hb.ot_font_set_funcs(font)
    if coords: font.set_variations(coords)
    glyphs=tt.getGlyphSet(location=coords or None)
    order=tt.getGlyphOrder()

    @lru_cache(maxsize=None)
    def glyph_info(gid):
        g=glyphs[order[gid]]
        bounds=BoundsPen(glyphs); g.draw(bounds)
        pen=SVGPathPen(glyphs); g.draw(pen)
        return bounds.bounds,hashlib.sha256(pen.getCommands().encode()).hexdigest()

    def shape(label,requested,language='en'):
        features={'kern':True,'liga':True}; features.update(requested)
        buf=hb.Buffer(); buf.add_str(DIGITS); buf.direction='ltr'; buf.script='Latn'; buf.language=language
        hb.shape(font,buf,features)
        infos=buf.glyph_infos; positions=buf.glyph_positions
        if len(infos)!=10 or [i.cluster for i in infos]!=list(range(10)) or any(i.codepoint==0 for i in infos):
            raise ValueError('Numeral run no longer maps one glyph per digit: '+relative)
        ids=[i.codepoint for i in infos]
        advances=[p.x_advance for p in positions]
        offsets=[[p.x_offset,p.y_offset] for p in positions]
        ink=[]; hashes=[]
        for i,p in zip(infos,positions):
            b,h=glyph_info(i.codepoint); hashes.append(h)
            ink.append([round(b[0]+p.x_offset,4),round(b[1]+p.y_offset,4),round(b[2]+p.x_offset,4),round(b[3]+p.y_offset,4)] if b else None)
        result={'id':label,'status':'measured','language':language,'requested_features':features,'glyph_ids':ids,'advances':advances,
                'offsets':offsets if any(x or y for x,y in offsets) else None,'ink_bounds':ink,'advances_equal':len(set(advances))==1,
                'advance_spread_units':max(advances)-min(advances),'advance_spread_em':(max(advances)-min(advances))/units,
                'ink_y_range':[min(b[1] for b in ink if b),max(b[3] for b in ink if b)]}
        return result,hashes

    baseline,baseline_hashes=shape('default',{})
    baseline['comparison_to_default']='self'
    settings=[baseline]; measured={}

    def add(label,features,language='en'):
        result,hashes=shape(label,features,language)
        result['glyph_substituted_digits']=[d for i,d in enumerate(DIGITS) if result['glyph_ids'][i]!=baseline['glyph_ids'][i]]
        result['outline_changed_digits']=[d for i,d in enumerate(DIGITS) if hashes[i]!=baseline_hashes[i]]
        result['advance_changed_digits']=[d for i,d in enumerate(DIGITS) if result['advances'][i]!=baseline['advances'][i]]
        result['offset_changed_digits']=[d for i,d in enumerate(DIGITS) if ((result['offsets'] or [[0,0]]*10)[i]!=(baseline['offsets'] or [[0,0]]*10)[i])]
        result['visual_change_to_default']=bool(result['outline_changed_digits'] or result['advance_changed_digits'] or result['offset_changed_digits'])
        settings.append(result); measured[label]=(tuple(hashes),tuple(result['advances']),tuple(tuple(o) for o in result['offsets'] or [[0,0]]*10))

    combinations=[('tabular_lining',{'tnum':True,'pnum':False,'lnum':True,'onum':False},['tnum','lnum']),
                  ('proportional_lining',{'pnum':True,'tnum':False,'lnum':True,'onum':False},['pnum','lnum']),
                  ('tabular_oldstyle',{'tnum':True,'pnum':False,'onum':True,'lnum':False},['tnum','onum']),
                  ('proportional_oldstyle',{'pnum':True,'tnum':False,'onum':True,'lnum':False},['pnum','onum'])]
    for label,features,needed in combinations:
        absent=sorted(set(needed)-tags)
        if absent:
            settings.append({'id':label,'status':'required_explicit_tags_absent','absent_tags':absent,
                             'note':'This does not mean the default lacks that figure form; only this explicit feature pair was not tested.'})
        else: add(label,features)
    # Still test available width switches when a font has no explicit figure-height
    # tags, and single onum where a font uses default lining/tabular figures.
    if not {'lnum','onum'}.issubset(tags):
        if 'tnum' in tags: add('tnum_default_height',{'tnum':True,'pnum':False})
        if 'pnum' in tags: add('pnum_default_height',{'pnum':True,'tnum':False})
        if 'onum' in tags: add('onum_default_width',{'onum':True,'lnum':False,'pnum':False})
    if 'zero' in tags: add('slashed_zero',{'zero':True})
    if family_id=='font-noto-serif-sc-vf':
        add('language_zh_Hans',{},'zh-Hans')
        add('locl_off_diagnostic_en',{'locl':False})
        settings[-1]['diagnostic_only']='Disabling locl diagnoses the raw-cmap versus shaped-default difference; it is not a design recommendation.'
    full_ids=['tabular_lining','proportional_lining','tabular_oldstyle','proportional_oldstyle']
    full=len(set(measured[k] for k in full_ids))==4 if all(k in measured for k in full_ids) else False
    versions=sorted({n.toUnicode() for n in tt['name'].names if n.nameID==5})
    cmap=tt.getBestCmap()
    raw_ids=[tt.getGlyphID(cmap[ord(d)]) for d in DIGITS]
    raw_advances=[round(glyphs[cmap[ord(d)]].width,4) for d in DIGITS]
    width_match=all(next(s for s in settings if s['id']==k)['advances_equal']==k.startswith('tabular') for k in full_ids) if all(k in measured for k in full_ids) else None
    default_based=None
    if family_id=='font-source-sans-3-vf':
        default_signature=(tuple(baseline_hashes),tuple(baseline['advances']),tuple(tuple(o) for o in baseline['offsets'] or [[0,0]]*10))
        mapping={'tabular_lining':'default','proportional_lining':'pnum_default_height','tabular_oldstyle':'onum_default_width','proportional_oldstyle':'proportional_oldstyle'}
        signatures=[default_signature]+[measured[k] for k in ['pnum_default_height','onum_default_width','proportional_oldstyle']]
        default_based={'mapping':mapping,'four_distinct_results':len(set(signatures))==4,
                       'requested_widths_match_strictly':all(next(s for s in settings if s['id']==setting)['advances_equal']==label.startswith('tabular') for label,setting in mapping.items()),
                       'note':'The default supplies lining/tabular forms; absence of explicit lnum/tnum tags is not absence of those forms.'}
    result={'family_id':family_id,'family':family,'file':relative,'style':style,'sha256':sha(path),'versions':versions,
            'coordinates':coords,'units_per_em':units,'table_features':tables,'numeric_feature_tags':sorted(tags&INTERESTING),
            'raw_cmap_glyph_ids':raw_ids,'raw_cmap_advances':raw_advances,
            'settings':settings,'four_explicit_combinations_measured_distinct':full,'four_explicit_combinations_match_widths_strictly':width_match,
            'default_based_combination_check':default_based}
    tt.close()
    return result


def build(repo,out_dir):
    results=[measure_file(repo,*s) for s in selected_sources(repo)]
    record={'schema_version':1,'measured_at':'2026-10-30','scope':f"Retained {len({f['family_id'] for f in results})} families / {len(results)} Roman or Italic files; ASCII Western digits only.",
            'runtime':{'fonttools':fontTools.__version__,'uharfbuzz':hb.__version__,'harfbuzz':hb.version_string()},
            'input':DIGITS,'shaping_context':{'script':'Latn','language':'en','direction':'ltr','scale':'units_per_em'},
            'method':'Original font bytes unchanged. wght=400; all other VF axes use original defaults. GSUB/GPOS tags are inventory; requested settings are actually shaped with HarfBuzz. Outline deltas compare glyph drawings, separately from ID, advance and offset deltas.',
            'semantics':{'offsets':'null means all glyph offsets are [0,0]; otherwise [x,y] per input digit.','ink_bounds':'Per-digit [xmin,ymin,xmax,ymax], relative to that glyph pen origin including shaped offset; y grows upward, units are font units.','advances':'Advance in the shaped input run, including actual OpenType positioning. Equal advances do not imply equal ink widths or figure heights.','required_explicit_tags_absent':'Explicit combination not tested because named enabling tag is absent. Default may already have that form; inspect other measured settings.'},
            'non_claims':['This measures font-specific behavior, not personal preference or calendar readability.','Common digits use a deliberate Latn/en context; no claim for all languages, scripts, font versions or user-selected axes.','A requested feature may legitimately produce no visible change because the default already matches it.','Oldstyle/lining form is not inferred solely from baseline bounds.'],
            'fonts':results}
    out_dir.mkdir(parents=True,exist_ok=True)
    (out_dir/'numeral-feature-audit.json').write_text(compact_json(record)+'\n')
    return record


def compact_json(value,level=0):
    """Keep small numeric arrays inline rather than repeating one number per line."""
    pad='  '*level; child='  '*(level+1)
    if isinstance(value,dict):
        return '{\n'+',\n'.join(child+json.dumps(k,ensure_ascii=False)+': '+compact_json(v,level+1) for k,v in value.items())+'\n'+pad+'}'
    if isinstance(value,list):
        if all(not isinstance(v,dict) and (not isinstance(v,list) or all(not isinstance(x,(list,dict)) for x in v)) for v in value):
            return json.dumps(value,ensure_ascii=False,separators=(',',':'))
        return '[\n'+',\n'.join(child+compact_json(v,level+1) for v in value)+'\n'+pad+']'
    return json.dumps(value,ensure_ascii=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[1])
    p.add_argument('--out-dir',type=Path,required=True)
    args=p.parse_args(); r=build(args.repo,args.out_dir)
    print('Measured',len(r['fonts']),'files /',len({f['family_id'] for f in r['fonts']}),'families.')
    for f in r['fonts']:
        print(f['family'],f['style'],'tags:',','.join(f['numeric_feature_tags']),'four:',f['four_explicit_combinations_measured_distinct'])
