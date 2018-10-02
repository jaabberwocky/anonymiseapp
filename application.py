from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_uploads import UploadSet, configure_uploads, DATA
import pandas as pd
import json
import time

# instantiate app objects
application = Flask(__name__)
bootstrap = Bootstrap(application)

# configure destination folder
# NOTE TESTING!
configurations = json.loads(open("config.json", "r").read())
application.config['UPLOADED_DATAFILES_DEST'] = configurations["SAVE_FILE_DESTINATION"]

# declare files for upload set
# DATA allows for only data extensions (".csv" etc)
datafiles = UploadSet('datafiles', DATA)
configure_uploads(application, datafiles)

@application.route('/upload', methods=['POST','GET'])
def files_upload():
	if request.method == 'POST':
		tic = time.time()
		uploaded_file = request.files['datafile']
		filename = datafiles.save(uploaded_file)
		uploaded_file.seek(0,2)
		file_size = uploaded_file.tell()
		return "%s with filesize of %.2fmb was uploaded in %.2fseconds" % (filename, file_size / 1024 / 1024, time.time() - tic)
	return render_template('index.html')

if __name__ == "__main__":
	application.run(debug=True)