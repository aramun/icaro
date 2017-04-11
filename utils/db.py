class Oracle():
    def __init__(self, conn_string):
        import cx_Oracle
        con = cx_Oracle.connect(con_string) 
	self.cursor = con.cursor()

class Postgres():
    def __init__(self, host, db, user, psw):
        import psycopg2
        con_string = "host='" + host + "' dbname='" + db + "' user='" + user + "' password='" + psw + "'"
	con = psycopg2.connect(con_string)
	self.cursor = con.cursor()
