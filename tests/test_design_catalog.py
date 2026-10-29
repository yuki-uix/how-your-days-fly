import copy
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import design_catalog as design


class JoinedDesignCatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index=design.build_catalog()
        cls.materials={a['id']:a for a in design.load('assets/library/catalog.json')['items']}

    def test_all_retained_studies_and_relationship_targets_resolve(self):
        index=self.index
        self.assertEqual(index,design.load('design/catalog.json'))
        design.verify_fresh(index)
        structures={s['id'] for s in index['structures']}
        rules={r['id'] for r in index['rules']}
        sources={s['id'] for s in index['learning_sources']}
        self.assertEqual(len(structures),8)
        self.assertEqual(len(rules),9)
        self.assertEqual(len(sources),8)
        self.assertEqual({s['id'] for s in index['studies']},set('ABCDEFGH')|{f'J{n}' for n in range(1,7)})
        for study in index['studies']:
            self.assertTrue((ROOT/study['source']).is_file())
            self.assertTrue(set(study['structure_ids'])<=structures)
            self.assertTrue({r['id'] for r in study['rule_links']}<=rules)
            self.assertTrue(set(study['used_material_ids'])<=self.materials.keys())
        for rule in index['rules']:
            self.assertTrue(set(rule['source_ids'])<=sources)
            self.assertTrue((ROOT/rule['decision_record']).is_file())
        for old in index['earlier_case_sources']:
            self.assertTrue((ROOT/old['original_record']).is_file())
            if old['material_reference_id']:
                self.assertIn(old['material_reference_id'],self.materials)

    def test_scale_lookup_brings_three_rounds_together_without_exclusive_asset_bins(self):
        expected={'year':set('ABCDE')|{'J1','J2','J3'},'month':{'F','J4'},'week':{'G','J5'},'day':{'H','J6'}}
        for scale,ids in expected.items():
            result=design.select(self.index,scale)
            self.assertEqual({s['id'] for s in result['studies']},ids)
            self.assertTrue(result['structures'])
            self.assertTrue(result['rules'])
            returned_rules={r['id'] for r in result['rules']}
            self.assertTrue(all(link['id'] in returned_rules for study in result['studies'] for link in study['rule_links']))
            self.assertEqual(len(result['primary_component_ids']),4)
            self.assertTrue(all(scale in a['scales'] for a in result['materials']))
        day=design.select(self.index,'day')
        self.assertIn('y-tabs',{a['id'] for a in day['materials']})
        modular=next(s for s in day['structures'] if s['id']=='modular-date')
        self.assertEqual(modular['study_ids'],[])
        self.assertEqual(modular['status'],'vocabulary-and-external-references-only')

    def test_recorded_rules_and_used_assets_are_not_retroactively_invented(self):
        later={s['id']:s for s in design.load('studies/learned-language/manifest.json')['studies']}
        for study in self.index['studies']:
            if study['id'] in later:
                self.assertEqual([r['id'] for r in study['rule_links']],later[study['id']]['design_card']['source_rules'])
                self.assertTrue(all(r['relation']=='recorded-in-original-design-card' for r in study['rule_links']))
            else:
                self.assertTrue(all(r['relation']=='recommended-retrospective-association' for r in study['rule_links']))
        month=design.select(self.index,'month')
        j4=next(s for s in month['studies'] if s['id']=='J4')
        self.assertEqual(j4['used_material_ids'],['paper-light-j4'])
        self.assertIn('cma-tulip',{a['id'] for a in month['materials']})
        self.assertNotIn('cma-tulip',j4['used_material_ids'])
        self.assertNotIn('m-dock',j4['used_material_ids'])

    def test_stale_relationship_index_requires_rebuild(self):
        stale=copy.deepcopy(self.index)
        first=next(iter(stale['source_hashes']))
        stale['source_hashes'][first]='0'*64
        with self.assertRaisesRegex(ValueError,'Source changed'):
            design.verify_fresh(stale)


if __name__=='__main__': unittest.main()
