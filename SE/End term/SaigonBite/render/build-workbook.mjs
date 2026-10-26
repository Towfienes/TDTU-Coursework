// Fill the instructor's original workbook; retain its sheets and input conventions.
import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const runtime = '/home/towfienes/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/package.json';
const { FileBlob, SpreadsheetFile } = await import(createRequire(runtime).resolve('@oai/artifact-tool'));
const data = JSON.parse(await fs.readFile(path.join(root, 'config/part1.json'), 'utf8'));
const team = JSON.parse(await fs.readFile(path.join(root, 'config/team.json'), 'utf8'));
const wb = await SpreadsheetFile.importXlsx(await FileBlob.load(path.resolve(root, '../SE_Sem01_2627_Team_Workbook_Template.xlsx')));
const sheet = name => wb.worksheets.getItem(name);
const put = (name, range, values) => { sheet(name).getRange(range).values = values; };
const fit = (name, range) => { sheet(name).getRange(range).format.autofitRows(); };
const [tien, thanh, phu] = team.members.map(m => m.student_id);
const reviewers = [phu,tien,thanh];
assert.equal(data.fr.length + data.nfr.length, 53);
assert.equal(wb.worksheets.items.length, 14);

put('Team & Tier', 'B4', [[team.project.team_id]]);
put('Team & Tier', 'B5', [[team.project.tier]]);
put('Team & Tier', 'B11:D13', team.members.map((m,i) => [m.full_name, m.student_id, `${m.use_case} owner: ${m.use_case_title}. Planned peer reviewer: ${reviewers[i]}.`]));
put('Team & Tier', 'B18:F23', [
 ['Place and Manage Orders','D','Create; track/read; edit in Placed; cancel in Placed/Confirmed (retain history).','Idea',tien],
 ['Manage Menu & Brands','A','Create; browse/filter; update details/availability; soft-delete.','Idea',thanh],
 ['Manage Hubs & Capacity','B','Create; view load; update address/capacity; soft-delete.','Idea',phu],
 ['Manage Vouchers','C','Create; read; edit; deactivate vouchers. Secondary scope.','Idea',tien],
 ['Manage User Accounts','E','Register; read; edit; deactivate accounts. Secondary scope.','Idea',thanh],
 ['Manage Deliveries','F','Create assignment; read; update delivery status; reassign before dispatch. Secondary scope.','Idea',phu],
 ]);
put('Team & Tier', 'D28', [[tien]]);
fit('Team & Tier','A11:G13'); fit('Team & Tier','A18:G23');

const questions = [
 'May an Admin manually assign an available shipper to a Ready order?',
 'For Failed delivery, should online payments be refunded in full and COD collect no cash?',
 'May we use address text with optional hotel name and room for a tourist?',
 'May we refuse the voucher and request explicit confirmation of the corrected total?',
 'On a Placed edit after a catalogue price change, should existing lines retain recorded prices and new lines use current prices?',
 ];
put('Ambiguity Log','A5:F9',data.ambiguities.map((r,i)=>[r.id,'Ambiguity',`${r.topic}. ${r.gap}`,questions[i],r.assumption,'Draft']));
put('Ambiguity Log','I5:J9',data.ambiguities.map(r=>[r.assumption,r.impact]));
fit('Ambiguity Log','A5:J9');

// The template has 45 slots; extend both linked registers to 53, then move totals.
const req = sheet('Requirements');
const rtm = sheet('RTM');
for (const [s,last] of [[req,'K'],[rtm,'I']]) {
 s.getRange(`A58:${last}60`).copyFrom(s.getRange(`A50:${last}52`),'all');
 s.getRange(`A50:${last}57`).clear({applyTo:'all'});
 for (let row=50;row<=57;row++) s.getRange(`A${row}:${last}${row}`).copyFrom(s.getRange(`A49:${last}49`),'all');
}
const nfrDesign = ['Pure PricingEngine','Payment Strategy and registration','Responsive views and localisation','Identity and authorisation policies','Append-only audit/history writer','Order state machine and price snapshot'];
const records = [
 ...data.fr.map(r=>({...r,kind:'FR',priority:'High',note:`Planned acceptance: ${r.test}. Source: ${r.source}.`,code:r.component})),
 ...data.nfr.map((r,i)=>({...r,kind:'NFR',priority:i<4?'High':'Medium',statement:`${r.attribute}: ${r.target}`,note:`${i<4?'Mandatory baseline':'Team-defined'}. ${r.verification}`,report:r.source.includes('R2')?'R2':'—',design:nfrDesign[i],code:nfrDesign[i],test:`TC-NFR-${i+1}`})),
 ];
