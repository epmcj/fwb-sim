import os
import sys
import json
import math

# input reading
inDir   = None
outName = None

for i in range(1, len(sys.argv), 2):
    if sys.argv[i] == "-i":
        inDir = sys.argv[i+1]
    if sys.argv[i] == "-o":
        outName = sys.argv[i+1]

if inDir is None:
    print("Missing input directory (-i [DIR])")
    exit(1)
if outName is None:
    print("Missing output file (-o [FILE])")
    exit(1)

#
odata        = {}
odata["bws"] = []

FBTPrefix = "fbt"
RTPrefix  = "rt"
UBTPrefix = "ubt"

FBTResults = {}
RTResults  = {}
UBTResults = {}

if not inDir.endswith("/"):
    inDir += "/"

# each subdirectory is for one of the bandwidth tests
for subDir in next(os.walk(inDir))[1]:
    dirName = inDir+subDir
    # extracting max bandwidth
    maxBw = int(dirName.split("/")[-1])
    odata["bws"].append(maxBw)

    FBTResults[maxBw] = []
    RTResults[maxBw]  = []
    UBTResults[maxBw] = []
    
    for filename in os.listdir(dirName):
        if not filename.endswith(".out"):
            continue
        fin  = open(dirName+"/"+filename, "r")
        idata = json.load(fin)
        # getting average values of the data previously collected
        compData = {}
        for field in idata["results"][0].keys():
            compData[field] = 0
            for result in idata["results"]:
                compData[field] += result[field]
            avgValue = compData[field] / len(idata["results"])
            errValue = 1.96 * avgValue / math.sqrt(len(idata["results"]))
            compData[field + ":avg"] = avgValue
            compData[field + ":err"] = errValue

        if filename.startswith(RTPrefix):
            # extracting the number of nodes 
            # ("rt_[NUM].out")
            values   = filename.split(".")
            values   = values[0].split("_")
            numNodes = int(values[-1])
            compData["nodes"] = numNodes
            RTResults[maxBw].append(compData)
        
        else:
            # extracting the number of levels ("fbt_[NUM].out" or 
            # "ubt_[NUM].out")
            values   = filename.split(".")
            values   = values[0].split("_")
            nlvls    = int(values[-1])
            if filename.startswith(FBTPrefix):
                numNodes          = (2 ** nlvls) - 1
                compData["nodes"] = numNodes
                FBTResults[maxBw].append(compData)
            elif filename.startswith(UBTPrefix):
                numNodes          = (2 ** nlvls)
                compData["nodes"] = numNodes
                UBTResults[maxBw].append(compData)

odata[FBTPrefix] = FBTResults
odata[RTPrefix]  = RTResults
odata[UBTPrefix] = UBTResults

with open(outName, "w") as outFile:
    json.dump(odata, outFile)