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
import sys
from datetime import date, timedelta
import time

########################################################################################
# defining the container class
# added 2013-08-21

class Url_info:
    def __init__(self, url_root, url_suffix, outputFolder, timeStringType, 
                    #minutes=[0, 6, 12, 24, 30, 36, 42, 48, 54 ],
                    minutes=[0,30],
                    ):
        self.url_root       = url_root
        self.url_suffix     = url_suffix
        self.outputFolder   = outputFolder
        self.timeStringType =  timeStringType
        self.minutes        = minutes
########################################################################################
# default parameters and settings - CHANGE THESE TO GET SPECIFIC RESULTS

#####
# 1. generate the current local time
# e.g. 2013,5,20 -> 2013-05-20
today           = date.today()
yesterday       = today - timedelta(1)

year, month, day= yesterday.year, yesterday.month, yesterday.day ###### <--------UNCOMMENT THIS TO GET YESTERDAY  #########
url_date_yesterday = str(year) + "-" + ("0"+str(month))[-2:] + "-" + ("0"+str(day))[-2:]  # for yesterday
year, month, day= today.year, today.month, today.day   ###### <--------UNCOMMENT THIS TO GET TODAY  #########
url_date_today = str(year) + "-" + ("0"+str(month))[-2:] + "-" + ("0"+str(day))[-2:]  # for today

url_date=url_date_yesterday

#url_date = "2013-05-18"   ###### <-------- UNCOMMENT THIS TO GET A SPECIFIC DATE  #########

#####
# 2. detect the current operating system and generate the folder separater
sep = os.sep        # "\\" for windows, "/" for linux
# actually, no need.  anyhow
#####
# 3. other parameters, server-end and user-end

defaultReloadMode = False
# http://cwb.gov.tw/V7/observe/radar/Data/MOS_1024/2013-05-19_0015.MOS0.jpg  (with relief)
url_root = "http://cwb.gov.tw/V7/observe/radar/Data/MOS_1024/"      
url_suffix= ".MOS0.jpg"
outputFolder = "charts"

# http://cwb.gov.tw/V7/observe/radar/Data/MOS2_1024/2013-05-20_0045.2MOS0.jpg (without relief)
url_root2 = "http://cwb.gov.tw/V7/observe/radar/Data/MOS2_1024/"   
url_suffix2= ".2MOS0.jpg"
outputFolder2 = "charts2"

# http://cwb.gov.tw/V7/observe/satellite/Data/sbo/sbo-2013-05-20-15-30.jpg (visible spectrum)
url_root3 = "http://cwb.gov.tw/V7/observe/satellite/Data/sbo/sbo-"    
url_suffix3= ".jpg"
outputFolder3 = "satellite1"

# http://cwb.gov.tw/V7/observe/satellite/Data/s3p/s3p-2013-05-20-15-30.jpg (colours)
url_root4 = "http://cwb.gov.tw/V7/observe/satellite/Data/s3p/s3p-"    
url_suffix4= ".jpg"
outputFolder4 = "satellite2"

# http://cwb.gov.tw/V7/observe/satellite/Data/s3q/s3q-2013-05-20-15-30.jpg (enhanced colours)
url_root5 = "http://cwb.gov.tw/V7/observe/satellite/Data/s3q/s3q-"    
url_suffix5= ".jpg"
outputFolder5 = "satellite3"

# http://cwb.gov.tw/V7/observe/satellite/Data/s3o/s3o-2013-05-20-15-30.jpg (black and white)
url_root6 = "http://cwb.gov.tw/V7/observe/satellite/Data/s3o/s3o-"    
url_suffix6= ".jpg"
outputFolder6 = "satellite4"

# http://cwb.gov.tw/V7/observe/temperature/Data/2013-05-20_1300.GTP.jpg  (temperature)
url_root7 = "http://cwb.gov.tw/V7/observe/temperature/Data/"    
url_suffix7= ".GTP.jpg"
outputFolder7 = "temperature"

