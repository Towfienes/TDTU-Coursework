// Shared front matter: covers, acknowledgement, declaration.
// Part 1 keeps its own frozen copy; Parts 2 and 3 use this module.
import fs from 'node:fs';

export const team = JSON.parse(
  fs.readFileSync(new URL('../config/team.json', import.meta.url), 'utf8'));

const TBD = '<span class="tbd">TBD</span>';
const tbd = (v) => (!v || v === 'TBD' ? TBD : v);

const COVER = {
  confederation: '0.75mm', university: '8.71mm', faculty: '16.49mm',
  logoTop: '29.96mm', logoLeft: '56.86mm',
  author1: '65.53mm', finalReport: '102.95mm', course: '128.41mm',
  advised: '188.18mm', instructor: '195.97mm',
  cityOuter: '190.47mm', cityInner: '212.02mm',
};
const LOGO = 'width:41.29mm;height:22.86mm;position:absolute;';

function logoDataUri() {
  try {
    return 'data:image/png;base64,' + fs.readFileSync(
      '/home/towfienes/TDTU/docs/report-reference/tdtu-logo.png').toString('base64');
  } catch { return ''; }
}

export function authorLines() {
  const known = team.members
    .filter((m) => m.full_name !== 'TBD' || m.student_id !== 'TBD')
    .map((m) => `${m.full_name} – ${m.student_id === 'TBD' ? 'TBD' : m.student_id}`);
  if (team.members.some((m) => m.full_name === 'TBD' && m.student_id === 'TBD')) known.push('TBD');
  return known.join('<br/>');
}

const byline = (partLabel) => `
  <img class="blk" src="${logoDataUri()}" style="top:${COVER.logoTop};left:${COVER.logoLeft};${LOGO}" alt="TDTU logo"/>
  <div class="blk" style="top:${COVER.author1};font-size:14pt;font-weight:bold;text-transform:uppercase;">${authorLines()}</div>
  <div class="blk" style="top:${COVER.finalReport};font-size:24pt;font-weight:bold;">FINAL REPORT</div>
  <div class="blk" style="top:${COVER.course};font-size:22pt;font-weight:bold;text-transform:uppercase;">${team.project.course_cover || 'SOFTWARE ENGINEERING'}</div>
  <div class="blk" style="top:146.0mm;font-size:14pt;font-weight:bold;text-transform:uppercase;">${team.project.name}</div>
  <div class="blk" style="top:153.0mm;font-size:13pt;">${team.project.tagline}</div>
  <div class="blk" style="top:163.0mm;font-size:13pt;font-style:italic;">${partLabel}</div>
  <div class="blk" style="top:171.0mm;font-size:13pt;font-weight:bold;">Technology Tier: ${team.project.tier} (maximum ${team.project.tier_cap.toFixed(1)})</div>`;

const masthead = `
  <div class="blk" style="top:${COVER.confederation};font-size:14pt;">VIETNAM GENERAL CONFEDERATION OF LABOR</div>
  <div class="blk" style="top:${COVER.university};font-size:14pt;font-weight:bold;">TON DUC THANG UNIVERSITY</div>
  <div class="blk" style="top:${COVER.faculty};font-size:14pt;font-weight:bold;">FACULTY OF INFORMATION TECHNOLOGY</div>`;

export const coverOuter = (partLabel) => `
<div class="cover">${masthead}${byline(partLabel)}
  <div class="blk" style="top:${COVER.cityOuter};font-size:14pt;font-weight:bold;">${team.project.city_year}</div>
</div>`;

export const coverInner = (partLabel) => `
<div class="cover">${masthead}${byline(partLabel)}
  <div class="blk" style="top:${COVER.advised};font-size:14pt;">Advised by</div>
  <div class="blk" style="top:${COVER.instructor};font-size:14pt;font-weight:bold;text-transform:uppercase;">${team.instructor.honorific ? team.instructor.honorific + ' ' : ''}${team.instructor.full_name}${team.instructor.title ? ', ' + team.instructor.title : ''}</div>
  <div class="blk" style="top:${COVER.cityInner};font-size:14pt;font-weight:bold;">${team.project.city_year}</div>
</div>`;

export const acknowledgement = (partLabel) => `
<h1 class="centered">ACKNOWLEDGEMENT</h1>
<p>We thank our lecturer for the Introduction to Software Engineering course, whose specification
made the boundary between the client's requirements and our own design decisions explicit, and the
Faculty of Information Technology at Ton Duc Thang University for the laboratory environment in
which the work was built.</p>
<p>This part of the report, ${partLabel}, was reviewed by all three members before submission. Where
we disagreed on a structural decision, the disagreement and its resolution are recorded in the
design justification rather than smoothed over.</p>
<div style="margin-top:24pt;text-align:right;font-size:13pt;font-style:italic;">
  Ho Chi Minh City, ${tbd(team.project.report_date)}<br/>
  ${team.members.map((m) => m.full_name).join(' · ')}
</div>`;

export const declaration = () => `
<h1 class="centered">DECLARATION OF AUTHORSHIP</h1>
<p>We declare that this report is our own work, produced for the Introduction to Software Engineering
final project in the semester Sem01_2627 at Ton Duc Thang University.</p>
<p>Every diagram, table and class in this document was drawn or written by the team and checked
against the requirement identifiers defined in Part 1. Generative artificial intelligence was used as
a drafting assistant and is declared in Appendix A of the consolidated report.</p>
<p style="font-weight:bold;">We take full responsibility for the content of this report. Any
fabrication of data, results or authorship would be a breach of academic integrity, and we confirm
that none exists in this document.</p>
<div style="margin-top:24pt;text-align:right;font-size:13pt;font-style:italic;">
  Ho Chi Minh City, ${tbd(team.project.report_date)}<br/>
  ${team.members.map((m) => m.full_name).join(' · ')}
</div>`;
