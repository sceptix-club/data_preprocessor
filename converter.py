import json
import fitz

WEIGHT=1
TEXT=0

pdfpath:str="data/acetone-acs-l (1).pdf"
outpath:str="output.json"


def writejson(content):
    jsoncontent=json.dumps(content)
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

weightarr=[("5.1",5),("3",3),("2",2),("1",1),("1",1),("2",1),("5.2",5),("1",1)] #test sample
#weightarr=scrape(pdfpath)
arrlen=len(weightarr)
weightstack=[]
index=0
outdict={}


'''
NOT WORKING
def getdict(arr:list):
    maxindex=0 #index of largest val
    subarr=[arr[maxindex],[]]
    i=maxindex+1
    while(i<len(arr)):
        if arr[maxindex][WEIGHT]>arr[i][WEIGHT]:
            subarr[maxindex+1].append(arr[i])
        if arr[maxindex][WEIGHT]<arr[i][WEIGHT]:
            maxindex=i
            subarr.append(arr[maxindex])
            subarr.append([])
        i+=1
    return subarr

def getvalue():
    global index #index of key
    i=index+1
    if i>=len(weightarr):
        return []
    keyarr=[]
    while(weightarr[i][WEIGHT]<weightstack[-1]):
        keyarr.append(weightarr[i])
        i+=1
        if i>=len(weightarr):
            break
    index=i
    return getdict(keyarr)


print("Weightarr: ",weightarr)
weightstack.append(weightarr[index][WEIGHT])
while (index<len(weightarr)):
    i=index
    outdict[weightarr[i][TEXT]]=getvalue()
print(outdict)
#writejson(outputdict)
'''


def getvalue(valindex:int): #returns key value(int, array or dictionary)
    #val is index of first key
    global index 
    nextval:int=valindex+1
    if nextval>=arrlen: #out of bounds
        index=nextval
        return weightarr[valindex][TEXT]
    elif weightarr[valindex][WEIGHT]<weightarr[nextval][WEIGHT]: 
        index=nextval
        return weightarr[valindex][TEXT]
    elif weightarr[valindex][WEIGHT]>weightarr[nextval][WEIGHT]:
        return {weightarr[valindex][TEXT]:getvalue(nextval)}
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
    outdict[weightarr[i][TEXT]]=getvalue(i+1)

writejson(outdict)