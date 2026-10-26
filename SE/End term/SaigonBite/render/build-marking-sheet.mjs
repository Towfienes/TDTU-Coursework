// Part 1 self-assessment in the instructor's five-sheet marking template.
import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';
import {createRequire} from 'node:module';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const runtime='/home/towfienes/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/package.json';
const {FileBlob,SpreadsheetFile}=await import(createRequire(runtime).resolve('@oai/artifact-tool'));
const team=JSON.parse(await fs.readFile(path.join(root,'config/team.json'),'utf8'));
const reviewers=[team.members[2].student_id,team.members[0].student_id,team.members[1].student_id];
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(path.resolve(root,'../SE_FP_SaigonBite_MarkingSheet_Sem01_2627.xlsx')));
const summary=wb.worksheets.getItem('Summary');
const marking=wb.worksheets.getItem('Marking');
const checklist=wb.worksheets.getItem('Checklist');
summary.getRange('B4').values=[[team.project.team_id]];
summary.getRange('B6').values=[[team.project.tier]];
summary.getRange('B18:D20').values=team.members.map((m,i)=>[m.full_name,m.student_id,`${m.use_case} - ${m.use_case_title}; secondary ${m.secondary_scope[0][0]}; ${m.reports_owned.map(r=>r.split(' - ')[0]).join(', ') || 'pricing/payment'}. Planned reviewer: ${reviewers[i]}.`]);
summary.getRange('B18:D20').format.autofitRows();
summary.getRange('B24').values=[['Provisional Part 1 team self-assessment, 25 Oct 2026: 19/20 (document 14.5/15; pitch 4.5/5). Each owner has a planned peer reviewer; joint baseline, shared-contract and integration reviews are in the tracking workbook. Pitch Yes is team self-assessment; live speaking/timing/Q&A were not independently verified. Parts 2/3/Final remain unscored. The /100 total is an incomplete whole-project subtotal, not a final grade. Lecturer cells are blank; calculated zeros are placeholders, not assigned marks.']];

marking.getRange('E5:E6').values=[[14.5],[4.5]];
marking.getRange('H5:H12').values=[
 ['Provisional team self-estimate 14.5/15 (Excellent band). Report §§1.1–1.5: 47 FRs, 6 measurable NFRs, 5 assumptions, UC/BR/report mappings and D/A/B CRUD ownership. Planned peer review: Phú reviews Tiến; Tiến reviews Thành; Thành reviews Phú. Workbook task board defines joint contracts, baseline review and end-to-end integration with future PR/comment/test evidence. Review completion and historical raw AI records remain pending; not a lecturer mark.'],
 ['Provisional team self-mark 4.5/5 (Excellent band). Team self-assessment records participation/ownership as Yes. Supporting assets: 5-slide PDF/PPTX, notes and a planned 6:15 script assigning D/A/B to all 3 members. Live speaking, duration and Q&A were not independently verified; lecturer review remains pending.'],
 ['Not assessed in this Part 1 snapshot. Part 2 requires owned UC specifications, behavioural/state diagrams, CRC/class/ERD, NFR-linked architecture and a public Figma prototype. Re-verify later artefacts before scoring.'],
 ['Not assessed. Live Design Review, technical explanation and individual Q&A must be observed before scoring.'],
 ['Not assessed. Re-run CRUD, pricing/state/payment, MVC and Tier 4 evidence checks; retain at least 20 EP/BVA and 5 invalid-transition results. The current RTM is a plan. No historical application results are certified here.'],
 ['Not assessed. Observe the actual demo of owned scopes, both reports and individual answers; prepared files are not live-demo evidence.'],
 ['Not assessed. Consolidate Parts 1–3 with bookmarks, feedback changes and individual Lessons Learnt after their reviews. The current PDF is a separate Part 1 report.'],
 ['Not assessed. Verify the final narrated end-to-end video covering both customer types and R1/R2; historical draft recordings were not reviewed in this task.'],
 ];
marking.getRange('A5:I12').format.autofitRows();

