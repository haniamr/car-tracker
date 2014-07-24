#RHandler.py:
import Helper
import SMSHandler
import GPS
import md5
import GPIO
import MDM
import MOD
import SER

SavedPassword = 0

def setPwd(sms):
	global SavedPassword
	Helper.writeLog('#Begin: SetPwd function')
	Helper.writeLog('-Password in sms is '+sms.password)

	if sms.password != '' and SavedPassword == 0 :
		Helper.writeLog('-In Password Condition')
		SavedPassword = sms.password
		
		Helper.writeLog('-Number is '+sms.sender)
		Helper.writeLog('-Before Sending the SMS')
		SMSHandler.sendSMS(sms.sender,'Password set successfully')
	elif MessageIndex != '1' :
		Helper.writeLog('-Deleting SMS')
		SMSHandler.deleteSMS(MessageIndex,'SETPWD')
		
	Helper.writeLog('##Left: setPwd function')
def getLocation(sms):
	global SavedPassword
	Helper.writeLog('#Begin: getLocation function')
	Helper.writeLog('-Password in sms is '+sms.password)

	if Password == SavedPassword and SavedPassword != 0 :
		Helper.writeLog('-In Password Condition')

		GPSLat = getGPSLocation('Lat')
		Helper.writeLog('-Latitude= '+GPSLat)

		GPSLon = getGPSLocation('Lon')
		Helper.writeLog('-Longitude= '+GPSLon)
		
		Helper.writeLog('-Before Sending the SMS')
	
		SMSHandler.sendSMS(sms.number,'http://maps.google.com/?q='+GPSLat.rstrip().lstrip()+','+GPSLon.rstrip().lstrip())

		Helper.writeLog('-Deleting SMS')
		SMSHandler.deleteSMS(MessageIndex,'GL')
	else :
		Helper.writeLog('Deleting SMS')
		SMSHandler.deleteSMS(MessageIndex,'GL 2')
		
	Helper.writeLog('##Left: getLocation function')
def update(sms):
	Helper.writeLog('#Begin: Update function')
	Helper.writeLog('-Password in sms is '+sms.password)

	if Password == SavedPassword and SavedPassword != 0:
		Helper.writeLog('-In UPD Pass Condition')
		update(sms.number,MessageIndex)
	else :
		Helper.writeLog('Deleting SMS')
		SMSHandler.deleteSMS(MessageIndex,'UPD 2')
def startEngine(sms):
	Helper.writeLog('#Begin: StartEngine function')
	Helper.writeLog('-Password in sms is '+sms.password)

	if Password == SavedPassword and SavedPassword != 0 :
		Helper.writeLog('-In Start engine Condition')

		GPSLat = getGPSLocation('Lat')
		Helper.writeLog('-Latitude= '+GPSLat)

		GPSLon = getGPSLocation('Lon')
		Helper.writeLog('-Longitude= '+GPSLon)				

		GPIO.setIOvalue(8,1)	

		Helper.writeLog('-Before Sending the SMS')
	
		SMSHandler.sendSMS(Number,'Your car now is ready to start at this location http://maps.google.com/?q='+GPSLat.rstrip().lstrip()+','+GPSLon.rstrip().lstrip())

		Helper.writeLog('-Deleting SMS')
		SMSHandler.deleteSMS(MessageIndex,'STRT')
	else :
		Helper.writeLog('-Deleting SMS')
		SMSHandler.deleteSMS(MessageIndex,'STRT 2')
def stopEngine(sms):
	Helper.writeLog('#Begin: StopEngine function')
	Helper.writeLog('-Password in sms is '+sms.password)

	if Password == SavedPassword and SavedPassword != 0 :
		Helper.writeLog('-In Stop engine Condition')

		GPSLat = getGPSLocation('Lat')
		Helper.writeLog('-Latitude= '+GPSLat)

		GPSLon = getGPSLocation('Lon')
		Helper.writeLog('-Longitude= '+GPSLon)				

		Number = sms.number

		GPIO.setIOvalue(8,0)	

		Helper.writeLog('-Before Sending the SMS')
	
		SMSHandler.sendSMS(Number,'Your car was last seen in this location http://maps.google.com/?q='+GPSLat.rstrip().lstrip()+','+GPSLon.rstrip().lstrip())

		Helper.writeLog('-Deleting SMS')
		SMSHandler.deleteSMS(MessageIndex,'STP')
	else :
		Helper.writeLog('Deleting SMS')
		SMSHandler.deleteSMS(MessageIndex,'STP 2')	
