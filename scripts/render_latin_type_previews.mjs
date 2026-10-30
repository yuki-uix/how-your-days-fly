import {createRequire} from 'node:module';
import {readFile} from 'node:fs/promises';
import {resolve,dirname} from 'node:path';
import {fileURLToPath} from 'node:url';
const root=resolve(dirname(fileURLToPath(import.meta.url)),'..');
const require=createRequire(process.argv[2]?resolve(process.argv[2],'__latin_preview__.cjs'):import.meta.url);
const sharp=require('sharp');
const folder=process.argv[3]?resolve(process.argv[3]):resolve(root,'studies/latin-type-atlas');
for (const name of ['latin-families','latin-details']) {
 await sharp(await readFile(resolve(folder,name+'.svg'))).flatten({background:'#F4F1E9'}).jpeg({quality:93,mozjpeg:true}).toFile(resolve(folder,name+'.jpg'));
}