// Stable report IDs replace only the template's suggested sequential ID formulas.
put('Requirements','A5:I57',records.map(r=>[r.id,r.statement,r.kind,r.priority,r.use_case,r.source,r.report,r.owner,r.note]));
put('Requirements','K5:K57',records.map(()=>['Draft']));
req.getRange('C59').formulas = [['=COUNTIF(C5:C57,"FR")']];
req.getRange('D59').formulas = [['=COUNTIF(C5:C57,"NFR")']];
req.getRange('D60').formulas = [['=IF(D59>=6,"OK","Need 6")']];
for(const [col,values] of [['C',['FR','NFR']],['D',['High','Medium','Low']],['K',['Draft','Agreed','Built','Tested']]]) {
 req.getRange(`${col}50:${col}57`).dataValidation = {rule:{type:'list',values}};
}
req.getRange('D52').conditionalFormats.deleteAll();
req.getRange('D60').conditionalFormats.addCustom('D60<>"OK"',{font:{bold:true,color:'#9C0006'},fill:'#FDE2E2'});
for(let row=50;row<=57;row++) {
 for(const [col,target] of [['A','A'],['B','B'],['C','E']]) rtm.getRange(`${col}${row}`).formulas = [[`=IF(Requirements!${target}${row}="","",Requirements!${target}${row})`]];
 rtm.getRange(`H${row}`).formulas = [[`=IF(A${row}="","",IF(F${row}="","No test","OK"))`]];
}
put('RTM','D5:G57',records.map(r=>[`Planned: ${r.design}`,`Planned: ${r.code}`,r.test,'Not tested']));
rtm.getRange('C59').formulas = [['=COUNTIF(G5:G57,"Pass")']];
rtm.getRange('C60').formulas = [['=COUNTIF(H5:H57,"No test")']];
rtm.getRange('G50:G57').dataValidation = {rule:{type:'list',values:['Pass','Fail','Not tested']}};
rtm.getRange('H50:H57').conditionalFormats.addCustom('H50="No test"',{font:{bold:true,color:'#9C0006'},fill:'#FDE2E2'});
fit('Requirements','A5:K57'); fit('RTM','A5:I57');

put('Plan & Risks','C5:G11',[
 ['Analyse BR1–BR18; assign D/A/B; draft 47 FR, 6 NFR and 5 ambiguities.',`${tien}, ${thanh}, ${phu}`,'Part 1 report and shared workbook','Planned',`Scrum plan: shared backlog and short daily coordination. Peer review rotation: ${phu} reviews ${tien}; ${tien} reviews ${thanh}; ${thanh} reviews ${phu}. Record findings before milestone review.`],
 ['Review report/workbook; rehearse all 3 speakers and submit the Solution Pitch.',`${tien}, ${thanh}, ${phu}`,'Part 1 report, workbook, 5-slide pitch','Planned','Due 26 Oct 2026, 07:00 UTC+7. Planned speaking time 6:15; rehearsal pending.'],
 ['Model each owned use case; state machine; CRC; class/ERD; MVC and payment Strategy.',`${tien}, ${thanh}, ${phu}`,'Part 2 design draft','Planned','Review mappings from FR/NFR IDs to design elements.'],
 ['Validate Figma screens and UML; present Design Review; apply received feedback.',`${tien}, ${thanh}, ${phu}`,'Part 2 report, prototype, Presentation 2','Planned','Due 9 Nov 2026, 07:00 UTC+7. Public Figma link required.'],
 ['Demonstrate running skeleton; analyse the actual instructor change request.',`${tien}, ${thanh}, ${phu}`,'Skeleton checkpoint and Change Request Impact Note','Planned','Phú coordinates impact note; Tiến owns payment extension boundary. No issued change invented.'],
 ['Implement D/A/B and secondary C/E/F; integrate sandbox, dashboards and automated QA.',`${tien}, ${thanh}, ${phu}`,'Integrated application and execution evidence','Planned','At least 20 EP/BVA cases plus 5 invalid-transition tests.'],
 ['Complete RTM, QA, demo/video and contribution records; tag and submit Part 3.',`${tien}, ${thanh}, ${phu}`,'Part 3 code/QA/demo package','Planned','Part 3 due 30 Nov 2026, 07:00 UTC+7. Separate final consolidation: 7 Dec; confirm portal.'],
 ]);
