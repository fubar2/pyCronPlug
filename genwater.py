#!/usr/bin/python3
# mad idea
# generate cron file to run a miiplug for a given number of seconds mostly during the day
# since we are watering plants.
# adjust the constants in SKEL to suit your device and the constants controlling total water time, hours to trigger watering in day and night 
# and the code will allocate the watering time so your night time watering is the equivalent of 1/DAYWEIGHT of a day time watering. 
# may need fiddling with to ensure all plants are totally soaked to maximum weight each watering event.
# plug pump into the xiaomi mi-plug so it runs under control of the cron jobs
# idea comes from watching weights not peak properly after day time waterings - most water is used during the day....
# use mirobo to get chuangmi plug token - it can't be found otherwise as it doesn't hook into the gateway's list of devices...go figure
# >mirobo discover
# INFO:miio.discovery:Discovering devices with mDNS, press any key to quit...
# INFO:miio.discovery:Found a supported 'ChuangmiPlug' at xxxxxxxxxxxxxx - token: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# INFO:miio.discovery:lumi-gateway-v3_miio73062210._miio._udp.local. @ xxxxxxxxxx, check https://github.com/Danielhiversen/PyXiaomiGateway: token: 00000000000000000000000000000000
# needs python-miio

import os
import sys
from pathlib import Path
import datetime

MYPATH = os.getcwd() # where cron jobs can find the generated scripts
MYNAME = sys.argv[0] # our name
from config import CFG
CRONTABFNAME = os.path.join(MYPATH,CFG.CTF)


def getCronf(task,hours2run):
	"""
	construct paths to our generated code and use specified virtual python path for each cron command
	Jobs run at 1 minute past the specified hour
	"""
	writeme = []
	cl = '%s %s' % (CFG.PYPATH, os.path.join(MYPATH,task))
	for i,h in enumerate(hours2run):
		s = '1	%s	*	*	*	%s 2>&1 >> %s\n' % (h,cl,os.path.join(MYPATH,CFG.LOGTO))
		writeme.append(s)
	return writeme

def writeCronf(cronlist):
	"""
	"""
	f = open(CRONTABFNAME,'w')
	now = datetime.datetime.now().ctime()
	f.write('# written by %s @ %s\n# m h dom mon dow command\n' % (MYNAME,now))
	f.write(''.join(cronlist))
	f.close()

def writeTask(taskName,hourtorun,duration):
	""" 
	Instantiate a script to turn the plug on for a specified time based on SKEL
	"""
	now = datetime.datetime.now().ctime()
	scrpt = CFG.SKEL % (CFG.PYPATH,MYNAME,now,CFG.IP,CFG.TOK,duration,duration)
	f = open(taskName,'w')
	f.write(scrpt)
	f.close()


def genCron():
	"""figure watering pattern to a total, weighted during the day for far less at night"""
	nDay = len(CFG.DAYWTIMES)
	nNight = len(CFG.NIGHTWTIMES)
	dayT = float(CFG.DAYWEIGHT)*(CFG.TOTTIME/(nNight + nDay*CFG.DAYWEIGHT)) 
	# algebra for 1/weight of a day water at night
	nightT  = (CFG.TOTTIME - nDay*dayT)/nNight # total watering at night for weightX during each day
	tN = 'runmeDay.py'
	writeTask(tN,CFG.DAYWTIMES,dayT)
	cronrows = getCronf(tN,CFG.DAYWTIMES)
	tN = 'runmeNight.py'
	writeTask(tN,CFG.NIGHTWTIMES,nightT)
	cronrows += getCronf(tN,CFG.NIGHTWTIMES)
	cl = [(int(x.split('\t')[1]),x) for x in cronrows] # decorate with hour
	cl.sort()
	cl = [x[1] for x in cl] # undecorate
	writeCronf(cl)
	os.system('crontab %s' % CRONTABFNAME)
	print('#### Updated your crontab file with:\n',''.join(cl))

if __name__ == "__main__":
	genCron()

			
