from datetime import datetime

def logfile(message = ""):
	now = datetime.now()

	f = open('logfile.txt','a')
	f.write(str(now) + " = " + message + '\n')
	f.close()