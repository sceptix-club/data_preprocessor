import json
import fitz

WEIGHT=1
TEXT=0

pdfpath:str="data/acetone-acs-l (1).pdf"
outpath:str="output.json"

def getdata(content):
    jsondict={}
    for i in content:
        jsondict[str(i[1])]=i[0]
    return jsondict

def writejson(content):
    jsoncontent=json.dumps(getdata(content))
    with open(outpath,"w") as fp:
        fp.write(jsoncontent)

def getweight(lines)->int:
    weight:int=int(lines['size'])
    if 'Bold' in lines['font']:
        weight+=1
    return weight

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
                        results.append((lines['text'],getweight(lines))) #lines['font']
    pdf.close()
    return results

#weightarr=scrape(pdfpath)
weightarr=[("5.1",5),("3",3),("1",2),("3.2",3),("1",1),("5.2",5),("2",2)]

outputdict={}
weightstack=[]
index=0

top=0
def push(n):
    weightstack[top]=n
    top+=1

def pop()->int:
    top-=1
    return weightstack.pop()

valuearr=[]
def setValuearr():
    global index
    i=index
    j=i+1
    valuearr.append(weightarr[i][TEXT])
    print("Appended:\t",weightarr[i][TEXT])
    while (j<len(weightarr) and weightarr[i][WEIGHT]==weightarr[j][WEIGHT]):
        print("Appended:\t",weightarr[j][TEXT])
        valuearr.append(weightarr[j][TEXT])
        i+=1
        j+=1
    index=j+1

def getkey():
    global index
    i=index+1
    j=i+1
    if j<len(weightarr):
        index+=1
        print("i: ",i,"\tj: ",j,"\tWeight i: ",weightarr[i][WEIGHT],"\tWeight j: ",weightarr[j][WEIGHT])
        if weightarr[i][WEIGHT]==weightarr[j][WEIGHT]:
            valuearr.clear()
            setValuearr()
            print("Val:\t",valuearr)
            return valuearr
        elif weightarr[i][WEIGHT]>weightarr[j][WEIGHT]:
            return getkey()
        else:
            print("Last:\t",weightarr[i][TEXT])
            return weightarr[i][TEXT]
    else:
        print("Out of bounds j=",j)
        return -1

while(True):
    print("Index: ",index)
    retvalue=getkey()
    if retvalue==-1:
        break
    print("Output:\t",getkey())
    index+=1

#writejson(outputdict)