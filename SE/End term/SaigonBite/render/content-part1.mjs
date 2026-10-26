// Content of the Part 1 deliverable: Proposal & Requirements Engineering.
// Structured blocks are rendered to HTML by build.mjs, which also derives the TOC and LOF.
import fs from 'node:fs';
import { signatureBlock } from './signatures.mjs';
export const register = JSON.parse(fs.readFileSync(new URL('../config/part1.json', import.meta.url), 'utf8'));

const team = JSON.parse(
  fs.readFileSync(new URL('../config/team.json', import.meta.url), 'utf8'));

const TBD = '<span class="tbd">TBD</span>';
const tbd = (v) => (!v || v === 'TBD' ? TBD : v);

const COVER = {
  confederation: '0.75mm', university: '8.71mm', faculty: '16.49mm',
  logoTop: '29.96mm', logoLeft: '56.86mm',
  author1: '65.53mm', author2: '71.20mm',
  finalReport: '102.95mm', course: '128.41mm',
  advised: '188.18mm', instructor: '195.97mm',
  cityOuter: '190.47mm', cityInner: '212.02mm',
};
const LOGO = 'width:41.29mm;height:22.86mm;position:absolute;';

/** Author block: one line per known member, a single TBD line when a member is unknown. */
function authorLines() {
  const known = team.members
    .filter((m) => m.full_name !== 'TBD' || m.student_id !== 'TBD')
    .map((m) => `${m.full_name} – ${m.student_id === 'TBD' ? 'TBD' : m.student_id}`);
  const unknown = team.members.filter(
    (m) => m.full_name === 'TBD' && m.student_id === 'TBD').length;
  if (unknown) known.push('TBD');
  return known.join('<br/>');
}

const coverOuter = () => `
<div class="cover">
  <div class="blk" style="top:${COVER.confederation};font-size:14pt;">VIETNAM GENERAL CONFEDERATION OF LABOR</div>
  <div class="blk" style="top:${COVER.university};font-size:14pt;font-weight:bold;">TON DUC THANG UNIVERSITY</div>
  <div class="blk" style="top:${COVER.faculty};font-size:14pt;font-weight:bold;">FACULTY OF INFORMATION TECHNOLOGY</div>
  <img class="blk" src="${logoDataUri()}" style="top:${COVER.logoTop};left:${COVER.logoLeft};${LOGO}" alt="TDTU logo"/>
  <div class="blk" style="top:${COVER.author1};font-size:14pt;font-weight:bold;text-transform:uppercase;">${authorLines()}</div>
  <div class="blk" style="top:${COVER.finalReport};font-size:24pt;font-weight:bold;">FINAL REPORT</div>
  <div class="blk" style="top:${COVER.course};font-size:22pt;font-weight:bold;text-transform:uppercase;">SOFTWARE ENGINEERING</div>
  <div class="blk" style="top:146.0mm;font-size:14pt;font-weight:bold;text-transform:uppercase;">${team.project.name}</div>
  <div class="blk" style="top:153.0mm;font-size:13pt;">${team.project.tagline}</div>
  <div class="blk" style="top:163.0mm;font-size:13pt;font-style:italic;">Part 1: Project Proposal and Requirements Engineering</div>
  <div class="blk" style="top:171.0mm;font-size:13pt;font-weight:bold;">Technology Tier: ${team.project.tier} (maximum ${team.project.tier_cap.toFixed(1)})</div>
  <div class="blk" style="top:${COVER.cityOuter};font-size:14pt;font-weight:bold;">${team.project.city_year}</div>
</div>`;