# http://cwb.gov.tw/V7/observe/rainfall/Data/hk520153.jpg               (rainfall -small grid)
url_root8 = "http://cwb.gov.tw/V7/observe/rainfall/Data/hk"    
url_suffix8= ".jpg"
outputFolder8 = "rainfall1"

# http://cwb.gov.tw/V7/observe/rainfall/Data/2013-05-20_1530.QZJ.grd2.jpg (rainfall -large gird)
url_root9 = "http://cwb.gov.tw/V7/observe/rainfall/Data/"    
url_suffix9= ".QZJ.grd2.jpg"
outputFolder9 = "rainfall2"
# 

############  ####################  ####################  ################################
# the following are added on 2013-08-21

# http://www.cwb.gov.tw/V7/observe/satellite/Sat_H_EA.htm?type=1#
# http://www.cwb.gov.tw/V7/observe/satellite/Data/HSAO/HSAO-2013-08-21-17-30.jpg  (high definition south-east asia - visible light)
url_root10 = "http://www.cwb.gov.tw/V7/observe/satellite/Data/HSAO/HSAO-"    
url_suffix10= ".jpg"
outputFolder10 = "hsao"
timeStringType10         = "satellite"


# 

############################################################################################################################################
#  charts

url_info_list = []

# http://www.cwb.gov.tw/V7/observe/satellite/Data/HS1O/HS1O-2013-08-21-17-30.jpg (high definition south-east asia - infra-red)
url_info_list.append(Url_info("http://www.cwb.gov.tw/V7/observe/satellite/Data/HS1O/HS1O-",
                              ".jpg",
                              "hs1o",
                              "satellite"))
# 

# http://www.cwb.gov.tw/V7/observe/satellite/Data/HS1P/HS1P-2013-08-21-17-30.jpg (high definition south-east asia - coloured)
url_info_list.append(Url_info("http://www.cwb.gov.tw/V7/observe/satellite/Data/HS1P/HS1P-",
                              ".jpg",
                              "hs1p",
                              "satellite"))

# http://www.cwb.gov.tw/V7/observe/satellite/Data/HS1Q/HS1Q-2013-08-21-17-30.jpg (high definition south-east asia - colour-enhanced)
url_info_list.append(Url_info("http://www.cwb.gov.tw/V7/observe/satellite/Data/HS1Q/HS1Q-",
                              ".jpg",
                              "hs1q",
                              "satellite"))

# http://www.cwb.gov.tw/V7/observe/satellite/Data/sco/sco-2013-08-21-17-30.jpg (global - visible light)
url_info_list.append(Url_info("http://www.cwb.gov.tw/V7/observe/satellite/Data/sco/sco-",
                              ".jpg",
                              "sco",
                              "satellite"))

# http://www.cwb.gov.tw/V7/observe/satellite/Data/s0p/s0p-2013-08-21-17-30.jpg (global - coloured)
url_info_list.append(Url_info("http://www.cwb.gov.tw/V7/observe/satellite/Data/s0p/s0p-",
                              ".jpg",
                              "s0p",
                              "satellite"))

# http://www.cwb.gov.tw/V7/observe/satellite/Data/s0q/s0q-2013-08-21-17-30.jpg (global - colour-enhanced)
url_info_list.append(Url_info("http://www.cwb.gov.tw/V7/observe/satellite/Data/s0q/s0q-",
                              ".jpg",
                              "s0q",
                              "satellite"))

# http://www.cwb.gov.tw/V7/observe/satellite/Data/s0o/s0o-2013-08-21-17-30.jpg (global - infra-red)
url_info_list.append(Url_info("http://www.cwb.gov.tw/V7/observe/satellite/Data/s0o/s0o-",
                              ".jpg",
                              "s0o",
                              "satellite"))

# http://www.cwb.gov.tw/V7/observe/rainfall/Data/hq821190.jpg (hourly rainfall)
url_info_list.append(Url_info("http://www.cwb.gov.tw/V7/observe/rainfall/Data/hq",
                              ".jpg",
                              "hq",
                              "rainfall1"))
