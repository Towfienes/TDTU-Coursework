// Render the Part 2 design document to the TDTU layout.
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildReport } from './build-report.mjs';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const DESIGN = path.resolve(HERE, '..', 'docs', 'part2-design');

const report = await buildReport({
  mdPath: path.join(DESIGN, 'part2.md'),
  diagramsDir: path.join(DESIGN, 'diagrams'),
  outFile: path.join(DESIGN, 'SaigonBite_Part2.pdf'),
  partLabel: 'Part 2: Software Design, Architecture and UI/UX',
});

console.log(JSON.stringify(report, null, 2));
if (report.problems.length) {
  console.error('\nBUILD PROBLEMS:', report.problems.length);
  process.exitCode = 1;
} else {
  console.log('\nOK — layout gates passed');
}
