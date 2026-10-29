#!/usr/bin/env python3
"""Create and check local calendar design records; never generate art or approval.

Standard library only. Records preserve evidence and selected file identities.
A successful check does not establish date accuracy, design quality, rights,
authenticity of feedback, or that a renderer was actually replayed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[4]
BASES={'unknown','user-stated','user-confirmed','default','hypothesis','verified-fact'}
BRIEF_FIELDS=('view','use','theme','theme_role','period','sequence','medium','dimensions','language','week_start','visual_preferences')


def decision():
    return {'value':None,'basis':'unknown','evidence':[]}


def new_case(case_id,request,kind='real',mode='create'):
    if not re.fullmatch(r'[a-z0-9][a-z0-9_-]{0,63}',case_id):
        raise ValueError('case_id must be 1–64 lowercase letters, digits, hyphens or underscores')
    if not isinstance(request,str) or not request.strip():
        raise ValueError('request must be nonempty text')
    return {
        'case_version':1,'case_id':case_id,'case_kind':kind,'mode':mode,'phase':'brief',
        'request':{'text':request,'source':'synthetic-example' if kind=='synthetic' else 'user-request'},
        'brief':{key:decision() for key in BRIEF_FIELDS},
        'questions':[],'directions':[],'selection':decision(),'revisions':[],
        'recipe':None,'learning':[],
        'sharing':{'status':'synthetic-public-example' if kind=='synthetic' else 'local-unreviewed'},
    }


def fingerprint(path,base,role='asset'):
    path=Path(path).resolve(); base=Path(base).resolve()
    content=path.read_bytes()
    return {'role':role,'path':Path(os.path.relpath(path,base)).as_posix(),
            'sha256':hashlib.sha256(content).hexdigest(),'bytes':len(content)}


def check_record(record,record_path):
    """Return actionable structural/provenance errors; allow unresolved design choices."""
    errors=[]
    def require(condition,message):
        if not condition: errors.append(message)
    def check_decision(value,label):
        if not isinstance(value,dict):
            errors.append(label+': expected decision object'); return
        basis=value.get('basis')
        require(basis in BASES,label+': unknown decision basis')
        if basis=='unknown': require(value.get('value') is None,label+': unknown must keep value null')
        else: require(value.get('value') is not None,label+': a stated/default/proposed value is missing')
        if basis in ('user-stated','user-confirmed','verified-fact'):
            evidence=value.get('evidence')
            require(isinstance(evidence,list) and bool(evidence) and all(isinstance(v,str) and v.strip() for v in evidence),label+': evidence/source required')
    def check_artifacts(entries,label):
        if not isinstance(entries,list): errors.append(label+': artifacts must be a list'); return
        for n,item in enumerate(entries):
            key=f'{label}[{n}]'
            if not isinstance(item,dict): errors.append(key+': artifact must be an object'); continue
            path=item.get('path'); expected=item.get('sha256')
            if not isinstance(path,str) or not path:
                errors.append(key+': path required'); continue
            if not isinstance(expected,str) or not re.fullmatch(r'[0-9a-f]{64}',expected):
                errors.append(key+': SHA-256 required'); continue
            try:
                target=Path(record_path).parent/path
                require(hashlib.sha256(target.read_bytes()).hexdigest()==expected,key+': retained file changed')
            except OSError:
                errors.append(key+': retained file is missing or unreadable')
    def check_review(review,label,revision_id,user=False):
        if not isinstance(review,dict): errors.append(label+': review object required'); return
        status=review.get('status')
        allowed={'not-requested','pending','feedback','approved','rejected'} if user else {'not-run','partial','passed','failed'}
        require(status in allowed,label+': unknown review status')
        if status in ('passed','approved','rejected'):
            evidence=review.get('evidence')
            require(isinstance(evidence,list) and bool(evidence),label+': outcome needs scoped evidence')
            require(review.get('revision_id')==revision_id,label+': evidence must target this revision')

    if not isinstance(record,dict): return ['record must be a JSON object']
    require(record.get('case_version')==1,'unsupported case_version')
    require(record.get('case_kind') in ('real','synthetic'),'case_kind must be real or synthetic')
    require(record.get('mode') in ('discuss','create','revise','replay'),'unknown request mode')
    brief=record.get('brief',{})
    if not isinstance(brief,dict): return errors+['brief must be an object']
    for key in BRIEF_FIELDS: check_decision(brief.get(key),'brief.'+key)
    view=brief.get('view',{})
    if isinstance(view,dict) and view.get('value') is not None:
        require(view['value'] in ('year','month','week','day'),'view must be year/month/week/day')
    start=brief.get('week_start',{})
    if isinstance(start,dict) and start.get('value') is not None:
        require(start['value'] in ('monday','sunday'),'week_start must be monday/sunday')
    selection=record.get('selection',{})
    check_decision(selection,'selection')
    directions=record.get('directions',[])
    if not isinstance(directions,list): return errors+['directions must be a list']
    direction_ids=[]
    for direction in directions:
        if not isinstance(direction,dict): errors.append('direction must be an object'); continue
        key=direction.get('id'); direction_ids.append(key)
        require(isinstance(key,str) and bool(key),'direction id required')
        require(direction.get('status') in ('proposed','rendered'),'direction status must be proposed/rendered')
        if direction.get('status')=='rendered':
            artifacts=direction.get('artifacts',[])
            require(isinstance(artifacts,list) and any(isinstance(a,dict) and a.get('role') in ('preview','export') for a in artifacts),'rendered direction needs a retained preview/export artifact')
        check_artifacts(direction.get('artifacts',[]),f'direction {key}')
    require(len(direction_ids)==len(set(str(v) for v in direction_ids)),'duplicate direction id')
    if isinstance(selection,dict) and selection.get('value') is not None:
        ids=selection['value']
        require(isinstance(ids,list) and bool(ids),'selection value must list direction IDs')
        if isinstance(ids,list): require(all(v in direction_ids for v in ids),'selection points to an unknown direction')
    revisions=record.get('revisions',[])
    if not isinstance(revisions,list): return errors+['revisions must be a list']
    known=[]
    for rev in revisions:
        if not isinstance(rev,dict): errors.append('revision must be an object'); continue
        key=rev.get('id'); parent=rev.get('parent_revision')
        require(isinstance(key,str) and bool(key) and key not in known,'unique revision id required')
        require(parent is None or parent in known,f'revision {key}: parent must precede child')
        if parent is not None:
            require(bool(rev.get('change_request')),f'revision {key}: change request required')
            require('keep' in rev and 'change' in rev,f'revision {key}: record kept and changed relationships')
        check_artifacts(rev.get('artifacts',[]),f'revision {key}')
        check_review(rev.get('technical_review',{}),f'revision {key} technical review',key)
        check_review(rev.get('user_review',{}),f'revision {key} user review',key,user=True)
        known.append(key)
    recipe=record.get('recipe')
    if recipe is not None:
        if not isinstance(recipe,dict): errors.append('recipe must be an object')
        else:
            require(recipe.get('revision_id') in known,'recipe must point to a retained revision')
            check_artifacts(recipe.get('artifacts',[]),'recipe')
            replay=recipe.get('replay',{})
            if not isinstance(replay,dict): errors.append('recipe replay must be an object')
            elif replay.get('status')=='passed':
                require(bool(replay.get('evidence')),'replay claim needs actual run/output evidence')
    if record.get('case_kind')=='real':
        sharing=record.get('sharing',{})
        require(isinstance(sharing,dict),'sharing must be an object')
        if isinstance(sharing,dict): require(sharing.get('status')!='synthetic-public-example','real case cannot be labelled synthetic')
    return errors


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    new=sub.add_parser('new',help='Create a local record without inferring preferences or approval.')
    new.add_argument('--id',required=True)
    new.add_argument('--request',required=True)
    new.add_argument('--kind',choices=['real','synthetic'],default='real')
    new.add_argument('--mode',choices=['discuss','create','revise','replay'],default='create')
    new.add_argument('--out',type=Path)
    check=sub.add_parser('check',help='Check structure, evidence scope and retained file hashes only.')
    check.add_argument('record',type=Path)
    files=sub.add_parser('fingerprint',help='Print file identities to insert into artifact lists.')
    files.add_argument('files',nargs='+',type=Path)
    files.add_argument('--base',type=Path,required=True,help='Directory containing the case record.')
    files.add_argument('--role',default='asset')
    args=parser.parse_args(argv)
    if args.command=='new':
        record=new_case(args.id,args.request,args.kind,args.mode)
        out=args.out or ROOT/'output/cases'/args.id/'record.json'
        out.parent.mkdir(parents=True,exist_ok=True)
        with out.open('x') as handle:
            json.dump(record,handle,ensure_ascii=False,indent=2); handle.write('\n')
        print(f'Created {out}; choices remain unknown until recorded with their basis.')
    elif args.command=='fingerprint':
        print(json.dumps([fingerprint(path,args.base,args.role) for path in args.files],indent=2))
    else:
        errors=check_record(json.loads(args.record.read_text()),args.record)
        if errors:
            for error in errors: print(error)
            return 1
        print('Record structure and retained file identities checked; design, rights and user approval are not certified.')
    return 0


if __name__=='__main__':
    try:
        raise SystemExit(main())
    except (OSError,ValueError,TypeError) as exc:
        raise SystemExit(str(exc))
