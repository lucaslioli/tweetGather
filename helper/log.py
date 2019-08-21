from datetime import datetime

def logfile(message="", filename=""):
	now = datetime.now()

	f = open("logfile"+filename+'txt','a')
	f.write(str(now) + " = " + message + '\n')
	f.close()

def print_and_log(message, filename="", newline = "\n"):
    logfile(message, filename)
    print(message, newline)