"""TDTU layout using the retained template's style definitions and logo."""
from copy import deepcopy
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION_START
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_LINE_SPACING, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt


def field(paragraph, instruction, cached='1'):
    element = OxmlElement('w:fldSimple')
    element.set(qn('w:instr'), instruction)
    run = OxmlElement('w:r')
    text = OxmlElement('w:t')
    text.text = cached
    run.append(text)
    element.append(run)
    paragraph._p.append(element)
    return element


class Report:
    def __init__(self, root, meta):
        self.root, self.meta = Path(root), meta
        self.doc = Document(self.root/'references/Template_EN.docx')
        self.doc.core_properties.title = 'Abalone Measurements and Shell Rings — Theory Endterm'
        self.doc.core_properties.author = '; '.join(a['name'] for a in meta['authors'])
        first_section = deepcopy(self.doc.sections[0]._sectPr)
        for element in list(self.doc._element.body):
            self.doc._element.body.remove(element)
        for element in list(first_section):
            if element.tag in {qn('w:headerReference'), qn('w:footerReference'), qn('w:pgNumType')}:
                first_section.remove(element)
        self.doc._element.body.append(first_section)
        self.entries, self.figures, self.tables = [], [], []
        self.bookmark_id = 0
        self.configure_styles()
        self.configure_section(self.doc.sections[0])

    def configure_styles(self):
        styles = self.doc.styles
        for style in styles:
            if style.type == 1:
                style.font.name = 'Times New Roman'
                style.font.color.rgb = __import__('docx').shared.RGBColor(0, 0, 0)
        for name, size in [('Normal',13),('Nidungvnbn',13),('Heading 1',16),('Heading 2',14),('Heading 3',14),('Caption',13)]:
            if name not in styles:
                continue
            style = styles[name]
            style.font.name, style.font.size = 'Times New Roman', Pt(size)
            style.paragraph_format.space_after = Pt(0)
            style.paragraph_format.space_before = Pt(0)
            style.paragraph_format.line_spacing = 1.5
        for name in ['Normal','Nidungvnbn']:
            if name in styles:
                styles[name].paragraph_format.first_line_indent = Cm(1.27)
                styles[name].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        for name in ['Heading 1','Heading 2','Heading 3']:
            for element in list(styles[name]._element.xpath('./w:pPr/w:numPr')):
                element.getparent().remove(element)
            styles[name].font.bold = True
            styles[name].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
            styles[name].paragraph_format.first_line_indent = Pt(0)
            styles[name].paragraph_format.left_indent = Pt(0)
            styles[name].paragraph_format.right_indent = Pt(0)
            styles[name].paragraph_format.keep_with_next = True
            styles[name].paragraph_format.space_before = Pt(8)
            styles[name].paragraph_format.space_after = Pt(6)
        styles['Heading 3'].font.italic = True
        for name in ['Figure Caption','Table Caption']:
            if name not in styles:styles.add_style(name,1)
            styles[name].base_style=styles['Caption']
            styles[name].font.name='Times New Roman';styles[name].font.size=Pt(13)
        for name in ['TOC 1','TOC 2']:
            if name not in styles:
                styles.add_style(name, 1)
            styles[name].font.name, styles[name].font.size = 'Times New Roman', Pt(13)
            styles[name].font.bold = name == 'TOC 1'
            styles[name].paragraph_format.first_line_indent = Pt(0)
            styles[name].paragraph_format.line_spacing = 1.5
            styles[name].paragraph_format.space_after = Pt(4)
            styles[name].paragraph_format.tab_stops.add_tab_stop(Cm(15.5), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)

    @staticmethod
    def configure_section(section):
        section.page_width, section.page_height = Cm(21), Cm(29.7)
        section.left_margin, section.right_margin = Cm(3.5), Cm(2)
        section.top_margin, section.bottom_margin = Cm(3.5), Cm(3)
        section.header_distance = section.footer_distance = Cm(1.27)
        section.different_first_page_header_footer = False

    def new_numbered_section(self, number_format, start=None, size=13):
        section = self.doc.add_section(WD_SECTION_START.NEW_PAGE)
        self.configure_section(section)
        section.header.is_linked_to_previous = False
        section.footer.is_linked_to_previous = False
        for paragraph in section.header.paragraphs:
            paragraph.clear()
        p = section.header.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.first_line_indent = Pt(0)
        p.paragraph_format.line_spacing = 1
        p.style = self.doc.styles['Normal']
        p.paragraph_format.first_line_indent = Pt(0)
        el = field(p, 'PAGE', 'i' if number_format == 'lowerRoman' else '1')
        props=OxmlElement('w:rPr'); font=OxmlElement('w:rFonts');font.set(qn('w:ascii'),'Times New Roman');font.set(qn('w:hAnsi'),'Times New Roman');props.append(font)
        sz=OxmlElement('w:sz');sz.set(qn('w:val'),str(2*size));props.append(sz);el[0].insert(0,props)
        for old in section._sectPr.findall(qn('w:pgNumType')):
            section._sectPr.remove(old)
        numbering = OxmlElement('w:pgNumType'); numbering.set(qn('w:fmt'),number_format)
        if start is not None:
            numbering.set(qn('w:start'),str(start))
        section._sectPr.append(numbering)
        return section

    def cover(self, inner=False):
        if inner:
            self.doc.add_page_break()
        cursor = 99.21

        def at(top, text='', size=14, bold=False, height=22.5, picture=False, left=False):
            nonlocal cursor
            p=self.doc.add_paragraph()
            fmt=p.paragraph_format
            fmt.first_line_indent=Pt(0)
            fmt.space_before=Pt(max(0,top-cursor));fmt.space_after=Pt(0)
            fmt.line_spacing_rule=WD_LINE_SPACING.EXACTLY;fmt.line_spacing=Pt(height)
            p.alignment=WD_ALIGN_PARAGRAPH.LEFT if left else WD_ALIGN_PARAGRAPH.CENTER
            if left: fmt.left_indent=Pt(36)
            run=p.add_run(text);run.font.name='Times New Roman';run.font.size=Pt(size);run.bold=bold
            if picture: run.add_picture(str(self.root/'report/assets/tdtu-logo.png'),width=Cm(4.129),height=Cm(2.286))
            cursor=top+height
            return p

        at(99.21,'VIETNAM GENERAL CONFEDERATION OF LABOR',size=14)
        at(121.71,'TON DUC THANG UNIVERSITY',bold=True)
        at(144.21,'FACULTY OF INFORMATION TECHNOLOGY',bold=True)
        at(194.7,picture=True,height=67.5)
        for i,author in enumerate(self.meta['authors']):
            at(282.5+i*16.2,f"{author['name']} – {author['id']}",bold=True,height=16.2)
        at(355,'Group: '+self.meta['group']+' · Theory N4',size=13,height=18)
        at(388,'ENDTERM REPORT',size=24,bold=True,height=30)
        at(458,'DATA ANALYSIS AND',size=22,bold=True,height=27)
        at(485,'VISUALIZATION',size=22,bold=True,height=27)
        at(535,'ABALONE MEASUREMENTS AND SHELL RINGS',size=14,bold=True,height=21)
        at(556,'Exploration, Statistical Inference and Regression',size=14,height=21)
        if not self.meta.get('submission_ready',False):at(585,'Review copy — submission details pending',size=11,height=16)
        if inner:
            at(630,'Advised by',height=21)
            at(651,self.meta['advisor'],bold=True,height=21)
        at(697 if inner else 637,'HO CHI MINH CITY, 2026',bold=True,height=21)

    def para(self,text='',bold=False,first=True):
        p=self.doc.add_paragraph(text,style='Nidungvnbn' if 'Nidungvnbn' in self.doc.styles else 'Normal')
        p.paragraph_format.first_line_indent=Cm(1.27) if first else Pt(0)
        p.paragraph_format.widow_control=True
        if bold:
            for run in p.runs:run.bold=True
        return p

    def title(self,text):
        p=self.para(text,first=False);p.alignment=WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after=Pt(18);p.paragraph_format.keep_with_next=True
        for run in p.runs:run.bold=True;run.font.size=Pt(16)
        return p

    def bookmark(self,p,prefix='item'):
        self.bookmark_id+=1;name=f'{prefix}_{self.bookmark_id}'
        start=OxmlElement('w:bookmarkStart');start.set(qn('w:id'),str(self.bookmark_id));start.set(qn('w:name'),name)
        end=OxmlElement('w:bookmarkEnd');end.set(qn('w:id'),str(self.bookmark_id))
        p._p.insert(0,start);p._p.append(end)
        return name

    def heading(self,text,level=1,new_page=False):
        p=self.doc.add_paragraph(text,style=f'Heading {level}')
        props=p._p.get_or_add_pPr();numbering=OxmlElement('w:numPr');number_id=OxmlElement('w:numId');number_id.set(qn('w:val'),'0');numbering.append(number_id);props.append(numbering)
        if new_page:p.paragraph_format.page_break_before=True
        self.entries.append({'label':text,'bookmark':self.bookmark(p,'heading'),'level':level})
        return p

    def index_placeholder(self,kind,title):
        self.title(title)
        p=self.doc.add_paragraph(f'[[{kind}]]')
        p.paragraph_format.first_line_indent=Pt(0)

    def caption(self,kind,number,text):
        label=f'{kind} {number}: {text}'
        p=self.doc.add_paragraph(style=f'{kind} Caption')
        p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.paragraph_format.first_line_indent=Pt(0)
        p.paragraph_format.line_spacing=1.15;p.paragraph_format.space_after=Pt(8)
        prefix,sequence=number.rsplit('.',1)
        p.add_run(f'{kind} {prefix}.')
        field(p,f'SEQ {kind}_{prefix.replace(".","_")} \\* ARABIC',sequence)
        p.add_run(': '+text)
        entry={'label':label,'bookmark':self.bookmark(p,kind.lower()),'level':2}
        (self.figures if kind=='Figure' else self.tables).append(entry)
        return p

    def figure(self,name,number,text,max_height=9.3):
        from PIL import Image
        p=self.doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.first_line_indent=Pt(0);p.paragraph_format.keep_with_next=True
        p.paragraph_format.space_before=Pt(6)
        source=self.root/'results/figures'/name
        with Image.open(source) as image:width,height=image.size
        scale=min(15.2/width,max_height/height)
        p.add_run().add_picture(str(source),width=Cm(width*scale),height=Cm(height*scale))
        return self.caption('Figure',number,text)

    def table(self,headers,rows,number,title,widths=None):
        p=self.caption('Table',number,title);p.paragraph_format.keep_with_next=True
        table=self.doc.add_table(rows=1,cols=len(headers));table.style='Table Grid';table.autofit=False
        if widths is None:widths=[15.5/len(headers)]*len(headers)
        for i,(text,width) in enumerate(zip(headers,widths)):
            table.columns[i].width=Cm(width);table.rows[0].cells[i].width=Cm(width);table.rows[0].cells[i].text=str(text)
        repeat=OxmlElement('w:tblHeader');table.rows[0]._tr.get_or_add_trPr().append(repeat)
        for row in rows:
            cells=table.add_row().cells
            for i,text in enumerate(row):cells[i].text=str(text);cells[i].width=Cm(widths[i])
        for row_index,row in enumerate(table.rows):
            trpr=row._tr.get_or_add_trPr();cant=OxmlElement('w:cantSplit');trpr.append(cant)
            for cell in row.cells:
                tcpr=cell._tc.get_or_add_tcPr()
                margins=OxmlElement('w:tcMar')
                for side in ['top','left','bottom','right']:
                    element=OxmlElement(f'w:{side}');element.set(qn('w:w'),'70');element.set(qn('w:type'),'dxa');margins.append(element)
                tcpr.append(margins)
                if row_index==0:
                    shade=OxmlElement('w:shd');shade.set(qn('w:fill'),'E7E7E7');tcpr.append(shade)
                for paragraph in cell.paragraphs:
                    paragraph.paragraph_format.first_line_indent=Pt(0);paragraph.paragraph_format.line_spacing=1.05
                    paragraph.paragraph_format.keep_with_next=row_index<len(table.rows)-1
                    paragraph.paragraph_format.space_before=Pt(2);paragraph.paragraph_format.space_after=Pt(2)
                    for run in paragraph.runs:run.font.name='Times New Roman';run.font.size=Pt(11);run.bold=row_index==0
        self.doc.add_paragraph().paragraph_format.space_after=Pt(2)
        return table

    def equation(self,left,numerator,denominator):
        p=self.doc.add_paragraph();p.paragraph_format.first_line_indent=Pt(0);p.alignment=WD_ALIGN_PARAGRAPH.CENTER
        math=OxmlElement('m:oMath')
        def mathrun(text):
            run=OxmlElement('m:r');props=OxmlElement('w:rPr');fonts=OxmlElement('w:rFonts');fonts.set(qn('w:ascii'),'Cambria Math');fonts.set(qn('w:hAnsi'),'Cambria Math');props.append(fonts);run.append(props)
            value=OxmlElement('m:t');value.text=text;run.append(value);return run
        math.append(mathrun(left+' = '));fraction=OxmlElement('m:f')
        for part,text in [('num',numerator),('den',denominator)]:
            element=OxmlElement('m:'+part);element.append(mathrun(text));fraction.append(element)
        math.append(fraction);p._p.append(math)

    def finalize_indexes(self):
        mappings={'TOC':(self.entries,'TOC \\o "1-2" \\h \\z \\u'),'LOF':(self.figures,'TOC \\t "Figure Caption,1" \\h'),'LOT':(self.tables,'TOC \\t "Table Caption,1" \\h')}
        for kind,(entries,instruction) in mappings.items():
            anchor=next(p for p in self.doc.paragraphs if p.text==f'[[{kind}]]')
            # Cached field results are generated from actual headings/captions and later pagination.
            previous=anchor._p
            for i,entry in enumerate(entries):
                p=OxmlElement('w:p');previous.addnext(p);previous=p
                from docx.text.paragraph import Paragraph
                paragraph=Paragraph(p,anchor._parent)
                paragraph.style=self.doc.styles['TOC 1' if entry['level']==1 else 'TOC 2']
                paragraph.paragraph_format.keep_with_next=False
                if i==0:
                    for tag,text in [('begin',None),('instruction',instruction),('separate',None)]:
                        run=OxmlElement('w:r')
                        if tag=='instruction':
                            el=OxmlElement('w:instrText');el.set(qn('xml:space'),'preserve');el.text=' '+text+' '
                        else:el=OxmlElement('w:fldChar');el.set(qn('w:fldCharType'),tag)
                        run.append(el);p.append(run)
                hl = OxmlElement('w:hyperlink')
                hl.set(qn('w:anchor'), entry['bookmark'])
                hl.set(qn('w:history'), '1')
                r_label = OxmlElement('w:r')
                t_label = OxmlElement('w:t')
                t_label.text = entry['label']
                r_label.append(t_label)
                hl.append(r_label)
                r_tab=OxmlElement('w:r');r_tab.append(OxmlElement('w:tab'));hl.append(r_tab)
                fld = OxmlElement('w:fldSimple')
                fld.set(qn('w:instr'), 'PAGEREF ' + entry['bookmark'] + ' \\h')
                r_num = OxmlElement('w:r')
                t_num = OxmlElement('w:t')
                t_num.text = '1'
                r_num.append(t_num)
                fld.append(r_num)
                hl.append(fld)
                p.append(hl)
                if i==len(entries)-1:
                    run=OxmlElement('w:r');el=OxmlElement('w:fldChar');el.set(qn('w:fldCharType'),'end');run.append(el);p.append(run)
            anchor._p.getparent().remove(anchor._p)
