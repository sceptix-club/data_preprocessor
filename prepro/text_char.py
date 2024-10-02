import pymupdf


def flags_decomposer(flags):
    l = []
    if flags & 2 ** 0:
        l.append("superscript")
    if flags & 2 ** 1:
        l.append("italic")
    if flags & 2 ** 2:
        l.append("serifed")
    else:
        l.append("sans")
    if flags & 2 ** 3:
        l.append("monospaced")
    else:
        l.append("proportional")
    if flags & 2 ** 4:
        l.append("bold")
    return ", ".join(l)

doc = pymupdf.open("./data/acetone-acs-l.pdf")
page = doc[0]

blocks = page.get_text("dict", flags=11)["blocks"]
for b in blocks:  
    for l in b["lines"]:  
        for s in l["spans"]:  
            print("")
            font_properties = "Font: '%s' (%s), size %g, color #%06x" % (
                s["font"],  # font name
                flags_decomposer(s["flags"]),  
                s["size"],  # font size
                s["color"],  # font color
            )