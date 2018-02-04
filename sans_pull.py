#!/usr/bin/python2.7
import sys
import requests
import xml.etree.ElementTree as ET
import ssl
#Miclain Keffeler
#Pulls and parses a coinhive list of domains 
#usage: python sans_pull.py
#Built for 2.7
 
if hasattr(ssl, '_create_unverified_context'):

        ssl._create_default_https_context = ssl._create_unverified_context
def main():

    filename = "threatlist.csv"
    sans_output = open(filename, 'w')
    sans_output.write('ip,date,lastseen' + '\n')

    proxy = {'https': 'http://proxy.autozone.com:8080/'}

    url = 'https://isc.sans.edu/api/threatlist/miner'
    res = requests.get(url, verify=True, timeout=10).text
    root = ET.fromstring(res)

    for miner in root.iter(tag='miner'):
        event = '%s' % (miner.find('ipv4').text)
        event += ',' + '%s' % (miner.find('date').text)
        event += ',' + '%s' % (miner.find('lastseen').text)
        event += '\n'
        sans_output.write(event)

if __name__ == "__main__":
    main()
