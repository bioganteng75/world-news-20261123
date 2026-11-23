// Entry for make.fun's "Sum up 23 November's world news in one image" bounty.
//
// The picture itself is entry.png beside this file: a front-page composition
// drawn by compose.py from four illustrated panels plus the day's headlines.
// This program's only job is to deliver those exact bytes to the grader:
// it copies entry.png to the output directory as entry.png, byte for byte,
// so both of the grader's runs produce an identical file.
//
// Node 22, standard library only, no network. Locally, MAKEFUN_OUTPUT_DIR
// stands in for the grader's /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outputDir, { recursive: true });

const source = new URL("./entry.png", import.meta.url);
copyFileSync(source, join(outputDir, "entry.png"));
