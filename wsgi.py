#==Imports==
# import threading
from flask import Flask, render_template, redirect, request, url_for
import mysql.connector
import random
from flask_socketio import SocketIO, emit, join_room, leave_room

#====
app = Flask(__name__,template_folder='templates')
socketio=SocketIO(app)

#==DB CONFIG=======================
#======LOCALHOST============
global db_host, db_user, db_password, db_database
# db_host="localhost"
# db_user="root"
# db_database="rmcs"
# db_password="akg2504"
# db_port="8080"
#======CLOUD==========
db_host="us-cdbr-east-04.cleardb.com"
db_user="b5ace312629951"
db_database="heroku_2755bac09e746fb"
db_password="af1b46b6"
db_port="3306"
#================================================
@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/new', methods=['POST','GET'])
def new():
    room_id=random.randint(1111,9999)
    createTable1dbCon=mysql.connector.connect(host=db_host,
                            user=db_user,
                            passwd=db_password,
                            database=db_database,
                            port=db_port)
    createTable1dbCur=createTable1dbCon.cursor()
    
    createTable1dbCur.execute("CREATE TABLE IF NOT EXISTS rooms(room_id INTEGER, members INTEGER,username1 VARCHAR(100),username2 VARCHAR(100),username3 VARCHAR(100),username4 VARCHAR(100), PRIMARY KEY(room_id))")      
    createTable1dbCon.commit()
    
    createTable1dbCur.execute("INSERT INTO rooms (room_id, members) VALUES (%s,%s)", (room_id,0))      
    createTable1dbCon.commit()

    createTable1dbCon.close()
    username=request.args.get('username')
    return redirect(url_for('connect_room',username=username,GetRoom_id=room_id))

@app.route("/room", methods=['GET'])
def sendToRoom():
    username=request.args.get('username')
    roomid=request.args.get('roomid')
    if username and roomid:
        return redirect(url_for('connect_room',username=username,GetRoom_id=roomid))
    else:
        return error_404("ON /ROOM")

    # if request.method == 'POST':
    # else:
    #     return error_404("/room")

@app.route("/room/<GetRoom_id>",methods=['GET','POST'])
def connect_room(GetRoom_id):
    username=request.args.get('username')
    if username:
        createTable1dbCon=mysql.connector.connect(host=db_host,
                            user=db_user,
                            passwd=db_password,
                            database=db_database,
                            port=db_port)
        createTable1dbCur=createTable1dbCon.cursor()

        createTable1dbCur.execute("CREATE TABLE IF NOT EXISTS rooms(room_id INTEGER, members INTEGER,username1 VARCHAR(100),username2 VARCHAR(100),username3 VARCHAR(100),username4 VARCHAR(100), PRIMARY KEY(room_id))")      
        createTable1dbCon.commit()
        
        createTable1dbCur.execute(f"SELECT * FROM rooms where room_id={GetRoom_id}")
        rooms_available=createTable1dbCur.fetchall()
        
        if len(rooms_available) != 0:
            room_data=rooms_available[0]
            print(room_data[1])
            print(type(room_data[1]))
            if room_data[1]==0:
                createTable1dbCur.execute(f"UPDATE rooms SET members={room_data[1]+1}, username1='{username}' WHERE room_id={room_data[0]}")
                createTable1dbCon.commit()
                data={'roomid':room_data[0], 'members':room_data[1]+1, 'username1':username, 'username2':room_data[3], 'username3':room_data[4], 'username4':room_data[5] }
                createTable1dbCon.close()
            elif room_data[1]==1:
                createTable1dbCur.execute(f"UPDATE rooms SET members={room_data[1]+1}, username2='{username}' WHERE room_id={room_data[0]}")
                createTable1dbCon.commit()
                data={'roomid':room_data[0], 'members':room_data[1]+1, 'username1':room_data[2], 'username2':username, 'username3':room_data[4], 'username4':room_data[5] }
                createTable1dbCon.close()
            elif room_data[1]==2:
                createTable1dbCur.execute(f"UPDATE rooms SET members={room_data[1]+1}, username3='{username}' WHERE room_id={room_data[0]}")
                createTable1dbCon.commit()
                data={'roomid':room_data[0], 'members':room_data[1]+1, 'username1':room_data[2], 'username2':room_data[3], 'username3':username, 'username4':room_data[5] }
                createTable1dbCon.close()
            elif room_data[1]==3:
                createTable1dbCur.execute(f"UPDATE rooms SET members={room_data[1]+1}, username4='{username}' WHERE room_id={room_data[0]}")
                createTable1dbCon.commit()
                data={'roomid':room_data[0], 'members':room_data[1]+1, 'username1':room_data[2], 'username2':room_data[3], 'username3':room_data[4], 'username4':username }
                createTable1dbCon.close()
            else:
                createTable1dbCon.close()
                return redirect("/")
            return render_template("game.html",data=data)
        else:
            return redirect("/")
    

@socketio.on('join')
def on_join(data):
    print(data['roomid'])
    join_room(str(data['roomid']))
    emit('joined',data, to=str(data['roomid']), broadcast=True)
    

@app.errorhandler(404)
def error_404(e):
    return render_template("404.html")
#==__name__=====================
if __name__ == '__main__':
    app.run()
