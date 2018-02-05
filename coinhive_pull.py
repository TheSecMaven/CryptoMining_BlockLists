import sys
import requests
import ssl
#Miclain Keffeler
#Pulls and parses a coinhive list of domains 
#usage: python coinhive_pull.py
#Built for 2.7
def main():
	filename = "coinhive_domains.csv"
	coinhive_output = open(filename, 'w+')

	coinhive_output.write('domain,' + '\n')
	proxy = {'https': 'http://proxy.autozone.com:8080/'}
	url = 'https://raw.githubusercontent.com/Marfjeh/coinhive-block/master/domains'

	res = requests.get(url, proxies=proxy, verify=True, timeout=10).text
	for line in res.split("\n"):
		coinhive_output.write(str(line) + "\n")

if __name__ == "__main__":
    main()
