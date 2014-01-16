import MDM
import MOD
import SER
import GPS
import md5
import GPIO
import SMSHandler
import Helper

WEBSVC_UPD_INTERVAL = 2
SLEEP_INTERVAL = 30
COUNTER = WEBSVC_UPD_INTERVAL

try:
	Helper.SavedPassword = SMSHandler.getSavedPassword()
except Exception,e:
		Helper.writeLog('###GetSavedPassword Exception###')
		Helper.writeLog(str(e))

while 1:
    try:
		Helper.writeLog('#Begin: While loop')
		Helper.writeLog('-Saved pass is '+str(Helper.SavedPassword))
		SMSListResult = SMSHandler.check4SMS()
		if len(SMSListResult) > 0:
			for i in range(0,len(SMSListResult)):
				SMSHandler.processSingleSMS(SMSListResult[i])

		Helper.writeLog('-Finished While Loop')
    except Exception,e:
		Helper.writeLog('###While Loop Exception###')
		Helper.writeLog(str(e))
        
    MOD.sleep(SLEEP_INTERVAL)
