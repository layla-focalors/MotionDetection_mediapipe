def connectdb(database, time, number, x, y, z, visi):
    # print(database)
    try: 
        import datetime
        import pymysql
    except:
        print("패키지 로드에 실패했습니다 : 403")
    try:
        dt = str(datetime.datetime.now())
    # print(dt)
        conn = pymysql.connect(host='localhost', user='root', password='root', db='model_log', charset='utf8')
        Q2 = f"INSERT INTO {database} VALUES('{dt}', {number}, {x}, {y}, {z}, {visi})"
        # print(Q2)
        cur = conn.cursor()
        cur.execute(Q2)
        conn.commit()
        conn.close()
        print(database, dt, number, x, y, z, visi)
    except:
        print("명령 실행에 실패했습니다! 504")
    
# connectdb(str("f7737beec6a34aac"), str("1992"), 4, 3,4,2,2)