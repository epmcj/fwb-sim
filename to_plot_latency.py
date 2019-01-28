import os
import sys
import json
import plotter

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
    fname = outDir + "latency.txt"
    with open(fname, "w") as fout:
        for prefix in prefixes:
            xs   = []
            ys   = []
            errs = []
            bws  = []
            for bw in data["bws"]:
                bws.append(bw)
                x   = []
                y   = []
                err = []
                for compData in data[prefix][str(bw)]:
                    x.append(compData["nodes"])
                    y.append(compData["avg_latency:avg"])
                    err.append(compData["avg_latency:err"])
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
            
            fout.write(prefix + "\n")
            fout.write("x   = {}\n".format(xs[0]))
            for i in range(len(bws)):
                fout.write("y   = {}\n".format(ys[i]))
                fout.write("err = {}\n\n".format(errs[i]))
