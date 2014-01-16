#Helper.py:
import MDM
import MOD
import SER
import GPS
import md5
import GPIO

LogVerbose = 1
SavedPassword = 0

def iterateCmd(comando, parametro, TIMEOUT_CMD, numCheck):
    while( numCheck >= 0):
        numCheck = numCheck - 1
        res  = sendCmd(comando, parametro, TIMEOUT_CMD)
        SER.send(res + ' ' + comando + '=' + parametro)
        if(res.find('OK') != -1) :
            return 1
        MOD.sleep(TIMEOUT_CMD)
        if(numCheck == 0):
            SER.send(res + ' ' + comando + '=' + parametro)
            return -1
def connectGPRS():
	writeLog('#Begin: Connecting GPRS')
	numCheck = 4
	TIMEOUT_CMD = 50
	CGDCONT = '1,"IP","internet.vodafone.net"'
	USERID = '"internet"'
	PASSW = '"internet"'
	res = iterateCmd('AT#GPRS', '0', TIMEOUT_CMD, numCheck)
	if res == -1 :
		return -1
	res = iterateCmd('AT+CGDCONT', CGDCONT, TIMEOUT_CMD, numCheck)
	if res == -1 :
		return -1
	res = iterateCmd('AT#USERID', USERID, TIMEOUT_CMD, numCheck)
	if res == -1 :
		return -1
	res = iterateCmd('AT#PASSW', PASSW, TIMEOUT_CMD, numCheck)
	if res == -1 :
		return -1
	res = iterateCmd('AT#GPRS', '1', TIMEOUT_CMD, numCheck)
	if res == -1 :
		return -1
	writeLog('#End: Connecting GPRS')
	return 1 # -1 => ERROR , 1 => OK
def writeLog(text):
	global LogVerbose
	if LogVerbose == 1 :
		SER.send(text + "\r\n")
def sendCmd(cmd,value,waitfor):
	if (value != ""):
		cmd = cmd + '='
	else:
		cmd = cmd + '\r'
	res = MDM.send(cmd, 0)
	if (value != ""):
		res = MDM.send(value, 0)
		res = MDM.send('\r', 0)
	if (waitfor > 0):
		res = MDM.receive (waitfor)
	return res
