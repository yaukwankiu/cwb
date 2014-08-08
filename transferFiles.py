# from source /CWB/ folder to target /CWB/ folder

source = "d:/CWB/"
target = "f:/CWB/"
dryRun = False
import os
import shutil
import time

L   = os.listdir(source)
L   = [v for v in L if os.path.isdir(source+v) and not ('.git' in v) and not ('allinone') in v]
L   = [v+"/" for v in L]

print '\t'.join(L)

time.sleep(3)

for typeFolder in L:
    L2 = os.listdir(source + typeFolder)   
    #print L2 #debug
    L2 = [v + "/" for v in L2 if not ('.git' in v)]
    for dateFolder in L2:
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
                    