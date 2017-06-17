def getdata():
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
            
        count = 0
        db = []
        for k in range(len(results)-1):
            end_point= float(results[k][1])*100
            if end_point < 24:
                flag += 1
                
            else:
                flag = 0
                
            if flag >= 20:
                count += 1
                flag = 0
                db.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(results[k][0]))))

        c = [k for k in results]
        i = [[u[0],float(u[1])*100] for u in c]
        f = {}

        for l in i:
            
            l[0] = l[0]
            if l[0] in f:
                f[l[0]] = (f[l[0]] + l[1])/2
            else:
                f[l[0]] = l[1]
        l = f.keys()
        l.sort()
        c = 0.01
        for m in l:
            y = str(m)+','+m1+','+str(f[m])+','+""+'\n'
            main.append(y)
            c += 0
        
  
        

    r = {}
    for t in db:
        l = t.split()[1]
        l = l.split(':')[0]
        if l in r:
            r[l] += 1
        else:
            r[l] = 1
    import time,pymysql

    db = pymysql.connect(ip,"root","root","timebased")
    cursor = db.cursor()
    for k in r:
        sql = "UPDATE main SET col%s = col%s+%s" % (k,k,r[k])
        print sql
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            print "ERROR Updating Sleep Stats"

    db = pymysql.connect(ip,"root","root","timebased")
    cursor = db.cursor()
    sql = "SELECT * FROM main"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
    except:
        print 'Error Getting Data'
    a = open('static/formatted_run.csv','w')
    for l in range(len(results[0])):
        u = '0'+str(l)+':00'
        if len(u) > 5:
            u = u[1:]
        u = u.split(':')
        u = datetime.datetime(2017,01,01,int(u[0]),int(u[1])).strftime('%s')
        main.append(str(u)+','+'Employees'+','+str(results[0][l])+',0\n')
    a.writelines(main)
    a.close()
    print 'DONE' 
