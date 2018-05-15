#!/az/arcsight/counteract_scripts/env/bin/python

import sys
import requests
import ssl
__author__ = 'mkkeffeler'

#Miclain Keffeler
#Pulls and parses a coinhive list of domains 
#usage: python coinhive_pull.py
#Built for 2.7
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
	filename = "coinhive_domains.csv"
	coinhive_output = open(filename, 'w+')
	summary_domain = open("summary_domains.txt","a+")
	coinhive_output.write('domain,' + '\n')
	proxy = {'https': 'http://proxy.autozone.com:8080/'}
	url = 'https://raw.githubusercontent.com/Marfjeh/coinhive-block/master/domains'

	res = requests.get(url, proxies=proxy, verify=True, timeout=10).text
	for line in res.split("\n"):
		#if (not_been_sent_yet(str(line))):
		#	summary_domain.write(str(line) + "\n")
		coinhive_output.write(str(line) + "\n")
	summary_domain.close()
	coinhive_output.close()
