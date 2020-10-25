#!/usr/bin/python3
	

import subprocess
import cgi
	
print("content-type: text/html")
print()	

form = cgi.FieldStorage()
get_cmd = form.getvalue("cmd")	

# cmd = "date"
cmd = "sudo "+get_cmd
print("command: {} | \n".format(cmd))
output = subprocess.getstatusoutput(cmd)
	
print("status-code: {} | \n".format(output[0]))
print()
print("output: <PRE> {} <PRE> \n".format(output[1]))
print()
