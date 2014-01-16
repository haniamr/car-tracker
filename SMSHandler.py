#SMSHandler.py:
import MDM
import MOD
import SER
import GPS
import md5
import GPIO
import RHandler
import Helper

class SMSMessage:
	def __init__(self, command, password, sender, index):
		self.command = command
		self.password = password
		self.sender = sender
		self.msgindex = index

def getSavedPassword():
	Helper.sendCmd('AT+CMGF','1', 50)
	
	data = Helper.sendCmd('AT+CMGR','1', 50)
	
	if(data.find('+CMGR:') != -1):
		SavedPassword = data.split('\r\n')[2]
		SavedPassword = SavedPassword.split(' ')[1].lstrip().rstrip()

		return SavedPassword
	else:
		return 0
def sendSMS(NUMBER, SMSText):
	TIMEOUT_CMD = 50
	Helper.writeLog('Starting sendSMS\r\n')
	
	res = Helper.sendCmd('AT+CMGF', '1', TIMEOUT_CMD) # select text format type
	Helper.writeLog('Finished AT+CMGF\r\n')
	
	res = Helper.sendCmd('AT+CNMI', '2,1', TIMEOUT_CMD) # alarm indicators
	Helper.writeLog('Finished AT+CNMI\r\n')
	
	res = Helper.sendCmd('AT+CMGS', NUMBER, TIMEOUT_CMD) # send the message without storing it
	Helper.writeLog('Finished AT+CMGS\r\n')
	
	if (res.find('>') == -1):
		return -1
	else:
		res = MDM.send(SMSText, 0)
		Helper.writeLog('Finished sending SMSText\r\n')
		
		res = MDM.sendbyte(0x1a, 0)
		Helper.writeLog('Finished CTRL+Z\r\n')
		
		for i in range(6):
			res=MDM.read()
			if(res.find("OK")!=-1):
				Helper.writeLog('Found and returning\r\n')
				return 1
			else:
				MOD.sleep(300)
		
		Helper.writeLog('REturning -1\r\n')
		return -1
def extractNumberFromSMS(smstext) :
	Number = smstext.split('\r\n')[0]
	Number = str(Number).split(',')[2].rstrip().lstrip()
	Number = Number.replace('"','')
	
	return Number
def check4SMS():
	Helper.sendCmd('AT+CMGF','1', 50)
	data= ''
	data = Helper.sendCmd('AT+CMGL','"ALL"',20)
	smslist=''
	#listen to what the telit says with a timeout of 20
	smslist = smslist + data
	while data != '':
		data = MDM.receive(20)
		smslist = smslist + data
    
	smsarray = []
	lines = smslist.split('+CMGL:')
	if len(lines) > 1:
		for i in range(1,len(lines)):
			smsarray.append(parseSMS(lines[i]))
	
	return smsarray
def parseSMS(smsText):
	Helper.writeLog('#Begin: Parsing the SMS\r\n')
	msgIndex = getMessageIndex(smsText)
	command = splitSMS(smsText,0)
	password = splitSMS(smsText,1)
	sender = extractNumberFromSMS(smsText)
	
	Helper.writeLog('#End: Parsing the SMS\r\n')
	return SMSMessage(command,password,sender,msgIndex)
def deleteSMS(MessageIndex, functionDeleting) :
	Helper.writeLog('Deleting SMS at Index ##'+str(MessageIndex)+' in function '+str(functionDeleting)+'\r\n')
	Helper.sendCmd('AT+CMGF','1', 50)
	Helper.sendCmd('AT+CNMI','2,1',50)
	Helper.sendCmd('AT+CMGD',MessageIndex,50)
	
	return
def splitSMS(smstext,Index) :
	res = smstext.split('\r\n')[1].lstrip().rstrip()
	Helper.writeLog(res+'\r\n')
	res = res.split(' ')[Index].lstrip().rstrip()
	Helper.writeLog(res+'\r\n')
	return res
def getMessageIndex(smstext) :
	#Index = SMSResult.split('\r\n')[1]
	Index = smstext.split(',')[0]
	#Index = Index.split(':')[1]
	Index = Index.lstrip().rstrip()

	return Index
def processSingleSMS(sms):
	try :
		Helper.writeLog('SMS received\r\n')
		MessageIndex = sms.msgindex
		Command = sms.command
		Password = sms.password
		
		Helper.writeLog('Message index is'+MessageIndex+'\r\n')
		Helper.writeLog('Command is'+Command+'\r\n')

		if Command == 'SETPWD' :
			RHandler.setPwd(sms)
		elif Command == 'GL' :
			RHandler.getLocation(sms)
		elif Command == 'UPD' :
			RHandler.update(sms)
		elif Command == 'STRT' :
			RHandler.startEngine(sms)
		elif Command == 'STP' :
			RHandler.stopEngine(sms)
		elif Command == 'DELALL' :
			RHandler.deleteAllMessages(sms)
		else :
			Helper.writeLog('Deleting SMS')
			deleteSMS(MessageIndex,'Parsing SMS')
		
		Helper.writeLog('-Finished ProcessSingleSMS')
	except Exception, e:
		Helper.writeLog('###ProcessSingleSMS Exception###')
		Helper.writeLog(str(e))
