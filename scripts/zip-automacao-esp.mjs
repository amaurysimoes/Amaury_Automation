// Gera public/downloads/automacao_esp.zip com o projeto Python (sem .venv, .pio, __pycache__ e .env).
// Roda antes do dev e do build (package.json); o .zip não é versionado, é gerado a cada build.
import { mkdirSync, readdirSync, readFileSync, statSync, writeFileSync } from 'node:fs';
import { join, relative, sep } from 'node:path';
import { zipSync } from 'fflate';

const SOURCE = 'automacao_esp';
const OUTPUT = 'public/downloads/automacao_esp.zip';
const SKIP_DIRS = new Set(['.venv', '.pio', '__pycache__', 'build', 'dist', '.git']);
const SKIP_FILES = new Set(['.env']);

const files = {};
function walk(dir) {
  for (const name of readdirSync(dir)) {
    const full = join(dir, name);
    if (statSync(full).isDirectory()) {
      if (!SKIP_DIRS.has(name)) walk(full);
    } else if (!SKIP_FILES.has(name) && !name.endsWith('.pyc')) {
      files[`${SOURCE}/${relative(SOURCE, full).split(sep).join('/')}`] = readFileSync(full);
    }
  }
}
walk(SOURCE);

mkdirSync('public/downloads', { recursive: true });
writeFileSync(OUTPUT, zipSync(files, { level: 9 }));
console.log(`${OUTPUT}: ${Object.keys(files).length} arquivos`);
