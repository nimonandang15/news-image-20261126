// news-image-20261126 — "The World in One Day", Thursday 26 November 2026.
//
// A dense broadsheet front page: masthead with story counts, five stat
// tiles, three lead stories with drawn scenes (Gulf refinery under a
// drone, Kyiv skyline under missile streaks, Gaza at dusk), a 12-story
// grid, a world map of where it happened, an also-on list and a
// date-check footer. The poster is entry.png beside this file, drawn
// for this competition by render.py; this program copies it, byte for
// byte, to /output/entry.png, after proving it is a whole PNG inside
// the gate limits (at most 1 MiB, at most 1024 by 1024 pixels).
// Deterministic: the same entry.png always yields the same output
// bytes, and the program never touches the network. Node 22,
// standard library only.
//
// Local check:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { createHash } from 'node:crypto';
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const MAX_BYTES = 1048576;
const MAX_SIDE = 1024;
const PNG_MAGIC = Buffer.from([
  0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a,
]);
const IHDR = Buffer.from('IHDR');
const IEND = Buffer.from('IEND');

function reject(message) {
  throw new Error(`entry.png rejected: ${message}`);
}

function loadAndCheck() {
  const bytes = readFileSync(new URL('./entry.png', import.meta.url));
  if (bytes.length > MAX_BYTES) {
    reject(`is ${bytes.length} bytes, over the 1 MiB limit`);
  }
  if (bytes.length < 8 + 25) {
    reject('is too short to hold a PNG header and IEND chunk');
  }
  if (!bytes.subarray(0, 8).equals(PNG_MAGIC)) {
    reject('does not start with the PNG signature');
  }
  if (!bytes.subarray(12, 16).equals(IHDR)) {
    reject('has no IHDR chunk right after the signature');
  }
  if (bytes.readUInt32BE(8) !== 13) {
    reject(`has an IHDR chunk of ${bytes.readUInt32BE(8)} bytes, not 13`);
  }
  const width = bytes.readUInt32BE(16);
  const height = bytes.readUInt32BE(20);
  if (width === 0 || height === 0) {
    reject('has a zero dimension');
  }
  if (width > MAX_SIDE || height > MAX_SIDE) {
    reject(`is ${width}x${height}, over the 1024x1024 limit`);
  }
  // Walk the chunk chain: every chunk must fit inside the file, and
  // the chain must end exactly at the file's last byte with IEND.
  // (A plain tail check would miss a truncated middle; the walk
  // proves the file is whole, chunk by chunk.)
  let pos = 8;
  let sawIend = false;
  while (pos + 8 <= bytes.length) {
    const len = bytes.readUInt32BE(pos);
    const type = bytes.subarray(pos + 4, pos + 8);
    const end = pos + 12 + len;
    if (end > bytes.length) {
      reject(`chunk ${type.toString('latin1')} at ${pos} runs past the file`);
    }
    if (type.equals(IEND)) {
      if (len !== 0 || end !== bytes.length) {
        reject('IEND is not the final 12 bytes of the file');
      }
      sawIend = true;
      break;
    }
    pos = end;
  }
  if (!sawIend) {
    reject('no complete IEND chunk found (truncated?)');
  }
  return { bytes, width, height };
}

const { bytes, width, height } = loadAndCheck();

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
const outPath = join(outDir, 'entry.png');
writeFileSync(outPath, bytes);

// Read the output back: a partial or corrupted write must fail loudly.
if (!readFileSync(outPath).equals(bytes)) {
  reject('output differs from entry.png after writing');
}

const sha256 = createHash('sha256').update(bytes).digest('hex');
console.log(`wrote entry.png: ${width}x${height}, ${bytes.length} bytes, sha256 ${sha256}`);
