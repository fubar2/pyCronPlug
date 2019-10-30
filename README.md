# pyCronPlug

Created to replace a simple ebay timer used to control watering duration and time because it only allows watering times to be fixed over both day and night.

Cron job and crontab generator designed to control automated watering times using a mi-plug. Uses python-miio to control a Xiaomi smart 240v plug through
a Xiaomi hub. Generates two python scripts, one for day an done for night that turn the plug on for a calculated amount of time.

User supplies:

* hours at which each script should be run as a separate list - e.g. [9,12,15,18], [22,4] for day and night
* the total time on - pumping seconds per 24 hours
* the weighting for daytime watering - e.g. 2 so night waterings total 1/2 of each daytime watering.

From some experiments recording plant weights it's clear that most water is used for transpiration during the day and relatively little is used at night so watering should be adjusted to be less wasteful.

Probably won't make much difference to efficiency but the main motive is to ensure that every watering event fills the pot to saturation so the successive peaks at successive waterings will show the slope of biomass growth - ceteris paribus.
Uses python-miio to control a Xiaomi smartplug or Chuangmi-plug into which the pump is plugged.
Generates two python scripts of daytime and nightime watering duration to suit and a crontab which it automatically installs for the current user

The times for watering are calculated from the desired total time, the weighting factor so daytime watering sums to a multiple (e.g. 3x) of the night time total split among the specified times for day and night watering.

Yes, this can all be done manually but hey. this is git.

Generated crontab using defaults:

```
# written by genwater.py @ Wed Oct 30 09:21:23 2019
# m h dom mon dow command
1       4       *       *       *       /home/ross/rossgit/loadcellflask/venv/bin/python /home/ross/rossgit/python-miio/runmeNight.py 2>&1 >> /home/ross/rossgit/python-miio/watercron.log
1       9       *       *       *       /home/ross/rossgit/loadcellflask/venv/bin/python /home/ross/rossgit/python-miio/runmeDay.py 2>&1 >> /home/ross/rossgit/python-miio/watercron.log
1       12      *       *       *       /home/ross/rossgit/loadcellflask/venv/bin/python /home/ross/rossgit/python-miio/runmeDay.py 2>&1 >> /home/ross/rossgit/python-miio/watercron.log
1       13      *       *       *       /home/ross/rossgit/loadcellflask/venv/bin/python /home/ross/rossgit/python-miio/runmeDay.py 2>&1 >> /home/ross/rossgit/python-miio/watercron.log
1       16      *       *       *       /home/ross/rossgit/loadcellflask/venv/bin/python /home/ross/rossgit/python-miio/runmeDay.py 2>&1 >> /home/ross/rossgit/python-miio/watercron.log
1       22      *       *       *       /home/ross/rossgit/loadcellflask/venv/bin/python /home/ross/rossgit/python-miio/runmeNight.py 2>&1 >> /home/ross/rossgit/python-miio/watercron.log
```
Generated daytime script

```
#!/usr/bin/python3
## written by genwater.py @ Wed Oct 30 09:21:23 2019
from miio import chuangmi_plug
from time import sleep
from datetime import datetime


IP="xxxx"
TOK="xxxx" # mine not yours...

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
```
and nighttime script

```
#!/usr/bin/python3
## written by genwater.py @ Wed Oct 30 09:21:23 2019
from miio import chuangmi_plug
from time import sleep
from datetime import datetime


IP="xxxx"
TOK="xxxx" # mine not yours...

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
```
