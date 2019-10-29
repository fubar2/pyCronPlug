# pyCronPlug

Cron job and crontab generator designed to control automated watering times using a mi-plug. uses python-miio
Needed to replace a simple ebay timer used to control watering duration and time because it only allows watering times to be fixed over both day and night.

From some experiments recording plant weights it's clear that most water is used for transpiration during the day and relatively little is used at night so watering should be adjusted to be less wasteful.

Probably won't make much difference to efficiency but the main motive is to ensure that every watering event fills the pot to saturation so the successive peaks at successive waterings will show the slope of biomass growth - ceteris paribus.
Uses python-miio to control a Xiaomi smartplug or Chuangmi-plug into which the pump is plugged.
Generates two python scripts of daytime and nightime watering duration to suit and a crontab which it automatically installs for the current user

The times for watering are calculated from the desired total time, the weighting factor so daytime watering sums to a multiple (e.g. 3x) of the night time total split among the specified times for day and night watering.

Yes, this can all be done manually but hey. this is git.