#http://www.cwb.gov.tw/V7/forecast/fcst/Data/SFC01.pdf
url_info_list.append(Url_info(url_root = "http://www.cwb.gov.tw/V7/forecast/fcst/Data/SFC01",
                              url_suffix=".pdf",
                              outputFolder="fcst",
                              timeStringType="fcst",
                              minutes=[0,-1],
                              ))

#   2014-07-25

#http://www.cwb.gov.tw/V7/observe/UVI/Data/UVI.png
url_info_list.append(Url_info(url_root = "http://www.cwb.gov.tw/V7/observe/UVI/Data/UVI",
                              url_suffix=".png",
                              outputFolder="uvi",
                              timeStringType="fcst",
                              minutes=[0,-1],
                              ))

#http://www.cwb.gov.tw/V7/observe/real/Data/Real_C.png
url_info_list.append(Url_info(url_root = "http://www.cwb.gov.tw/V7/observe/real/Data/Real_C",
                              url_suffix=".png",
                              outputFolder="real_c",
                              timeStringType="fcst",
                              minutes=[0,-1],
                              ))
                              
#http://www.cwb.gov.tw/V7/observe/real/Data/Real_E.png
url_info_list.append(Url_info(url_root = "http://www.cwb.gov.tw/V7/observe/real/Data/Real_E",
                              url_suffix=".png",
                              outputFolder="real_e",
                              timeStringType="fcst",
                              minutes=[0,-1],
                              ))
                              
#http://www.cwb.gov.tw/V7/observe/real/Data/Real_I.png
url_info_list.append(Url_info(url_root = "http://www.cwb.gov.tw/V7/observe/real/Data/Real_I",
                              url_suffix=".png",
                              outputFolder="real_i",
                              timeStringType="fcst",
                              minutes=[0,-1],
                              ))
                              
#http://www.cwb.gov.tw/V7/observe/real/Data/Real_N.png
url_info_list.append(Url_info(url_root = "http://www.cwb.gov.tw/V7/observe/real/Data/Real_N",
                              url_suffix=".png",
                              outputFolder="real_n",
                              timeStringType="fcst",
                              minutes=[0,-1],
                              ))
                              
#http://www.cwb.gov.tw/V7/observe/real/Data/Real_S.png
url_info_list.append(Url_info(url_root = "http://www.cwb.gov.tw/V7/observe/real/Data/Real_S",
                              url_suffix=".png",
                              outputFolder="real_s",
                              timeStringType="fcst",
                              minutes=[0,-1],
                              ))


#   end charts
############################################################################################################################################

############################################################################################################################################
#   htmls

# http://www.cwb.gov.tw/V7/marine/sst_report/cht/tables/sea_P.html
# http://www.cwb.gov.tw/V7/marine/sst_report/cht/charts/sea_B.png
#   "A"~"P" = chr(65) ~ chr(80)
regionalLetters = [chr(v) for v in range(65,81)]
seaTemperatureCharts = []
for ch in regionalLetters:
    seaTemperatureCharts.append(Url_info(url_root = "http://www.cwb.gov.tw/V7/marine/sst_report/cht/tables/sea_%s" %ch,
                                  url_suffix=".html",
                                  outputFolder="sea_%s" %ch,
                                  timeStringType="sea",
                              minutes=[0,-1],
                              ))
    
    seaTemperatureCharts.append(Url_info(url_root = "http://www.cwb.gov.tw/V7/marine/sst_report/cht/charts/sea_%s" %ch,
                                  url_suffix=".png",
                                  outputFolder="sea_%s" %ch,
                                  timeStringType="sea",
                              minutes=[0,-1],
                              ))

url_info_list += seaTemperatureCharts
#   end htmls
############################################################################################################################################

