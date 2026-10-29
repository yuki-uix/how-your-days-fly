import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'.agents/skills/calendar-design-lab/scripts/design_case.py'
spec=importlib.util.spec_from_file_location('design_case_helper',SCRIPT)
case=importlib.util.module_from_spec(spec)
spec.loader.exec_module(case)


def proposal(key):
    return {'id':key,'status':'proposed','artifacts':[]}


def revision(key,parent=None):
    return {'id':key,'parent_revision':parent,'change_request':'Synthetic scoped edit' if parent else '',
            'keep':['date columns'] if parent else [],'change':['notes allocation'] if parent else [],
            'artifacts':[],
            'technical_review':{'status':'not-run','evidence':[]},
            'user_review':{'status':'pending','evidence':[]}}


class DesignCaseTests(unittest.TestCase):
    def test_new_record_keeps_interpretations_unknown_and_unapproved(self):
        record=case.new_case('books','A synthetic request about books',kind='synthetic')
        self.assertTrue(all(d['basis']=='unknown' and d['value'] is None for d in record['brief'].values()))
        self.assertIsNone(record['selection']['value'])
        self.assertEqual(record['revisions'],[])
        self.assertIsNone(record['recipe'])
        self.assertEqual(case.check_record(record,Path('/tmp/record.json')),[])

    def test_confirmed_choice_requires_evidence_but_explicit_defaults_do_not_become_confirmed(self):
        record=case.new_case('example','Synthetic',kind='synthetic')
        record['brief']['week_start']={'value':'monday','basis':'default','evidence':[]}
        self.assertEqual(case.check_record(record,Path('/tmp/record.json')),[])
        record['brief']['week_start']['basis']='user-confirmed'
        self.assertTrue(any('evidence/source required' in e for e in case.check_record(record,Path('/tmp/record.json'))))
        record['brief']['week_start']['evidence']=['Synthetic user explicitly selected Monday.']
        self.assertEqual(case.check_record(record,Path('/tmp/record.json')),[])

    def test_direction_selection_can_mix_existing_directions_without_approving_a_render(self):
        record=case.new_case('example','Synthetic',kind='synthetic')
        record['directions']=[proposal('a'),proposal('b')]
        record['selection']={'value':['a','b'],'basis':'user-stated','evidence':['Synthetic request combines a and b.']}
        self.assertEqual(case.check_record(record,Path('/tmp/record.json')),[])
        record['selection']['value'].append('missing')
        self.assertTrue(any('unknown direction' in e for e in case.check_record(record,Path('/tmp/record.json'))))

    def test_revision_approval_is_scoped_and_cannot_be_inherited(self):
        record=case.new_case('example','Synthetic',kind='synthetic')
        r1,r2=revision('r1'),revision('r2','r1')
        r1['user_review']={'status':'approved','revision_id':'r1','evidence':['Synthetic approval of r1 only.']}
        record['revisions']=[r1,r2]
        self.assertEqual(case.check_record(record,Path('/tmp/record.json')),[])
        r2['user_review']=copy.deepcopy(r1['user_review'])
        self.assertTrue(any('evidence must target this revision' in e for e in case.check_record(record,Path('/tmp/record.json'))))
        r2['parent_revision']='missing'
        self.assertTrue(any('parent must precede child' in e for e in case.check_record(record,Path('/tmp/record.json'))))

    def test_selected_file_hashes_detect_edits_and_rendered_status_needs_visible_output(self):
        with tempfile.TemporaryDirectory() as folder:
            base=Path(folder); artwork=base/'layout.svg'
            artwork.write_text('<svg xmlns="http://www.w3.org/2000/svg"/>')
            record=case.new_case('example','Synthetic',kind='synthetic')
            record['directions']=[{'id':'a','status':'rendered','artifacts':[case.fingerprint(artwork,base,'source')]}]
            self.assertTrue(any('preview/export' in e for e in case.check_record(record,base/'record.json')))
            record['directions'][0]['artifacts'][0]['role']='preview'
            self.assertEqual(case.check_record(record,base/'record.json'),[])
            artwork.write_text('<svg xmlns="http://www.w3.org/2000/svg"><rect width="1" height="1"/></svg>')
            self.assertTrue(any('retained file changed' in e for e in case.check_record(record,base/'record.json')))

    def test_replay_claim_requires_evidence_and_recipe_requires_an_existing_revision(self):
        record=case.new_case('example','Synthetic',kind='synthetic')
        record['revisions']=[revision('r1')]
        record['recipe']={'revision_id':'missing','replay':{'status':'passed','evidence':[]}}
        errors=case.check_record(record,Path('/tmp/record.json'))
        self.assertTrue(any('retained revision' in e for e in errors))
        self.assertTrue(any('actual run/output evidence' in e for e in errors))

    def test_cli_new_refuses_overwrite_and_check_runs_without_extra_packages(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'record.json'
            command=[sys.executable,str(SCRIPT),'new','--id','test-case','--request','Synthetic request','--kind','synthetic','--out',str(path)]
            subprocess.run(command,check=True,capture_output=True,text=True)
            initial=path.read_bytes()
            duplicate=subprocess.run(command,capture_output=True,text=True)
            self.assertNotEqual(duplicate.returncode,0)
            self.assertEqual(path.read_bytes(),initial)
            checked=subprocess.run([sys.executable,str(SCRIPT),'check',str(path)],capture_output=True,text=True)
            self.assertEqual(checked.returncode,0,checked.stdout+checked.stderr)

    def test_published_example_is_synthetic_proposed_and_unselected(self):
        path=ROOT/'.agents/skills/calendar-design-lab/examples/book-weekly.json'
        record=json.loads(path.read_text())
        self.assertEqual(record['case_kind'],'synthetic')
        self.assertTrue(all(d['status']=='proposed' and not d['artifacts'] for d in record['directions']))
        self.assertIsNone(record['selection']['value'])
        self.assertEqual(record['revisions'],[])
        self.assertEqual(case.check_record(record,path),[])


if __name__=='__main__': unittest.main()
