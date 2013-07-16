#!/usr/bin/env python
import os
import sys
from collections import defaultdict
from myapk import MyAPK

def print_db_sorted_by_value(db):
	for key,value in sorted(db.iteritems(),key=lambda (k,v):(v,k),reverse=True):
		output = ("%s : %s" %(key,value))
		print output

def simple_hash_entry(entry,db):
	db[entry] += 1

def hash_entry(entry,db):
	if entry == None:
		db[0] += 1
	elif entry != None:
		db[entry] += 1

def app_name(entry,db):
	name = entry.get_package()
	hash_entry(name,db)

def process_apk_file(apkfile):
	global apk,nonapk
	try:
		a = MyAPK(apkfile,zipmodule=1)
		apk += 1
		app_name(a,appnamedb)
#		if a.is_sharedUserIdSet():
#			print apkfile
#		uid = a.get_sharedUserId()
#		simple_hash_entry(uid,userid)
#        uid = a.get_sharedUserId(uid,userid)
#        simple_hash_entry(uid,userid)
	except:
		nonapk += 1

def process_files(directory):
	listing = os.listdir(directory)
	for infile in listing:
		temp = directory+'/'+infile
		process_apk_file(temp)

def print_results():
	print 'total apk valid files',apk
	print 'total non-apk valid files',nonapk

	print 'app names obtained'
	print_db_sorted_by_value(appnamedb)	
#	print 'size of userid db',len(userid)
#	for key in userid:
#		print key," => ",userid[key]

def main():
	directory = sys.argv[1]	
	process_files(directory)
	print_results()

#Global variables
userid = defaultdict(int)
appnamedb = defaultdict(int)
apk = 0
nonapk = 0

if __name__ == '__main__':
	main()
