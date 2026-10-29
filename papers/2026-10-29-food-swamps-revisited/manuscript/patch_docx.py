"""Patch the pandoc Word output: Times New Roman, double-spaced body, line numbers, single-spaced 8.5pt tables
at full width, figures 6.3 in wide, 1-inch margins."""
import sys
from docx import Document
from docx.shared import Pt, Inches, Emu
from docx.enum.text import WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
d = Document(sys.argv[1])
for st in d.styles:
    try:
        if st.type == 1 or st.type == 3:
            st.font.name = 'Times New Roman'
            rpr = st.element.get_or_add_rPr(); rf = rpr.find(qn('w:rFonts'))
            if rf is None: rf = OxmlElement('w:rFonts'); rpr.append(rf)
            for a in ('w:ascii', 'w:hAnsi', 'w:cs', 'w:eastAsia'): rf.set(qn(a), 'Times New Roman')
            for a in ('w:asciiTheme', 'w:hAnsiTheme', 'w:cstheme', 'w:eastAsiaTheme'):
                if rf.get(qn(a)) is not None: del rf.attrib[qn(a)]
    except Exception: pass
for name in ('Normal', 'Body Text', 'First Paragraph', 'Compact'):
    try: d.styles[name].font.size = Pt(12)
    except KeyError: pass
for s in d.sections:
    s.left_margin = s.right_margin = s.top_margin = s.bottom_margin = Inches(1)
    ln = OxmlElement('w:lnNumType'); ln.set(qn('w:countBy'), '1'); ln.set(qn('w:restart'), 'continuous'); ln.set(qn('w:distance'), '360')
    pg = s._sectPr.find(qn('w:pgMar')); pg.addnext(ln)
for p in d.paragraphs:
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE
    for r in p.runs: r.font.name = 'Times New Roman'
for t in d.tables:
    tblPr = t._tbl.tblPr
    w = tblPr.find(qn('w:tblW'))
    if w is None: w = OxmlElement('w:tblW'); tblPr.append(w)
    w.set(qn('w:type'), 'pct'); w.set(qn('w:w'), '5000')
    for row in t.rows:
        for c in row.cells:
            for p in c.paragraphs:
                p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
                p.paragraph_format.space_after = Pt(0)
                pPr = p._p.get_or_add_pPr(); sup = OxmlElement('w:suppressLineNumbers'); pPr.append(sup)
                for r in p.runs: r.font.size = Pt(8.5); r.font.name = 'Times New Roman'
    # table borders
    b = OxmlElement('w:tblBorders')
    for e in ('top', 'bottom', 'insideH'):
        x = OxmlElement(f'w:{e}'); x.set(qn('w:val'), 'single'); x.set(qn('w:sz'), '4'); x.set(qn('w:color'), '808080'); b.append(x)
    tblPr.append(b)
for sh in d.inline_shapes:
    ratio = sh.height / sh.width; sh.width = Inches(6.3); sh.height = Emu(int(Inches(6.3) * ratio))
d.save(sys.argv[2])
