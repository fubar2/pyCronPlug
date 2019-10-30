#!/usr/bin/python3
# mad idea
# generate cron file to run a miiplug for a given number of seconds mostly during the day
# since we are watering plants.
# adjust the constants in SKEL to suit your device and the constants controlling total water time, hours to trigger watering in day and night 
# and the code will allocate the watering time so your night time watering is the equivalent of 1/DAYWEIGHT of a day time watering. 
# may need fiddling with to ensure all plants are totally soaked to maximum weight each watering event.
# plug pump into the xiaomi mi-plug so it runs under control of the cron jobs
# idea comes from watching weights not peak properly after day time waterings - most water is used during the day....


import os
import sys
from pathlib import Path
import datetime

MYPATH = os.getcwd() # where cron jobs can find the generated scripts
MYNAME = sys.argv[0] # our name

PYPATH="/home/ross/rossgit/loadcellflask/venv/bin/python" 
# find this path using `which python` while in a virtual environment - must use the same VM for cron jobs 

TOTTIME=200 # total seconds turned on per 24 hours
DAYWEIGHT=3 # 3 times as much during day as night
DAYWTIMES = [9,11,13,15,17] # run a day time watering at each of these hours
NIGHTWTIMES = [22,4] # and these for night
CRONTABFILE = os.path.join(MYPATH,'gencrontab.txt')

LOGTO = 'watercron.log'

# adjust the script skeleton to suit your chuangmi plug token and ip
# obtaining these is left as an exercise for the reader :)

SKEL = """#!/usr/bin/python3
## written by %s @ %s
from miio import chuangmi_plug
from time import sleep
from datetime import datetime


IP="192.168.1.30"
TOK="3530efcedbd24a95df4716de429a7b0c" # mine not yours...

cP = chuangmi_plug.ChuangmiPlug(ip=IP, token=TOK, start_id=0, debug=0, lazy_discover=True, model='chuangmi.plug.m1')
cP.on()
sleep(0.01)
tstamp = datetime.now().ctime()
print('### %%s: watering cron job has turned plug on for %f seconds' %% tstamp)
print(cP.status())
sleep(%f)
cP.off()
sleep(0.01)
tstamp = datetime.now().ctime()
print('### %%s: watering cron job has turned plug off' %% tstamp)
print(cP.status())

"""



def getCronf(task,hours2run):
	"""
	construct paths to our generated code and use specified virtual python path for each cron command
	Jobs run at 1 minute past the specified hour
	"""
	writeme = []
	cl = '%s %s' % (PYPATH, os.path.join(MYPATH,task))
	for i,h in enumerate(hours2run):
		s = '1	%s	*	*	*	%s 2>&1 >> %s\n' % (h,cl,os.path.join(MYPATH,LOGTO))
		writeme.append(s)
	return writeme

def writeCronf(cronlist):
	"""
	"""
	f = open(CRONTABFILE,'w')
	now = datetime.datetime.now().ctime()
	f.write('# written by %s @ %s\n# m h dom mon dow command\n' % (MYNAME,now))
	f.write(''.join(cronlist))
	f.close()

def writeTask(taskName,hourtorun,duration):
	""" 
	Instantiate a script to turn the plug on for a specified time based on SKEL
	"""
	now = datetime.datetime.now().ctime()
	scrpt = SKEL % (MYNAME,now,duration,duration)
	f = open(taskName,'w')
	f.write(scrpt)
	f.close()


def genCron():
	"""figure watering pattern to a total, weighted during the day for far less at night"""
	nDay = len(DAYWTIMES)
	nNight = len(NIGHTWTIMES)
	dayT = DAYWEIGHT*(TOTTIME/(nNight + nDay*DAYWEIGHT)) 
	# algebra for 1/3 of a day water at night
	nightT  = (TOTTIME - nDay*dayT)/nNight # total watering at night for 3X during day
	tN = 'runmeDay.py'
	writeTask(tN,DAYWTIMES,dayT)
	cronrows = getCronf(tN,DAYWTIMES)
	tN = 'runmeNight.py'
	writeTask(tN,NIGHTWTIMES,nightT)
	cronrows += getCronf(tN,NIGHTWTIMES)
	cl = [(int(x.split('\t')[1]),x) for x in cronrows] # decorate with hour
	cl.sort()
	cl = [x[1] for x in cl] # undecorate
	writeCronf(cl)
	os.system('crontab %s' % CRONTABFILE)
	print('#### Updated your crontab file with:\n',''.join(cl))

if __name__ == "__main__":
	genCron()

			
