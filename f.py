#!/usr/bin/python
#This work is licensed under the Creative Commons Attribution-ShareAlike 3.0 Unported License. To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/3.0/.

import socket,sys,time,argparse

class fuzzer():

	def __init__(self):	
		self.buffer = ['A']
		self.counter = 20
		self.commands_post = ['LIST','STOR','ABOR','CWD','DELE','MDTM','MKD','NLST','PORT','PWD','RETR','RMD','RNFR','RNTO','SITE','SIZE','TYPE','ACCT','APPE','CDUP','HELP','MODE','NOOP','REIN','STAT','STOU','STRU','SYST']
		self.commands_pre = ['USER','PASS']
		self.chars = ["(",")","-","_","=","+","!","@","#","$","%","^","&","*","}","{",";",":",".","/","?","<",">","`","~","\n"] 
	def createbuffer(self,l):
		self.l = l
		while len(self.buffer) <= l:		
			self.buffer.append('A'*self.counter)
			self.counter = self.counter + 20
	def fuzzloop_preauth(self,h,u):
		self.h = h
		self.u = str(u)
		for string in self.buffer:	
			try:	
				self.s =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				self.s.connect((self.h, 21))
				print '[*] connecting to server....'
				data=self.s.recv(1024)
				print '%s\r\n'%data
			except:
				print 'coudn\'t connect'
			print  "[*]Fuzzing USER" + " with length " + str(len(string))
			self.s.send('USER ' + string + '\r\n')
			d = self.s.recv(1024)
			self.s.send('QUIT\r\n')
			q = self.s.recv(1024)
			self.s.close()
			print '%s\n%s'%(d,q)
		for string in self.buffer:	
			try:	
				self.s =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				self.s.connect((self.h, 21))
				print '[*] connecting to server....'
				data=self.s.recv(1024)
				print '%s\r\n'%data
			except:
				print 'coudn\'t connect'
			print "[*]Fuzzing PASS" + " with length " + str(len(string))
			self.s.send('USER ' + self.u + '\r\n')
			d = self.s.recv(1024)
			self.s.send('PASS ' + string + '\r\n')
			q = self.s.recv(1024)
			self.s.send('QUIT\r\n')
			self.s.recv(1024)
			print '%s\r\n%s'%(d,q)
			self.s.close()
	def fuzzloop_postauth(self,h,u,p):
		self.h = h
		self.p = str(p)
		self.u = str(u)
		for command in self.commands_post:
			for string in self.buffer:		
				try:	
					self.s =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					self.s.connect((self.h, 21))
					print '[*] connecting to server....'
					data=self.s.recv(1024)
					print '%s\r\n'%data
				except:
					print 'coudn\'t connect'
				self.s.send('USER ' + self.u + '\r\n')
				d=self.s.recv(1024)
				self.s.send("PASS " + self.p + "\r\n")	
				q = self.s.recv(1024)
				self.s.send("PASV\r\n")
				p = self.s.recv(1024)
				print "[*]Fuzzing " + command + " with length " + str(len(string))
				print '%s\r\n%s\r\n%s'%(d,q,p)
				self.s.send(command + ' ' + string + '\r\n')
				d=self.s.recv(1024)
				print d		
				self.s.close()

print """
#################################################
# Simple FTP Fuzzer				#
# Saif El Sherei				#
# http://www.elsherei.com			#
# https://twitter.com/Saif_Sherei		#						#
#################################################"""


parser = argparse.ArgumentParser(
	description = 'A Simple Ftp Fuzzer',
	epilog = 'And That\'s how you Fuzz an FTP server')
parser.add_argument('-s','--post', help = 'post authentication',action='store_true')
parser.add_argument('-r','--pre', help = 'pre-authentication',action='store_true')
parser.add_argument('-u','--user', help = 'UserName')
parser.add_argument('-p','--password', help = 'password')
parser.add_argument('-c','--host', help = 'Host')
parser.add_argument('-l','--length', help = 'Buffer Length')
p = parser.parse_args()
print p 

f=fuzzer()
if p.length and p.pre == True:
	l = int(p.length)/20
	f.createbuffer(l)
	f.fuzzloop_preauth(p.host,p.user)
elif p.length and p.password and p.post == True:
	l= int(p.length)/20
	f.createbuffer(l)
	f.fuzzloop_postauth(p.host,p.user,p.password)
elif p.user == None:
	print "Please Enter UserName\r\n"
	parser.print_help() 
elif p.length == None:
	print "Please Enter Buffer Length\r\n"
        parser.print_help()
elif p.host == None:
	print "Please Enter Host\r\n"
	parser.print_help()
elif p.post == True and p.password == None:
	print "Please Enter Password\r\n"
	parser.print_help()
elif p.pre == False or p.post == False:
	print "Please Enter Fuzzing Mode\r\n"
        parser.print_help()
else:
	parser.print_help()
