from oscpy.server import OSCThreadServer
from oscpy.client import OSCClient
from math import floor
import logging

host = "127.0.0.1"
port = 8000
page = 3
osc = OSCClient(host, port)
def setOSCData(Host, Port, Page):
    print("setting OSC data to : ", Host, Port)
    host = Host
    port = Port
    page = Page
    osc = OSCClient(host, port)
    

def sendOSC(execItem, ButtonStatus):
    logging.info("OSC sending to ", host, port, page, execItem)
    oscstring = '/exec/'+str(page)+'/'+str(execItem)
    oscbytes = oscstring.encode('utf-8')
    print(oscbytes)
    send_message(oscbytes, ButtonStatus)
    
""" def ping():
    osc = OSCClient(host, port)
    for i in range(2):
        oscstring = '/exec/'+str(3)+'/'+str(1)
        oscbytes = oscstring.encode('utf-8')
        osc.send_message(oscbytes, [1])
        print(b'/ping', [1]) """

def send_message(data, buttonData):
    osc.send_message(data, [buttonData])
