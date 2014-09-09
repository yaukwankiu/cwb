import os, shutil, sys
import time

timeString = str(int(time.time()))
def putAllInOneFolder(folderName="hs1q/", startingFrom="", verbose=True, overWrite=True):
    inputFolder  = folderName
    outputFolder = folderName[:-1] + '-allinone-'+'/'
    try:
        print 'creating folder'
        os.makedirs(outputFolder)
    except:
        print 'folder exists!'
    L = os.listdir(inputFolder)
    L = [v for v in L if v>=startingFrom]       #2014-06-09
    L.sort()            # ['2013-08-20', ...]
    for m in L: 
        subfolder = inputFolder + m + '/' # subfolder = '2013-08-20', etc
        M = os.listdir(subfolder)
        for n in M:
            src = subfolder + n
            dst = outputFolder + n
            if verbose:
                print src, '-->', outputFolder,
            if overWrite or (not os.path.exists(dst)):
                shutil.copyfile(src, dst)
                print "..copied"
            else:
                print "..FILE EXISTS AND SKIPPED"


def main(folderName='hs1q', startingFrom="", verbose=True, overWrite=True, looping=False):
    argv = sys.argv
    if len(argv)>1:
        folderName = argv[1]
    if len(argv)>2:
        try:
            secs = int(argv[2])
            print 'time now:', time.asctime()
            print 'sleeping', secs,' seconds'
            time.sleep(secs)
        except:
            startingFrom = argv[2]
    if len(argv)>3:
        if 'looping' in argv or 'daily' in argv:
            looping = True
        if 'overWrite' in argv or 'overwrite' in argv:
            overWrite=True
        if 'fast' in argv or 'quick' in argv:
            overWrite = False
    if looping:
        countDown = -1  # so that it never reaches 0
    else:
        countDown = 1

    print "folderName, looping, startingFrom:", folderName, looping, startingFrom
    while countDown != 0:
        timeString = int(time.time())
        print 'copying folder', folderName
        print 'timeString:', timeString
        print 'sleeping 3 seconds'
        time.sleep(3)
        if not folderName.endswith('/'):
            folderName+="/"
        putAllInOneFolder(folderName, startingFrom=startingFrom ,verbose=verbose, overWrite=overWrite)
        timeSpent = int(time.time()) - int(timeString)
        print "time spent:", timeSpent
        countDown -= 1
        print 'time now', time.asctime()
        print 'sleeping', max(85000, 86400-timeSpent),  'seconds...'
        time.sleep(max(85000, 86400-timeSpent))

    print 'countDown=0.  goodbye!'
if __name__ == '__main__':
	main()
