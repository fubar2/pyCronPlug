#!/usr/bin/python3
## written by genwater.py @ Wed Oct 30 11:27:26 2019
from miio import chuangmi_plug
from time import sleep
from datetime import datetime


IP="192.168.1.30"
TOK="3530efcedbd24a95df4716de429a7b0c" # mine not yours...

cP = chuangmi_plug.ChuangmiPlug(ip=IP, token=TOK, start_id=0, debug=0, lazy_discover=True, model='chuangmi.plug.m1')
cP.on()
sleep(0.01)
tstamp = datetime.now().ctime()
print('### %s: watering cron job has turned plug on for 42.857143 seconds' % tstamp)
print(cP.status())
sleep(42.857143)
cP.off()
sleep(0.01)
tstamp = datetime.now().ctime()
print('### %s: watering cron job has turned plug off' % tstamp)
print(cP.status())

