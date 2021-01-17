# import compare_face_cloud
from flask import Flask, request, redirect, session, url_for, Response, json, render_template, send_from_directory
from werkzeug.utils import secure_filename
from flask.json import jsonify
from pymongo import MongoClient
from flask_cors import CORS
from google.cloud import datastore
from google.cloud import vision
from google.cloud import storage
import os
import recognizerimage
# import faceutils


with open('credentials.json', 'r') as f:
    creds = json.load(f)

mongostr = creds["mongostr"]
client = MongoClient(mongostr)

db = client["remind"]


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config.from_object(__name__)
CORS(app)



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



def uploadtogcp(filename):
    # Explicitly use service account credentials by specifying the private key
    # file.
    storage_client = storage.Client.from_service_account_json('gc.json')

    # Make an authenticated API request
    ##buckets = list(storage_client.list_buckets())
    ##print(buckets)

    bucketname = "hackybucket"
    # filename = sys.argv[2]


    bucket = storage_client.get_bucket(bucketname)

    destination_blob_name = "current.jpg"
    source_file_name = filename

    blob = bucket.blob(destination_blob_name)
    blob.cache_control = "no-cache"

    blob.upload_from_filename(source_file_name)
    blob.make_public()
    blob.cache_control = "no-cache"

    print('File {} uploaded to {}.'.format(source_file_name, destination_blob_name))


@app.route("/file_upload", methods=["POST"])
def fileupload():

    if 'file' not in request.files:
          return "No file part"
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
      return "No selected file"
    if file and allowed_file(file.filename):
        # UPLOAD_FOLDER = "./uploads"
        UPLOAD_FOLDER = "uploads"
  
        filename = secure_filename(file.filename)
        # file.save(os.path.join(UPLOAD_FOLDER, filename))
        file.save(filename)
        # uploadtogcp(os.path.join(UPLOAD_FOLDER, filename))
        uploadtogcp(os.path.join(filename))
        return 'https://storage.googleapis.com/hackybucket/current.jpg' 
    
    return 'file not uploaded successfully', 400

@app.route("/controller", methods=["POST"])
def controller():

    if 'file' not in request.files:
          return "No file part"
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
      return "No selected file"
    if file and allowed_file(file.filename):
        # UPLOAD_FOLDER = "./uploads"
        UPLOAD_FOLDER = "uploads"
  
        filename = secure_filename(file.filename)
        # file.save(os.path.join(UPLOAD_FOLDER, filename))
        file.save(filename)
        fin = recognizerimage.getgesture(filename)

        ser = serial.Serial(portname, baud)

        print ("connected to: " + ser.portstr)
        reading = {}
        ts1 = int(time.time())

        if fin == 0:
            ##everything off
            ser.writeLine("0")
            ser.writeLine("0")
            
        if fin == 1:
            ser.writeLine("0")
            ser.writeLine("1")
            ##light on

        if fin ==2: 
            ##fan on light on
            ser.writeLine("50")
            ser.writeLine("1")
        
        if fin ==3: 
            ##fan on light off
            ser.writeLine("50")
            ser.writeLine("0")

        # uploadtogcp(os.path.join(UPLOAD_FOLDER, filename))
        # uploadtogcp(os.path.join(filename))
        return 'complete' 
    
    return 'file not uploaded successfully', 400





@app.route("/dummyJson", methods=['GET', 'POST'])
def dummyJson():

    print(request)

    res = request.get_json()
    print (res)

    resraw = request.get_data()
    print (resraw)

##    args = request.args
##    form = request.form
##    values = request.values

##    print (args)
##    print (form)
##    print (values)

##    sres = request.form.to_dict()
 

    status = {}
    status["server"] = "up"
    status["message"] = "some random message here"
    status["request"] = res 

    statusjson = json.dumps(status)

    print(statusjson)

    js = "<html> <body>OK THIS WoRKS</body></html>"

    resp = Response(statusjson, status=200, mimetype='application/json')
    ##resp.headers['Link'] = 'http://google.com'

    return resp




@app.route("/dummy", methods=['GET', 'POST'])
def dummy():

    ##res = request.json

    js = "<html> <body>OK THIS WoRKS</body></html>"

    resp = Response(js, status=200, mimetype='text/html')
    ##resp.headers['Link'] = 'http://google.com'

    return resp

@app.route("/api", methods=["GET"])
def index():
    if request.method == "GET":
        return {"hello": "world"}
    else:
        return {"error": 400}


if __name__ == "__main__":
    # app.run(debug=True, host = 'localhost', port = 8003)
    app.run(debug=True, host = '45.79.199.42', port = 8003)
