import json
import fitz

WEIGHT=1
TEXT=0

pdfpath:str="data/acetone-acs-l (1).pdf"
outpath:str="output.json"


def writejson(content):
    jsoncontent=json.dumps(content,indent=4)
    with open(outpath,"w") as fp:
        fp.write(jsoncontent)

def getweight(lines,text)->int:
    weight:int=int(lines['size'])
    if 'Bold' in lines['font']:
        weight+=1
    if text[-1]==":":
        weight+=1
    return weight

def getweighttup(lines)->tuple:
    text=lines['text']
    text=text.strip()
    if text=="":
        return None
    weight=getweight(lines,text)
    return (text,weight)

def scrape(filePath):
    results = [] # list of tuples that store the information as (text, font size, font name) 
    pdf = fitz.open(filePath) # filePath is a string that contains the path to the pdf
    for page in pdf:
        dict = page.get_text("dict")
        blocks = dict["blocks"]
        for block in blocks:
            if "lines" in block.keys():
                spans = block['lines']
                for span in spans:
                    data = span['spans']
                    for lines in data:
                        tup=getweighttup(lines)
                        if tup:
                            results.append(getweighttup(lines))
    pdf.close()
    return results

weightarr=[("5.1",5),("3",3),("2",2),("1",1),("1",1),("2",1),("5.2",5),("1",1)] #test sample
#weightarr=scrape(pdfpath)
arrlen=len(weightarr)
weightstack=[]
index=0
outdict={}

def getvalue(keyindex:int): #returns key value(int, array or dictionary)
    #val is index of first key
    global index
    valindex=keyindex+1
    print("Index at getvalue: ",valindex-1,"\Key: ",weightarr[valindex-1])
    nextval:int=valindex+1
    if nextval>=arrlen: #out of bounds
        index=nextval
        return weightarr[valindex][TEXT]
    elif weightarr[valindex][WEIGHT]<weightarr[nextval][WEIGHT]: 
        index=nextval
        return weightarr[valindex][TEXT]
    elif weightarr[valindex][WEIGHT]>weightarr[nextval][WEIGHT]:
        valdict={}
        valdict[weightarr[valindex][TEXT]]=getvalue(nextval)
        return valdict
    else:
        valarr:list=[]
        valarr.append(weightarr[valindex][TEXT])
        for i in range(nextval,arrlen-1):
            if weightarr[nextval][WEIGHT]==weightarr[i][WEIGHT]:
                valarr.append(weightarr[i][TEXT])
        index=i
        return valarr

while(index<arrlen):
    i=index
    outdict[weightarr[i][TEXT]]=getvalue(i)

writejson(outdict)