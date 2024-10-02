import pymupdf
fname = "./data/acetone-acs-l.pdf"
with pymupdf.open(fname) as doc:  # open document
    text = chr(12).join([page.get_text() for page in doc])
    print(text)  # print text