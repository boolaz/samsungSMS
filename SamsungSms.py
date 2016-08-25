#!/usr/bin/python
# -*- coding: utf-8 -*-
#  ------------------------------------------------------------------------
#  Name: samsungSMS.py
#  Author : Bruno VALENTIN (bruno@boolaz.com)
#  Revision : 1.0
#  Date : 27/07/2016
#  Description : parses SMS from Samsung SMB-550H Cellphone (.vmg files)

import os,sys,re
from sys import argv
import fnmatch

softdesc={"name":"samsungSMS",
          "version":"1.0", \
          "release":"27/07/2016", \
          "purpose":"parses SMS from Samsung SMB-550H Cellphone", \
          "link":"https://github.com/boolaz/samsungSMS" }

usage_text="""Usage: samsungSMS.py SMS_directory"""

extensions=["*.vmg"]

#-------------------------
class Banner(object):
    """Banner for the program"""
    def __init__(self, banner_values):
        super(Banner, self).__init__()
        self.banner_values = banner_values

    def display(self):
        print("""
****************************************************** \n\
* {0} {1} ({2}) - bruno@boolaz.com \n\
* {3}           \n\
* Updates : {4} \n\
******************************************************""" \
         .format(self.banner_values['name'],self.banner_values['version'],
                 self.banner_values['release'],self.banner_values['purpose'],
                 self.banner_values['link']))

#-------------------------
def usage(usage_text):
    """Usage"""
    print usage_text

#-------------------------
def replace_special_chars(sms_text):
	sms_text=sms_text.replace("=C5=93","oe")
	sms_text=sms_text.replace("=C3=A9","é")
	sms_text=sms_text.replace("=C3=A8","è")
	sms_text=sms_text.replace("=C3=A7","ç")
	sms_text=sms_text.replace("=C3=AA","ê")
	sms_text=sms_text.replace("=C3=A0","à")
	sms_text=sms_text.replace("=C3=A2","â")
	sms_text=sms_text.replace("=C3=87","C")
	sms_text=sms_text.replace("=C3=80","A")
	sms_text=sms_text.replace("=C3=87","C")
	sms_text=sms_text.replace("=C3=AE","î")
	sms_text=sms_text.replace("=C3=AF","ï")
	sms_text=sms_text.replace("=C3=B4","ô")
	sms_text=sms_text.replace("=C3=AC","i")
	sms_text=sms_text.replace("=C3=B6","ô")
	return sms_text

#-------------------------
def main(argv):

	my_banner=Banner(softdesc)
	my_banner.display()

	# parses arguments ----
	try:
		chemin=sys.argv[1]
	except:
		usage(usage_text)
		sys.exit(2)

	# search for files ----
	fichiers=[]
	try:
		for root, dirs, files in os.walk(chemin, topdown=False):
			for extension in extensions:
				for name in fnmatch.filter(files, extension):
					fichiers.append(os.path.join(root, name))
	except:
		print 'A problem occured during file enumeration'

	# analysis of files
	out_file=open("SMS.csv","w")
	for fichier in fichiers:
		sms_status=sms_box=sms_cell=sms_date=sms_text=''
		in_body=False
		in_file=open(fichier,"r")
		for line in in_file:
			match_flag=False
			if not match_flag:
				value=re.search("X-IRMC-STATUS:([a-z]+)", "{0}".format(line), re.I)
				if value:
					sms_status=value.group(1)
					match_flag=True

			if not match_flag:
				value=re.search("X-IRMC-BOX:([a-z]+)", "{0}".format(line), re.I)
				if value:
					sms_box=value.group(1)
					match_flag=True

			if not match_flag:
				value=re.search("TEL;CELL:([0-9+]+)", "{0}".format(line), re.I)
				if value:
					sms_cell=value.group(1)
					match_flag=True

			if not match_flag:
				value=re.search("Date:(.+)\n$", "{0}".format(line), re.I)
				if value:
					sms_date=value.group(1)
					sms_date=sms_date.strip('\r')
					match_flag=True

			if not match_flag:
				value=re.search("TEXT;[^:]+:(.+)$", "{0}".format(line), re.I)
				if value:
					sms_text=value.group(1).strip('\r\n')
					sms_text = re.sub(r"=$", "", sms_text)
					#sms_text=sms_text
					in_body=True
					match_flag=True

			if not match_flag and in_body:
				value=re.search("END:VBODY", "{0}".format(line), re.I)
				if value:
					in_body=False
				else:
					sms_text+=re.sub(r"=$", "", line.strip('\r\n'))

		if sms_date:
			sms_text=sms_text.replace("\n",". ")
			try:
				out_file.write ("{0};{1};{2};{3};{4}\n".format(sms_date,sms_cell,sms_box,sms_status,replace_special_chars(sms_text)))
			except:
				print "Error occured exporting file"

		in_file.close()

	out_file.close()
	print "{0!s} SMS successfully exported to SMS.csv".format(len(fichiers))

if __name__ == "__main__":
	main(sys.argv[1:])
