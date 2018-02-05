#!/usr/bin/python2.7
import sys
import requests
import ssl
from coinblocker_pull import main as coinmain
from coinhive_pull import main as hivemain
from adblock_pull import main as adblockmain
from sans_pull import main as sansmain
from submit_event import generate_cef_event,syslog,which_field


#Miclain Keffeler
#Runs all of the lists together and then will ultimately send them as a CEF (Common Event Format) Event to a server
#usage: python crypto_collection.py
#Built for 2.7

def last_updatedtimecheck():
    filename = ".cryptoupdatedtime"
    cryptotime = open(filename, 'r')
    return cryptotime.readline()
def last_updatedtimewrite(time):
    filename = ".cryptoupdatedtime"
    cryptoupdatedtime = open(filename, 'w')
    cryptoupdatedtime.write(str(time))
    cryptoupdatedtime.close()
def validate_IPV4_azure_clientIP(address):
    parts = address.split(".")
    if len(parts) != 4:
        return False
    for item in parts:
        if not 0 <= int(item) <= 255:
            return False
    return True 
def main():
    coinmain()
    hivemain() #Call all the mains to update and create newest files
    adblockmain()
    sansmain()

    domains = ["coinhive_domains.csv","coinblocker_domains.csv","adblock_domains.csv"]
    IPs = ["Coinblocker_IPs.csv","threatlist.csv"]

    for file in domains:  #Submit all of the domains
        with open(file,"r") as readfile:
            for line in readfile:   #Generate events for all entries
                event = generate_cef_event("Domain",str(line.split(",")[0]),"NULL")
                syslog(event)
                print(event)
    for file in IPs:  #Submit all of the IP's
        with open(file,"r") as readfile:
            for line in readfile:   #Generate events for all entries
                event = generate_cef_event("IP",str(line.split(",")[0]),"NULL")
                syslog(event)
                print(event)
    print ("All Events Pushed")

if __name__ == "__main__":
    main()
