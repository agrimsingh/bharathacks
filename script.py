def refreshstats():
    import time,pymysql
    name = ['prateek','agrim']
    import datetime
    ip = "192.178.5.10"

    db = pymysql.connect(ip,"root","root","bharathacks")
    cursor = db.cursor()
    main = ['Seconds,Data,value,Altitude\n']
    for m1 in name:
        sql = "SELECT * FROM "+ m1
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
        except:
            print 'Error Getting Data'
    print results

refreshstats()