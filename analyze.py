#!/usr/bin/env python
import os
import sys
from collections import defaultdict
from androguard.core import *
from androguard.core.bytecodes.apk import *
apk = 0
nonapk = 0
permhash = defaultdict(int)	
minsdk = defaultdict(int)
maxsdk = defaultdict(int)
targetsdk = defaultdict(int)
appnamesdb = defaultdict(int)
nonapklist = []
def sort_print_db(db):
	for key in sorted(db,key=int):
		print key,"=>",db[key]	
def sort_by_value_print_db(db):
	for key,value in sorted(db.iteritems(),key=lambda 
							(k,v):(v,k),reverse=True):
		output = ("%s : %s" %(key,value))	
		print output
def hash_entry(entry,db):
	if entry == None:
		db[0] += 1	
	elif entry != None:
		db[entry] += 1 
def apk_permissions(myapk):
	global apk, nonapk
	try:
		a = APK(myapk,zipmodule=1)
		apk += 1
		min_sdk_version = a.get_min_sdk_version()
		max_sdk_version = a.get_max_sdk_version()
		target_sdk_version = a.get_target_sdk_version()
		appname = a.get_package()
		hash_entry(min_sdk_version,minsdk)
		hash_entry(max_sdk_version,maxsdk)
		hash_entry(target_sdk_version,targetsdk)
		hash_entry(appname,appnamesdb)
		for perm in a.get_permissions():
			permhash[perm] += 1	
	except:
		nonapk += 1
		nonapklist.append(myapk)	
	
print(sys.argv[1]) 
listing = os.listdir(sys.argv[1])

for infile in listing:
	apk_permissions(sys.argv[1]+"/"+infile)
print "total correct apk files: ",apk
print "total non-apk files: ",nonapk
print "min sdk versions targeted"
sort_by_value_print_db(minsdk)
print "max sdk versions targeted"
sort_by_value_print_db(maxsdk)
print "target sdk versions"
sort_by_value_print_db(targetsdk)
#print "app names found"
print "appnamesdb size ",len(appnamesdb)
#for key,value in sorted(appnamesdb.iteritems(),key=lambda (k,v):(v,k),reverse=True):
#	output = ("%s : %s" %(key,value))	
#	print output	
if len(nonapklist) != 0:
	print "size of nonapklist",len(nonapklist)
	nonapkfile=open('/home/punisher/scripts/output.txt','w')
	for entry in nonapklist:
		newentry = entry + '\n'
		nonapkfile.write(newentry)
	nonapkfile.close()
if len(permhash) != 0:
	print "size of permhash:",len(permhash)
	#permhashfile=open('/home/punisher/scripts/permissions.txt','w')
	#for key,value in sorted(permhash.iteritems(),key=lambda (k,v):(v,k),reverse=True):
	#	output = ("%s : %s\n" %(key,value))	
	#	permhashfile.write(output)
	#permhashfile.close()
