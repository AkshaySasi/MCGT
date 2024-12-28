import pymysql
def connection():
    con=pymysql.connect(host='localhost',user='root',password='',db='myprivacy',port=3306)
    cu=con.cursor()
    return con,cu