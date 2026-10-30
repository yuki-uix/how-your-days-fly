#!/usr/bin/env python3
"""Deterministically prepare renamed static study fonts from retained OFL VFs.

Original variable fonts and licenses remain unchanged. Working copies are
cache outputs, never represented as new typeface designs or public defaults.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

import fontTools
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

ROOT=Path(__file__).resolve().parents[1]
FONT_RECORD=ROOT/'assets/fonts/type-study/manifest.json'


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare(out_dir=ROOT/'tmp/type-layout-fonts'):
    records=json.loads(FONT_RECORD.read_text())
    out_dir.mkdir(parents=True,exist_ok=True)
    outputs=[]
    for asset in records['assets']:
        for f in asset['local_files']:
            if sha(ROOT/f['path'])!=f['sha256']: raise ValueError('Retained font/license changed: '+f['path'])
        original=next(f for f in asset['local_files'] if f['path'].endswith('.ttf'))
        license_file=next(f for f in asset['local_files'] if f['path'].endswith('OFL.txt'))
        serif='serif' in asset['id']
        family='Calendar Atlas Serif SC' if serif else 'Calendar Atlas Sans SC'
        for weight in ([400,600] if serif else [400,500]):
            key=('serif' if serif else 'sans')+str(weight)
            target=out_dir/(key+'.ttf')
            # Preserve byte replay regardless of optional HarfBuzz installation.
            source=TTFont(ROOT/original['path'],recalcTimestamp=False,cfg={'fontTools.ttLib.tables.otBase:USE_HARFBUZZ_REPACKER':False})
            work=instantiateVariableFont(source,{'wght':weight},inplace=True,optimize=True)
            style={400:'Regular',500:'Medium',600:'SemiBold'}[weight]
            ps=family.replace(' ','')+'-'+style
            names={1:family,2:style,3:ps+';'+str(weight),4:family+' '+style,6:ps,16:family,17:style}
            for record in list(work['name'].names):
                if record.nameID in names:
                    work['name'].setName(names[record.nameID],record.nameID,record.platformID,record.platEncID,record.langID)
            work['OS/2'].usWeightClass=weight
            if 'DSIG' in work: del work['DSIG']
            work.recalcTimestamp=False; work.save(target); work.close()
            shutil.copyfile(ROOT/license_file['path'],out_dir/(key+'-OFL.txt'))
            outputs.append({'alias':key,'file':target.name,'sha256':sha(target),'weight':weight,
                            'family':family,'source_id':asset['id'],'source_sha256':original['sha256'],
                            'modified':True,'modification':'wght instantiated; primary names changed; original license/copyright retained'})
    manifest={'fonttools':fontTools.__version__,'fonts':outputs,'license':'OFL-1.1; original licenses accompany cached working copies'}
    (out_dir/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    return manifest


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out-dir',type=Path,default=ROOT/'tmp/type-layout-fonts')
    args=parser.parse_args()
    print(json.dumps(prepare(args.out_dir),indent=2))
