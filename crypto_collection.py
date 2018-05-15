#!/az/arcsight/counteract_scripts/env/bin/python

import sys
import requests
import ssl
from coinblocker_pull import main as coinmain
from coinhive_pull import main as hivemain
from adblock_pull import main as adblockmain
from sans_pull import main as sansmain
from submit_event import generate_cef_event,which_field
__author__ = 'mkkeffeler'


#Miclain Keffeler
#Runs all of the lists together and then will ultimately send them as a CEF (Common Event Format) Event to a server
#usage: python crypto_collection.py
#Built for 2.7
def not_been_sent_yet(domain):
    domain = domain.split("\n")[0]
    istrue = 0
    with open("summary_domains.txt","r") as pastdomains:
        for prevdomain in pastdomains:
            prevdomain = prevdomain.split("\n")[0]
            if (prevdomain == domain):
                return False
            else:
                istrue = 0
    if (istrue == 0):
        return True
def not_been_sent_yet_ip(domain):
    domain = domain.split("\n")[0]
    print (domain)
    istrue = 0
    with open("summary_ips.txt","r") as pastdomains:
        for prevdomain in pastdomains:
            prevdomain = prevdomain.split("\n")[0]
           # print (prevdomain)
            if (prevdomain == domain):
                return False
            else:
                istrue = 0
    if (istrue == 0):
        return True
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
    summary_domains = open("summary_domains.txt","a+")
    summary_ips = open("summary_ips.txt","a+")
    domains = ["coinhive_domains.csv","coinblocker_domains.csv","adblock_domains.csv"]
    IPs = ["Coinblocker_IPs.csv"]
    linecount = 0
    for files in domains:  #Submit all of the domains
        linecount = 0 
        with open(files,"r") as readfile:
            for line in readfile:   #Generate events for all entries
     #           print (line)
                linecount += 1
    #            print ("IT IS : " + str(not_been_sent_yet(line)))
                if ( str(line) != "" and linecount != 1 and not_been_sent_yet(line)): #If we are not looking at the header of the file
                    event = generate_cef_event("Domain",str(line),"NULL",files[:-12])
                    summary_domains.write(str(line))
 #                   syslog(event)
                    print(event)
    for files in IPs:  #Submit all of the IP's
        linecount = 0
        with open(files,"r") as readfile:
            for line in readfile:   #Generate events for all entries
                linecount += 1
                if ( str(line) != "" and linecount != 1 and not_been_sent_yet_ip(line.split(",")[0])): #If we are not looking at the header of the file
                    event = generate_cef_event("IP",str(line.split(",")[0]),"NULL",files[:-8])
                    summary_ips.write(str(line.split(",")[0]))
#                    syslog(event)
                   # print(event)
    print ("All Events Pushed")

if __name__ == "__main__":
    main()
