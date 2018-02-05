import sys
import requests
import ssl
#Miclain Keffeler
#Pulls and parses a coinhive list of domains 
#usage: python coinblocker_pull.py
#Built for 2.7
#coinblocker_domains.csv and coinblocker_IPs.csv are the files created
#My updated flag file must be created before running to ensure when we read the file it exists.
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
    filename = "coinblocker_domains.csv"
    coinhive_output = open(filename, 'w+')

    coinhive_output.write('domain' + '\n')
    proxy = {'https': 'http://proxy.autozone.com:8080/'}

    url = 'https://raw.githubusercontent.com/ZeroDot1/CoinBlockerLists/master/list.txt' #domains list
    res = requests.get(url, proxies=proxy, verify=True, timeout=10).text
    for line in res.split("\n"):
        coinhive_output.write(repr(line)[2:-1] + "\n")

    url = 'https://raw.githubusercontent.com/ZeroDot1/CoinBlockerLists/master/list_optional.txt' #optional domains list
    res = requests.get(url, proxies=proxy, verify=True, timeout=10).text
    for line in res.split("\n"):
        coinhive_output.write(repr(line)[2:-1] + "\n")

    url = 'https://raw.githubusercontent.com/ZeroDot1/CoinBlockerLists/master/list_browser.txt' #Browser mining list
    res = requests.get(url, proxies=proxy, verify=True, timeout=10).text
    for line in res.split("\n"):
        coinhive_output.write(repr(line)[2:-1] + "\n")
    coinhive_output.close()
    filename = "Coinblocker_IPs.csv"

    url = 'https://raw.githubusercontent.com/ZeroDot1/CoinBlockerLists/master/MiningServerIPList.txt' #mining server IP list
    res = requests.get(url, proxies=proxy, verify=True, timeout=10).text
    if str(res.split("\n")[1].split("Last modified: ")[1]) != str(last_updatedtimecheck()):
        IP_addresses = open(filename, 'w+')
        IP_addresses.write('IP' + '\n')
        last_updatedtimewrite(res.split("\n")[1].split("Last modified: ")[1])
        for line in res.split("\n"):
            if '#' in line:
                continue
            else:
                if (validate_IPV4_azure_clientIP(str(repr(line)[2:-1]))):
                    IP_addresses.write(repr(line)[2:-1] + "\n")

        IP_addresses.close()



if __name__ == "__main__":

    main()
