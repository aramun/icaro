import os
import socket

def checkPort(port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	result = sock.connect_ex(('127.0.0.1', port))
	if result == 0:
		return True
	else:
		return False

def selfLocation():
	return os.path.dirname(os.path.realpath(__file__))

def readLines(path):
	file = open(path, "r")
	content = file.readlines()
	file.close()
	return "".join(content)

def createFolder(path):
	if not os.path.exists(path):
		os.mkdir(path)

def fileWrite(file,content):
	file = open(file, "w")
	file.write(content)
	file.close()

def importer(source, destination):
	fileWrite(destination,readLines(source))

def mkDir(path):
	if not os.path.exists(path):
		os.makedirs(path)