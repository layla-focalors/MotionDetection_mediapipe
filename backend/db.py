def db_create(uuid):
    try:     
        import pymysql
    except:
        print("패키지 불러오기 실패! | 501")
    try:    
        conn = pymysql.connect(host='localhost', user='root', password='root', db='model_log', charset='utf8')
    except:
        print("서버 연결 실패! | 404")
    try:
        cur = conn.cursor()
        Q1 = f"CREATE TABLE {uuid} (time VARCHAR(200), NUMBER INT, X VARCHAR(200), Y VARCHAR(200), Z VARCHAR(200), VISI VARCHAR(200));"
        cur.execute(Q1)
        conn.commit()
        conn.close()
    except:
        print("쿼리 처리 실패 : 502")
    
# db_create("sq29")