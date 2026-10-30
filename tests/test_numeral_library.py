import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import material_catalog as materials
HAS_NUMERALS=importlib.util.find_spec('fontTools') is not None and importlib.util.find_spec('uharfbuzz') is not None


class NumeralMaterialTests(unittest.TestCase):
    def test_profiles_join_licensed_originals_and_use_queries(self):
        index=materials.build_catalog()
        candidates=materials.select(index,kind='font',tag='date-type',shareable_only=True)
        self.assertEqual(len(candidates),16)
        self.assertEqual(len({a['numeral_profile']['alias'] for a in candidates}),16)
        for a in candidates:
            p=a['numeral_profile']
            self.assertEqual(p['font_id'],a['id'])
            for field,digest in [('source_file','source_sha256'),('license_file','license_sha256')]:
                self.assertEqual(hashlib.sha256((ROOT/p[field]).read_bytes()).hexdigest(),p[digest])
        dense=materials.select(index,kind='font',numeral_use='dense-grid')
        self.assertIn('font-barlow-condensed-regular',{a['id'] for a in dense})
        self.assertNotIn('font-dseg7-classic-regular',{a['id'] for a in dense})

    def test_actual_feature_audit_keeps_locale_and_no_change_distinct(self):
        audit=json.loads((ROOT/'docs/research/numeral-feature-audit.json').read_text())
        self.assertEqual(len(audit['fonts']),19)
        for f in audit['fonts']:
            self.assertEqual(hashlib.sha256((ROOT/f['file']).read_bytes()).hexdigest(),f['sha256'])
        noto=next(f for f in audit['fonts'] if f['family_id']=='font-noto-serif-sc-vf')
        settings={s['id']:s for s in noto['settings']}
        self.assertTrue(settings['default']['advances_equal'])
        self.assertFalse(settings['language_zh_Hans']['advances_equal'])
        azeret=next(f for f in audit['fonts'] if f['family_id']=='font-azeret-mono-vf')
        tab=next(s for s in azeret['settings'] if s['id']=='tnum_default_height')
        self.assertTrue(tab['advances_equal'])
        self.assertTrue(tab['outline_changed_digits'])


@unittest.skipUnless(HAS_NUMERALS,'Install requirements-numerals.txt for actual-feature SVG checks')
class NumeralProofTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import render_numeral_atlas as atlas
        cls.atlas=atlas; cls.folder=tempfile.TemporaryDirectory()
        cls.target=Path(cls.folder.name)/'proofs'
        atlas.build(cls.target,Path(cls.folder.name)/'fonts')
        cls.manifest=json.loads((cls.target/'manifest.json').read_text())

    @classmethod
    def tearDownClass(cls): cls.folder.cleanup()

    def test_replay_and_actual_four_forms(self):
        saved=ROOT/'studies/numeral-atlas'
        self.assertEqual(self.manifest['working_fonts'],json.loads((saved/'manifest.json').read_text())['working_fonts'])
        for path in saved.glob('*.svg'):
            self.assertEqual(path.read_bytes(),(self.target/path.name).read_bytes())
            tree=ET.fromstring(path.read_text())
            ids=[n.get('id') for n in tree.iter() if n.get('id')]
            self.assertEqual(len(ids),len(set(ids)))
            for n in tree.iter():
                href=n.get('href')
                if href and href.startswith('#'): self.assertIn(href[1:],ids)
        forms=self.manifest['four_forms']
        self.assertEqual([f['default_or_requested_digits_tabular'] for f in forms],[False,True,False,True])
        self.assertEqual(len({json.dumps(f['glyph_ids'],sort_keys=True) for f in forms}),4)
        self.assertEqual(len(self.manifest['family_measurements']),16)
        from glyph_study import font
        for entry in self.manifest['working_fonts']['fonts']:
            names=font(entry['alias'])[1]['name'].names
            self.assertTrue(all(n.toUnicode().startswith('Calendar Numerals Study ') for n in names if n.nameID in (1,4,16,18,21)))

    def test_context_dates_and_real_locale_substitution(self):
        groups={s['id']:s['represented_dates'] for s in self.manifest['calendar_contexts']}
        self.assertEqual([len(groups[x]) for x in ['quarter','month','week','day']],[91,29,7,1])
        for values in groups.values(): self.assertEqual(len(values),len(set(values)))
        self.assertEqual(groups['day'],['2028-02-29'])
        self.assertEqual(groups['week'],['2028-02-28','2028-02-29','2028-03-01','2028-03-02','2028-03-03','2028-03-04','2028-03-05'])
        from glyph_study import shape,GlyphStudy
        en,_=shape('num-noto-serif','0123456789',(),language='en')
        zh,_=shape('num-noto-serif','0123456789',(),language='zh-Hans')
        self.assertNotEqual([g[0] for g in en],[g[0] for g in zh])
        self.assertEqual(len({g[2] for g in en}),1)
        self.assertGreater(len({g[2] for g in zh}),1)
        with self.assertRaises(NotImplementedError): GlyphStudy('x','x',10,10,'#fff',{}).pdf(None)


if __name__=='__main__': unittest.main()