const coverInner = () => `
<div class="cover">
  <div class="blk" style="top:${COVER.confederation};font-size:14pt;">VIETNAM GENERAL CONFEDERATION OF LABOR</div>
  <div class="blk" style="top:${COVER.university};font-size:14pt;font-weight:bold;">TON DUC THANG UNIVERSITY</div>
  <div class="blk" style="top:${COVER.faculty};font-size:14pt;font-weight:bold;">FACULTY OF INFORMATION TECHNOLOGY</div>
  <img class="blk" src="${logoDataUri()}" style="top:${COVER.logoTop};left:${COVER.logoLeft};${LOGO}" alt="TDTU logo"/>
  <div class="blk" style="top:${COVER.author1};font-size:14pt;font-weight:bold;text-transform:uppercase;">${authorLines()}</div>
  <div class="blk" style="top:${COVER.finalReport};font-size:24pt;font-weight:bold;">FINAL REPORT</div>
  <div class="blk" style="top:${COVER.course};font-size:22pt;font-weight:bold;text-transform:uppercase;">SOFTWARE ENGINEERING</div>
  <div class="blk" style="top:146.0mm;font-size:14pt;font-weight:bold;text-transform:uppercase;">${team.project.name}</div>
  <div class="blk" style="top:153.0mm;font-size:13pt;">${team.project.tagline}</div>
  <div class="blk" style="top:163.0mm;font-size:13pt;font-style:italic;">Part 1: Project Proposal and Requirements Engineering</div>
  <div class="blk" style="top:171.0mm;font-size:13pt;font-weight:bold;">Technology Tier: ${team.project.tier} (maximum ${team.project.tier_cap.toFixed(1)})</div>
  <div class="blk" style="top:${COVER.advised};font-size:14pt;">Advised by</div>
  <div class="blk" style="top:${COVER.instructor};font-size:14pt;font-weight:bold;text-transform:uppercase;">${team.instructor.honorific ? team.instructor.honorific + ' ' : ''}${team.instructor.full_name}${team.instructor.title ? ', ' + team.instructor.title : ''}</div>
  <div class="blk" style="top:${COVER.cityInner};font-size:14pt;font-weight:bold;">${team.project.city_year}</div>
</div>`;

function logoDataUri() {
  try {
    const p = '/home/towfienes/TDTU/docs/report-reference/tdtu-logo.png';
    return 'data:image/png;base64,' + fs.readFileSync(p).toString('base64');
  } catch { return ''; }
}

// ---------------------------------------------------------------- front matter
const signoff = () => signatureBlock(team.members.map(m => m.full_name), team.project.report_date);

const acknowledgement = () => `
<h1 class="centered">ACKNOWLEDGEMENT</h1>
<p>We thank our lecturer, ${team.instructor.honorific} ${team.instructor.full_name}, for the SaigonBite case study, project specification and student survival guide. These materials define the business problem and the engineering decisions that this proposal must address.</p>
<p>This report sets out the proposed scope, individual use case ownership, measurable requirements and working assumptions for Part 1. We acknowledge the course sources in REFERENCES and disclose assistance from generative AI in Appendix A.</p>
${signoff()}`;
const declaration = () => `
<h1 class="centered">DECLARATION OF AUTHORSHIP</h1>
<p>We submit this Part 1 proposal for Software Engineering, Sem01_2627, Ton Duc Thang University. The business rules BR1–BR18 originate from the course specification; our refined requirements and working assumptions are identified separately.</p>
<p>Generative AI assistance and the availability of supporting records are disclosed in Appendix A. The traceability matrix describes planned design and verification work; it does not certify that the application or its tests have passed.</p>
<p style="font-weight:bold">The team is responsible for checking the submitted content, explaining its requirements and decisions, and declaring all assistance. No signatures, instructor approvals or execution results are supplied on behalf of the members.</p>
${signoff()}`;

