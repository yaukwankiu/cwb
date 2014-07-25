# downloadpics.py
# python script to download cwb radar patterns for today
# examples : 
# http://cwb.gov.tw/V7/observe/radar/Data/MOS_1024/2013-05-19_0015.MOS0.jpg  (with relief)
# http://cwb.gov.tw/V7/observe/radar/Data/MOS2_1024/2013-05-20_0045.2MOS0.jpg (without relief)
# http://cwb.gov.tw/V7/observe/satellite/Data/sbo/sbo-2013-05-20-15-30.jpg (visible spectrum)
# http://cwb.gov.tw/V7/observe/satellite/Data/s3p/s3p-2013-05-20-15-30.jpg (colours)
# http://cwb.gov.tw/V7/observe/satellite/Data/s3q/s3q-2013-05-20-15-30.jpg (enhanced colours)
# http://cwb.gov.tw/V7/observe/satellite/Data/s3o/s3o-2013-05-20-15-30.jpg (black and white)
# http://cwb.gov.tw/V7/observe/temperature/Data/2013-05-20_1300.GTP.jpg  (temperature)
# http://cwb.gov.tw/V7/observe/rainfall/Data/hk520153.jpg               (rainfall -small grid)
# http://cwb.gov.tw/V7/observe/rainfall/Data/2013-05-20_1530.QZJ.grd2.jpg (rainfall -large gird)
# 
# 
# 

"""
USE:
0. install python (preferrably 2.7, though 2.5 probably suffices)
1. put this script in any folder (for me, it is f:\work\CWB\)
2. just run it;  the folders will be created automatically: 
                        .\charts for radar patterns with taiwan relief
                        .\charts2 for pure patterns with taiwan coastline

3. to run:  (for example, if your python.exe is in c:\python27 just like mine)

    c:\python27\python.exe downloadpics.py

4. to download a specific date:
    uncomment and edit the following line:
    url_date = "2013-05-18"   ###### <-------- UNCOMMENT THIS TO GET A SPECIFIC DATE  #########

NOTE:
    At present the Central Weather Bureau keeps every radar pattern for 48 hours.

"""


########################################################################################
# imports
import urllib
import urllib2
import zipfile
import re  
import os
#import sys
from datetime import date, timedelta

########################################################################################
# default parameters and settings - CHANGE THESE TO GET SPECIFIC RESULTS

#####
# 1. generate the current local time
# e.g. 2013,5,20 -> 2013-05-20
today           = date.today()
yesterday       = today - timedelta(1)
year, month, day= yesterday.year, yesterday.month, yesterday.day ###### <--------UNCOMMENT THIS TO GET YESTERDAY  #########
#year, month, day= today.year, today.month, today.day   ###### <--------UNCOMMENT THIS TO GET TODAY  #########

url_date = str(year) + "-" + ("0"+str(month))[-2:] + "-" + ("0"+str(day))[-2:]  # for today
#url_date = "2013-05-25"   ###### <-------- UNCOMMENT THIS TO GET A SPECIFIC DATE  #########

#####
# 2. detect the current operating system and generate the folder separater
sep = os.sep        # "\\" for windows, "/" for linux

#####
# 3. other parameters, server-end and user-end

# http://cwb.gov.tw/V7/observe/radar/Data/MOS_1024/2013-05-19_0015.MOS0.jpg  (with relief)
url_root = "http://cwb.gov.tw/V7/observe/radar/Data/MOS_1024/"      
url_suffix= ".MOS0.jpg"
outputfolder = "charts"

# http://cwb.gov.tw/V7/observe/radar/Data/MOS2_1024/2013-05-20_0045.2MOS0.jpg (without relief)
url_root2 = "http://cwb.gov.tw/V7/observe/radar/Data/MOS2_1024/"   
url_suffix2= ".2MOS0.jpg"
outputfolder2 = "charts2"

# http://cwb.gov.tw/V7/observe/satellite/Data/sbo/sbo-2013-05-20-15-30.jpg (visible spectrum)
url_root3 = "http://cwb.gov.tw/V7/observe/satellite/Data/sbo/sbo-"    
url_suffix3= ".jpg"
outputfolder3 = "satellite1"

# http://cwb.gov.tw/V7/observe/satellite/Data/s3p/s3p-2013-05-20-15-30.jpg (colours)
url_root4 = "http://cwb.gov.tw/V7/observe/satellite/Data/s3p/s3p-"    
url_suffix4= ".jpg"
outputfolder4 = "satellite2"

# http://cwb.gov.tw/V7/observe/satellite/Data/s3q/s3q-2013-05-20-15-30.jpg (enhanced colours)
url_root5 = "http://cwb.gov.tw/V7/observe/satellite/Data/s3q/s3q-"    
url_suffix5= ".jpg"
outputfolder5 = "satellite3"

# http://cwb.gov.tw/V7/observe/satellite/Data/s3o/s3o-2013-05-20-15-30.jpg (black and white)
url_root6 = "http://cwb.gov.tw/V7/observe/satellite/Data/s3o/s3o-"    
url_suffix6= ".jpg"
outputfolder6 = "satellite4"

