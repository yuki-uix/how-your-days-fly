from datetime import date,timedelta
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
NS={'svg':'http://www.w3.org/2000/svg'}
AVAILABLE=importlib.util.find_spec('fontTools') is not None
if AVAILABLE:
    sys.path.insert(0,str(ROOT/'scripts'))
    import render_language_studies as studies
    from design_scene import font_info


@unittest.skipUnless(AVAILABLE,'Install requirements-design.txt for visual-study checks')
class LanguageStudyTests(unittest.TestCase):
    def test_annual_views_retain_all_civil_dates(self):
        for year,count in [(2027,365),(2028,366)]:
            expected={(date(year,1,1)+timedelta(days=i)).isoformat() for i in range(count)}
            for scene in studies.build_studies(year)[:3]:
                with self.subTest(year=year,study=scene.key):
                    represented=[v['date'] for v in scene.dates]
                    self.assertEqual(len(represented),count)
                    self.assertEqual(set(represented),expected)
                    for v in scene.dates:
                        self.assertEqual(date.fromisoformat(v['date']).weekday(),v['weekday_monday0'])

    def test_ring_pair_has_identical_controls_and_distinct_mappings(self):
        a=studies.ring(2027,'equal-civil-day'); b=studies.ring(2027,'equal-month')
        for key in ['display_extent','temporal_unit','spatial_layout','typographic_roles','style','control_group']:
            self.assertEqual(a.card[key],b.card[key])
        self.assertNotEqual(a.card['temporal_mapping'],b.card['temporal_mapping'])
        self.assertEqual([v['date'] for v in a.dates],[v['date'] for v in b.dates])
        for left,right in zip(a.dates,a.dates[1:]):
            self.assertAlmostEqual(right['angle_degrees']-left['angle_degrees'],360/365)
        starts=[v['angle_degrees'] for v in b.dates if v['date'].endswith('-01')]
        for left,right in zip(starts,starts[1:]): self.assertAlmostEqual(right-left,30)
        feb=[v for v in b.dates if v['date'].startswith('2027-02-')]
        self.assertAlmostEqual(feb[1]['angle_degrees']-feb[0]['angle_degrees'],30/28)

    def test_scope_specific_samples_keep_their_dates_and_writing_areas(self):
        month,week,day=studies.build_studies(2027)[3:]
        self.assertEqual(len(month.dates),30)
        self.assertEqual(month.dates[0]['date'],'2027-04-01')
        self.assertEqual(month.dates[0]['column'],3)
        self.assertEqual(month.dates[-1]['date'],'2027-04-30')
        self.assertEqual([v['date'] for v in week.dates],[f'2027-04-{i:02d}' for i in range(5,12)])
        self.assertEqual({v['writing_width'] for v in week.dates},{180})
        self.assertEqual(day.dates,[{'date':'2027-04-18','weekday_monday0':6}])
        six_rows=studies.image_month(2029)
        self.assertEqual(max(v['row'] for v in six_rows.dates),5)

    def test_numeric_roles_have_actual_font_properties(self):
        for alias in ['mono','sans-medium']:
            f,cmap,_,_=font_info(alias)
            self.assertEqual(len({f['hmtx'][cmap[ord(c)]][0] for c in '0123456789'}),1)
        f,cmap,_,_=font_info('display-italic')
        self.assertGreater(len({f['hmtx'][cmap[ord(c)]][0] for c in '0123456789'}),1)

    def test_actual_glyph_bounds_fit_each_artboard(self):
        for scene in studies.build_studies(2027)+[studies.image_month(2029)]:
            for text,(x0,y0,x1,y1),role in scene.text_bounds():
                with self.subTest(study=scene.key,text=text,role=role):
                    self.assertGreaterEqual(x0,-.01); self.assertGreaterEqual(y0,-.01)
                    self.assertLessEqual(x1,scene.width+.01); self.assertLessEqual(y1,scene.height+.01)

    def test_outlined_svg_references_are_local_and_resolve(self):
        sample=studies.build_studies(2027)
        for source in [s.svg() for s in sample]+[studies.overview(sample)]:
            root=ET.fromstring(source)
            ids=[node.attrib['id'] for node in root.iter() if 'id' in node.attrib]
            self.assertEqual(len(ids),len(set(ids)))
            for node in root.iter():
                href=node.attrib.get('href')
                if href:
                    if node.tag.endswith('image'): self.assertTrue(href.startswith('data:image/png;base64,'))
                    else: self.assertIn(href.removeprefix('#'),ids)
            self.assertFalse(root.findall('.//svg:text',NS))

    def test_retained_font_and_image_files_match_provenance(self):
        data=json.loads(studies.FONT_PROVENANCE.read_text())
        for entry in data['files']:
            self.assertEqual(hashlib.sha256((ROOT/entry['path']).read_bytes()).hexdigest(),entry['sha256'])
        image=json.loads((studies.IMAGE.parent/'provenance.json').read_text())
        self.assertEqual(hashlib.sha256(studies.IMAGE.read_bytes()).hexdigest(),image['sha256'])
        self.assertEqual(image['generation']['reference_images'],[])

    def test_svg_replay_uses_chosen_assets_without_random_regeneration(self):
        first=studies.build_studies(2027); second=studies.build_studies(2027)
        self.assertEqual([s.svg() for s in first],[s.svg() for s in second])
        self.assertEqual(studies.overview(first),studies.overview(second))

    def test_overview_year_follows_the_study_date_range(self):
        source=studies.overview(studies.build_studies(2028))
        self.assertIn('data-text="Calendar studies / 2028"',source)
        self.assertNotIn('data-text="Calendar studies / 2027"',source)

    def test_replay_rejects_inconsistent_asset_provenance(self):
        fonts=json.loads(studies.FONT_PROVENANCE.read_text())
        fonts['files'][0]['sha256']='0'*64
        with tempfile.TemporaryDirectory() as folder:
            target=Path(folder)/'provenance.json'
            target.write_text(json.dumps(fonts))
            with patch.object(studies,'FONT_PROVENANCE',target):
                with self.assertRaisesRegex(ValueError,'Font asset changed'):
                    studies.verify_assets()


if __name__=='__main__': unittest.main()