const p = (text) => ({ t: 'p', text });
const h = (text) => ({ t: 'h3', text });
const table = (head, rows, widths = ['25%', '75%']) => ({ t: 'table', head, rows, widths });
const chapter = (number, title, blocks) => ({ id: 'ch' + number, kind: 'chapter', number, title, blocks });
const figArchitecture = `<svg viewBox="0 0 440 290" xmlns="http://www.w3.org/2000/svg" font-family="Times New Roman" font-size="17.4">
<rect x="1" y="1" width="438" height="72" fill="#e8f0fb" stroke="#315a82"/>
<text x="18" y="26" font-weight="bold">Presentation: MVC controllers and views</text><text x="18" y="51">Bootstrap; English / Vietnamese interface</text>
<path d="M220 73 V98 m-5 -7 l5 7 5 -7" fill="none" stroke="#333"/>
<rect x="1" y="99" width="438" height="91" fill="#eaf6ea" stroke="#347348"/>
<text x="18" y="124" font-weight="bold">Business: pricing and order lifecycle</text><text x="18" y="150">OrderService; payment Strategies; reports</text><text x="18" y="175">Admission, availability and actor checks</text>
<path d="M220 190 V215 m-5 -7 l5 7 5 -7" fill="none" stroke="#333"/>
<rect x="1" y="216" width="438" height="72" fill="#fdf3e3" stroke="#a86a12"/>
<text x="18" y="242" font-weight="bold">Data: EF Core Code-First and SQL Server</text><text x="18" y="267">Price snapshots; soft deletion; audit history</text></svg>`;
const figTrace = `<svg viewBox="0 0 440 100" xmlns="http://www.w3.org/2000/svg" font-family="Times New Roman" font-size="17.4"><rect x="1" y="1" width="438" height="98" fill="#e8f0fb" stroke="#315a82"/><text x="220" y="30" text-anchor="middle">FR / NFR and source rule</text><text x="220" y="57" text-anchor="middle">Use case and owner → planned design / code</text><text x="220" y="84" text-anchor="middle">Acceptance test → actual result in Part 3</text></svg>`;
const ch1 = () => chapter(1, 'INTRODUCTION', [
 h('1.1 Problem Statement'),
 p('SaigonBite is a planned network of delivery-only kitchens in Ho Chi Minh City. Each hub operates several virtual food brands. Customers need one place to browse a hub’s menu, see a transparent price, pay and track an order; staff need a controlled process from placement to delivery.'),
 p('The client faces uneven kitchen demand and two customer groups with different identity and payment needs. Quiet kitchens should attract demand through a discount, while hubs at or above 90% load must refuse new orders. Pricing, payment eligibility and status transitions must be enforced consistently on the server, not left to interface behaviour.'),
 h('1.2 Customers and Stakeholders'),
 p('Local Customers register with a Vietnamese phone number and simulated OTP and use MoMo, VNPay or COD. Foreign Tourists register with passport, nationality, email and a simulated email code and use Apple Pay, PayPal or COD. Kitchen Staff work at one hub; assigned Shippers perform delivery; System Admins manage catalogue, capacity, vouchers, accounts, rain settings and reports. The two customer types share one database schema.'),
 h('1.3 Scope and Deliverables'),
 p('Part 1 contains the proposal, requirements baseline, measurable quality attributes, working ambiguity decisions and an initial traceability matrix. It proposes three main CRUD use cases, with secondary scopes covering the remaining system functions. R1 Revenue and R2 Hub Utilization are mandatory. Detailed UML, the Figma prototype, implementation, sandbox evidence and execution results belong to subsequent parts.'),
 p('Sources: Project Specification sections 1–4 and Case Study sections 1–4. Requirements are proposed obligations, not claims that implementation is complete.')]);
