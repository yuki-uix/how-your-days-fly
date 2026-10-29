#!/usr/bin/env python3
"""Build or query the retained calendar material index. Standard library only."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT/'assets/library/catalog.json'
SCALES = ('year', 'month', 'week', 'day')


def load(relative):
    return json.loads((ROOT/relative).read_text())


def build_catalog():
    items=[]
    for a in load('assets/library/components/manifest.json')['assets']:
        items.append({**a,'kind':'component','scales':a['suggested_scales'],
                      'ready':True,'distribution_status':'not-specified'})
    for a in load('assets/library/open-images/manifest.json')['assets']:
        items.append({**a,'kind':'image','scales':a['suggested_scales'],
                      'role':'source-image','ready':True,'distribution_status':'CC0-1.0'})
    font_files=load('assets/fonts/provenance.json')['files']
    for family in ['instrumentserif','ibmplexmono','ibmplexsanscondensed']:
        items.append({
            'id':'font-'+family,'title':family,'kind':'font','scales':list(SCALES),
            'role':'typography','tags':['type','numeral',family],
            'local_files':[f for f in font_files if '/'+family+'/' in f['path']],
            'rights_status':'OFL-1.1','distribution_status':'OFL-1.1','ready':True,
            'usage_notes':'Retain original OFL license. Existing proofs verify English/digits only; inspect coverage before another language.',
            'source_record':'assets/fonts/provenance.json',
        })
    items.append({
        'id':'paper-light-j4','title':'Paper and light / retained generated image',
        'kind':'image','scales':['year','month','week','day'],
        'role':'source-image','tags':['abstract','light','paper','blue','apricot'],
        'local_path':'assets/images/paper-light/paper-light-j4-v1.png',
        'source_record':'assets/images/paper-light/provenance.json',
        'rights_status':'project-generated-provenance-recorded',
        'distribution_status':'not-specified','ready':True,
        'usage_notes':'Original selected asset already used in J4. Generation metadata is recorded; no blanket public reuse grant is asserted.',
    })
    am=load('docs/research/annual-monthly-materials.json')
    wd=load('docs/research/weekly-daily-materials.json')
    for a in am['records']+wd['references']:
        items.append({**a,'kind':'reference','role':'design-evidence','ready':False,
                      'distribution_status':'research-only','local_asset':None})
    for a in wd['original_proposals']:
        items.append({**a,'title':a['element'],'kind':'proposal','role':'design-proposal',
                      'ready':False,'rights_status':'project-proposal',
                      'distribution_status':'not-an-asset'})
    groups={scale:{
        'components':[a['id'] for a in items if a['kind']=='component' and a['primary_scale']==scale],
        'candidate_images':[a['id'] for a in items if a['kind']=='image' and scale in a['scales']],
        'references':[a['id'] for a in items if a['kind']=='reference' and scale in a['scales']],
        'font_families':[a['id'] for a in items if a['kind']=='font'],
        'proposals':[a['id'] for a in items if a['kind']=='proposal' and scale in a['scales']],
    } for scale in SCALES}
    return {
        'schema_version':1,'updated_at':'2026-10-29','groups':groups,'items':items,
        'semantics':{
            'scales':'Suggested viewing/use extent, not mutually exclusive asset ownership.',
            'ready':'A retained asset exists. This does not imply a complete series, print resolution, user approval, or a public reuse license.',
            'distribution_status':'CC0-1.0 or OFL-1.1 pass the explicit-license filter; OFL conditions still apply. Original project assets retain their separately unspecified scope.',
        },
        'source_files':[
            'assets/library/components/manifest.json','assets/library/open-images/manifest.json',
            'assets/fonts/provenance.json','assets/images/paper-light/provenance.json',
            'docs/research/annual-monthly-materials.json','docs/research/weekly-daily-materials.json',
        ],
    }


def select(catalog, scale=None, kind=None, tag=None, ready_only=False, shareable_only=False):
    found=catalog['items']
    if scale: found=[a for a in found if scale in a['scales']]
    if kind: found=[a for a in found if a['kind']==kind]
    if tag: found=[a for a in found if tag.casefold() in [t.casefold() for t in a.get('tags',[])]]
    if ready_only: found=[a for a in found if a['ready']]
    if shareable_only: found=[a for a in found if a['distribution_status'] in ('CC0-1.0','OFL-1.1')]
    return found


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--build',action='store_true',help='Refresh retained index from its six source records.')
    p.add_argument('--scale',choices=SCALES)
    p.add_argument('--kind',choices=['component','image','font','reference','proposal'])
    p.add_argument('--tag')
    p.add_argument('--ready-only',action='store_true')
    p.add_argument('--shareable-only',action='store_true',help='Only assets with recorded CC0/OFL scope; retain conditions.')
    p.add_argument('--json',action='store_true')
    args=p.parse_args(argv)
    if args.build:
        catalog=build_catalog()
        CATALOG.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
    else:
        catalog=json.loads(CATALOG.read_text())
    found=select(catalog,args.scale,args.kind,args.tag,args.ready_only,args.shareable_only)
    if args.json:
        print(json.dumps(found,ensure_ascii=False,indent=2))
    else:
        for a in found:
            print(f'{a["id"]:37} {a["kind"]:10} {a.get("title_zh") or a.get("title") or a.get("element")} [{a["distribution_status"]}]')
        print(f'{len(found)} records')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
