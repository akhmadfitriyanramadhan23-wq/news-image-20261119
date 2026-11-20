// news-image-20261119 — one image summing up Thursday 19 November 2026.
// This entry's program copies the front-page infographic stored beside it
// (entry.png, drawn by tools/make-image.py from that day's verified news)
// to the grader's output directory as /output/entry.png. The copy is
// byte-for-byte and deterministic: no network, no randomness, no image
// generation at run time, so two runs always write the same file.
// The program also makes sure the output directory exists first, so it
// works whether the grader hands it a fresh directory or a reused one,
// and reports the path and size it wrote for the run log.
//
// A working news-image-daily entry (Node 22, standard library only): its image is the entry.png beside this file, and
// the program copies it to /output/entry.png. A starting point, not a winner: replace the image. The gate takes a
// whole PNG or JPEG of at most 1 MiB and 1024 by 1024 pixels, and the judge sees exactly the bytes copied.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync, statSync } from 'node:fs';
import { join } from 'node:path';

const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
if (!existsSync(outputDir)) mkdirSync(outputDir, { recursive: true });
const outputPath = join(outputDir, 'entry.png');
copyFileSync(new URL('./entry.png', import.meta.url), outputPath);
console.log(`wrote ${outputPath} (${statSync(outputPath).size} bytes)`);