def deleteAllMessages(sms):
	Helper.writeLog('#Begin: DeleteAllMessages function')
	Helper.writeLog('-Password in sms is '+Password)

	if Password == SavedPassword and SavedPassword != 0 :
		Helper.writeLog('-In Delete All Condition')

		Number = sms.number

		Helper.writeLog('-Before Sending the SMS')

		Helper.writeLog('-Deleting SMS')
		AllSMS = SMSHandler.check4SMS()
		if len(AllSMS) > 1:
			for i in range(1,len(AllSMS)):
				SMSHandler.deleteSMS(AllSMS[i].msgindex,'DELALL')

		SavedPassword = 0
		SMSHandler.sendSMS(Number,'All messages has been deleted!')
	else :
		Helper.writeLog('-Deleting SMS')
		SMSHandler.deleteSMS(MessageIndex,'DELALL 2')

def getGPSLocation(type) :
	gpsStatus = GPS.getPowerOnOff()
	if gpsStatus == 0:
		GPS. powerOnOff(1)
	
	gpsStatus = GPS.getPowerOnOff()
	while gpsStatus == 0 :
		gpsStatus = GPS.getPowerOnOff()
	
	GPSResult = GPS.getPosition()
	SER.send(str(GPSResult)+'\r\n')
	
	Latitude = str(GPSResult).split(',')[0].replace('(','')
	Latitude = Latitude[0:len(Latitude)-7]+'.'+Latitude[len(Latitude)-7:len(Latitude)]
	
	Longitude = str(GPSResult).split(',')[2].replace(')','')
	Longitude = Longitude[0:len(Longitude)-7]+'.'+Longitude[len(Longitude)-7:len(Longitude)]
	
	if type == 'Lat' :
		GPSResult = Latitude
	elif type == 'Lon' :
		GPSResult = Longitude
	
	return GPSResult
def extractCurrFile():
	strLen=15
	res=Helper.sendCmd('AT#ESCRIPT','',10)
	index=res.find('UPD')
	if (index!= -1):
		currFile=res[index:index+strLen]
		return currFile
	else:
		return -1
def check4Updates(currFile,mode):
	UPDLIST="updlist.txt"
	res = Helper.connectGPRS()
	if res != -1:
		data = transferFTP('GET',UPDLIST,0,0)
		
		if mode == 'Name':
			returnValue = parser(data,currFile,'Name')
		else:
			returnValue = parser(data,currFile,'Size')
		
		return returnValue
	else:
		SER.send('Error: connectGPRS returned -1\r\n')
		return -1
def parser(data,currFile,returnType):
	lastVersionIdx = lastIndexOf(data,'UPD')
	
	if lastVersionIdx != -1 :
		lastVersionName = data[lastVersionIdx:len(data)].split(',')[0]
		lastVersionSize = data[lastVersionIdx:len(data)].split(',')[1]
		
		SER.send('Last version name = '+lastVersionName+'\r\n')
		SER.send('Last version size = '+lastVersionSize+'\r\n')
		
		if returnType == 'Name':
			return lastVersionName
		else:
			return lastVersionSize
			
	else :
		return -1
def iterateHTTPCmd(comando, parametro, TIMEOUT_CMD, numCheck):
    while( numCheck >= 0):
        numCheck = numCheck - 1
        res  = Helper.sendCmd(comando, parametro, TIMEOUT_CMD)
        SER.send(res + ' ' + comando + '=' + parametro)
        if(res.find('CONNECT') != -1) :
            return 1
        MOD.sleep(TIMEOUT_CMD)
        if(numCheck == 0):
            SER.send(res + ' ' + comando + '=' + parametro)
            return -1
def transferFTP(transferType, fileName, mode, expectedFileSize):  
	SER.send('transferFTP\r\n')
	TIMEOUT_CMD = 50
	TIMEOUT_CMD_FTP =100
	FTP_PARAMETER = '"ftp.alwaysdata.com", "USERNAME", "PASSWORD",1'
	fileName = '"' + fileName + '"'
	numCheck = 3
	res = Helper.iterateCmd('AT#FTPCLOSE', '', TIMEOUT_CMD, numCheck)
	if(res == -1):
		SER.send("ERROR: setting AT#FTPCLOSE \r\n")
		return -1
	
	res = Helper.iterateCmd('AT#FTPOPEN', FTP_PARAMETER, TIMEOUT_CMD_FTP, numCheck)
	if(res == -1):
		textLog = "ERROR: setting AT#FTPOPEN = " + FTP_PARAMETER + "\r"
		SER.send(textLog)
		return -1
	
	res = Helper.sendCmd('AT#FTPTYPE', '0', TIMEOUT_CMD)
	
	if(transferType.find('GET') != -1):
		SER.send('ftp get\r\n')
		data = ''
		res = Helper.sendCmd('AT#FTPGET',fileName,0)
		SER.send('data  found\r\n')
		SER.send(data)
        
		dataList = []
		
		timer = MOD.secCounter()
		timeout = timer + 100 #secondi
		temp = ''
        
		if mode == 1:
			SER.send('In Save file'+fileName+'\r\n')

		fileSize = 0
		while(((temp.find('NO CARRIER') == -1) or (MDM.getDCD() != 0))):
			SER.send('temp is '+temp+'\r\n')
			temp = MDM.read()

			if len(temp) != 0 :
				dataList.append(temp)

				if mode == 1:
					fileSize = fileSize + len(temp)

					timer = MOD.secCounter()
        
		if mode != 1:
			SER.send('Length of data list: '+str(len(dataList))+'\r\n')                
			data = ''.join(dataList)
			SER.send('Length of data: '+str(len(data))+'\r\n')        
			SER.send('fuori while\r\n')
			if(len(data) == 0):
				SER.send("ERROR: data to save is empty \r\n")
				return -1
	
			startIndex = 0
			endIndex = len(data)
			if(data.find('CONNECT\r\n') != -1):
				startIndex = data.find('CONNECT\r\n') + len ('CONNECT\r\n')
				endIndex = len(data) - 12

				data= data[startIndex: endIndex]

				SER.send('Start Index: '+str(startIndex)+'\r\n')      
				SER.send('End Index: '+str(endIndex)+'\r\n')      
				SER.send('Length of data: '+str(len(data))+'\r\n')                
				SER.send('data fron ftp server:\r\n')
				return data
        
		else:
			SER.send('Sending command AT#WSCRIPT\r\n')
			SER.send('File size calculated = '+str(fileSize)+'\r\n')
			
			fileSize = fileSize - 25
			
			if fileSize == int(expectedFileSize) :
				writeScript(fileName,dataList,123,int(expectedFileSize))
				return 1
	
	return -1 #inutile
