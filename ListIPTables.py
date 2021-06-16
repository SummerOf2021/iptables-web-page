import json

f = open("list.txt", "r")
ipList = f.read()
f.close()
ipList = ipList.splitlines()

chain = ["INPUT", "FORWARD", "OUTPUT"]
k = 0

dict1 = {}
numDict = 0
fields = ["chain", "id", "pkts", "bytes", "target", "prot", "opt", "in", "out", "source", "destination", "spt", "dpt"]
id = 1

i = 2
while i < len(ipList):
    if ipList[i] == "":
        i += 2
        k += 1
        id = 1
        if k == 3:
            break
    else:
        ipList[i] = chain[k] + " " + str(id) + ipList[i]
        id += 1
        line = ipList[i].split(None, -1)
        dict2 = {}
        j = 0
        while j < len(fields):
            try:
                if j > 10:
                    dict2[fields[j]] = line[j+1][4:]
                else:
                    dict2[fields[j]] = line[j]
            except:
                dict2[fields[j]] = ""
            j += 1
        dict1[numDict] = dict2
        numDict += 1
    i += 1

output = open("list.json", "w")
json.dump(dict1, output, indent=2)
output.close()