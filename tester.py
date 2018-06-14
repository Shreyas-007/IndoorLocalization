import iwlist
from time import sleep, gmtime, strftime
import time,os

terminate = False


loc = int(raw_input("Enter the location ID of capture : "))

#Create Directory to store the captured traces
try:
    folderName = "Location-"+str(loc)
    os.makedirs(folderName)
    os.chdir(os.getcwd()+"/"+folderName)
except OSError as e:
    print("Error "+e.errno)

try:
	#delay = int(raw_input("Enter a numeric delay in second(s)"))
	delay=3
except:
	print("Numeric delay expected, starting program wihout delay")
	delay=0

sleep(delay)

while not terminate: 
	print("----------------------WAR DRIVING-------------------------------")
	#sleep(1)

	
	data = open('Iwlist_wlp3s0_Params.txt','a')
	data.flush()

	for i in range(20):
		content = iwlist.scan(interface='wlp3s0')
		cells = iwlist.parse(content)
		#print(cells)	

		newDict = dict()
		newList = list()


		for dicts in cells:
			newDict = dict()
			newDict["Date/Time"]=strftime("%Y-%m-%d %H:%M:%S", gmtime())
			newDict["Location"]=loc

			for key, value in dicts.items():
				'''if key in ["mac","signal_quality","cellnumber","channel","essid"]:
					newDict[key]=value'''
				if key=="mac":
					newDict["MAC Address"]=value
				if key=="signal_level_dBm":
					newDict["Signal Level"]=value+"dBm"
				if key=="cellnumber":
					newDict["Cell Number"]=value
				if key=="channel":
					newDict["Channel"]=value
				if key=="essid":
					newDict["SSID"]=value
				if key=="signal_quality":
					qual_num = value
				if key=="signal_total":
					qual_denom = value
					newDict["Signal Quality"]=qual_num+"/"+qual_denom

			newList.append(newDict)

		if i==0:
			data.write("\n\n--------------------------------------------------------------------------------------------------------------------------\n\n")
			#print "{:<50} {:<10}".format('Parameter','Value')
			# print "{:<20} {:<20} {:<20} {:<20} {:<20} {:<20} {:<20} {:<20}" .format('Date/Time','Location', 'Channel','Signal Quality','SSID','MAC Address','Signal Level','Cell Number')
			data.write("{:<20} {:<20} {:<20} {:<20} {:<20} {:<20} {:<20} {:<20}" .format('Signal Quality','SSID','MAC Address','Signal Level','Cell Number','Date/Time','Location', 'Channel'))
			data.write("\n\n---------------------------------------------------------------------------------------------------------------------------\n\n")
		data.flush()

		for d in newList:
		
			str=""
			#print("----------------------------------------------------------------------------------")
			for k, v in d.iteritems():
				str=str + "{:<20}".format(v)

			data.write(str+"\n")
			data.flush()
			#print("----------------------------------------------------------------------------------")

	rdata = open('Iwlist_wlp3s0_Params.txt','r')
	
	count=0
	for line in rdata:
		count=count+1

	
	if count>200:
		terminate=True
		break

	print "Data not captured. Pausing for 3s and recapturing data...."
	sleep(3)
		
	
	
