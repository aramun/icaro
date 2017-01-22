import cx_Oracle
import psycopg2

def oracle_con(con_string):
	con = cx_Oracle.connect(con_string) 
	return con.cursor()

def postgre_con(host, db, user, psw):
	con_string = "host='" + host + "' dbname='" + db + "' user='" + user + "' password='" + psw + "'"
	con = psycopg2.connect(con_string)
	return con.cursor()
