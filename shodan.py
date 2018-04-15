#!/az/arcsight/counteract_scripts/env/bin/python
import requests
import sys
import ipaddress
import dateutil.parser
from pprint import pprint
import json
api_key = 'yBRbzFFRy2mZ6mh07BsB4YkMcHuZJ7xB'

if(len(sys.argv) < 2):
    print ("Invalid Parameters")
    exit()
ip = sys.argv[1]
def Port_list(shodan):
    message = ""
    for port in shodan['ports']:
       message += str(port) + " "
    if (message == ""):
        return "No Historical Port Information."
    else:
        return message
def hostname_list(shodan):
    message = ""
    for hostname in shodan['hostnames']:
       message += str(hostname) + " "
    if (message == ""):
        return "No Historical Hostname Information."
    else:
        return message
def certificate_status(shodan):
    message = ""
    if "ssl" in shodan.keys():
        if "cert" in shodan['ssl'].keys():
            return "Certificate Expired: " + str(shodan['ssl']['cert']['expired'])
    else:
        return "Certificate Unknown."

def check_org(shodan):
    message = ""
    if "org" in shodan.keys():
        return str(shodan['org'])
    else:
        return "No Organization Listed"

def check_time(shodan):
    message = ""
    if "timestamp" in shodan['data'][0].keys():
        return str(dateutil.parser.parse(str(shodan['data'][0]['timestamp'])).strftime("%x"))
    else:
        return "No Updated Time Available."

def check_asn(shodan):
    message = ""
    if "asn" in shodan.keys():
        return str(shodan['asn'])
    else:
        return "No ASN Provided."

def optional_arg2(arg_default,Event_ID): #Confirms the presence or lack of an IP address in -i option. 
    def func(option,opt_str,value,parser):   #Function to hold parser data
        if len(parser.rargs) ==  0:
            print ("Domain Name: Unknown")
            exit()
        else:
            global my_ip
            my_ip = parser.rargs[0]
    return func

def domain_list(shodan):
    message = ""
    for domain in shodan:
        message += str(domain) + " "
    if (message == ""):
        return "No Historical Domain Name Information."
    else:
        return message
def warn_and_exit(msg):
    print('Error:')
    print(msg)
    exit()

try:
    parsed_ip = ipaddress.ip_address(ip)
    if parsed_ip.is_private:
        warn_and_exit('This is a private IP: {0}'.format(str(parsed_ip)))


except Exception as ex:
    warn_and_exit(str(ex))
if ip == "":
    warn_and_exit("There was no IP address provided on execution")

response = requests.get('https://api.shodan.io/shodan/host/%s?key=%s' % (str(parsed_ip), api_key))

shodan= response.json()
print("Base Info:")
if 'data' in shodan.keys():
    print("Geolocation: " + str(shodan['data'][0]['location']['country_name']))
    print("All Historic Hostnames: " + hostname_list(shodan))
    print("Current Domain Name: " + domain_list(shodan['data'][0]['domains']))
    print("Certificate Status: " + certificate_status(shodan['data'][0]))
    print("ASN: " + check_asn(shodan))
    print("Organization: " + check_org(shodan))
    print("All Historic Ports: " + Port_list(shodan))
    print("Last Updated: " + check_time(shodan))
else:
    print(shodan['error'])