const ch2 = () => chapter(2, 'PROJECT PROPOSAL', [
 h('2.1 SDLC Methodology and Schedule'),
 p('We propose Scrum with a prioritised backlog, a short daily coordination meeting, reviews at deliverable milestones and retrospectives after each review. The integration lead coordinates priorities; all three members develop and review their owned scopes. This lightweight allocation suits a three-person academic team and allows the Week 5 change request to enter the backlog without obscuring existing requirements.'),
 table(['Period', 'Goal and milestone'], [
 ['Weeks 1–2', 'Analyse requirements, assign ownership and agree the proposed tier. Part 1 report, workbook and pitch due 26 Oct 2026, 07:00 UTC+7.'],
 ['Weeks 3–4', 'Model assigned use cases, architecture, state machine and Figma UI. Part 2 due 9 Nov 2026, 07:00 UTC+7.'],
 ['Weeks 5–6', 'Show a running skeleton at the Week 5 checkpoint; analyse the issued change request; implement and test the use cases.'],
 ['Week 7', 'Complete Part 3 code/QA, traceability and product demo. Deadline: 30 Nov 2026, 07:00 UTC+7.'],
 ['Final consolidation', 'Apply feedback and compile the final report/video. Survival Guide separately lists 7 Dec 2026; confirm the final portal instruction when published.']]),
 p('The analysis-to-Part-3 plan spans seven weeks. The separate final consolidation date is not represented as an additional week inside those seven weeks. The current Part 1 portal deadline takes precedence for this submission.'),
 h('2.2 Team Roles and Ownership'),
 table(['Member', 'Main use case, role and secondary scope'],team.members.map(m=>[`${m.full_name}<br/>${m.student_id}`, `${m.use_case} — ${m.use_case_title}. ${m.secondary_scope.join('; ')}. Reports: ${m.reports_owned.join('; ') || 'none; owns shared pricing/payment infrastructure'}.`]),['31%','69%']),
 p('Ngô Lâm Tiến (524H0195) is the named owner of D and the shared pricing/payment interface. Nguyễn Công Thành (524H0191) owns A and R1. Nguyễn Trọng Phú (524H0179) owns B and R2. Secondary scopes C, E and F remain assigned to these same owners. Each member must claim the main use case in the live pitch; this assignment is planned responsibility, not evidence of completed contribution.'),
 h('2.3 Complete CRUD Boundaries'),
 table(['Use case', 'Create, Read, Update and Delete meaning'],[
 ['D — Orders', 'Create a priced order; read/track owned orders; edit items only in Placed; cancel in Placed or Confirmed. Delete means business cancellation, preserving history.'],
 ['A — Menu and Brands', 'Create brands and menu items; browse/filter; edit details and availability; soft-delete brands/items while preserving historical order data.'],
 ['B — Hubs and Capacity', 'Create hubs with positive integer capacity; read hubs/current load; edit address and capacity; soft-delete hubs while preserving order/report history.']]),
 h('2.4 Proposed Tier and Architecture'),
 p('The instructor technology-tier table supplied for this revision gives the ceilings below. These are maximum scores, not awarded marks. Source: instructor table archived at docs/references/instructor-technology-tiers.png; supplied by the student on 24 Oct 2026.'),
 table(['Tier','Max /10','Required stack and architecture'],register.technology.tiers.map(r=>[r.tier,r.cap.toFixed(1),r.stack]),['16%','17%','67%']),
 p(`The proposed target remains ${team.project.tier}, with a ${team.project.tier_cap.toFixed(1)}/10 ceiling: the full Tier 3 foundation plus all three Tier 4 additions. We propose ASP.NET Core MVC (.NET 8), EF Core Code-First, SQL Server and Bootstrap 5. The table names ASP.NET MVC and Entity Framework without explicitly naming Core; instructor confirmation of this variant is pending. No approval or score is inferred. A mock payment does not meet the live sandbox criterion; the Tier 3 ceiling of 9.5 applies only when its foundation is accepted and delivered.`),
 table(['Tier criterion','Planned delivery, owner and acceptance evidence'],register.technology.acceptance.map(r=>[r.criterion,`${r.plan}<br/><b>Owner:</b> ${r.owner}.<br/><b>Evidence:</b> ${r.evidence}<br/><b>Trace:</b> ${r.references}. Status: Planned.`]),['25%','75%']),
 p('.NET 8 is retained as the existing project baseline. Microsoft lists end of support on 10 Nov 2026, before later submission dates. The team must record this lifecycle risk and obtain agreement on any runtime update; this proposal does not silently change the stack.'),
 {t:'figure',caption:'Figure 2.4.1: Proposed layers and their responsibilities',svg:figArchitecture},
 p('Pricing is a pure calculation over validated input and the placement snapshot. Availability, hub membership and authorisation checks belong to business services before pricing; BR12 does not require database lookups inside the arithmetic function. Payment Strategies are selected by actor type. A state transition and its audit record should be committed together.'),
 h('2.5 Risks and Definition of Done'),
 {t:'ul',items:['Sandbox credentials and external availability: arrange access early; keep a clearly labelled simulated fallback, but claim Tier 4 only with real sandbox evidence.','Change request: assess its scope in Week 5. The one-class/one-registration objective applies to a new payment method, not every possible change.','Each requirement keeps a stable ID, source, owner and acceptance test. Design and test evidence must be linked before a requirement can receive a PASS verdict.','Plan at least 20 EP/BVA cases covering numeric thresholds in BR1–BR12 and BR14, plus at least five forbidden-transition tests; final counts and outcomes must come from execution.']}]);
