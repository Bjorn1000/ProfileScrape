import os
import re
import csv
from os import listdir
from os.path import isfile, join
import glob

def GetAllLogs(url):
	onlyfiles = [f for f in listdir(url) if isfile(join(url, f))]
	onlyfiles = [url + x for x in onlyfiles]
	return onlyfiles
	
def newestExport(path):
	files = [s for s in os.listdir(path) if "profiles_export" in s]
	paths = [os.path.join(path, basename) for basename in files]
	return max(paths, key=os.path.getctime)

#profile log and challenge log

class Log():
	def __init__(self, log):
		self.log = log
		
	def getLog(self):
		return self.log
		
	def turnToLines(self):
		with open(self.log) as f:
				self.lines = f.read().splitlines()
	
	def getLines(self):
		return self.lines
		
	def SearchLog(self, word):
		self.lines = [s for s in self.lines if word in s]

# Directory for profile export and for log file
class Directory:
    def __init__(self, fullDir):
        self.fullDir = fullDir
        
    def getDir(self):
        return self.fullDir
    
    def addOn(self, adding):
        self.fullDir = self.fullDir+adding
        
    def pull(self, file):
        return open((file), "r", encoding='UTF8')
		
class Account:
	def __init__(self, name):
		self.name = name
		
	def getName(self):
		return self.name



current = Directory(os.getcwd())
current2 = Directory(os.getcwd())
account = Account(current.getDir().split("\\")[2])
current.addOn("\\AppData\Roaming\MP\Logs\\")
logs = GetAllLogs(current.getDir())
mainDirectory = Directory([x for x in logs if "mainlog.log" in x][0])


current2.addOn("\\AppData\Roaming\MP\ImageTempFolder\\")
profileLog = GetAllLogs(current2.getDir())
latestProfile = newestExport(current2.getDir())
profile_export = [x for x in profileLog if latestProfile in x][0]
mainLog = Log(mainDirectory.getDir())

mainLog.turnToLines()
mainLog.SearchLog("Send Message")
mainLog.SearchLog("Finalized operation")
messageExert2 = mainLog.getLines()

# need to scale from here on
profileData = list(csv.reader(open(profile_export)))
[r.pop(8) for r in profileData]

colTitles = ["name", "email/username", "password", "proxy-ip:port", "proxy username", "proxy password", "tags", "date of birth", "unique name", "email username", "email pass", "email pop3server", "email validation port", "device", "message sent to", "timestamp", "from account" ]
all = []

for x in messageExert2:
		
		name = re.findall(r"'(.*?)'", x)[0]
		userId = re.findall(r"'(.*?)'", x)[1]
		splitted = x.split("-")[0:3]
		timestamp = "-".join(splitted)
		entry = [name, userId, timestamp]
		all.append(entry)
		
		
	
csvData = []
for x in profileData:
		for y in all:
				if y[0] == x[0]:
						addedProperties = [y[1],y[2],account.getName()]
						no = x + addedProperties
						csvData.append(no)
						#print(no)
						
				
with open('messageProfiles.csv', 'w') as myfile:
	wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
	wr.writerow(colTitles)
	for item in csvData:
		wr.writerow(item)
		
