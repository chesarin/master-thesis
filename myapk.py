#!/usr/bin/env python
from androguard.core.bytecodes.apk import APK 

class MyAPK(APK):
	def get_sharedUserId(self):
		return self.get_element('manifest',
								'android:sharedUserId')

	def is_sharedUserIdSet(self):
		result = False
		element = self.get_element('manifest',
								   'android:sharedUserId')
		if element != None:
			result = True
		return result

	def get_sharedUserIdInfo(self):
		userinfo = ( None, None)
		sharedUserId = self.get_element('manifest',
										'android:sharedUserId')	
		sharedUserLabel = self.get_element('manifest',
										   'android:sharedUserLabel')
		if self.is_sharedUserIdSet():
			userinfo = (sharedUserId,sharedUserLabel)
		return userinfo

	def get_creationDate(self):
		manifest = self.zip.getinfo('AndroidManifest.xml')
		date = manifest.date_time
		return (str(date[0])+'-'+str(date[1])
				+'-'+str(date[2])+' '+str(date[3])
				+':'+str(date[4])+':'+str(date[4]))

		
