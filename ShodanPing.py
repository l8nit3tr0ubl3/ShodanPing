###This program takes a user input search query 'SEARCH'
###and scans Shodan.io for matching IP addresses over
### 'PAGES' number of pages. Once a list is compiled
### we then ping every aIP in the list to ensure it is
### actually alive. Then return list of alive IP's to user.
#!/usr/bin/python

import shodan
import pyping
import time

###User Settings
APIkey = "API KEY HERE"
SEARCH = "SEARCH TERM HERE"
PAGES = 2

### Required variables - Dont change
ipList = []
api = shodan.Shodan(APIkey)

###Function for scanning 'x' pages of shodan for a string
def Shodan_Search():
    counter = 0
    kill = 0
    print "Searching Shodan now for {}.".format(SEARCH)
    try:
        while counter < PAGES:
            results = api.search(SEARCH,page=counter,limit=None)
            for item in results['matches']:
                ip = item['ip_str']
                if ip not in ipList:
                    ipList.append(ip)
                else:
                    print "Reached end of list on page {}.".format(counter)
                    kill = 1
                    break
            if kill is 1 :
                break
            else:
                print "Page {} scanned.".format(counter + 1)
                time.sleep(1)
                counter = counter + 1
    except shodan.APIError, e:
        print e
        
def Ping_Address_List():
    pingCounter = 0
    print "Pinging each address to verify its up."
    for address in ipList:
        pingresponse = pyping.ping(address)
        if pingresponse.ret_code == 0:
            pingCounter = pingCounter + 1
            print address
        else:
            pass
    print "Total results {}".format(len(ipList))
    print "Total alive results: {}".format(pingCounter)

Shodan_Search()
Ping_Address_List()