put('Plan & Risks','B15:G23',[
 ['Baseline FR/NFR and order/pricing acceptance criteria','D; BR1–BR18',tien,1,'In progress','Report sections 1.3–1.4; Requirements sheet'],
 ['Catalogue/accounts and R1 requirement review','A/E; R1',thanh,1,'To do','Report sections 1.1/1.3; Requirements sheet'],
 ['Hub/delivery and R2 requirement review','B/F; R2',phu,1,'To do','Report sections 1.1/1.3; Requirements sheet'],
 ['Rehearse Solution Pitch and coordinate Part 1 submission','D/A/B',tien,2,'To do','Presentation1_SpeakerNotes_VI.md; all 3 members speak'],
 ['Order state and payment Strategy UML','D; BR13–BR17',tien,3,'To do','Planned Part 2 UML and CRC'],
 ['Catalogue/accounts and R1 UI prototype','A/E; R1',thanh,4,'To do','Planned Figma and design review'],
 ['Hub/delivery design and Change Request impact','B/F; R2',phu,5,'To do','Record actual Week 5 change only'],
 ['Live sandbox integration and core automated tests','D; BR1–BR18',tien,6,'To do','Redacted callback logs; at least 20 EP/BVA and 5 invalid-transition cases'],
 ['Interactive R1/R2 Admin dashboard and access checks','R1/R2',`${thanh} / ${phu}`,6,'To do','Filter/chart/table reconciliation and non-Admin denial'],
 ]);
put('Plan & Risks','G15:G23',[
 [`Report §§1.3–1.4; Requirements. Planned reviewer: ${phu}; check load, lifecycle and delivery boundaries with ${tien}.`],
 [`Report §§1.1/1.3. Planned reviewer: ${tien}; check catalogue-to-checkout and R1/payment consistency with ${thanh}.`],
 [`Report §§1.1/1.3. Planned reviewer: ${thanh}; check hub/catalogue membership and R2 data with ${phu}.`],
 ['Shared pitch notes; all 3 speakers claim D/A/B. Planned joint rehearsal checks handovers, one client journey and cross-scope questions.'],
 [`Planned Part 2 UML/CRC. Reviewer ${phu} checks order/delivery guards; ${thanh} checks account/payment and catalogue dependencies.`],
 [`Planned Figma/design review. Reviewer ${tien} checks checkout/R1 flow; ${phu} checks hub context.`],
 [`Actual Week 5 request only. Reviewer ${thanh} checks R2/data impact; ${tien} checks payment/pricing impact.`],
 [`Planned reviewers ${thanh} and ${phu}; retain redacted callbacks and joint regression logs, at least 20 EP/BVA and 5 invalid transitions.`],
 [`Planned reviewer ${tien}; reconcile chart/table totals with payment outcomes and delivery/load data owned by ${thanh}/${phu}.`],
 ]);
put('Plan & Risks','B24:G26',[
 ['Agree shared hub/menu/order/payment contracts','D/A/B; FR-A6; FR-D14',tien,2,'To do',`Planned joint review: all 3 members agree hub membership, availability, capacity, placement snapshot and payment boundaries; record decisions against FR IDs.`],
 ['Cross-review requirements and assumptions before baseline','47 FR; 6 NFR; A1–A5',thanh,2,'To do',`Planned rotation: ${phu} reviews D/C; ${tien} reviews A/E; ${thanh} reviews B/F. Resolve comments in the shared register/RTM; retain reviewer links.`],
 ['Joint end-to-end integration and release review','A/B/D/F; R1/R2',phu,6,'To do',`Planned all-member journey: browse menu, select hub, checkout/pay, prepare/deliver, reconcile R1/R2. Retain scoped PRs, peer comments and linked test logs.`],
 ]);