########################################################################################
# defining the functions
def download(url, to_filename, url_date=url_date, folder=".", reload=defaultReloadMode, verbose=False):
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
    # check if to_path exists first!!!
    # added  2013-08-21
    if os.path.isfile(to_path) and reload==False:
        if verbose:
            print to_path, ' <--- already exists!!'
        if os.path.getsize(to_path) >= 6000:
            return 0.5
        else:
            print to_path,  'file broken! - removed'
    try:
        try:
            f = urllib.urlretrieve(url, to_path)
        except:
            print "using urllib2"
            f = urllib2.urlopen(url)
            x = f.read()
            open(to_path, 'w').write(x)

        if (url.endswith('.png') or url.endswith('.jpg')) and os.path.getsize(to_path) < 1000 \
            and 'sea' not in url[:-20]: #hack
            os.remove(to_path)
            print url, '-->not found--> ' + to_path 
            returnvalue = 0
        else:
            print to_path, '- fetched!!!!!!!!!!!!!!!!!!!!!'
        returnvalue = 1
    except:
        print "Error !", url
        returnvalue = 0
    # delete if filesize < 6000 (with safety margin)
    return returnvalue

def downloadoneday(url_root=url_root, url_date=url_date, url_suffix=url_suffix, 
                 outputFolder=outputFolder, minutes=[0, 6, 12, 24, 30, 36, 42, 48, 54 ],    #2014-07-25
                 type="radar"):
    onceAdayOnly = False #setting the flag
    #print type, url_date, url_suffix
    try:
        for hour in range(24):
            if onceAdayOnly:
                print outputFolder, "once a day only"
                #time.sleep(.2)   #throttle
                break
            #for minute in [0, 7, 15, 22, 30, 37, 45,52 ]:
            for minute in minutes:  #2014-07-25
                if minute <0 :
                    onceAdayOnly =True
                    break               # set the minutes to [0, -999] if you want to download it once for the day
                #print 'checkpoint 1' #debug
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
                elif type =="fcst" or type=='sea':
                    timestring = ""                 # http://www.cwb.gov.tw/V7/forecast/fcst/Data/SFC01.pdf
                    
                if type =="fcst" or type=='sea':
                    url = url_root + timestring + url_suffix        #2014-07-22
                else:
                    url = url_root + url_date + timestring + url_suffix

                if type == "rainfall1":           # "520153" for 2013-05-20 15:30, 
                                                  # "520010" for 2013-05-20 01:00, 
                                                  # "520100" for 2013-05-20 10:00 - the odd man out
                                                  # "a02090" for 2013-10-02 09:00
                    
                    m = int(url_date[5:7])
                    if m < 10:
                        monthString = str(m)
                    else:
                        monthString = chr(m+87)  # 'a' for 10, 'b' for 11, etc
                    #url = url_root + monthString + str(int(url_date[8:10])) + timestring + url_suffix   # doesn't work any more 2013-10-01
                    url = url_root + monthString + url_date[8:10] + timestring + url_suffix   # added 2013-10-01
                    #debug
                    print url
                    #time.sleep(1)
                    #end debug
                #print 'checkpoint 2' #debug

                if type == "fcst":
                    #to_filename = "SFC01" + "_" + time.asctime().replace(" ","_").replace(":",".") + url_suffix   #2014-07-22
                    to_filename =  outputFolder + "_" + time.asctime().replace(" ","_").replace(":","") + url_suffix   #2014-07-25
                elif type =='sea':
                    to_filename =  outputFolder + "_" + time.asctime().replace(" ","_").replace(":","")[:10] + url_suffix   #2014-07-25
                else:
                    to_filename = url_date +"_" +("0"+str(hour))[-2:] +("00"+str(minute))[-2:] +url_suffix
                #print 'checkpoint 3' #debug
                download(url=url, to_filename=to_filename, url_date=url_date, folder=outputFolder)

        if len(minutes)==1:
            time.sleep(.5)

    except:
        print "--------------------------------------------------------"
        print "Error!!!! During", type, url_root + url_suffix
        

def downloadoneday2(url_info, url_date=url_date):
    u = url_info
    return downloadoneday(url_root=u.url_root, url_date=url_date, url_suffix=u.url_suffix, 
                        outputFolder=u.outputFolder, type=u.timeStringType)

        
