from datetime import date, timedelta
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET


ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'scripts/render_pattern_atlas.py'
spec=importlib.util.spec_from_file_location('pattern_atlas',SCRIPT)
atlas=importlib.util.module_from_spec(spec)
spec.loader.exec_module(atlas)
NS={'svg':'http://www.w3.org/2000/svg'}


class PatternAtlasTests(unittest.TestCase):
    def test_each_annual_structure_represents_every_day_exactly_once(self):
        for year,count in [(2027,365),(2028,366)]:
            expected={(date(year,1,1)+timedelta(days=i)).isoformat() for i in range(count)}
            for drawing in atlas.build_studies(year)[:5]:
                with self.subTest(year=year,mode=drawing.key):
                    self.assertEqual(len(drawing.marked_dates),count)
                    self.assertEqual(set(drawing.marked_dates),expected)
                    svg=ET.fromstring(drawing.svg())
                    self.assertEqual(len(svg.findall('.//svg:g[@data-date]',NS)),count)

    def test_month_week_and_day_samples_have_their_own_period(self):
        f,g,h=atlas.build_studies(2027)[5:]
        self.assertEqual(f.marked_dates[0],'2027-01-01')
        self.assertEqual(f.marked_dates[-1],'2027-01-31')
        self.assertEqual(len(f.marked_dates),31)
        self.assertEqual(g.marked_dates,[f'2027-01-{day:02d}' for day in range(4,11)])
        self.assertEqual(h.marked_dates,['2027-01-01'])

    def test_svg_sources_replay_without_random_state(self):
        a=atlas.build_studies(2027)
        b=atlas.build_studies(2027)
        self.assertEqual([d.svg() for d in a],[d.svg() for d in b])
        self.assertEqual(atlas.overview_svg(a),atlas.overview_svg(b))

    def test_cross_year_week_caption_matches_actual_dates(self):
        drawing=atlas.writing_week(2026)
        self.assertEqual(drawing.marked_dates[0],'2025-12-29')
        self.assertEqual(drawing.marked_dates[-1],'2026-01-04')
        labels=[p['value'] for kind,p in drawing.ops if kind=='text']
        self.assertIn('29 DEC 2025',labels)
        self.assertIn('TO 04 JAN 2026',labels)

    def test_artwork_clipping_survives_overview_composition(self):
        studies=atlas.build_studies(2027)
        for source in [studies[5].svg(),atlas.overview_svg(studies)]:
            root=ET.fromstring(source)
            groups=root.findall('.//svg:g[@clip-path]',NS)
            self.assertEqual(len(groups),1)
            ids={n.attrib['id'] for n in root.iter() if 'id' in n.attrib}
            for group in groups:
                target=group.attrib['clip-path'].removeprefix('url(#').removesuffix(')')
                self.assertIn(target,ids)

    def test_original_svgs_are_self_contained_and_well_formed(self):
        studies=atlas.build_studies(2027)
        for source in [d.svg() for d in studies]+[atlas.overview_svg(studies)]:
            root=ET.fromstring(source)
            self.assertFalse(root.findall('.//svg:image',NS))
            self.assertNotIn('href=',source)
            self.assertNotIn('<script',source)
            ids=[node.attrib['id'] for node in root.iter() if 'id' in node.attrib]
            self.assertEqual(len(ids),len(set(ids)))

    def test_cli_manifest_matches_saved_source_files(self):
        with tempfile.TemporaryDirectory() as folder:
            subprocess.run([sys.executable,str(SCRIPT),'--year','2027','--out-dir',folder],check=True,capture_output=True,text=True)
            target=Path(folder)
            manifest=json.loads((target/'manifest.json').read_text())
            self.assertFalse(manifest['personal_preferences_inferred'])
            self.assertEqual(len(manifest['studies']),8)
            for record in manifest['studies']:
                content=(target/record['file']).read_bytes()
                self.assertEqual(hashlib.sha256(content).hexdigest(),record['sha256'])
            self.assertTrue((target/'overview.svg').exists())


if __name__=='__main__': unittest.main()
