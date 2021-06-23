#==Imports==
from flask import Flask, render_template, redirect, Request
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
    createTable1dbCon=mysql.connector.connect(host="us-cdbr-east-04.cleardb.com",
                            user="b5ace312629951",
                            passwd="af1b46b6",
                            database="heroku_2755bac09e746fb")
    createTable1dbCur=createTable1dbCon.cursor()
    if Request.method == 'POST':
        createTable1dbCur.execute("SELECT room_id FROM rooms")
        rooms_available=createTable1dbCur.fetchall()
        createTable1dbCon.close()
        print(rooms_available)
        if str(Request.form['roomid'])+',' in str(rooms_available):
            return redirect(f"/room/{Request.form['roomid']}")
        else:
            return redirect("/")
    else:
        return redirect("/")

@app.route("/room/<GetRoom_id>",methods=['GET','POST'])
def join_room(GetRoom_id):
    createTable1dbCon=mysql.connector.connect(host="us-cdbr-east-04.cleardb.com",
                            user="b5ace312629951",
                            passwd="af1b46b6",
                            database="heroku_2755bac09e746fb")
    createTable1dbCur=createTable1dbCon.cursor()
    createTable1dbCur.execute("SELECT room_id FROM rooms")
    rooms_available=createTable1dbCur.fetchall()
    
    createTable1dbCon.close()
    if GetRoom_id in str(rooms_available)+',':
        return GetRoom_id
    else:
        return redirect("/")
    
@app.errorhandler(404)
def error_404(e):
    return render_template("404.html")
#==__name__=====================
if __name__ == '__main__':
    app.run(debug=True)