"""
Created on Wed Jan  9 11:59:32 2019

@author: Krutika Lodaya
"""
from flask import Flask, render_template, request, Response
from flask_cors import CORS, cross_origin
from os.path import join as pjoin
from werkzeug.utils import secure_filename

APP = Flask(__name__)
CORS(APP)

@APP.route('/',methods=['GET'])
@cross_origin()
def upload_file():
   return render_template('file_upload.html')

@APP.route('/uploader',methods=['POST'])
@cross_origin()
def file_upload():
    f = request.files['photo']
    f.save()
    f.save(secure_filename(f.filename))
    return 'file uploaded successfully'

if __name__ == '__main__':
    APP.run(host="0.0.0.0",debug=True, port=8080)