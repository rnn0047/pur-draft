# flask app using s3 to store files
import json
import os
import logging
import uuid
from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from werkzeug import secure_filename
from tools.config import UPLOAD_FOLDER
from tools.storage_utils import StorageUtils
from xform.tranImage import XForm
""" Notes
    1. TODO - big brother Lambda function to delete all obj older than 12 hours
    2. UPLOAD_FOLDER is temp folder for all interim processing
"""

FILENAME_KEYS = ['.photo', '.style']
ALLOWED_EXTENSIONS = set(['png', 'ico', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
Bootstrap(app)
#app.jinja_env.filters['file_type'] = file_type
su = StorageUtils()
@app.route('/')
def index():
    styles = ['tony', 'tigris', 'stripes']
    return render_template('index.html', styles = styles)

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/submit", methods=['POST'])
def postFiles():
    if 'styleFile' not in request.files and 'photoFile' not in request.files:
        return "No file key's present for upload in request.files"
    styleID = 'tony'
    photo = request.files['photoFile']
    userID = None

    if (styleID != None ) and \
       (photo.filename != None and len(photo.filename) > 2) :
        userID = uuid.uuid1().hex
        if allowed_file(photo.filename):
            filename    = secure_filename(photo.filename)
            fileWPath   = os.path.join(UPLOAD_FOLDER, filename)
            photo.save(fileWPath)
            objName     = userID + ".photo"
            status, msg = su.fileUpload(fileWPath, objName)
            if status == False:
                return("failed uploading file to S3")
            logging.info("fileUpload - {}".format(msg))
            os.remove(fileWPath)
        else:
            logging.info("File {} not acceptable".format(photo.filename))
    else:
        return redirect("/")

    messages = json.dumps({"userID": userID, "styleID": styleID})
    return redirect(url_for('.transformPhoto', messages = messages))

@app.route("/xForm")
def transformPhoto():
    messages = request.args['messages']
    messages = json.loads(messages)
    #print("messages = {}".format(messages))
    userID = messages['userID']
    styleID = messages['styleID']

    remoteFile = userID + ".photo"
    localFile = os.path.join(UPLOAD_FOLDER, remoteFile)
    status, msg = su.downloadFile(remoteFile, localFile)
    if status == False:
        logging.error("Error in fileDownload {}".format(msg))
        return "Couldn't download user {} file from S3".format(userID)
    #For now lets keep the style data with the deployment
    xf = XForm()
    status, msg = xf.process_image(localFile, styleID, True)
    if status == False:
        return "Failed xforming the image, Reason: {}".format(msg)
    #outphoto should be saved into S3 as userID + outphoto
    #remove local file after rendering ??
    messages = json.dumps({"userID": userID, \
                            "styleID": styleID })
    return redirect(url_for('.displayXForm', messages = messages))

@app.route("/xFormPhoto")
def displayXForm():
    messages = request.args['messages']
    messages = json.loads(messages)
    userID = messages['userID']
    styleID = messages['styleID']
    #not sure why this gives error
    infile = os.path.join(UPLOAD_FOLDER, userID + ".photo")
    outfile = os.path.join(UPLOAD_FOLDER, userID + "_{}_xform.jpg".format(styleID))
    print("inf = {}, out = {}".format(infile, outfile))
    return render_template('xform.html', infile = infile, outfile = outfile)

@app.route("/listFiles")
def listFiles():
    """
    Utility function to check content of the S3
    """
    my_bucket   = su._getBucketObj()
    summaries   = su.listFiles()
    return render_template('listFiles.html', my_bucket=my_bucket,
            files=summaries)

if __name__ == "__main__":
    app.run()