########################################################################################
# running
def main(url_date=url_date):

    """ """
    downloadoneday(url_root=url_root, url_date=url_date, url_suffix=url_suffix,
                        outputFolder=outputFolder, type="radar")
    downloadoneday(url_root=url_root2, url_date=url_date, url_suffix=url_suffix2, 
                        outputFolder=outputFolder2, type="radar")
    downloadoneday(url_root=url_root3, url_date=url_date, url_suffix=url_suffix3, 
                        outputFolder=outputFolder3, minutes = [0,30],
                        type="satellite")
    downloadoneday(url_root=url_root4, url_date=url_date, url_suffix=url_suffix4, 
                        outputFolder=outputFolder4, minutes = [0,30],
                        type="satellite")
                        
    downloadoneday(url_root=url_root5, url_date=url_date, url_suffix=url_suffix5, 
                        outputFolder=outputFolder5, 
                        minutes = [0,30],
                        type="satellite")
                        
    downloadoneday(url_root=url_root6, url_date=url_date, url_suffix=url_suffix6, 
                        outputFolder=outputFolder6, minutes = [0,30],
                        type="satellite")
    downloadoneday(url_root=url_root7, url_date=url_date, url_suffix=url_suffix7, 
                        outputFolder=outputFolder7,minutes = [0,30],
                        type="temperature")
    downloadoneday(url_root=url_root8, url_date=url_date, url_suffix=url_suffix8, 
                        outputFolder=outputFolder8, minutes = [0,30],
                        type="rainfall1")
    downloadoneday(url_root=url_root9, url_date=url_date, url_suffix=url_suffix9, 
                        outputFolder=outputFolder9,minutes = [0,30],
                         type="rainfall2")
    downloadoneday(url_root=url_root10, url_date=url_date, url_suffix=url_suffix10, 
                        outputFolder=outputFolder10,minutes = [0,30],
                         type=timeStringType10)
    for u in url_info_list:
        downloadoneday(url_root=u.url_root, url_date=url_date, url_suffix=u.url_suffix, 
                        outputFolder=u.outputFolder, type=u.timeStringType, minutes=u.minutes)
        


if __name__ == '__main__':
    time0= int(time.time())
    argv = sys.argv
    if len(argv) > 1:
        try:
            secs = int(argv[1])
            print 'sleeping %d seconds' % secs, 'from localtime', time.asctime()
            print 'waking up at localtime', time.asctime(time.localtime( time.time()+ secs ))
            time.sleep(secs)
            while True:
                timeStart       = time.time()
                today           = date.today()
                yesterday       = today - timedelta(1)
                year, month, day= yesterday.year, yesterday.month, yesterday.day ###### <--------UNCOMMENT THIS TO GET YESTERDAY  #########
                #year, month, day= today.year, today.month, today.day   ###### <--------UNCOMMENT THIS TO GET TODAY  #########
                
                url_date = str(year) + "-" + ("0"+str(month))[-2:] + "-" + ("0"+str(day))[-2:]  # for today
                main(url_date=url_date)
                timeSpent   = int(time.time()) - timeStart
                print "time spent", timeSpent
                print 'sleeping', 86400-timeSpent, 'seconds, from localtime', time.asctime(time.localtime())
                print 'waking up at local time', time.asctime(time.localtime( time.time()+ 86400-timeSpent ))
                time.sleep(86400-timeSpent)
        except ValueError:
            for url_date in sys.argv[1:]:
                main(url_date)
    else:
        print "\n\nYESTERDAY:\n"
        main(url_date=url_date_yesterday)
        print "\n\nTODAY:\n"
        main(url_date=url_date_today)

    #main(url_date='2013-07-11')
    #main(url_date='2013-07-09')
    #main(url_date='2013-07-08')
    #main(url_date='2013-07-07')
    print "\nTime spent:", int(time.time()) - time0
    print "Time now:", time.asctime()
