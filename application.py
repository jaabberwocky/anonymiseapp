from flask import Flask, render_template, request, flash, url_for, redirect, send_file
from flask_bootstrap import Bootstrap
from flask_uploads import UploadSet, configure_uploads, DATA
import pandas as pd
import json
import time
import hashlib
import os
import uuid

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

#### FUNCTIONS ####

# hashing function to be applied to pandas dataframe
# salt is prepended to string
def hashthis(string, salt):
	hash_string = salt+string
	sha = hashlib.sha256(hash_string.encode()).hexdigest()
	return sha

# pandas processing function to anonymise ids column
def anonymise(filename, column, salt=""):
	df = pd.read_csv(os.path.join('data', filename))

	# process salt
	df[column] = df[column].apply(hashthis)
	
	# save CSV with UUID to ensure no collision
	completed_filename = uuid.uuid4()
	df.to_csv('data/%s.csv' % completed_filename, index=False)

	# return this so it can be passed as URL
	return completed_filename

#### ROUTES ####

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

		# process file
		completed_filename = anonymise(filename, salt=salt)

		# send flash to index
		flash("%s with filesize of %.2fmb was processed in %.2fseconds.  Salt: %s" % (filename, file_size / 1024 / 1024, time.time() - tic, salt), "msg")
		flash("%s" % completed_filename, "completed_filename")
		return redirect(url_for('index'))
	return render_template('upload.html')

@application.route('/downloadfile_<completed_filename>')
def download_file(completed_filename):
	
	return send_file('data/%s.csv' % completed_filename, 
		attachment_filename=completed_filename + '.csv', 
		as_attachment=True)

if __name__ == "__main__":
	application.run(debug=True)