def writeScript(name, data, hidden, fileSize):
	SER.send('In write script with length = '+str(len(data))+'\r\n')
	SER.send('AT#WSCRIPT=%s,%d\r' % (name,fileSize))
	MDM.send('AT#WSCRIPT=%s,%d\r' % (name,fileSize), 2)
	res = ''
	while 1:
		res = res + MDM.receive(2)
		if res.find('>>>') != -1:
			break
			
	SER.send("1:"+str(res)+"\r\n")
	
	for i in range(1,len(data)-1):
		MDM.send(data[i], 2)
		MOD.sleep(10)
	
	res = ''
	while 1:
		res = res + MDM.receive(2)
		if res.find('OK') != -1 or res.find('ERROR') != -1:
			break

	SER.send("2:"+str(res)+"\r\n")
def lastIndexOf(data,text) :
    Temp = data.find(text)
    
    SER.send(str(Temp)+'\r\n')
    
    while Temp != -1 :
        Index = Temp
        Temp = data.find(text,Temp + len(text))
        
        SER.send('Index = '+str(Index)+', Temp = '+str(Temp)+'\r\n')   
    
    return Index
def enableAndReb(fileToExec, Number, MessageIndex):
    #deleteSMS(MessageIndex)
    SER.send('In Save file'+fileToExec+'\r\n')
    SER.send('After renaming file'+fileToExec+'\r\n')
    NUMBER = Number
    SMSText = "I'm going to reboot, enabling the following file: "+fileToExec
    SER.send("enableAndReb: trying to enable and reboot the module\r\n")
    fileName = '"' + fileToExec + '"'
    res=MDM.read()
    res = Helper.sendCmd('AT#ESCRIPT',fileName,0)
    res=MDM.receive(30)
    
    if res.find('OK') != -1:
        MOD.sleep(200)
        text = "script qualified :" + fileName + '\r\n'
        SER.send(text+"\r\n")
        res= sendSMS(NUMBER,SMSText)
        MOD.sleep(200)
        res= MDM.send('AT#REBOOT\r',0)
        MOD.sleep(200)
        SER.send('rebooting\r\n')
        return 1
    else:
        return -1
def update(Number, MessageIndex):
	currFile=extractCurrFile()
	text = "EXTRACTED FILE: " + currFile + "\r\n"
	SER.send(text)
	if(currFile==-1):
		SER.send("ERROR IN EXTRACT CURRENT FILE\r\n")
		return -1
	fileToExec=check4Updates(currFile,'Name')
	fileSize=check4Updates(currFile,'Size')

	if(fileToExec==-1):
		SER.send("ERROR: check4Update return -1\r\n")
		return -1
	elif(fileToExec!=currFile):
		data=transferFTP('GET', fileToExec,1,fileSize) #download the update file
		if( data == -1):
			SER.send("ERROR in FTP transfer\r\n")
			return -1
		
		SER.send("Before enableandreb\r\n")  
		res=enableAndReb(fileToExec, Number,MessageIndex)
		SER.send("ERROR ENABLING OR REBOOTING MODULE\r\n")
		return -1
	
	else:
		SER.send("NO UPDATE AVAILABLE\r\n")
		NUMBER = Number
		SMSText="No new update, call: " + currFile
		res = sendSMS(NUMBER, SMSText)
		deleteSMS(MessageIndex,'Update')
		return 1
