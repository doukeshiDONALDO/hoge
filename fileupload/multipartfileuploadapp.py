# -*- coding: utf-8 -*-
from flask import Flask, request, make_response, jsonify
import os
import werkzeug
from datetime import datetime
import sqlite3
import subprocess
import sys
import signal

db_name = 'filename.db'

# flask
app = Flask(__name__)

# limit upload file size : 1MB
#app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

# ex) set UPLOAD_DIR_PATH=C:/tmp/flaskUploadDir
UPLOAD_DIR = '/home/niki/hoge/fileupload/static'

# rest api : request.files with multipart/form-data
# <form action="/data/upload" method="post" enctype="multipart/form-data">
#   <input type="file" name="uploadFile"/>
#   <input type="submit" value="submit"/>
# </form>
@app.route('/data/upload', methods=['POST'])
def upload_multipart():

    if 'uploadFile' not in request.files:
        make_response(jsonify({'result':'uploadFile is required.'}))

    file = request.files['uploadFile']
    fileName = file.filename
    if '' == fileName:
        make_response(jsonify({'result':'filename must not empty.'}))

    saveFileName =  werkzeug.utils.secure_filename(fileName)
    # "home_pi_PythonScripts_Incubator_Cameras_piCamera000000000000.png" to "piCamera000000000000.png" 
    saveName = saveFileName.split(b'_')
    file.save(os.path.join(UPLOAD_DIR, saveName[5]))

    # c3 = (id, camera1, camera2, ndvi) 
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    sql = "select * from ndvi order by id desc limit 1"
    c2 = c.execute(sql)
    c3 = c2.fetchone()
    conn.commit()
    conn.close()
    clist = list(c3)


    # insert new record
#    if c3[3] is not None:
    if clist[1] is not None and clist[2] is not None:

        # piNoir00000000000000.png
        if 'Noir' in saveName[5]:
            sql = "insert into ndvi (camera1) values ('{}')".format(saveName[5])

        # piCamera000000000000.png
        else: 
            sql = "insert into ndvi (camera2) values ('{}')".format(saveName[5])

        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        print(sql)
        c.execute(sql)
        conn.commit()
        conn.close()

    # update record
    else:

        # piNoir00000000000000.png
        if 'Noir' in saveName[5]:
            clist[1] = saveName[5]
            sql = "update ndvi set camera1 = '{}' where id = '{}'".format(clist[1],clist[0])

        # piCamera000000000000.png
        else: 
            clist[2] = saveName[5]
            sql = "update ndvi set camera2 = '{}' where id = '{}'".format(clist[2],clist[0])

        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        print(sql)
        c.execute(sql)
        conn.commit()
        conn.close()

        # TODO: 2filenames send outputNDVI.py

        cmd = "python /home/niki/hoge/imaging/outputNDVIarea.py /home/niki/hoge/fileupload/static/{} /home/niki/hoge/fileupload/static/{}".format(clist[1],clist[2])
        subprocess.call(cmd.split())
        print(cmd)
    return make_response(jsonify({'result':'upload OK.'}))

@app.errorhandler(werkzeug.exceptions.RequestEntityTooLarge)
def handle_over_max_file_size(error):
    print("werkzeug.exceptions.RequestEntityTooLarge")
    return 'result : file size is overed.'

def handler(singnal,frame):
    sys.exit(0)

# main
if __name__ == "__main__":
    print(app.url_map)
    app.run(host='0.0.0.0', port=3000,threaded=True)


    signal.signal(signal.SIGINT,handler)
    signal.pause()

