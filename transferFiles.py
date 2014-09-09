# from source /CWB/ folder to target /CWB/ folder

source = "d:/CWB/"
target = "f:/CWB/"
dryRun = False
keys=["charts",'fcst', 'hs1', 'hsao','hq', 'qpf', 'rainfall', "satellite", 'sco', "sea", "temper", "s0",'uvi',]
nokeys = ['allinone', '.git',]

print "keys:", keys
print "nokeys:", nokeys
print "transferring:", source, "->", target
print "sleeping 3 seconds"
import time
time.sleep(3)

#key1 = "hs1"
#nokey='charts2'

import os
import shutil
import time

L   = os.listdir(source)
for nokey in nokeys:
    L = [v for v in L if not (nokey in v)]
    L = [v for v in L if os.path.isdir(v)]

L1  = []
for key in keys:
    L1.extend([v+"/" for v in L if key in v])
L= L1
print "L:", '\t'.join(L)
print "sleeping 3 seconds"
time.sleep(3)

for typeFolder in L:
    print "\n--------------------------\ntransferring", typeFolder
    L2 = os.listdir(source + typeFolder)   
    #print L2 #debug
    L2 = [v + "/" for v in L2 if not ('.git' in v)]
    for dateFolder in L2:
        print '\n............\ntransferring', dateFolder
        if '.git' in dateFolder:
            continue # /.git/     folder
        L3 = os.listdir(source+typeFolder+dateFolder)
        if L3 == []:
            continue
        else:
            for fileName in L3:
                #if '.git' in fileName:
                #    continue # /.git/     folder
                if os.path.exists(target+typeFolder+dateFolder+fileName):
                    pass
                    #print "target exists!"
                else:
                    print source + typeFolder  + dateFolder  + fileName , 
                    print "->",
                    print target
                    if not dryRun:
                        if not os.path.exists(target+typeFolder+dateFolder):
                            os.makedirs(target+typeFolder+dateFolder)
                        shutil.copyfile( source + typeFolder  + dateFolder  + fileName,  target + typeFolder  + dateFolder  + fileName )
                    