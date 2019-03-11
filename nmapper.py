#!/usr/bin/python3



import logging, re, os, time, shelve, datetime, netaddr #, nmap
logging.basicConfig(filename='./logging.log', level=logging.INFO, format=' %(asctime)s - %(levelname)s  - %(message)s')

def theLibrarian():
	# the librarian goes through the shelve/dictionary file searching for any MAC addresses whose epochTime (the time it was last seen) is older than a month.
	# When it finds a MAC address that hasn't been seen for a month it deletes it from the dictionary file.

	epochNow = int(time.time())
	for k, epochLastSeen in myDict.copy().items():
		if (epochNow - epochLastSeen) > 2678400:

			theDate = datetime.datetime.fromtimestamp(epochLastSeen).strftime('%A')
			logging.info('Deleting MAC Address: %s Date: %s ' % (k, theDate))
			myDict.pop(k, None)
		else:
			pass



def loadArp():
	dataLocation = "./data/"

	# Get directory listing of all ARP files
	dirContents = os.listdir(dataLocation)
	regexArp = re.compile(r'.*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*(.{4}\..{4}\..{4}).*')
	
	for file in dirContents:
		if "arp" in file:

			arpFile = open(dataLocation + file)
		else:
			continue
		for line in arpFile:
			# For each line in the arpFile regex out the mac and IP address
			matchObject = None
			matchObject = regexArp.search(line)
			
			try:
				shelfChecker(matchObject.group(1), matchObject.group(2), time.time())
				# Send the MAC, IP, and Current time to shelfChecker
			except:
				pass

def shelfChecker(ip, mac, time):
	
	if (mac in myDict.keys()) == True:
		# If the MAC is already in the dictionary, then we've seen it within the last month and we should do nothing
		pass
	else:
		# NMAP the device
		nmapper(ip, mac)

	# Write the key value pair of MAC address and current time to the dictionary
	myDict[mac] = int(time)





	
def nmapper(ip, mac):
	# The following will NMAP the device as long as it's not in a specific CIDR range

	if netaddr.IPAddress(ip) in  netaddr.IPNetwork("10.0.0.1/19"):
		logging.info('Reject %s with MAC Address %s:  Not in Range' % (ip, mac))
		# Write a log message
	else:
		logging.info('NMAP %s with MAC Address %s' % (ip, mac))
		# Write a log message

		###  Following code would scan 
		# nm = nmap.PortScanner()
		# logging.info('Scanning $s' % (ip)
		# nm.scan(hosts=ip, ports='5900,2701,1776,8192')
		# print("Scanned " + ip)
		# if (nm[ip]['tcp'][5900]['state'] == 'open') or (nm[ip]['tcp'][270]['state'] == 'open') or (nm[ip]['tcp'][1776]['state'] == 'open') or (nm[ip]['tcp'][8192]['state'] == 'open'):
		# 	print(ip + " has 22 open")
		# else:
		# 	nm.scan(hosts=ip, arguments='-A --osscan-guess')
		



myDict = {}
if os.path.isfile('./shelvedDict.db'):
	# If the dictionary file exists load it into the myDict file
	myShelvedDict = shelve.open('./shelvedDict.db')
	myDict = myShelvedDict['myDict']
else:
	# Otherwise create a new shelve file
	myShelvedDict = shelve.open('./shelvedDict.db')

# load the Librarian to clean the dictionary file out of old MAC addresses
theLibrarian()
# Load the mac addresses and check to see if they are previously seen
loadArp()

myShelvedDict['myDict'] = myDict
logging.info('Script Run')