const groups=[['A','3.1 Manage Menu and Brands'],['B','3.2 Manage Hubs and Capacity'],['C','3.3 Manage Vouchers'],['D','3.4 Place and Manage Orders'],['E','3.5 Manage User Accounts'],['F','3.6 Manage Deliveries'],['P','3.7 Payments'],['R','3.8 Mandatory Reports'],['S','3.9 Cross-cutting Requirements']];
const ch3=()=>chapter(3,'FUNCTIONAL REQUIREMENTS',[
 p('All amounts are VND. Time windows use Vietnam local time (UTC+7); start is inclusive and end exclusive. Each requirement below cites its source. R1/R2 and NFR sources are cited directly where no separate BR defines the capability. Group letters identify requirement families; the RTM gives the accountable use case and owner.'),
 ...groups.flatMap(([group,title])=>[h(title),...register.fr.filter(r=>r.id[3]===group).map(r=>({t:'requirement',...r}))]),
 h('3.10 Order Lifecycle Acceptance Baseline'),
 table(['From → To', 'Allowed actor and condition'],[
 ['Placed → Confirmed', 'Kitchen Staff at the order’s hub.'],['Placed → Cancelled','Customer; or Kitchen Staff at the hub with a rejection reason.'],['Confirmed → Preparing','Kitchen Staff at the order’s hub.'],['Confirmed → Cancelled','Customer or Admin.'],['Preparing → Ready','Kitchen Staff at the order’s hub.'],['Ready → Out for Delivery','Assigned Shipper; a shipper must already be assigned.'],['Out for Delivery → Delivered','Assigned Shipper; COD cash must be confirmed first.'],['Out for Delivery → Failed','Assigned Shipper; customer unreachable.']]),
 p('All other transitions are forbidden, including transitions from Delivered, Cancelled and Failed. Staff and shippers must be authorised for the specific order. Source: Specification section 2C, BR14–BR16.'),
 {t:'raw',html:'<div class="keep-section">'},h('3.11 Pricing Precision and Boundary Checks'),
 p('The nine BR10 steps are: subtotal S; Quiet Kitchen Q; voucher V; food F; delivery D and waiver; rush R; rain R2; raw sum; final half-up rounding. Preserve fractional discounts until the final rounding. With S=200,000, load=20%, d=3.2 km, time=15:00, rain off and no voucher, the specification gives Q=20,000, D=25,000 and rounded total=205,000.'),
 p('Precision acceptance case: S=61,111, load=20%, a valid 10% voucher without a binding cap, d=1 km, outside rush and no rain. Q=6,111.1; V=5,499.99; raw=64,499.91; rounded total=64,000. Truncating Q/V would incorrectly produce 65,000. This is an independently calculated acceptance example, not an application execution result.'),
 p('Boundary tests must include 49,999/50,000; 2/2.01, 5/5.01 and 8/8.01 km; the inclusive/exclusive rush endpoints; 299,999/300,000; loads just below/at 30% and 90%; voucher dates/minimum/cap; line and quantity limits; half-thousand totals; and COD 1,000,000/1,001,000.'),{t:'raw',html:'</div>'}]);
