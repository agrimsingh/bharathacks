import os
import pymysql, time
from flask import *
app = Flask(__name__, static_url_path='/static')
@app.route('/')
def index():
    t = []
    name = ['prateek','agrim']
    ip = "192.178.5.10"
    db = pymysql.connect(ip,"root","root","bharathacks")
    cursor = db.cursor()
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
                i = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(results[k][0])))
                i1 = i.split()
                i2 = ''.join(i1[0].split('-'))
                i3 = ''.join(i1[1].split(':'))
                f = '-'.join([i2,i3])
                db.append([i,f])

        finalvar = [count,db]
        list1 = []
        for f in os.listdir('output'):
            list1.append(f[:-4])
        if len(finalvar[1]) != 0:
            for m in range(len(finalvar[1])):
                if finalvar[1][m][1] in list1:
                    finalvar[1][m].append(finalvar[1][m][1]+'.avi')
                else:
                    o = finalvar[1][m][1].split('-')

                    o[1] = str(int(o[1])+1)
                    o = '-'.join(o)
                    if o in list1:
                        finalvar[1][m].append(o+'.avi')
                    else:
                        o = finalvar[1][m][1].split('-')
                        o[1] = str(int(o[1])-1)
                        if len(o[1]) != 6:
                            o[1] = "0"+o[1]
                        o = '-'.join(o)
                        if o in list1:
                            finalvar[1][m].append(o+'.avi')
                        else:
                            finalvar[1][m].append(0)
                finalvar[1][m].append(m1)
            t.append(finalvar)

    results_dict={}
    c= 1
    for l in t:
        for o in l[1]:
            results_dict[str(c)] = [o[3],o[0],o[2]]
            c += 1

    Table = []
    temp = ['S.No','Name','Time','Proof']
    Table.append(temp)
    for key, value in results_dict.iteritems():
        temp = []

        temp.extend([key,value[0],value[1],'<a href="http://0.0.0.0:5000/'+str(value[2])+'"> Check Status </a>'])
          #Note that this will change depending on the structure of your dictionary
        Table.append(temp)

    return render_template('main.html',table=Table)

@app.route('/<filename>')
def router(filename):
    return send_from_directory('output', filename)

if __name__=="__main__":
    app.run(debug =True,host='0.0.0.0')