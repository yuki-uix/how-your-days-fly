from datetime import date
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
import material_catalog as catalog

HAS_FONTS=importlib.util.find_spec('fontTools') is not None
if HAS_FONTS:
    import build_material_library as materials


class MaterialIndexTests(unittest.TestCase):
    def test_distribution_filter_keeps_research_and_unlicensed_originals_out(self):
        index=catalog.build_catalog()
        allowed=catalog.select(index,shareable_only=True)
        self.assertEqual({a['kind'] for a in allowed},{'image','font'})
        self.assertEqual(len(allowed),19)  # 8 item-verified CC0 images + 5 retained OFL families.
        self.assertTrue(all(a['ready'] for a in allowed))
        self.assertFalse(any(a['kind'] in ('reference','proposal','component') for a in allowed))
        self.assertEqual(index,json.loads(catalog.CATALOG.read_text()))
        self.assertEqual(len({a['id'] for a in index['items']}),len(index['items']))
        for scale,group in index['groups'].items():
            self.assertEqual(len(group['components']),4)
            self.assertGreaterEqual(len(group['references']),4)
            self.assertTrue(all(scale in a['scales'] for a in catalog.select(index,scale=scale)))

    @unittest.skipUnless(importlib.util.find_spec('PIL') is not None,'Install Pillow for image checks')
    def test_retained_images_match_bytes_dimensions_and_item_rights_evidence(self):
        from PIL import Image
        entries=catalog.load('assets/library/open-images/manifest.json')['assets']
        for a in entries:
            with self.subTest(asset=a['id']):
                path=ROOT/a['local_path']
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),a['sha256'])
                with Image.open(path) as image:
                    self.assertEqual(image.size,(a['dimensions']['width'],a['dimensions']['height']))
                evidence=catalog.load(a['rights_evidence']['snapshot_path'])['record']
                self.assertEqual(a['license'],'CC0-1.0')
                if a['id'].startswith('met-'):
                    self.assertTrue(evidence['isPublicDomain'])
                else:
                    self.assertEqual(evidence['share_license_status'],'CC0')
                self.assertTrue(a['source_url'].startswith('https://'))
                self.assertIn('high_resolution_url',a)


@unittest.skipUnless(HAS_FONTS,'Install requirements-design.txt for material render checks')
class MaterialComponentTests(unittest.TestCase):
    def test_date_modules_preserve_identity_leap_year_and_six_row_month(self):
        for year,count in [(2027,365),(2028,366)]:
            source={s.key:s for s,_,_ in materials.component_records(year)}
            ribbon=source['y-ribbon']
            self.assertEqual(len(ribbon.dates),count)
            self.assertAlmostEqual(sum(d['width'] for d in ribbon.dates),708)
            self.assertEqual(ribbon.dates[0]['date'],f'{year}-01-01')
            self.assertEqual(ribbon.dates[-1]['date'],f'{year}-12-31')
            month=source['m-dock']
            self.assertEqual([d['date'] for d in month.dates],[f'{year}-05-{n:02}' for n in range(1,32)])
            for d in month.dates:
                self.assertEqual(d['column'],date.fromisoformat(d['date']).weekday())
            if year==2027: self.assertEqual(max(d['row'] for d in month.dates),5)
            for key in ['w-hours','w-notes','w-habit']:
                week=source[key]
                self.assertEqual(len(week.dates),7)
                self.assertEqual(date.fromisoformat(week.dates[0]['date']).weekday(),0)
                self.assertTrue(any(week.dates[0]['date'] in p['value'] and week.dates[-1]['date'] in p['value'] for kind,p in week.ops if kind=='text'))

    def test_retained_vectors_replay_and_no_glyph_overflow(self):
        baseline=json.loads((ROOT/'assets/library/components/manifest.json').read_text())
        saved={a['id']:a for a in baseline['assets']}
        for year in [2027,2028,2029]:
            for scene,svg,record in materials.component_records(year):
                if year==2027:
                    self.assertEqual(svg,(ROOT/saved[scene.key]['local_path']).read_text())
                    self.assertEqual(hashlib.sha256(svg.encode()).hexdigest(),saved[scene.key]['sha256'])
                for text,(x0,y0,x1,y1),_ in scene.text_bounds():
                    with self.subTest(year=year,component=scene.key,text=text):
                        self.assertGreaterEqual(min(x0,y0),-.01)
                        self.assertLessEqual(x1,scene.width+.01)
                        self.assertLessEqual(y1,scene.height+.01)

    def test_alternate_year_build_does_not_overwrite_baseline(self):
        baseline=(ROOT/'assets/library/components/y-ribbon.svg').read_bytes()
        manifest=(ROOT/'assets/library/components/manifest.json').read_bytes()
        with tempfile.TemporaryDirectory() as folder:
            materials.build(Path(folder),2028)
            self.assertIn('366 civil days',(Path(folder)/'y-ribbon.svg').read_text())
        self.assertEqual(baseline,(ROOT/'assets/library/components/y-ribbon.svg').read_bytes())
        self.assertEqual(manifest,(ROOT/'assets/library/components/manifest.json').read_bytes())

    def test_grouped_boards_have_unique_ids_and_only_retained_embedded_images(self):
        for path in (ROOT/'studies/material-library').glob('*.svg'):
            root=ET.fromstring(path.read_text())
            ids=[n.attrib['id'] for n in root.iter() if 'id' in n.attrib]
            self.assertEqual(len(ids),len(set(ids)),path.name)
            images=0
            for node in root.iter():
                href=node.attrib.get('href','')
                if href.startswith('#'):
                    self.assertIn(href[1:],ids)
                elif href:
                    self.assertTrue(href.startswith('data:image/jpeg;base64,'))
                    images+=1
            self.assertEqual(images,8 if path.stem=='overview' else 2)


if __name__=='__main__': unittest.main()
