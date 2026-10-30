import {createRequire} from 'node:module';
import {readFile} from 'node:fs/promises';
import {resolve,dirname} from 'node:path';
import {fileURLToPath} from 'node:url';
const root=resolve(dirname(fileURLToPath(import.meta.url)),'..');
const require=createRequire(process.argv[2]?resolve(process.argv[2],'__type_preview__.cjs'):import.meta.url);
const sharp=require('sharp');
for (const name of ['type-specimens','layout-relations']) {
 const folder=resolve(root,'studies/type-layout-atlas');
 await sharp(await readFile(resolve(folder,name+'.svg'))).flatten({background:'#F5F5ED'}).jpeg({quality:93,mozjpeg:true}).toFile(resolve(folder,name+'.jpg'));
}
