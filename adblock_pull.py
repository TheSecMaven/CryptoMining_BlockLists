#!/az/arcsight/counteract_scripts/env/bin/python

import sys
import requests
__author__ = 'mkkeffeler'

#Miclain Keffeler
#Pulls and parses a adblock list of domains 
#usage: python adblock_pull.py
#Built for 2.7
#My updated flag file must be created before running so that when we read it it is there.
def last_updatedtimecheck():
    filename = ".adblockupdated"
    cryptotime = open(filename, 'r')
    return cryptotime.readline()
def last_updatedtimewrite(time):
    filename = ".adblockupdated"
    cryptoupdatedtime = open(filename, 'w')
    cryptoupdatedtime.write(str(time))
    cryptoupdatedtime.close()
def not_been_sent_yet(domain):
    istrue = 0
    with open("summary_domains.txt","r") as pastdomains:
        for prevdomain in pastdomains:
            prevdomain = prevdomain.split("\n")[0]
           # print (prevdomain)
            if (istrue == 1):
                return True
            if (prevdomain == domain):
                istrue = 1
            else:
                istrue = 0

def main():
    filename = "adblock_domains.csv"
    proxy = {'https': 'http://proxy.autozone.com:8080/'}
    

    url = 'https://raw.githubusercontent.com/hoshsadiq/adblock-nocoin-list/master/hosts.txt' #mining server Domain List
    res = requests.get(url, proxies=proxy, verify=True, timeout=10).text
    if str(res.split("\n")[8].split("Last modified: ")[1]) != str(last_updatedtimecheck()): #If the file has been updated since last pull
        summary_domain = open("summary_domains.txt","a+")
        adblock_domains = open(filename, 'w+')
        adblock_domains.write('Domain,' + '\n')
        last_updatedtimewrite(res.split("\n")[8].split("Last modified: ")[1])
        for line in res.split("\n"):
                if '#' in line or line == "":
                    continue
                else:
                   # if (not_been_sent_yet(repr(line.split(" ")[1])[2:-1])):
                    #    summary_domain.write(repr(line.split(" ")[1])[2:-1] + "\n")
                    adblock_domains.write(repr(line.split(" ")[1])[2:-1] + "\n")
        adblock_domains.close()
        summary_domain.close()
    else:
        adblock_domains = open(filename, 'w+')
        adblock_domains.write('Domain,' + '\n')
        adblock_domains.close()
        print ("ADBLOCK WAS NOT UPDATED")
        return
if __name__ == "__main__":

    main()
