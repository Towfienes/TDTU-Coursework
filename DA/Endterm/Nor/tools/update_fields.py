"""Populate native PAGEREF caches from rendered pagination, preserving Word fields."""
import argparse
import io
import json
from pathlib import Path
import re
import shutil
import subprocess
import unicodedata
import zipfile

from lxml import etree
from pypdf import PdfReader

NS = {'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}


def normalized(text):
    return re.sub(r'\s+',' ',unicodedata.normalize('NFKC',text).replace('\u00ad','')).strip()


def materialize(original, numbers):
    source = zipfile.ZipFile(io.BytesIO(original))
    document = etree.fromstring(source.read('word/document.xml'))
    for element in document.xpath('//w:fldSimple',namespaces=NS):
        instruction=element.get('{'+NS['w']+'}instr','')
        match=re.match(r'PAGEREF\s+(\w+)',instruction)
        if match:
            texts=element.xpath('.//w:t',namespaces=NS)
            texts[0].text=str(numbers[match[1]])
    output=io.BytesIO()
    with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED) as target:
        for item in source.infolist():
            target.writestr(item,etree.tostring(document,xml_declaration=True,encoding='UTF-8',standalone=True) if item.filename=='word/document.xml' else source.read(item.filename))
    return output.getvalue()


def update(source,target,index_file,soffice):
    source,target=Path(source).resolve(),Path(target).resolve()
    entries=json.loads(Path(index_file).read_text())
    original=source.read_bytes();payload=original;last_numbers=None
    build=source.parent/'pagination';build.mkdir(exist_ok=True)
    for iteration in range(4):
        directory=build/f'pass-{iteration}';directory.mkdir(exist_ok=True)
        candidate=directory/'report.docx';candidate.write_bytes(payload)
        subprocess.run([str(soffice),'--headless','--convert-to','pdf','--outdir',str(directory),str(candidate)],check=True,capture_output=True,text=True,timeout=90)
        pdf=candidate.with_suffix('.pdf')
        pages=[normalized(page.extract_text()) for page in PdfReader(pdf).pages]
        locations={}
        for entry in entries:
            label=normalized(entry['label'])
            matches=[i for i,text in enumerate(pages) if label in text]
            if not matches:raise RuntimeError(f'Cannot locate rendered heading/caption: {entry["label"]}')
            locations[entry['bookmark']]=matches[-1]
        body_start=locations[entries[0]['bookmark']]
        numbers={bookmark:physical-body_start+1 for bookmark,physical in locations.items()}
        if any(number<1 for number in numbers.values()):raise RuntimeError('Unexpected front-matter entry in body indexes.')
        if numbers==last_numbers:
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(payload)
            shutil.copy2(pdf,target.with_suffix('.pdf'))
            receipt={'method':'native TOC/SEQ/PAGEREF fields; caches materialized from rendered headings/captions',
                     'render_passes':iteration+1,'physical_pages':len(pages),'body_start_physical_page':body_start+1,
                     'entries':[dict(entry,page=numbers[entry['bookmark']],physical_page=locations[entry['bookmark']]+1) for entry in entries]}
            (source.parent/'report_pagination.json').write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+'\n')
            print(f'Pagination verified after {iteration+1} renders: {len(pages)} pages, {len(entries)} index entries.')
            return
        payload=materialize(original,numbers);last_numbers=numbers
    raise RuntimeError('Report pagination did not stabilize in four passes.')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('source');parser.add_argument('target');parser.add_argument('--index',required=True);parser.add_argument('--soffice',default=shutil.which('soffice'))
    args=parser.parse_args()
    if not args.soffice:parser.error('Provide --soffice or place LibreOffice on PATH.')
    update(args.source,args.target,args.index,args.soffice)
