#!/az/arcsight/counteract_scripts/env/bin/python

import sys
import requests
import xml.etree.ElementTree as ET
import ssl
__author__ = 'mkkeffeler'

#Miclain Keffeler
#Pulls and parses a coinhive list of domains 
#usage: python sans_pull.py
#Built for 2.7
#TODO: Implement last updated/modified time so that if an IP has already been seen we don't send it as a CEF 2 times within a day or less of each other
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context
def not_been_sent_yet(domain):
    istrue = 0
    with open("summary_ips.txt","r") as pastdomains:
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

    filename = "threatlist.csv"
    sans_output = open(filename, 'w')
    sans_output.write('ip,date,lastseen' + '\n')

    proxy = {'https': 'http://proxy.autozone.com:8080/'}

    url = 'https://isc.sans.edu/api/threatlist/miner'
    res = requests.get(url, proxies=proxy,verify=True, timeout=10).text
    root = ET.fromstring(res)
    summary_domain = open("summary_ips.txt","a+")

    for miner in root.iter(tag='miner'):
        event = '%s' % (miner.find('ipv4').text)
    #    if (not_been_sent_yet(event)):
     #       summary_domain.write(event + "\n")

        sans_output.write(event + "\n")
    summary_domain.close()
if __name__ == "__main__":
    main()
