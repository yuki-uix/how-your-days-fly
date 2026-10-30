#!/usr/bin/env python3
"""Prepare renamed static study instances; retain original OFL variable fonts."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

import fontTools
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

ROOT=Path(__file__).resolve().parents[1]
FONT_RECORD=ROOT/'assets/fonts/latin-study/manifest.json'
PLANS=[
    ('ss4','Source Serif 4',False,20),
    ('ss4italic','Source Serif 4',True,20),
    ('ss4small','Source Serif 4',False,8),
    ('ss4display','Source Serif 4',False,60),
    ('news','Newsreader',False,16),
    ('newsitalic','Newsreader',True,16),
    ('bodoni','Bodoni Moda',False,24),
    ('sourcesans','Source Sans 3',False,None),
    ('inter','Inter',False,14),
    ('space','Space Grotesk',False,None),
]


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize(value): return ''.join(c for c in value.casefold() if c.isalnum())


def prepare(out_dir=ROOT/'tmp/latin-study-fonts'):
    assets=json.loads(FONT_RECORD.read_text())['assets']
    for asset in assets:
        for item in asset['local_files']:
            if sha(ROOT/item['path'])!=item['sha256']:
                raise ValueError('Retained source changed: '+item['path'])
    out_dir.mkdir(parents=True,exist_ok=True)
    outputs=[]
    for alias,family,italic,opsz in PLANS:
        asset=next(a for a in assets if normalize(a.get('family') or a['title'])==normalize(family))
        source_file=next(f for f in asset['local_files'] if f['path'].endswith('.ttf') and ('italic' in Path(f['path']).name.casefold())==italic)
        license_file=next(f for f in asset['local_files'] if f['path'].endswith('OFL.txt'))
        font=TTFont(ROOT/source_file['path'],recalcTimestamp=False)
        axes={a.axisTag:a.defaultValue for a in font['fvar'].axes}
        axes['wght']=400
        if opsz is not None: axes['opsz']=opsz
        for axis in font['fvar'].axes:
            if not axis.minValue<=axes[axis.axisTag]<=axis.maxValue:
                raise ValueError('Study axis outside source range: '+alias)
        work=instantiateVariableFont(font,axes,inplace=True,optimize=True)
        renamed='Calendar Latin Study '+alias
        style='Italic' if italic else 'Regular'
        ps=renamed.replace(' ','')+'-'+style
        names={1:renamed,2:style,3:ps,4:renamed+' '+style,6:ps,16:renamed,17:style}
        for record in list(work['name'].names):
            if record.nameID in names:
                work['name'].setName(names[record.nameID],record.nameID,record.platformID,record.platEncID,record.langID)
        work['OS/2'].usWeightClass=400
        if 'DSIG' in work: del work['DSIG']
        target=out_dir/(alias+'.ttf')
        work.recalcTimestamp=False; work.save(target); work.close()
        shutil.copyfile(ROOT/license_file['path'],out_dir/(alias+'-OFL.txt'))
        outputs.append({'alias':alias,'family':family,'file':target.name,'sha256':sha(target),
                        'source_id':asset['id'],'source_file':source_file['path'],'source_sha256':source_file['sha256'],
                        'coordinates':axes,'style':style,'modified':True,
                        'modification':'All variable axes pinned; primary names changed; original license and copyright retained.'})
    manifest={'fonttools':fontTools.__version__,'fonts':outputs,'license':'OFL-1.1; matching original license accompanies each working instance.'}
    (out_dir/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    return manifest


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out-dir',type=Path,default=ROOT/'tmp/latin-study-fonts')
    args=parser.parse_args(); prepare(args.out_dir)
