#!/home/ross/rossgit/loadcellflask/venv/bin/python3

from miio import chuangmi_plug
from config import CFG

IP = CFG.IP
TOK = CFG.TOK 

cP = chuangmi_plug.ChuangmiPlug(ip=IP, token=TOK, start_id=0, debug=0, lazy_discover=True, model='chuangmi.plug.m1')
print(cP.status())


