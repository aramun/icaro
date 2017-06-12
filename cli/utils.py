import os
import socket
import shutil
import json
import tarfile

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

def jsonUpdate(source, key, val):
    content = json.loads(readLines(source))
    content[key] = val
    fileWrite(source, json.dumps(content))

def jsonArrayUpdate(source, key, val):
    content = json.loads(readLines(source))
    for obj in content:
        obj[key] = val
    fileWrite(source, json.dumps(content))

def get_tar_byte(source):
    with tarfile.open("api.tar.gz", "w:gz") as tar:
        tar.add(source, arcname=os.path.basename(source))
    with open("api.tar", "rb") as binary_file:
        return binary_file.read()
    

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

def insertIntoFile(offset1, stringToInsert, file):
	content = readLines(file)
	if content.strip().find(stringToInsert.strip()) == -1:
		n = content.find(offset1)
		if n != -1:
			while (content[n] != "{"):
				n += 1
			content = content[:n+1] + stringToInsert + content[n+1:]
			fileWrite(file, content)

def line_prepender(filename, line):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)

def copytree(source, destination):
	if not os.path.exists(destination):
		shutil.copytree(source, destination)

def getHome():
	return os.path.expanduser("~")