const risks = [
 ['Sandbox credentials/provider availability could prevent live Tier 4 evidence.','High','High',tien,'Open','Arrange credentials early; retain real redacted callbacks. Label simulation; do not count it as live evidence.'],
 ['Core MVC/EF Core variant has not been confirmed against the instructor tier wording.','Medium','High',tien,'Open','Ask instructor to confirm the proposed foundation before claiming Tier 4 eligibility.'],
 ['Concurrent hub admission or forbidden transitions may violate BR8/BR15.','Medium','High',phu,'Open','Business-layer checks, transactional updates, boundary/state tests and audit consistency.'],
 ['Week 5 change request may affect existing pricing/payment classes.','Medium','High',tien,'Open','Review actual impact; isolate payment Strategies; record class changes and regression results.'],
 ['Dashboard totals or role access may disagree between chart and table.','Medium','High',thanh,'Open','One authorised query path; reconcile R1/R2 totals, date/hub filters and non-Admin denial.'],
 ['Planned tests, missing historical AI transcripts or commit attribution may be mistaken for evidence.','Medium','High',tien,'Open','Keep verdicts Not tested; recover original AI exports and audit per-student GitHub commits.'],
 ['Runtime support may expire before later deadlines (.NET 8 baseline).','High','Medium',tien,'Open','Review the documented lifecycle risk with the instructor; record any approved runtime update.'],
 ];
put('Plan & Risks','B43:D49',risks.map(r=>r.slice(0,3)));
put('Plan & Risks','F43:H49',risks.map(r=>r.slice(3)));
fit('Plan & Risks','A5:H11'); fit('Plan & Risks','A15:H26'); fit('Plan & Risks','A43:H49');

const checklist = [
 'Proposed ASP.NET Core MVC + EF Core Code-First + SQL Server + Bootstrap 5. Instructor confirmation of Core variant pending.',
 'Planned MVC controllers/views, business services and EF persistence. Verify actual separation in Parts 2/3.',
 'Planned Bootstrap responsive layout; test 390, 768 and 1440 px with English/Vietnamese.',
 'Planned payment Strategy per method and actor; extension test: one new class plus registration.',
 'Planned pure PricingEngine with placement snapshot; test BR1–BR14 boundaries and eligibility in services.',
 'Planned business-layer OrderStateMachine; cover every allowed and at least 5 forbidden transitions.',
 'Planned R1 Revenue and R2 Hub Utilization with authorised queries and reconciled totals.',
 'Tagged GitHub release and clean runbook are later deliverables; not verified in this Part 1 revision.',
 ];
put('Tier Checklist','E6:E13',checklist.map(x=>[x]));
put('Tier Checklist','E15:E17',[
 [`Planned live VNPay sandbox. Owner ${tien}. Require real success/failure callbacks, authentication, amount/order checks and replay-safe handling; mock is insufficient.`],
 [`Planned interactive R1/R2 Admin dashboard. Owners ${thanh} / ${phu}. Require working filters, matching chart/table totals and role denial.`],
 ['Planned unit/integration/E2E execution with retained logs, at least 20 EP/BVA and 5 forbidden transitions. Every member covers their scope.'],
 ]);
fit('Tier Checklist','A6:E17');
put('Contribution & Commits','B5:G7',team.members.map((m,i)=>[m.full_name,m.student_id,'Not verified',`${m.use_case}; ${m.secondary_scope.join('; ')}`,`Planned ownership: ${m.use_case_title}; ${m.reports_owned.join('; ') || 'pricing/payments'}. Planned peer reviewer: ${reviewers[i]}. Review shared interfaces and joint acceptance cases.`,`Planned evidence: scoped PRs, peer-review comments and linked FR/test IDs. Reviewer ${reviewers[i]}; commit counts and completed reviews not audited.`]));
fit('Contribution & Commits','A5:H7');
const ai = [...data.ai,{
 tool:'OpenAI Codex, 25 Oct 2026',purpose:'Align team Excel with the instructor original',
 prompt:'User requested the original SE_Sem01_2627_Team_Workbook_Template.xlsx and authorised implementation once downloaded.',
 kept:'Retained all 14 sheets, original headers and student/instructor input colours. Mapped 47 FR, 6 NFR, 5 ambiguities; extended Requirements/RTM by 8 rows.',
 verification:'Source hash, template features, canonical records, formulas and rendered ranges checked. No instructor answer, tested verdict or individual commit count invented.',
 },{
 tool:'OpenAI Codex, 25 Oct 2026',purpose:'Clarify planned team collaboration',
 prompt:'The team requested clearer teamwork and stronger evidence in its Excel deliverables.',
 kept:'Added named planned peer reviewers, joint contract/requirements/integration tasks and future PR/review/test evidence. Main ownership and requirement IDs retained.',
 verification:'Template fidelity, reviewer separation, task status and synchronisation checked. No completed meeting, review, commit count or test result invented.',
 }];