# http://cwb.gov.tw/V7/observe/temperature/Data/2013-05-20_1300.GTP.jpg  (temperature)
url_root7 = "http://cwb.gov.tw/V7/observe/temperature/Data/"    
url_suffix7= ".GTP.jpg"
outputfolder7 = "temperature"

# http://cwb.gov.tw/V7/observe/rainfall/Data/hk520153.jpg               (rainfall -small grid)
url_root8 = "http://cwb.gov.tw/V7/observe/rainfall/Data/hk"    
url_suffix8= ".jpg"
outputfolder8 = "rainfall1"

# http://cwb.gov.tw/V7/observe/rainfall/Data/2013-05-20_1530.QZJ.grd2.jpg (rainfall -large gird)
url_root9 = "http://cwb.gov.tw/V7/observe/rainfall/Data/"    
url_suffix9= ".QZJ.grd2.jpg"
outputfolder9 = "rainfall2"
# 

########################################################################################
# defining the functions
def download(url, to_filename, folder="."):
    ################
    # first, create the directory if it doesn't exist
    try: 
        os.makedirs(folder + sep + url_date)
    except OSError:
        if not os.path.isdir(folder + sep + url_date):
            raise
    ###############
    # download
    to_path = folder + sep + url_date + sep + to_filename
    try:
        f = urllib.urlretrieve(url, to_path)
        print to_path
        returnvalue = 1
    except:
        print "Error!", url
        returnvalue = 0
    # delete if filesize < 3000 (with safety margin)
    if os.path.getsize(to_path) < 3000:
        os.remove(to_path)
    return returnvalue
def downloadoneday(url_root=url_root, url_date=url_date, url_suffix=url_suffix, 
                 outputfolder=outputfolder, type="radar"):

    for hour in range(24):
        for minute in [0, 7, 15, 22, 30, 27, 45,52 ]:
            #if (minute == 15 or minute ==45) and \
            #    (type == "rainfall1" or type =="rainfall2" or type =="satellite"):
            #    continue                        # no data
            if type == "radar":
                timestring = "_" + ("0"+str(hour))[-2:] + ("00"+str(minute))[-2:]
            elif type == "satellite":           # 2013-05-20-15-30
                timestring = "-" + ("0"+str(hour))[-2:] + "-" + ("00"+str(minute))[-2:]
            elif type == "temperature":         # "2013-05-20_1300"
                timestring = "_" + ("0"+str(hour))[-2:] + ("00"+str(minute))[-2:]
            elif type == "rainfall2":           # "2013-05-20_1530"
                timestring = "_" + ("0"+str(hour))[-2:] + ("00"+str(minute))[-2:]
            elif type == "rainfall1":           # "520100" for 2013-05-20 10:00 - the odd man out
                timestring = ("0"+str(hour))[-2:] + str(minute)[0]

            url = url_root + url_date + timestring + url_suffix

            if type == "rainfall1":           # "520153" for 2013-05-20 15:30, 
                                              # "520010" for 2013-05-20 01:00, 
                                              # "520100" for 2013-05-20 10:00 - the odd man out
                url = url_root + str(int(url_date[5:7])) + str(int(url_date[8:10])) + \
                      timestring + url_suffix 
            to_filename = url_date +"_" +("0"+str(hour))[-2:] +("00"+str(minute))[-2:] +url_suffix
            download(url=url, to_filename=to_filename, folder=outputfolder)

########################################################################################
# running
def main():
    """ """
    downloadoneday(url_root=url_root, url_date=url_date, url_suffix=url_suffix,
                        outputfolder=outputfolder, type="radar")
    downloadoneday(url_root=url_root2, url_date=url_date, url_suffix=url_suffix2, 
                        outputfolder=outputfolder2, type="radar")
    downloadoneday(url_root=url_root3, url_date=url_date, url_suffix=url_suffix3, 
                        outputfolder=outputfolder3, type="satellite")
    downloadoneday(url_root=url_root4, url_date=url_date, url_suffix=url_suffix4, 
                        outputfolder=outputfolder4, type="satellite")
                        
    downloadoneday(url_root=url_root5, url_date=url_date, url_suffix=url_suffix5, 
                        outputfolder=outputfolder5, type="satellite")
                        
    downloadoneday(url_root=url_root6, url_date=url_date, url_suffix=url_suffix6, 
                        outputfolder=outputfolder6, type="satellite")
    downloadoneday(url_root=url_root7, url_date=url_date, url_suffix=url_suffix7, 
                        outputfolder=outputfolder7, type="temperature")
    downloadoneday(url_root=url_root8, url_date=url_date, url_suffix=url_suffix8, 
                        outputfolder=outputfolder8, type="rainfall1")
    downloadoneday(url_root=url_root9, url_date=url_date, url_suffix=url_suffix9, 
                        outputfolder=outputfolder9, type="rainfall2")

if __name__ == '__main__':
    main()
    
