# -*- coding: utf-8 -*-
from flask import Flask, request, make_response, jsonify
import os
import werkzeug
from datetime import datetime

# flask
app = Flask(__name__)

# ★ポイント1
# limit upload file size : 1MB
#app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

# ★ポイント2
# ex) set UPLOAD_DIR_PATH=C:/tmp/flaskUploadDir
UPLOAD_DIR = '/home/niki/hoge/fileupload/static'

# rest api : request.files with multipart/form-data
# <form action="/data/upload" method="post" enctype="multipart/form-data">
#   <input type="file" name="uploadFile"/>
#   <input type="submit" value="submit"/>
# </form>
@app.route('/data/upload', methods=['POST'])
def upload_multipart():

    # ★ポイント3
    if 'uploadFile' not in request.files:
        make_response(jsonify({'result':'uploadFile is required.'}))

    file = request.files['uploadFile']
    fileName = file.filename
    if '' == fileName:
        make_response(jsonify({'result':'filename must not empty.'}))

    # ★ポイント4
    saveFileName =  werkzeug.utils.secure_filename(fileName)
    file.save(os.path.join(UPLOAD_DIR, saveFileName))
    return make_response(jsonify({'result':'upload OK.'}))

# ★ポイント5
@app.errorhandler(werkzeug.exceptions.RequestEntityTooLarge)
def handle_over_max_file_size(error):
    print("werkzeug.exceptions.RequestEntityTooLarge")
    return 'result : file size is overed.'

# main
if __name__ == "__main__":
    print app.url_map
    app.run(host='localhost', port=3000)
