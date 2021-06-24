#==Imports==
import time
from flask import Flask, render_template, redirect, request
import mysql.connector
import random

#====
app = Flask(__name__,template_folder='templates')
#================================================
@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/new', methods=['POST','GET'])
def new():
    room_id=random.randint(1111,9999)
    createTable1dbCon=mysql.connector.connect(host="us-cdbr-east-04.cleardb.com",
                            user="b5ace312629951",
                            passwd="af1b46b6",
                            database="heroku_2755bac09e746fb")
    createTable1dbCur=createTable1dbCon.cursor()
    
    createTable1dbCur.execute("CREATE TABLE IF NOT EXISTS rooms(room_id INTEGER, members INTEGER, PRIMARY KEY(room_id))")      
    createTable1dbCon.commit()
    
    createTable1dbCur.execute("INSERT INTO rooms (room_id, members) VALUES (%s,%s)", (room_id,0))      
    createTable1dbCon.commit()

    createTable1dbCon.close()
    return redirect(f"/room/{room_id}")

@app.route("/room", methods=['POST','GET'])
def sendToRoom():
    # time.sleep(2)
    # createTable1dbCon=mysql.connector.connect(host="us-cdbr-east-04.cleardb.com",
    #                         user="b5ace312629951",
    #                         passwd="af1b46b6",
    #                         database="heroku_2755bac09e746fb")
    # createTable1dbCur=createTable1dbCon.cursor()
    if request.method == 'POST':
        return redirect(f"/room/{request.form['roomid']}")
    else:
        return error_404("as")

@app.route("/room/<GetRoom_id>",methods=['GET','POST'])
def join_room(GetRoom_id):
    if GetRoom_id.isdigit():
        createTable1dbCon=mysql.connector.connect(host="us-cdbr-east-04.cleardb.com",
                                user="b5ace312629951",
                                passwd="af1b46b6",
                                database="heroku_2755bac09e746fb")
        createTable1dbCur=createTable1dbCon.cursor()
        createTable1dbCur.execute("SELECT * FROM rooms")
        rooms_available=createTable1dbCur.fetchall()
        
        for i in rooms_available:
            if int(GetRoom_id) in rooms_available[rooms_available.index(i)]:
                if rooms_available[rooms_available.index(i)][1] < 4:
                    createTable1dbCur.execute(f"UPDATE rooms SET members={rooms_available[rooms_available.index(i)][1]+1} WHERE room_id={rooms_available[rooms_available.index(i)][0]}")
                    createTable1dbCon.commit()
                    createTable1dbCon.close()
                    return render_template("game.html",lst=[1,2,3,4,5,6])
                else:
                    return redirect("/")
        return redirect("/")
    else:
        return "RUKO JARA SABAR KARO/ HAATH SE LIKHNA BAND KARO... URL"
    
@app.errorhandler(404)
def error_404(e):
    return render_template("404.html")
#==__name__=====================
if __name__ == '__main__':
    app.run(debug=True)
