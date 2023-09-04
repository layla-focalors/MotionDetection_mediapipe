import pymysql
conn = pymysql.connect(host='localhost', user='root', password='root', db='log', charset='utf8')

cur = conn.cursor()
cur.execute()
conn.commit()
conn.close()