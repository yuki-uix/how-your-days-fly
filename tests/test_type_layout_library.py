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
import design_catalog as design

HAS_FONTS=importlib.util.find_spec('fontTools') is not None
if HAS_FONTS:
    import render_type_layout_atlas as atlas
    import design_scene as scene


class TypeLayoutIndexTests(unittest.TestCase):
    def test_conditions_join_real_sources_fonts_and_proofs(self):
        index=materials.build_catalog(); by_id={a['id']:a for a in index['items']}
        elements=materials.select(index,kind='design-element')
        self.assertEqual(len(elements),10)
        self.assertEqual(len(by_id),len(index['items']))
        for item in elements:
            self.assertTrue(item['condition'] and item['choices'] and item['tradeoff'] and item['counterexample'])
            for key in item['reference_ids']: self.assertEqual(by_id[key]['kind'],'reference')
            for key in item['candidate_font_ids']: self.assertEqual(by_id[key]['kind'],'font')
            for study in item['study_refs']: self.assertTrue((ROOT/study['path']).is_file())
        for path in materials.TYPE_RESEARCH_FILES:
            source=json.loads((ROOT/path).read_text())
            for item in source['sources']:
                self.assertEqual(item['rights_status'],'research-only')
                self.assertTrue(item['reading_locator'] and item['actual_reading'] and item['limitations'])

    def test_domain_role_keyword_and_license_filters_compose(self):
        index=materials.build_catalog()
        pair=materials.select(index,scale='week',domain='typography',role='font-pairing')
        self.assertEqual([a['id'] for a in pair],['type-role-pairing'])
        found=materials.select(index,domain='typography',query='混排')
        self.assertIn('type-cjk-language',{a['id'] for a in found})
        allowed=materials.select(index,domain='typography',shareable_only=True)
        self.assertEqual(len(allowed),5)
        self.assertTrue(all(a['kind']=='font' and a['distribution_status']=='OFL-1.1' for a in allowed))
        joined=design.select(design.build_catalog(),'week','layout')
        self.assertEqual(len(joined['design_elements']),4)
        self.assertTrue(all('layout' in a['domains'] for a in joined['materials']))
        self.assertEqual({s['id'] for s in joined['studies']},{'G','J5'})

    def test_retained_original_font_bytes_and_public_boundary(self):
        record=json.loads((ROOT/'assets/fonts/type-study/manifest.json').read_text())
        for asset in record['assets']:
            self.assertEqual({a['tag'] for a in asset['axes']},{'wght'})
            for item in asset['local_files']:
                self.assertFalse(item['modified'])
                self.assertEqual(hashlib.sha256((ROOT/item['path']).read_bytes()).hexdigest(),item['sha256'])
        self.assertFalse(record['assets'][0]['measurements_400']['default_numerals_tabular'])
        self.assertTrue(record['assets'][1]['measurements_400']['default_numerals_tabular'])
        for path in materials.TYPE_RESEARCH_FILES+['assets/fonts/type-study/manifest.json','assets/library/type-layout-elements.json']:
            body=(ROOT/path).read_text()
            self.assertNotIn('/Users/',body)
            self.assertNotIn('output/cases/',body)


@unittest.skipUnless(HAS_FONTS,'Install requirements-design.txt for outline study checks')
class TypeLayoutProofTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initializes and verifies deterministic, renamed static working fonts.
        with tempfile.TemporaryDirectory() as folder:
            atlas.build(Path(folder))

    def test_proofs_replay_with_complete_leap_week_and_local_references(self):
        saved=ROOT/'studies/type-layout-atlas'
        with tempfile.TemporaryDirectory() as folder:
            target=Path(folder); atlas.build(target)
            for path in saved.glob('*.svg'):
                self.assertEqual(path.read_bytes(),(target/path.name).read_bytes())
                root=ET.fromstring(path.read_text())
                ids=[n.attrib['id'] for n in root.iter() if 'id' in n.attrib]
                self.assertEqual(len(ids),len(set(ids)))
                for node in root.iter():
                    href=node.attrib.get('href')
                    if href: self.assertIn(href.removeprefix('#'),ids)
            record=json.loads((target/'manifest.json').read_text())
            expected=[d['date'] for d in record['date_model']['days']]
            self.assertIn('2028-02-29',expected)
            for card in record['layout_cards']:
                self.assertEqual([d['date'] for d in card['represented_dates']],expected)

    def test_ink_matching_and_actual_numeral_advances(self):
        for font in ['serif400','sans400']:
            size,_=atlas.ink_scale(font,'日子的形状',56)
            *_,units=scene.font_info(font)
            boxes=[scene.glyph_bounds(font,c) for c in '日子的形状']
            height=(max(b[3] for b in boxes)-min(b[1] for b in boxes))*size/units
            self.assertAlmostEqual(height,56)
        f,cmap,_,_=scene.font_info('serif400')
        self.assertGreater(len({f['hmtx'][cmap[ord(c)]][0] for c in '0123456789'}),1)
        f,cmap,_,_=scene.font_info('sans400')
        self.assertEqual(len({f['hmtx'][cmap[ord(c)]][0] for c in '0123456789'}),1)


if __name__=='__main__': unittest.main()
