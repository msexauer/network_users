#!/bin/python
#Python script to get IP's and hostname from local network & write to DB

import sqlite3
import nmap
import datetime

#Global Variables
db_file = "netscan.db"
db_path = "/Users/msexauer/house/"
data_diff = False #should be false here, currently testing
today = datetime.date.today

#sql connection stuff
connection = sqlite3.connect(db_path + db_file)
c = connection.cursor()

#The network scan, we will be calling this often
scan = nmap.PortScanner()
scan.scan(hosts='10.1.120.0/23', arguments='-sn') #Network space defined here

#Main loop
for host in scan.all_hosts():
    previous_hosts = []
    current_host = [scan[host].hostname()]

    # Query database for data
    for row in c.execute('SELECT * FROM network'):
        query = list(row)
        previous_hosts.append(query[2])

    # If the host is not currently on the list, data_diff = True
    if set(previous_hosts).intersection(current_host) == set([]):
        data_diff = True

    #If data_diff, write differences to db
    if data_diff == True:
        with connection:
            c.execute('INSERT INTO network (date, ip, host) VALUES (?,?,?)', (today(), host, scan[host].hostname()))
        data_diff = False # Reset for next instance of loop

#Wrap up stuff
connection.commit
connection.close

#Done
