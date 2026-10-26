"""Fill the SE course template, preserving unrelated DOCX package parts."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree as E
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT.parent / 'SE_Sem01_2627_Report_Template.docx'
OUT = ROOT / 'docs/part1-proposal-req'
TMP = ROOT / 'render/.build/course-template'
SKILL = Path('/home/towfienes/.config/orca/codex-accounts/7616683f-bc45-47bd-8020-a90b265c1f67/home/plugins/cache/openai-primary-runtime/documents/26.1020.11127/skills/documents')
data = json.loads((ROOT / 'config/part1.json').read_text())
team = json.loads((ROOT / 'config/team.json').read_text())
group = team['project']['team_id']
OUT.mkdir(parents=True, exist_ok=True)
TMP.mkdir(parents=True, exist_ok=True)
with ZipFile(REF) as z:
    parts = {n: z.read(n) for n in z.namelist()}
original_hash = hashlib.sha256(REF.read_bytes()).hexdigest()
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': W}
q = lambda tag: '{' + W + '}' + tag
doc = E.fromstring(parts['word/document.xml'])
body = doc.find('w:body', NS)
source = list(body)
for el in list(body): body.remove(el)
headings = []
content = lambda el: ''.join(n.text or '' for n in el.iter(q('t')))


def clone(el):
    result = deepcopy(el)
    for tag in ['bookmarkStart','bookmarkEnd','proofErr','lastRenderedPageBreak']:
        for node in result.findall('.//' + q(tag)): node.getparent().remove(node)
    return result


def fill(p, value, placeholder=False):
    first = p.find('w:r/w:rPr', NS)
    props = deepcopy(first) if first is not None else None
    if placeholder and props is not None:
        for color in props.findall('w:color',NS): color.set(q('val'),'000000')
    for node in list(p):
        if node.tag != q('pPr'): p.remove(node)
    run = E.SubElement(p,q('r'))
    if props is not None: run.append(props)
    for i,line in enumerate(str(value).split('\n')):
        if i: E.SubElement(run,q('br'))
        node=E.SubElement(run,q('t')); node.set('{http://www.w3.org/XML/1998/namespace}space','preserve'); node.text=line
    return p


def para(index, value=None, heading=False):
    p=clone(source[index])
    if value is not None: fill(p,value,placeholder=index in (42,49))
    if heading:
        key=f'sgb_{len(headings)}'; number=str(1000+len(headings))
        p.insert(1,E.Element(q('bookmarkStart'),{q('id'):number,q('name'):key}))
        p.append(E.Element(q('bookmarkEnd'),{q('id'):number}))
        style=p.find('w:pPr/w:pStyle',NS).get(q('val'))
        headings.append({'key':key,'title':content(p),'level':int(style[-1])})
    body.append(p)
    return p


def table(index, rows, headers=None, widths=None):
    t=clone(source[index]); originals=t.findall('w:tr',NS); header,sample=originals[:2]
    for row in originals: t.remove(row)
    values=[headers or [None]*len(header.findall('w:tc',NS))]+rows
    for pos,record in enumerate(values):
        row=clone(header if pos==0 else sample); cells=row.findall('w:tc',NS)
        assert len(record)==len(cells),(index,record)
        props=row.find('w:trPr',NS)
        if props is None: props=E.Element(q('trPr')); row.insert(0,props)
        if props.find('w:cantSplit',NS) is None: E.SubElement(props,q('cantSplit'))
        if pos==0 and props.find('w:tblHeader',NS) is None: E.SubElement(props,q('tblHeader'))
        for cell,value in zip(cells,record):
            p=cell.find('w:p',NS)
            for child in list(cell):
                if child.tag!=q('tcPr') and child is not p: cell.remove(child)
            if value is not None: fill(p,value,placeholder=pos>0)
        t.append(row)
    if widths:
        assert sum(widths)==9360
        for col,width in zip(t.find('w:tblGrid',NS),widths): col.set(q('w'),str(width))
        for row in t.findall('w:tr',NS):
            for cell,width in zip(row.findall('w:tc',NS),widths): cell.find('w:tcPr/w:tcW',NS).set(q('w'),str(width))
    body.append(t)
    return t


para(16,'SaigonBite'); para(17)
para(19,f"Advised by {team['instructor']['honorific']} {team['instructor']['full_name']}")
para(18)
for i,m in enumerate(team['members']): para(19+i,f"{i+1}. {m['student_id']} : {m['full_name']}")
table(22,[[group,f"{team['project']['tier']} proposed\nCeiling {team['project']['tier_cap']:.1f}/10",team['project']['report_version'],team['project']['report_date']]])
para(23)
table(24,[[f"SaigonBite addresses inconsistent prices, fragmented ordering and uneven hub workloads in Ho Chi Minh City's cloud kitchens. {group} proposes an MVC application with explicit use case ownership, deterministic pricing and a controlled order lifecycle. This Part 1 baseline specifies 47 functional requirements, six quality attributes and five working assumptions, with planned traceability. Tier 4 is proposed through a Code-First foundation, live payment sandbox, interactive Admin dashboard and automated tests; implementation and execution evidence are later-phase deliverables."]])
para(25,heading=True)
for i in range(26,33): para(i,content(source[i]).replace('[year]','2026').replace('Team XX',group))
para(33,heading=True)
toc=clone(source[34]); toc_content=toc.find('w:sdtContent',NS)
for node in list(toc_content): toc_content.remove(node)
body.append(toc)
para(35,heading=True)
table(37,[['Presentation 1','Not yet received; presentation pending.','No instructor feedback is claimed in this submission.','Pending'],['Part 1 marking','Not yet received; marking pending.','Record the actual comments and resulting changes after marking.','Pending']])
para(38,heading=True); para(39,heading=True); para(41)
para(42,'We propose Scrum in a seven-week plan, using one-week planning cycles, a short daily coordination meeting, a weekly integration review and a retrospective after each milestone. Small cycles expose integration risks early while preserving the Part 1, Part 2 and Part 3 submission milestones. The Week 5 change request enters the backlog with an explicit impact assessment.')
roles=['Team leader; pricing and payment integration','Data model, catalogue and Revenue report','Hub capacity, dispatch and Hub Utilization report']
table(43,[[str(i+1),m['full_name']+'\n'+m['student_id'],roles[i],'; '.join(m['secondary_scope']+m['reports_owned'])] for i,m in enumerate(team['members'])])
para(45)
table(46,[[f'UC{i+1}',m['use_case_title'],m['student_id'],m['use_case']] for i,m in enumerate(team['members'])])
para(26,'UC1 (D) belongs to Ngô Lâm Tiến: create an order; read/track owned orders; edit items only while Placed; cancel while Placed or Confirmed, retaining history. UC2 (A) belongs to Nguyễn Công Thành: create, read, update and soft-delete brands/menu items. UC3 (B) belongs to Nguyễn Trọng Phú: create, read, update and soft-delete hubs/capacity while retaining order history. Every member must speak and claim this main use case in Presentation 1.')
para(41,'Schedule and submission milestones')
table(3,[['Weeks 1–2','26 Oct 2026, 07:00 UTC+7','Part 1 report, tracking workbook and 5–7 minute Solution Pitch.'],['Weeks 3–4','9 Nov 2026, 07:00 UTC+7','Part 2 modelling, architecture and Figma prototype.'],['Weeks 5–7','30 Nov 2026, 07:00 UTC+7','Running skeleton, change-request analysis, implementation, QA and Part 3 demo.'],['Final consolidation','7 Dec 2026','Survival Guide date; follow the final portal instruction when published.']],['Period','Milestone','Planned output'])
para(41,'Technology tier and acceptance plan')
table(3,[[r['tier'],f"{r['cap']:.1f}",r['stack']] for r in data['technology']['tiers']],['Tier','Ceiling /10','Required stack and architecture'],[1100,1100,7160])
para(26,f"The proposed target is {team['project']['tier']}, ceiling {team['project']['tier_cap']:.1f}/10 under the instructor table supplied on 24 October 2026. The cap limits the rubric result; it is not an awarded mark. We propose ASP.NET Core MVC, EF Core Code-First, SQL Server and Bootstrap 5. The source names ASP.NET MVC/Entity Framework, so acceptance of the Core variant remains pending. SQL Server is the submission baseline; SQLite is only a labelled local fallback.")
for r in data['technology']['acceptance']:
    para(41,r['criterion']); para(26,r['plan'])
    para(26,'Owner: '+r['owner']+'. Evidence: '+r['evidence']+' Trace: '+r['references']+'. Status: Planned.')
para(26,'.NET 8 is the existing baseline and reaches end of support on 10 November 2026, before later milestones. Record this lifecycle risk and agree any runtime upgrade with the instructor. Arrange sandbox credentials early. A simulated payment is an explicitly labelled fallback and does not meet the live-sandbox criterion.')
para(47,heading=True)
para(49,'Customers need one reliable way to browse food across brands and hubs, understand the complete price before paying, and track delivery. Kitchen staff must see orders belonging to their hub, control preparation and avoid accepting work when capacity is saturated. Administrators need consistent Revenue and Hub Utilization reports; shippers need authorised delivery transitions and COD confirmation. Local Customers and Foreign Tourists require different identity and payment options, while sharing the same pricing and order lifecycle. SaigonBite therefore needs traceable requirements that reconcile transparent charging, hub capacity, actor permissions and retained order history.')
para(26,'This Part 1 submission defines the proposal and requirements baseline. Detailed UML, Figma, source implementation, sandbox transactions and application test results belong to later deliverables. Planned components, tests and ownership are not completed execution evidence.')
para(50,heading=True)
para(26,'Amounts are VND; time windows use Vietnam local time (UTC+7), start inclusive and end exclusive. UC1=D, UC2=A and UC3=B; secondary scopes C/E/F remain assigned to these owners. R1 and R2 are mandatory. Each stable FR ID below maps to its source and use case; the seeded RTM adds owner/component/test mappings.')
table(52,[[r['id'],r['statement'],r['use_case'],r['source'],r['report']] for r in data['fr']])
para(41,'Order lifecycle and precision acceptance baseline')
para(26,'Allowed transitions are Placed→Confirmed (Kitchen Staff at the hub), Placed→Cancelled (Customer or hub staff with rejection reason), Confirmed→Preparing (hub staff), Confirmed→Cancelled (Customer/Admin), Preparing→Ready (hub staff), Ready→Out for Delivery (assigned Shipper), Out for Delivery→Delivered (assigned Shipper; COD collected first) and Out for Delivery→Failed (assigned Shipper; unreachable customer). Delivered, Cancelled and Failed are terminal; every other transition is forbidden. Source: specification section 2C and BR14–BR16.')
para(26,'Preserve fractional discounts until the final half-up rounding (BR10/BR11). Acceptance example: subtotal 61,111; load 20%; valid uncapped 10% voucher; 1 km; no rush/rain. Quiet Kitchen discount=6,111.1; voucher=5,499.99; raw=64,499.91; final=64,000. Intermediate truncation would incorrectly yield 65,000. These are independent expected values, not application test results.')
para(53,heading=True)
para(26,'NFR1–NFR4 refine the mandatory performance, maintainability, usability and security baselines; NFR5/NFR6 are team-defined. All verification is planned. Each target below retains its source and owner in the RTM.')
table(55,[[r['id'],r['attribute'],r['target'],r['verification']] for r in data['nfr']])
para(26,'Sources and ownership: '+'; '.join(f"{r['id']}: {r['source']}; owner {r['owner']}" for r in data['nfr'])+'.')
para(56,heading=True)
para(26,'These are working assumptions, not instructor approvals. Fixed thresholds, calculation order and authorised state transitions are not open ambiguities. A changed answer requires updating the affected requirements, design and tests.')
table(58,[[r['id'],r['topic']+': '+r['gap']+'\nImpact: '+r['impact'],r['assumption'],r['answer']] for r in data['ambiguities']])
para(145,heading=True)
references=[
 'Ton Duc Thang University, Faculty of Information Technology (2026). SE Final Project Specification: SaigonBite, version 1.0, Sem01_2627. BR1–BR18, Part 1 checklist and rubric.',
 'Ton Duc Thang University (2026). SaigonBite Case Study: Cloud-Kitchen Food Delivery Hub. Context, FR1–FR9 and quality baselines.',
 'Ton Duc Thang University (2026). SaigonBite Student Survival Guide. Milestones, checklists and presentation guidance.',
 'Course instructor (2026). SE_Sem01_2627_Report_Template.docx. Required report structure, Part 1 sections 1.1–1.5 and appendices. Original retained unchanged with the course source files.',
 'Course instructor. Technology tiers (from the specification; instructor may edit the blue caps). Image supplied by the student on 24 October 2026; publication date not shown. Archived at docs/references/instructor-technology-tiers.png.',
 'Schwaber, K. and Sutherland, J. (2020). The Scrum Guide. https://scrumguides.org/scrum-guide.html. Basis for the proposed iterative process.',
 'Microsoft (2026). .NET 8 and .NET 9 will reach End of Support on November 10, 2026. https://devblogs.microsoft.com/dotnet/dotnet-8-9-end-of-support/. Runtime lifecycle risk.'
]
for i,r in enumerate(references,1): para(26,f'{i}. {r}')
para(148,heading=True); para(149,heading=True)
para(26,'The following responsibilities are planned. The course requires signatures from all members at the start of Part 3. Members must supply their own signatures, dates and actual contributions; no signature is generated in this Part 1 submission.')
table(151,[[m['full_name']+'\n'+m['student_id'],m['use_case']+' — '+m['use_case_title'],'; '.join(m['secondary_scope']+m['reports_owned']),'Signature: __________\nDate: __________'] for m in team['members']])
para(152,heading=True)
para(26,'AI assistance is disclosed below. Original full historical DSH prompts/outputs have not been located; recover the original exports for the instructor’s 48-hour request. The available Codex record at docs/appendix/prompts/CODEX_2026-10-24.md is labelled excerpts and a work summary, not a full transcript.')
table(154,[[r['tool'],r['purpose'],r['prompt'],r['kept'],r['verification']] for r in data['ai']])
para(152,'Appendix C: Requirements Traceability Matrix',heading=True)
para(26,'This is the Part 1 seed for the RTM completed in template section 3.5 at Part 3. Every FR/NFR has a planned design, component, test and owner. All verdicts are Planned; no application run is certified.')
rows=[[r['id'],r['use_case']+'\nOwner '+r['owner'],r['design'],r['component'],r['test'],'Planned'] for r in data['fr']]
designs=['Pure PricingEngine','IPaymentStrategy / DI','Responsive views / localisation','Identity / authorisation','Append-only history','State machine / price snapshot']
components=['PricingEngine','IPaymentStrategy / DI registration','Views / Localisation','Identity / Policies','OrderStatusHistory','OrderStateMachine / PricingEngine']
rows += [[r['id'],r['use_case']+'\nOwner '+r['owner'],designs[i],components[i],f'TC-NFR-{i+1}','Planned'] for i,r in enumerate(data['nfr'])]
table(128,rows)
body.append(deepcopy(source[-1]))


def update_toc(pages):
    for node in list(toc_content): toc_content.remove(node)
    prototype=source[34].find('w:sdtContent/w:p',NS)
    for i,h in enumerate(headings):
        p=clone(prototype); props=p.find('w:pPr',NS)
        props.find('w:pStyle',NS).set(q('val'),'TOC'+str(h['level']))
        for node in list(p):
            if node is not props:p.remove(node)
        if i==0:
            for tag,val in [('fldChar','begin'),('instrText','TOC \\h \\o "1-3"'),('fldChar','separate')]:
                node=E.SubElement(E.SubElement(p,q('r')),q(tag))
                if tag=='fldChar':node.set(q('fldCharType'),val)
                else:node.text=val
        link=E.SubElement(p,q('hyperlink'),{q('anchor'):h['key'],q('history'):'1'})
        E.SubElement(E.SubElement(link,q('r')),q('t')).text=h['title']
        E.SubElement(E.SubElement(link,q('r')),q('tab'))
        for tag,val in [('fldChar','begin'),('instrText',f" PAGEREF {h['key']} \\h "),('fldChar','separate'),('t',str(pages.get(h['title'],0))),('fldChar','end')]:
            node=E.SubElement(E.SubElement(link,q('r')),q(tag))
            if tag=='fldChar':node.set(q('fldCharType'),val)
            else:node.text=val
        if i==len(headings)-1:E.SubElement(E.SubElement(p,q('r')),q('fldChar'),{q('fldCharType'):'end'})
        toc_content.append(p)


footer=E.fromstring(parts['word/footer1.xml']); nodes=footer.findall('.//w:t',NS)
nodes[0].text=f'SE Report  |  {group}  |  Sem01_2627  |  Page '
for node in nodes[1:-1]:node.text=''
settings=E.fromstring(parts['word/settings.xml']); update=settings.find('w:updateFields',NS)
if update is None:update=E.SubElement(settings,q('updateFields'))
update.set(q('val'),'true')
core=E.fromstring(parts['docProps/core.xml'])
for node in core:
    local=E.QName(node).localname
    if local=='title':node.text=f'{group} SaigonBite Part 1 Proposal and Requirements'
    if local in ('creator','lastModifiedBy'):node.text=group
docx=OUT/f'{group}_SE_Final_Report_SaigonBite.docx'


def save():
    edits={'word/document.xml':doc,'word/footer1.xml':footer,'word/settings.xml':settings,'docProps/core.xml':core}
    with ZipFile(docx,'w',ZIP_DEFLATED) as z:
        for name,value in parts.items():z.writestr(name,E.tostring(edits[name],xml_declaration=True,encoding='UTF-8',standalone=True) if name in edits else value)
    with ZipFile(docx) as z:assert all(z.read(n)==value for n,value in parts.items() if n not in edits)


update_toc({}); save()
for iteration in (1,2):
    qa=TMP/f'pass-{iteration}'
    subprocess.run([sys.executable,str(SKILL/'render_docx.py'),str(docx),'--output_dir',str(qa),'--emit_pdf'],check=True)
    pdf=qa/(docx.stem+'.pdf'); reader=PdfReader(pdf); pages={}
    def visit(items):
        for item in items:
            if isinstance(item,list):visit(item)
            else:pages[item.title]=reader.get_destination_page_number(item)+1
    visit(reader.outline)
    assert all(h['title'] in pages for h in headings),('Missing PDF bookmarks',pages)
    if iteration==1:expected=pages; update_toc(pages); save()
    else:
        assert pages==expected,'TOC cache refresh changed pagination'
        shutil.copyfile(pdf,OUT/'SaigonBite_Part1.pdf'); shutil.copyfile(pdf,OUT/(docx.stem+'.pdf'))
        for name in [docx.stem+'.pdf','524H0195_524H0191_SaigonBite_Part1.pdf','524H0195_524H0191_524H0179_SaigonBite_Part1.pdf','docs/part1-proposal-req/SaigonBite_Part1.pdf']:
            target=ROOT.parent/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(pdf,target)
        report={'template_sha256':original_hash,'pages':len(reader.pages),'headings':pages,'docx':str(docx),'pdf':str(OUT/'SaigonBite_Part1.pdf'),'qa_dir':str(qa),'preserve_only_parts':'byte-identical'}
        (TMP/'build-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
        print(json.dumps(report,ensure_ascii=False,indent=2))
assert hashlib.sha256(REF.read_bytes()).hexdigest()==original_hash
