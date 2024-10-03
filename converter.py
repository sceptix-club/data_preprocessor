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
    if lines['text'].rstrip()[-1]==":":
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
weightarr=[("5.1",5),("3",3),("5",5),("3.2",3)]
#weightarr=scrape(pdfpath)
weightstack=[]
index=0
outdict={}


'''
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

def getkey():
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
    outdict[weightarr[i][TEXT]]=getkey()
print(outdict)
#writejson(outputdict)
'''

def getkey(): #returns dictionary (assuming no duplicate weights)
    global index #index of key
    i=index
    j=i+1
    valdict={}
    if j>=len(weightarr):
        index=len(weightarr)
        return {"Footer": weightarr[-1][TEXT]}
    elif weightarr[i][WEIGHT]>weightarr[j][WEIGHT]:
        index=j+1
        return {weightarr[j][TEXT]:getkey()}
    else:index+=1


while (index<len(weightarr)):
    keyindex=index
    outdict[weightarr[keyindex][TEXT]]=getkey()

print(outdict)
writejson(outdict)