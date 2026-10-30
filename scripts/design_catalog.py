#!/usr/bin/env python3
"""Join calendar structures, source-based rules, studies and retained materials.

The index stores relationships and source pointers. Original manifests, notes
and material provenance remain authoritative; this is not a new renderer.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import material_catalog

ROOT=Path(__file__).resolve().parents[1]
INDEX=ROOT/'design/catalog.json'
REF='.agents/skills/calendar-design-lab/references/'
SCALES=('year','month','week','day')

STRUCTURES=[
    ('month-matrix','月份矩阵',['year','month']),
    ('month-strips','月份长条',['year','month']),
    ('continuous-weeks','连续周流',['year','month','week']),
    ('radial-cycle','环形周期',['year','month']),
    ('equal-day-field','等日单元场',['year','month','week']),
    ('agenda-matrix','时间／议程矩阵',['week','day']),
    ('serial-units','单位序列',['month','week','day']),
    ('modular-date','模块式日期组合',['day']),
]
RULES=[
    ('temporal:continuous-order','保留日期顺序与边界','temporal-semantics.md',['source:timeviz-book','source:ggtime']),
    ('temporal:declared-normalization','声明等日或等月归一化','temporal-semantics.md',['source:timeviz-book','source:ggtime']),
    ('type:display-versus-lookup','展示字与查读数字分工','typographic-composition.md',['source:datawrapper','source:google-fonts-guide']),
    ('type:shared-anchors','共用边缘与基线','typographic-composition.md',['source:vignelli']),
    ('type:image-date-anchors','图像与日期共享锚点','typographic-composition.md',['source:vignelli']),
    ('type:nested-hierarchy','分层安排年份、月份与日号','typographic-composition.md',['source:vignelli','source:datawrapper']),
    ('type:purposeful-whitespace','为空白指定用途','typographic-composition.md',['source:vignelli']),
    ('type:series-invariants','保存系列中的固定与变化关系','typographic-composition.md',['source:vignelli']),
    ('type:expressive-display-numerals','表达性数字配完整日期索引','typographic-composition.md',['source:datawrapper','source:google-fonts-guide']),
]
SOURCES=[
    ('timeviz-book','Visualization of Time-Oriented Data','https://timeviz.net/','temporal-semantics.md','第3章 §3.1.1–3.1.2；第4章 §4.1、§4.2.2','selective-reading-recorded'),
    ('timeviz-browser','TimeViz Browser','https://browser.timeviz.net/','learning-guide.md','优先阅读第2项：按问题浏览案例','listed-learning-resource'),
    ('timelines','Timelines Revisited','https://timelinesrevisited.github.io/','learning-guide.md','优先阅读第3项：representation / scale / layout','listed-learning-resource'),
    ('vignelli','The Vignelli Canon','https://www.rit.edu/vignellicenter/sites/rit.edu.vignellicenter/files/documents/The%20Vignelli%20Canon.pdf','typographic-composition.md','印刷页48、52、68、72、80、84、92','selective-reading-recorded'),
    ('datawrapper','Fonts for charts and tables','https://www.datawrapper.de/blog/fonts-for-data-visualization','typographic-composition.md','数字形式、字形覆盖、字重、字号与对比度','selective-reading-recorded'),
    ('google-fonts-guide','Choosing Web Fonts','https://design.google/library/choosing-web-fonts-beginners-guide','typographic-composition.md','项目范围、文本量、大小与语言','selective-reading-recorded'),
    ('calendar-vis','Calendar-based graphics','https://robjhyndman.com/publications/calendar-vis/','learning-guide.md','实现研究第7项：日期坐标与单元内容','listed-learning-resource'),
    ('ggtime','ggtime preprint','https://arxiv.org/html/2510.25656v1','temporal-semantics.md','§§4–7；预印本，不标作已核实的同行评审结论','selective-reading-recorded'),
]

# A–H preceded the source-reading round. These are present-day associations,
# never backfilled as evidence that those rules originally produced the files.
EARLY_RULE_LINKS={
    'A':['type:nested-hierarchy','type:display-versus-lookup'],
    'B':['temporal:continuous-order'],
    'C':['type:nested-hierarchy'],
    'D':['temporal:declared-normalization'],
    'E':['temporal:continuous-order'],
    'F':['type:image-date-anchors'],
    'G':['type:purposeful-whitespace'],
    'H':['type:expressive-display-numerals'],
}
LATER_STRUCTURES={'J1':'continuous-weeks','J2':'radial-cycle','J3':'radial-cycle','J4':'month-matrix','J5':'agenda-matrix','J6':'serial-units'}
READING_TASKS={
    'year':'看全年关系、跨度、循环或累积变化',
    'month':'查当月、观看主题、建立月与月之间的系列关系',
    'week':'安排和记录七天，并给未归属某天的内容留空间',
    'day':'定位今天、揭示一个内容或保留一次观察',
}
RECOMMENDED_RULES={
    'year':['temporal:continuous-order','temporal:declared-normalization','type:display-versus-lookup','type:nested-hierarchy'],
    'month':['temporal:continuous-order','type:image-date-anchors','type:display-versus-lookup','type:series-invariants'],
    'week':['temporal:continuous-order','type:purposeful-whitespace','type:shared-anchors','type:series-invariants'],
    'day':['type:expressive-display-numerals','type:display-versus-lookup','type:series-invariants'],
}
LEGACY_CASES=[
    ('stendig','Stendig / Vignelli Center','https://artsandculture.google.com/asset/stendig-calendar-vignelli-massimo/aQHwHqYgKY7K0w?hl=en',None,'patterns.md'),
    ('neuyear','NeuYear','https://www.neuyear.net/collections/giant-6ft-x-3ft-wall-calendars','ref-y-01','patterns.md'),
    ('anaptar','Anaptár','https://anaptar.com/about/','ref-y-02','patterns.md'),
    ('muji','MUJI month / week planner','https://www.muji.us/products/b6-faux-suede-monthly-weekly-planner-from-dec-2026-ne2b4a6a',None,'patterns.md'),
    ('mack','MACK daily art calendar','https://www.mackpublishing.au/products/page-a-day-calendar-2026-damien-poulain','daily-mack-art-sequence','patterns.md'),
    ('timor','Danese Timor','https://www.danesemilano.com/contents/files/products/timor_files_mari_timor_481.pdf','daily-danese-timor-modular','learning-guide.md'),
]


def load(relative):
    return json.loads((ROOT/relative).read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_catalog():
    material=load('assets/library/catalog.json')
    early=load('studies/pattern-atlas/manifest.json')
    later=load('studies/learned-language/manifest.json')
    studies=[]
    for s in early['studies']:
        studies.append({
            'id':s['id'],'title':s['title'],'scale':s['design_axes']['scale'],
            'structure_ids':[s['design_axes']['time_structure']],
            'source':f'studies/pattern-atlas/{s["file"]}',
            'record':'studies/pattern-atlas/manifest.json',
            'rule_links':[{'id':r,'relation':'recommended-retrospective-association'} for r in EARLY_RULE_LINKS[s['id']]],
            'used_material_ids':[],
            'asset_note':'Original procedural art and system-font-dependent proof; see original manifest. No later library components are claimed as used.',
            'scope_note':'One retained study; a single month/week/day does not constitute a complete series.',
        })
    for s in later['studies']:
        studies.append({
            'id':s['id'],'title':s['title'],'scale':s['design_card']['display_extent']['view'],
            'structure_ids':[LATER_STRUCTURES[s['id']]],
            'structure_relation':'current-classification-of-retained-study',
            'source':f'studies/learned-language/{s["source"]}',
            'record':'studies/learned-language/manifest.json',
            'rule_links':[{'id':r,'relation':'recorded-in-original-design-card'} for r in s['design_card']['source_rules']],
            'used_material_ids':['paper-light-j4'] if s['id']=='J4' else [],
            'font_record':'assets/fonts/provenance.json',
            'scope_note':'One retained study; J2/J3 form a controlled mapping pair. See original design card for actual assets, comparison scope and review status.',
        })
    structures=[{
        'id':key,'title':title,'suggested_scales':scales,
        'definition':REF+'patterns.md',
        'study_ids':[s['id'] for s in studies if key in s['structure_ids']],
        'status':'has-retained-study' if any(key in s['structure_ids'] for s in studies) else 'vocabulary-and-external-references-only',
    } for key,title,scales in STRUCTURES]
    rules=[{'id':key,'title':title,'decision_record':REF+doc,'source_ids':sources,
            'status':'conditional-project-transfer-not-universal-law'} for key,title,doc,sources in RULES]
    sources=[{'id':'source:'+key,'title':title,'url':url,'reading_record':REF+doc,
              'locator':locator,'reading_status':status,
              'rights_note':'Learning evidence; this index grants no right to redistribute source figures, text, fonts or software.'}
             for key,title,url,doc,locator,status in SOURCES]
    groups={scale:{
        'reading_task':READING_TASKS[scale],
        'structure_ids':[s['id'] for s in structures if scale in s['suggested_scales']],
        'rule_ids':list(dict.fromkeys(RECOMMENDED_RULES[scale]+[
            link['id'] for study in studies if study['scale']==scale for link in study['rule_links']
        ])),
        'study_ids':[s['id'] for s in studies if s['scale']==scale],
        'material_ids':[a['id'] for a in material['items'] if scale in a['scales']],
        'primary_component_ids':material['groups'][scale]['components'],
        'design_element_ids':material['groups'][scale]['design_elements'],
        'material_relation':'Candidates for a new design or adaptation, not a claim of use in retained studies.',
    } for scale in SCALES}
    workflow={
        'skill':'.agents/skills/calendar-design-lab/SKILL.md',
        'discovery':REF+'discovery.md','exploration':REF+'design-exploration.md',
        'case_record':REF+'case-record.md','review':REF+'review.md','recipe':REF+'recipe.md',
    }
    inputs=[REF+name for name in ['patterns.md','design-language.md','learning-guide.md','temporal-semantics.md','typographic-composition.md']]+list(workflow.values())
    inputs+=['studies/pattern-atlas/manifest.json','studies/learned-language/manifest.json','assets/library/catalog.json']+material['source_files']
    inputs=list(dict.fromkeys(inputs))
    return {
        'schema_version':1,'entrypoint':'docs/design-atlas.md',
        'semantics':{
            'structures':'Open working vocabulary, not eight fixed templates; suggested scales are not implemented coverage.',
            'rules':'Conditional transfers; exact explanations and evidence remain in linked notes.',
            'studies':'Retained outputs and original manifests; technical checks, replay scope and user review remain distinct.',
            'materials':'Only IDs are joined here. Read the material index for original files, provenance, resolution and rights.',
            'used_material_ids':'Indexed source imagery actually used; fonts and implementation are linked separately. This field is not a complete bill of materials.',
        },
        'structures':structures,'rules':rules,'learning_sources':sources,'studies':studies,'groups':groups,
        'earlier_case_sources':[{
            'id':'case:'+key,'title':title,'url':url,'original_record':REF+doc,
            'material_reference_id':material_id,'rights_status':'research-only',
            'status':'previously-recorded-case-linked-without-new-analysis',
        } for key,title,url,material_id,doc in LEGACY_CASES],
        'material_catalog':'assets/library/catalog.json',
        'workflow':workflow,
        'source_hashes':{p:sha(ROOT/p) for p in inputs},
        'builder_sha256':sha(Path(__file__)),
    }


def verify_fresh(index):
    if index['builder_sha256']!=sha(Path(__file__)):
        raise ValueError('Design index builder changed; run scripts/design_catalog.py --build.')
    for path,expected in index['source_hashes'].items():
        if sha(ROOT/path)!=expected:
            raise ValueError(f'Source changed: {path}; run scripts/design_catalog.py --build.')


def select(index,scale=None,domain=None):
    group=index['groups'][scale] if scale else None
    def subset(key,ids):
        return [s for s in index[key] if ids is None or s['id'] in ids]
    mat=load(index['material_catalog'])
    selected_materials=[a for a in mat['items'] if group is None or a['id'] in group['material_ids']]
    if domain: selected_materials=[a for a in selected_materials if domain in a.get('domains',[])]
    return {
        'scale':scale or 'all',
        'reading_task':group['reading_task'] if group else 'Choose a reading task and viewing extent before selecting visual materials.',
        'structures':subset('structures',group['structure_ids'] if group else None),
        'rules':subset('rules',group['rule_ids'] if group else None),
        'studies':subset('studies',group['study_ids'] if group else None),
        'materials':selected_materials,
        'design_elements':[a for a in selected_materials if a['kind']=='design-element'],
        'domain':domain,
        'learning_sources':index['learning_sources'],
        'earlier_case_sources':index['earlier_case_sources'],
        'primary_component_ids':group['primary_component_ids'] if group else None,
        'material_relation':'Selection candidates; used_material_ids on a study records actual retained use.',
        'semantics':index['semantics'],
        'workflow':index['workflow'],
    }


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--build',action='store_true',help='Refresh the material index and the joined design index.')
    p.add_argument('--scale',choices=SCALES)
    p.add_argument('--domain',help='Narrow materials to typography or layout while retaining the scale context.')
    p.add_argument('--json',action='store_true')
    args=p.parse_args(argv)
    if args.build:
        material_catalog.CATALOG.write_text(json.dumps(material_catalog.build_catalog(),ensure_ascii=False,indent=2)+'\n')
        INDEX.parent.mkdir(parents=True,exist_ok=True)
        index=build_catalog()
        INDEX.write_text(json.dumps(index,ensure_ascii=False,indent=2)+'\n')
    else:
        index=load('design/catalog.json')
    verify_fresh(index)
    result=select(index,args.scale,args.domain)
    if args.json: print(json.dumps(result,ensure_ascii=False,indent=2))
    else:
        print(result['scale']+' / '+result['reading_task'])
        for key in ['structures','rules','studies']:
            print(key+': '+', '.join(s['id'] for s in result[key]))
        for kind in ['component','image','font','reference','proposal','design-element']:
            print(kind+': '+', '.join(a['id'] for a in result['materials'] if a['kind']==kind))
        print('Entry: docs/design-atlas.md; material candidates are separate from recorded asset use.')
    return 0


if __name__=='__main__':
    try:
        raise SystemExit(main())
    except ValueError as exc:
        raise SystemExit(str(exc))
