def getdata():
    import time,pymysql
    db = pymysql.connect('localhost',"root","root","bharathacks")
    cursor = db.cursor()
    sql = "SELECT * FROM prateek"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
    except:
        print 'Error Getting Data'

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
    o = ['Seconds,Data,value,Altitude\n']
    c = 0.01
    for m in l:
        y = str(m)+','+'EAR'+','+str(f[m])+','+""+'\n'
        o.append(y)
        y = str(m)+','+'Threshold'+','+'15.0,'+""+'\n'
        o.append(y)
        c += 0
    b = open('static/formatted_run.csv','w')
    b.writelines(o)
    b.close()
    print ' Data File Synced ' 