const ch4=()=>chapter(4,'QUALITY ATTRIBUTES',[
 p('NFR1–NFR4 refine the mandatory Case Study baselines; NFR5 and NFR6 are team-defined. These are measurable acceptance obligations. Their status is Planned; no application benchmark or role test is certified by this Part 1 report.'),
 ...register.nfr.flatMap((r,i)=>[{t:'raw',html:'<div class="keep-section">'},h(`4.${i+1} ${r.id} ${r.attribute}`),p(r.target),p(`<b>Verification:</b> ${r.verification}`),p(`<b>Source and ownership:</b> ${r.source}; UC ${r.use_case}; ${r.owner}.`),{t:'raw',html:'</div>'}]),
 h('4.7 Design Implications'),p('A pure pricing component supports deterministic tests and isolates I/O from the calculation. MVC separates interface, business services and persistence. Payment Strategies meet the extension constraint. Server-side role/resource checks support NFR4; append-only history and recorded price snapshots support NFR5/NFR6 and the preparation-time calculation in R2.')]);
const ch5=()=>chapter(5,'AMBIGUITY LOG',[
 p('The following are working assumptions, not instructor approvals. The Specification is authoritative for fixed rules; an ambiguity cannot override a stated threshold, calculation order or transition. The same A IDs are used in the workbook and pitch.'),
 ...register.ambiguities.flatMap((r,i)=>[h(`5.${i+1} ${r.id} ${r.topic}`),p(`<b>Gap:</b> ${r.gap}`),p(`<b>Assumption:</b> ${r.assumption}`),p(`<b>Impact:</b> ${r.impact}`),p(`<b>Instructor answer/status:</b> ${r.answer}`)]),
 p('Changes to these assumptions require updating affected FRs, design mappings and acceptance tests. The current portal screenshot names SaigonBite consistently; no product-name conflict is asserted. BR3’s distance discontinuity and BR11’s final-only rounding are fixed rules, not open assumptions.')]);
const ch6=()=>chapter(6,'REQUIREMENTS TRACEABILITY MATRIX',[
 h('6.1 Purpose and Status'),p(`The seed matrix contains ${register.fr.length} FRs and ${register.nfr.length} NFRs. Every row has an accountable use case, planned implementation mapping and acceptance test reference. Component names are proposed mappings, to be reconciled with Part 2 design and Part 3 code. All verification verdicts remain Planned; tests listed here have not been executed as part of Part 1.`),
 {t:'figure',caption:'Figure 6.1.1: Traceability from source requirement to later verification',svg:figTrace},
 h('6.2 Functional Requirement Mappings'),
 table(['Requirement', 'Planned trace and acceptance test'],register.fr.map(r=>[r.id,`UC ${r.use_case}; owner ${r.owner}. Source: ${r.source}.<br/>Design: ${r.design}; code: ${r.component}.<br/>Tests: ${r.test}. Verdict: Planned.`]),['19%','81%']),
 h('6.3 Quality Attribute Mappings'),table(['Requirement','Planned trace and acceptance test'],register.nfr.map((r,i)=>[r.id,`UC ${r.use_case}; owner ${r.owner}. Source: ${r.source}.<br/>Design/code: ${['pure PricingEngine','IPaymentStrategy and registration','responsive views and localisation','identity and authorisation policies','audit/history writer','state machine and pricing snapshot'][i]}.<br/>Test: TC-NFR-${i+1}. ${r.verification} Verdict: Planned.`]),['19%','81%']),
 h('6.4 Change Control'),p('The report and workbook are generated from config/part1.json. Every new or changed ID must appear in both and keep its source/owner/test mapping. Part 2 adds approved diagrams; Part 3 records actual components, execution evidence and PASS/FAIL verdicts. A test identifier is a plan until its execution record exists.')]);
