"""Make renamed ASCII study instances from retained original licensed fonts."""
from pathlib import Path
import argparse,hashlib,json,shutil
import fontTools
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools import subset

ROOT=Path(__file__).resolve().parents[1]
PROFILES=ROOT/'assets/fonts/numeral-study/profiles.json'


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare(out_dir=ROOT/'tmp/numeral-study-fonts'):
    source=json.loads(PROFILES.read_text()); out_dir.mkdir(parents=True,exist_ok=True); result=[]
    for index,profile in enumerate(source['profiles'],1):
        original=ROOT/profile['source_file']; lic=ROOT/profile['license_file']
        if sha(original)!=profile['source_sha256'] or sha(lic)!=profile['license_sha256']:
            raise ValueError('Retained font/license changed: '+profile['font_id'])
        work=TTFont(original,recalcTimestamp=False,cfg={'fontTools.ttLib.tables.otBase:USE_HARFBUZZ_REPACKER':False})
        if 'fvar' in work:
            axes={a.axisTag:a.defaultValue for a in work['fvar'].axes}; axes.update(profile['coordinates'])
            for a in work['fvar'].axes:
                if not a.minValue<=axes[a.axisTag]<=a.maxValue: raise ValueError('Axis outside range')
            work=instantiateVariableFont(work,axes,inplace=True,optimize=True)
        else: axes={}
        family=f'Calendar Numerals Study {index:02}'
        names={1:family,2:'Regular',3:family.replace(' ',''),4:family+' Regular',6:family.replace(' ','')+'-Regular',16:family,17:'Regular',18:family+' Regular',21:family,22:'Regular',25:family.replace(' ','')}
        for record in list(work['name'].names):
            if record.nameID in names: work['name'].setName(names[record.nameID],record.nameID,record.platformID,record.platEncID,record.langID)
        options=subset.Options(); options.layout_features=['*']; options.name_IDs=['*']; options.name_languages=['*']; options.name_legacy=True
        select=subset.Subsetter(options); select.populate(unicodes=range(32,127)); select.subset(work)
        if 'DSIG' in work: del work['DSIG']
        target=out_dir/(f'numeral-study-{index:02}.ttf'); work.recalcTimestamp=False; work.save(target); work.close()
        license_target=out_dir/(profile['alias']+'-LICENSE.txt'); shutil.copyfile(lic,license_target)
        result.append({'alias':profile['alias'],'font_id':profile['font_id'],'file':target.name,'sha256':sha(target),
                       'license_file':license_target.name,'license_sha256':sha(license_target),'source_file':profile['source_file'],
                       'source_sha256':profile['source_sha256'],'coordinates':axes,'modified':True,
                       'modification':'All axes pinned where variable; ASCII subset retaining layout-feature closure; primary names changed. Original copyright and license retained.'})
    manifest={'fonttools':fontTools.__version__,'profiles_sha256':sha(PROFILES),'fonts':result,'scope':'Study-only working instances, not newly authored typefaces or website loading assets.'}
    (out_dir/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    return manifest


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--out-dir',type=Path,default=ROOT/'tmp/numeral-study-fonts')
    prepare(p.parse_args().out_dir)