const evidence = new Map([
 [13,['Yes','Report title page: SaigonBite, TeamG4, all 3 names/IDs and proposed Tier 4.']],
 [14,['Yes','Report §1.1: Tiến0195 owns D, Thành0191 owns A, Phú0179 owns B; CRUD explicit. Planned peer review: Phú reviews Tiến; Tiến reviews Thành; Thành reviews Phú. Shared contracts and integration tasks are planned in the workbook; completed reviews are not claimed.']],
 [15,['Yes','Report §1.3 and workbook Requirements/RTM: 47 stable FR IDs, shall statements, sources, use cases and owners.']],
 [16,['Yes','Report §1.4: NFR1–4 mandatory baselines plus NFR5 auditability and NFR6 reliability; targets and verification plans.']],
 [17,['Yes','R1 Revenue owner Thành0191, planned reviewer Tiến0195. R2 Hub Utilization owner Phú0179, planned reviewer Thành0191. Joint checks will reconcile payments, hub/delivery data and report totals.']],
 [18,['Yes','Report §1.5 and workbook Ambiguity Log: A1–A5, working assumptions and affected scopes; answers pending.']],
 [19,['Yes','Team self-assessment: Yes. Prepared deck/script assigns D/A/B to all 3 speakers. Live speaking, duration and Q&A were not independently verified.']],
 [21,['No','Pending Part 2 verification: overall UC diagram and Customer specialisations.']],
 [22,['No','Pending Part 2 verification: a complete specification for every owned main use case.']],
 [23,['No','Pending Part 2 verification: matching Sequence/Activity diagram for each owned use case.']],
 [24,['No','Pending Part 2 verification: all 8 order states, allowed actors and guarded transitions.']],
 [25,['No','Pending Part 2 verification: CRC/class/ERD and payment Strategy design.']],
 [26,['No','Pending Part 2 verification: architecture and design evidence tied to NFRs; Part 1 only proposes the layers.']],
 [27,['No','Public Figma link and 4-stage flow verification remain pending.']],
 [29,['No','Release/tag and clean execution were not verified at this checkpoint.']],
 [30,['No','Lecturer commit-count cells left blank; per-student GitHub attribution and >10 meaningful commits not audited.']],
 [31,['No','Contribution scopes assigned; actual signed Contribution Statement is a later human deliverable.']],
 [32,['No','Pricing implementation and boundary/rounding execution not re-verified in this Part 1 task.']],
 [33,['No','Business-layer state enforcement and atomic history writes require execution evidence.']],
 [34,['No','Proposed MVC/EF Code-First/Bootstrap foundation; actual separation and Core variant acceptance pending.']],
 [35,['No','Run full CRUD journeys for D/A/B before confirming this item.']],
 [36,['No','Run both customer types and all actor-eligible payment methods; live sandbox proof is required for the Tier 4 claim.']],
 [37,['No','R1/R2 requirements and owners specified; authorised live report behaviour not re-verified here.']],
 [38,['No','The original workbook Test Cases sheet is retained, but detailed inputs/expected/actual execution rows are not completed for Part 1.']],
 [39,['No','At least 20 EP/BVA cases are planned; no fresh executed case count is claimed.']],
 [40,['No','At least 5 forbidden-transition cases are planned; execution not certified.']],
 [41,['No','Historical logs were not rerun or certified in this Part 1 document revision.']],
 [42,['No','Record the actual Week 5 instructor request, implementation and class-change evidence when issued.']],
 [43,['No','Final-versus-Part-2 design comparison belongs to the later QA report.']],
 [44,['Partial','53 seed RTM rows link every FR/NFR to planned design/code/test IDs. All verdicts Not tested; actual code/execution reconciliation pending.']],
 [45,['No','Deployment/release run path not verified in this task.']],
 [46,['No','Tier 4 applies. Real sandbox transaction/callback evidence pending; a mock does not establish completion.']],
 [47,['No','Tier 4 applies. Working R1/R2 filters, chart/table reconciliation and non-Admin denial require verification.']],
 [48,['No','Tier 4 applies. Retain actual automated workflow execution logs; plans or historical counts alone are insufficient.']],
 [50,['No','Final consolidated Parts 1–3 PDF not assessed; current submitted report is Part 1 only.']],
 [51,['No','No lecturer feedback has been recorded in the current feedback log; apply actual feedback when received.']],
 [52,['No','Each member must supply their own Lessons Learnt; not completed or invented here.']],
 [53,['No','Final video coverage and narration were not reviewed in this Part 1 task.']],
 [54,['Partial','AI use disclosed in report Appendix B and project log. Full historical DSH exports and a separate final Appendix.pdf remain pending.']],
 [55,['No','Confidential individual peer-review forms are a later human submission.']],
 ]);
assert.equal(evidence.size,40);
for(const [row,[status,note]] of evidence) {
 checklist.getRange(`D${row}`).values=[[status]];
 checklist.getRange(`F${row}`).values=[[note]];
 checklist.getRange(`F${row}`).format.wrapText=true;
 checklist.getRange(`A${row}:F${row}`).format.autofitRows();
}
wb.recalculate();
assert.equal(summary.getRange('B7').values[0][0],10);
assert.equal(marking.getRange('E13').values[0][0],19);
assert.deepEqual(checklist.getRange('D5:D8').values,[[7],[2],[31],[0]]);
console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|#N/A',options:{useRegex:true,maxResults:10},maxChars:1000})).ndjson);
const out=path.join(root,`docs/part1-proposal-req/${team.project.team_id}_SE_MarkingSheet_SaigonBite.xlsx`);
await (await SpreadsheetFile.exportXlsx(wb)).save(out);
await fs.rm(out+'.inspect.ndjson',{force:true});
const calc='/tmp/saigonbite-marking/recalculated';
await fs.mkdir(calc,{recursive:true});
await fs.rm(path.join(calc,path.basename(out)),{force:true});
const soffice='/home/towfienes/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/libreoffice-headless/libreoffice/program/soffice';
execFileSync(soffice,['-env:UserInstallation=file:///tmp/saigonbite-marking/lo-profile','--headless','--convert-to','xlsx','--outdir',calc,out],{timeout:60000,stdio:'pipe'});
await fs.copyFile(path.join(calc,path.basename(out)),out);
const preview=await SpreadsheetFile.importXlsx(await FileBlob.load(out));
for(const [sheetName,range,name] of [
 ['Instructions','A1:D15','instructions'],['Summary','A4:G25','summary'],['Marking','A4:I6','part1-marking'],['Marking','A7:I13','later-marking'],
 ['Checklist','A4:F19','part1-checklist'],['Checklist','A21:F27','part2-checklist'],['Checklist','A29:F48','part3-checklist'],['Checklist','A50:F55','final-checklist'],['Rubric Guide','A4:F6','rubric-guide'],
 ]) {
 const img=await preview.render({sheetName,range,scale:1,format:'png'});
 await fs.writeFile(`/tmp/saigonbite-marking/${name}.png`,new Uint8Array(await img.arrayBuffer()));
}
console.log('Saved',out);
