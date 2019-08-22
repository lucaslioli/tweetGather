from datetime import datetime

def logfile(message="", filename=""):
	'''
	Function used to record log messages with date and time into a file
	
	message: Information to be printed and recorded as log
	filename: First part of the file name where the log will be recorded
	'''
	
	now = datetime.now()
	log_msg = "{} = {}\n".format(now, message)

	f = open("logfile"+filename+'.txt','a')
	f.write(log_msg)
	f.close()

def print_and_log(message, filename="", newline=""):
    '''
	Function used to print a message and also to record into a log file
	
	message: info to be printed and recorded as log
	filename: first part of the file name where the log will be recorded
	newline: used to print a new line after the message
	'''

    logfile(message, filename)
    print(message + newline)