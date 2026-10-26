// Part 1 uses the retained SE course DOCX; other reports keep their own layout.
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';
const here = path.dirname(fileURLToPath(import.meta.url));
const python = '/home/towfienes/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python';
execFileSync(python, [path.join(here, 'build-part1.py')], { stdio: 'inherit' });
