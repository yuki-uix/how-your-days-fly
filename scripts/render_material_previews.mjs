// Optional raster previews. SVG + Python source remain the editable masters.
// Usage: node scripts/render_material_previews.mjs [absolute node_modules dir]
import { createRequire } from 'node:module';
import { readFile, writeFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const require = createRequire(process.argv[2] ? resolve(process.argv[2], '__calendar_preview__.cjs') : import.meta.url);
const sharp = require('sharp');
const output = resolve(root, 'studies/material-library');
for (const name of ['year', 'month', 'week', 'day', 'overview']) {
  const svg = await readFile(resolve(output, name + '.svg'));
  await sharp(svg).flatten({background:'#F5F1E8'}).jpeg({quality:90,mozjpeg:true}).toFile(resolve(output, name + '.jpg'));
}
await writeFile(resolve(output, 'preview-runtime.json'), JSON.stringify({
  purpose:'Optional contact-sheet rasterization; original images are unmodified and retained separately.',
  sharp:sharp.versions.sharp, librsvg:sharp.versions.rsvg, node:process.versions.node,
},null,2)+'\n');
console.log('Rendered five material-library JPEG previews.');
