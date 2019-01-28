import os
import sys
import json
import plotter

# Legend in format "BW %d-%d-...-%d MHz"
def get_legend(maxBW):
    bws = [maxBW]
    while bws[-1] != 2:
        bws.append(bws[-1]/2)
    bws.sort()
    legend = "BW "
    for bw in bws:
        legend += str(int(bw)) + "-"
    legend = legend[:-1] + " MHz"
    return legend


# input reading
inName = None
outDir = None

for i in range(1, len(sys.argv), 2):
    if sys.argv[i] == "-i":
        inName = sys.argv[i+1]
    if sys.argv[i] == "-o":
        outDir = sys.argv[i+1]
        if not outDir.endswith("/"):
            outDir += "/"

if inName is None:
    print("Missing input file (-i [FILE])")
    exit(1)
if outDir is None:
    print("Missing output dir (-o [DIR])")
    exit(1)

FBTPrefix = "fbt"
RTPrefix  = "rt"
UBTPrefix = "ubt"
prefixes = [FBTPrefix, RTPrefix, UBTPrefix]

with open(inName, "r") as inFile:
    # reading pre-compressed data using "compress_data.py"
    data = json.load(inFile)
    for prefix in prefixes:
        xs   = []
        ys   = []
        errs = []
        bws  = []
        # for bw in data["bws"]:
        for bw in data["coi"]:
            bws.append(bw)
            x   = []
            y   = []
            err = []
            for compData in data[prefix][str(bw)]:
                x.append(compData["nodes"])
                y.append(compData["num_slots:avg"])
                err.append(compData["num_slots:err"])
            temp = sorted(zip(x, y, err))
            x   = [e for e,_,_ in temp]
            y   = [e for _,e,_ in temp]
            err = [e for _,_,e in temp]
            xs.append(x)
            ys.append(y)
            errs.append(err)
        temp = sorted(zip(bws, xs, ys, errs))
        bws  = [e for e,_,_,_ in temp]
        xs   = [e for _,e,_,_ in temp]
        ys   = [e for _,_,e,_ in temp]
        errs = [e for _,_,_,e in temp]
        legends = []
        # for bw in bws:
        #     legends.append(get_legend(bw))
        legends = data["coi"]
        fname = outDir + prefix + "_tslots.png"
        plotter.plotMultLineChart(xs, ys, errs, legends, "Nodes", 
                                  "Number of timeslots", title=None, 
                                  fileName=fname, fontsize=18, linewidth=2)