const appendixA=()=>({id:'apxA',kind:'appendix',title:'APPENDIX A. GENERATIVE AI USAGE LOG',blocks:[
 p('AI assistance is disclosed below using the columns required by Specification section 7. Historical DSH activity is summarised from the existing project log; its original full prompts and outputs have not been located in this workspace. The team must recover the original records for the instructor’s 48-hour request requirement. A reconstructed summary must not be represented as an original transcript.'),
 ...register.ai.flatMap((r,i)=>[h(`A.${i+1} ${r.tool}`),table(['Required field','Disclosure'],[['Tool and date',r.tool],['Purpose',r.purpose],['Prompt (summary)',r.prompt],['What was kept or changed',r.kept],['How verified',r.verification]],['30%','70%'])]),
 p('The available Codex request excerpts and work summary are retained in docs/appendix/prompts/CODEX_2026-10-24.md; that file is labelled as excerpts and a summary. No full historical transcript or unrecorded human review is claimed.') ]});
const appendixB=()=>({id:'apxB',kind:'appendix',title:'APPENDIX B. CONTRIBUTION STATEMENT',blocks:[p('Planned responsibility is set out below. The course requires a statement signed by all members at the start of Part 3. Signatures, dates and actual contribution percentages must be supplied by the members; none are generated here.'),table(['Member','Planned responsibility'],team.members.map(m=>[`${m.full_name}<br/>${m.student_id}`,`Main UC ${m.use_case}: ${m.use_case_title}. Secondary: ${m.secondary_scope.join('; ')}. Reports: ${m.reports_owned.join('; ') || 'none'}.`]),['31%','69%']),...team.members.map(m=>p(`${m.full_name} (${m.student_id})<br/>Signature: ____________________ Date: ______________`))]});
const references=()=>({id:'refs',kind:'references',title:'REFERENCES',blocks:[
 {t:'ref',text:'Ton Duc Thang University, Faculty of Information Technology (2026). <i>SE Final Project Specification: SaigonBite</i>, version 1.0, Sem01_2627. BR1–BR18, Part 1 checklist and rubric.'},
 {t:'ref',text:'Ton Duc Thang University (2026). <i>SaigonBite Case Study: Cloud-Kitchen Food Delivery Hub</i>, Sem01_2627. Context, FR1–FR9 and quality baselines.'},
 {t:'ref',text:'Ton Duc Thang University (2026). <i>SaigonBite Student Survival Guide</i>, Sem01_2627. Milestones and presentation guidance.'},
 {t:'ref',text:'Course instructor. <i>Technology tiers (from the specification; the instructor may edit the blue caps)</i>. Image supplied by the student on 24 Oct 2026; publication date not shown. Archived at docs/references/instructor-technology-tiers.png. Current ceilings: 7.0, 7.5, 8.5, 9.5 and 10.0.'},
 {t:'ref',text:'Schwaber, K. and Sutherland, J. (2020). <i>The Scrum Guide</i>. https://scrumguides.org/scrum-guide.html. Basis for the proposed iterative process.'},
 {t:'ref',text:'Microsoft (2026). <i>.NET 8 and .NET 9 will reach End of Support on November 10, 2026</i>. https://devblogs.microsoft.com/dotnet/dotnet-8-9-end-of-support/. Runtime lifecycle risk.'}
]});
export const part1={team,coverOuter,coverInner,front:[{id:'ack',html:acknowledgement},{id:'dec',html:declaration}],body:[ch1,ch2,ch3,ch4,ch5,ch6,appendixA,appendixB,references]};