put('AI Usage Log','B5:G9',ai.map(r=>[r.tool,r.purpose,r.prompt,r.kept,r.verification,'TeamG4 (team-wide assistance)']));
fit('AI Usage Log','A5:H9');

put('Team & Tier','B5',[['Tier 3']]);
assert.equal(sheet('Team & Tier').getRange('B6').values[0][0],9.5);
put('Team & Tier','B7',[['Tier 2']]);
assert.equal(sheet('Team & Tier').getRange('B6').values[0][0],8.5);
put('Team & Tier','B7',[[null]]);
put('Team & Tier','B5',[[team.project.tier]]);
wb.recalculate();
// Materialise dependent cells as well as summary cells before XLSX cache export.
for(const s of wb.worksheets.items) s.getUsedRange().values;
for(const [cell,expected] of [['B6',10],['B8',3]]) assert.equal(sheet('Team & Tier').getRange(cell).values[0][0],expected,cell);
assert.deepEqual(req.getRange('C59:D59').values,[[47,6]]);
assert.equal(sheet('Ambiguity Log').getRange('D21').values[0][0],5);
assert.equal(rtm.getRange('A57').values[0][0],'NFR6');
assert.equal(rtm.getRange('C59').values[0][0],0);
console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|#N/A|#NULL!',options:{useRegex:true,maxResults:10},summary:'formula error scan',maxChars:1200})).ndjson);
const out=path.join(root,`docs/part1-proposal-req/${team.project.team_id}_SE_Team_Workbook_SaigonBite.xlsx`);
await (await SpreadsheetFile.exportXlsx(wb)).save(out);
await fs.rm(out+'.inspect.ndjson',{force:true});
// Recalculate shared-formula caches that the exporter omits for follower cells.
const calculated = '/tmp/saigonbite-workbook/recalculated';
await fs.mkdir(calculated,{recursive:true});
await fs.rm(path.join(calculated,path.basename(out)),{force:true});
const soffice = '/home/towfienes/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/libreoffice-headless/libreoffice/program/soffice';
execFileSync(soffice,['-env:UserInstallation=file:///tmp/saigonbite-workbook/lo-build-profile','--headless','--convert-to','xlsx','--outdir',calculated,out],{timeout:60000,stdio:'pipe'});
await fs.copyFile(path.join(calculated,path.basename(out)),out);
await fs.copyFile(out,path.resolve(root,'../SE_Sem01_2627_Team_Workbook_524H0195_524H0191_524H0179.xlsx'));
await fs.mkdir('/tmp/saigonbite-workbook/final',{recursive:true});
const previewWb = await SpreadsheetFile.importXlsx(await FileBlob.load(out));
// Render the verified Calc cache: this renderer cannot evaluate array SEARCH correctly.
const ownerCache = execFileSync('python3',['-c','import openpyxl,sys; print(openpyxl.load_workbook(sys.argv[1],data_only=True)["Team & Tier"]["D27"].value)',out],{encoding:'utf8'}).trim();
assert.equal(ownerCache,'OK');
previewWb.worksheets.getItem('Team & Tier').getRange('D27').values = [[ownerCache]];
const previews = [
 ['Instructions','A1:D16','instructions'],['Team & Tier','A4:G13','team'],['Team & Tier','A16:G29','ownership'],['Team & Tier','A35:G41','tiers'],
 ['Ambiguity Log','A4:J9','ambiguity'],['Requirements','A4:K7','requirements'],['Requirements','A51:K60','nfr-and-counts'],
 ['Plan & Risks','A4:H11','plan'],['Plan & Risks','A42:H49','risks'],['RTM','A51:I60','rtm'],['Tier Checklist','A4:E17','tier-checklist'],
 ['Plan & Risks','A14:H26','teamwork-tasks'],
 ['Contribution & Commits','A4:H7','contribution'],['AI Usage Log','A4:H8','ai'],
 ['EP-BVA Planner','A1:G6','ep-bva'],['Test Cases','A1:M6','test-cases'],['State Tests','A1:I7','state-tests'],
 ['Change Request','A1:F7','change-request'],['Feedback Log','A1:F6','feedback'],
 ];
for(const [sheetName,range,name] of previews) {
 const img=await previewWb.render({sheetName,range,scale:1,format:'png'});
 await fs.writeFile(`/tmp/saigonbite-workbook/final/${name}.png`,new Uint8Array(await img.arrayBuffer()));
}
console.log('Workbook saved:',out);
