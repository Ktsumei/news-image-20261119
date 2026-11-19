// The World in One Day — 19 November 2026 (Node 22, standard library only).
// The image is entry.png beside this file, drawn by draw.py (same directory:
// python3 draw.py regenerates it byte-for-byte, deterministic, no network).
// This program checks the image is a whole PNG within the limits, then
// copies it to /output/entry.png, or to $MAKEFUN_OUTPUT_DIR/entry.png
// outside the grader's container:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const source = new URL('./entry.png', import.meta.url);
const bytes = readFileSync(source);
const MAX_BYTES = 1048576;
if (bytes.length > MAX_BYTES) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB limit`);
}
if (bytes.subarray(0, 8).toString('hex') !== '89504e470d0a1a0a') {
  throw new Error('entry.png is not a PNG');
}
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width > 1024 || height > 1024) {
  throw new Error(`entry.png is ${width}x${height}, over the 1024x1024 limit`);
}
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
copyFileSync(source, join(outDir, 'entry.png'));
console.log(`wrote ${join(outDir, 'entry.png')} (${width}x${height}, ${bytes.length} bytes)`);
