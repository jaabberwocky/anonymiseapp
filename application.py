from flask import Flask, render_template, request, flash, url_for, redirect
from flask_bootstrap import Bootstrap
from flask_uploads import UploadSet, configure_uploads, DATA
import pandas as pd
import json
import time

# instantiate app objects
application = Flask(__name__)
bootstrap = Bootstrap(application)


# load configurations json (kept secret)
configurations = json.loads(open("config.json", "r").read())

# set file destination
application.config['UPLOADED_DATAFILES_DEST'] = configurations["SAVE_FILE_DESTINATION"]

# declare files for upload set
# DATA allows for only data extensions (".csv" etc)
datafiles = UploadSet('datafiles', DATA)
configure_uploads(application, datafiles)

# set secret
application.secret_key = configurations['SECRET_KEY']

@application.route('/')
def index():
	return render_template('index.html')

@application.route('/upload', methods=['POST','GET'])
def files_upload():
	if request.method == 'POST':
		# start clock ticking on upload
		tic = time.time()

		# set file
		uploaded_file = request.files['datafile']

		# save file to UploadSet
		filename = datafiles.save(uploaded_file)

		# tell filesize without loading into memory
		uploaded_file.seek(0,2)
		file_size = uploaded_file.tell()

		# salt
		salt = request.form['salt']

		# send flash to index
		flash("%s with filesize of %.2fmb was uploaded in %.2fseconds.  Salt: %s" % (filename, file_size / 1024 / 1024, time.time() - tic, salt))
		return redirect(url_for('index'))
	return render_template('upload.html')

# pandas processing file

if __name__ == "__main__":
	application.run(debug=True)