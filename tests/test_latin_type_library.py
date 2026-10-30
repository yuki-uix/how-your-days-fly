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
HAS_FONTS=importlib.util.find_spec('fontTools') is not None


class LatinFontSourcesTests(unittest.TestCase):
    def test_retained_sources_licenses_and_styles(self):
        record=json.loads((ROOT/'assets/fonts/latin-study/manifest.json').read_text())
        self.assertEqual(len(record['assets']),6)
        for asset in record['assets']:
            self.assertEqual(asset['distribution_status'],'OFL-1.1')
            self.assertTrue(any(f['path'].endswith('OFL.txt') for f in asset['local_files']))
            for f in asset['local_files']:
                body=(ROOT/f['path']).read_bytes()
                self.assertFalse(f['modified'])
                self.assertEqual(hashlib.sha256(body).hexdigest(),f['sha256'])
                git_blob=hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest()
                self.assertEqual(git_blob,f['upstream_git_blob_sha'])
        for family in ['Source Serif 4','Newsreader']:
            a=next(a for a in record['assets'] if a['family']==family)
            self.assertEqual({f['style'] for f in a['local_files'] if f['path'].endswith('.ttf')},{'Roman','Italic'})

    @unittest.skipUnless(HAS_FONTS,'Install requirements-design.txt for English proof replay')
    def test_original_fonts_to_proofs_replay_and_all_nine_families(self):
        import render_latin_type_atlas as atlas
        saved=ROOT/'studies/latin-type-atlas'
        with tempfile.TemporaryDirectory() as folder:
            target=Path(folder)/'studies'; cache=Path(folder)/'fonts'
            atlas.build(target,cache)
            for path in saved.glob('*.svg'):
                self.assertEqual(path.read_bytes(),(target/path.name).read_bytes())
                root=ET.fromstring(path.read_text())
                ids=[n.attrib['id'] for n in root.iter() if 'id' in n.attrib]
                self.assertEqual(len(ids),len(set(ids)))
                for n in root.iter():
                    if n.attrib.get('href'): self.assertIn(n.attrib['href'].removeprefix('#'),ids)
            rebuilt=json.loads((target/'manifest.json').read_text())
            retained=json.loads((saved/'manifest.json').read_text())
            self.assertEqual(rebuilt['working_fonts'],retained['working_fonts'])
            self.assertEqual(len(rebuilt['family_studies']),9)
            by_alias={a['alias']:a for a in rebuilt['working_fonts']['fonts']}
            self.assertEqual([by_alias[a]['coordinates']['opsz'] for a in ['ss4small','ss4','ss4display']],[8,20,60])
            self.assertEqual(by_alias['ss4italic']['style'],'Italic')
            self.assertNotEqual(by_alias['ss4italic']['source_file'],by_alias['ss4']['source_file'])
            measures={f['alias']:f['measurements'] for f in rebuilt['family_studies']}
            self.assertTrue(measures['sourcesans']['default_digits_tabular'])
            self.assertFalse(measures['inter']['default_digits_tabular'])


if __name__=='__main__': unittest.main()
