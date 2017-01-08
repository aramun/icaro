import json
import uuid
import crypt
from cassandra.cluster import Cluster


def create_session(session):
	query = """
			CREATE TABLE sessions (
				session_id text PRIMARY KEY,
				vars list<text>,
				validation int
			);
			"""
	session.execute(query)

def create_cache(session):
	query = """
			CREATE TABLE cache (
				cache_id text PRIMARY KEY,
				content text,
				validation int
			);
			"""
	session.execute(query)

def init():
	cluster = Cluster()#[192.168.0.1, ....]->you can connect more machine
	session = cluster.connect("session")
	create_session(session)
	create_cache(session)
	return session

def set(req, var, value):
	session = init()
	session_id = crypt.crypt("&&".join(req.headers), "$6$random_salt")
	var = crypt.crypt(var, "$6$random_salt")
	value = crypt.crypt(value, "$6$random_salt")
	print session_id
	print var
	print value

