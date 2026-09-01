#!/usr/bin/env python3
"""Post-process docx footers: enforce PAGE \\* ROMAN / \\* arabic instrText per
section, and strip empty <w:pgNumType/> from cover section (WPS compat)."""
import re, shutil, sys, zipfile, os

DOCX = sys.argv[1] if len(sys.argv) > 1 else \
    "/home/z/my-project/download/novelty_assessment_automata_unified.docx"
TMP = DOCX + ".tmp"

with zipfile.ZipFile(DOCX, "r") as zin:
    names = zin.namelist()
    items = {n: zin.read(n) for n in names}

# Identify footer files and their section association via document.xml order.
docxml = items["word/document.xml"].decode("utf-8")

# Map footer rIds -> footer files via rels
rels = items["word/_rels/document.xml.rels"].decode("utf-8")
rid2file = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="(footer\d+\.xml)"', rels))

# Walk sectPr blocks in order; find footerReference rIds per section.
sect_blocks = re.findall(r"<w:sectPr.*?</w:sectPr>", docxml, re.S)
print(f"sections found: {len(sect_blocks)}")
section_footers = []  # list of (fmt, [footer files])
for i, blk in enumerate(sect_blocks):
    fmt_m = re.search(r'<w:pgNumType[^>]*w:fmt="([^"]+)"', blk)
    fmt = fmt_m.group(1) if fmt_m else None
    rids = re.findall(r'<w:footerReference[^>]*r:id="(rId\d+)"', blk)
    files = [rid2file[r] for r in rids if r in rid2file]
    section_footers.append((fmt, files))
    print(f"  section {i+1}: fmt={fmt} footers={files}")

# Expected: section2 = UPPER_ROMAN, section3 = DECIMAL (section1 cover: none)
patched = 0
for fmt, files in section_footers:
    if not files:
        continue
    want = None
    if fmt and "oman" in fmt:
        want = "ROMAN"
    elif fmt and fmt.lower() in ("decimal", "arabic"):
        want = "arabic"
    if not want:
        continue
    for f in files:
        key = "word/" + f
        xml = items[key].decode("utf-8")
        new = re.sub(
            r'(<w:instrText[^>]*>)([^<]*PAGE[^<]*)(</w:instrText>)',
            lambda m: m.group(1) + f" PAGE \\* {want} \\* MERGEFORMAT " + m.group(3),
            xml)
        if new != xml:
            items[key] = new.encode("utf-8")
            patched += 1

# Strip empty pgNumType (no attributes) from document.xml (cover section artifact)
newdoc = re.sub(r"<w:pgNumType/>", "", docxml)
if newdoc != docxml:
    items["word/document.xml"] = newdoc.encode("utf-8")
    print("removed empty pgNumType")

with zipfile.ZipFile(TMP, "w", zipfile.ZIP_DEFLATED) as zout:
    for n in names:
        zout.writestr(n, items[n])
shutil.move(TMP, DOCX)
print(f"patched {patched} footer files; wrote {DOCX}")
