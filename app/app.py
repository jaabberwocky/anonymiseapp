from flask import Flask, render_template, request, flash, url_for, redirect, send_file, session, current_app
from flask import abort
from flask_bootstrap import Bootstrap
from flask_uploads import UploadSet, configure_uploads, DATA, patch_request_class
import pandas as pd
import json
import hashlib
import os
import uuid

# instantiate app objects
application = Flask(__name__)
Bootstrap(application)
application.config['BOOTSTRAP_SERVE_LOCAL'] = True

try:
    # load configurations json (kept secret)
    configurations = json.loads(open("config.json", "r").read())


except FileNotFoundError:
    configurations = {
        "SAVE_FILE_DESTINATION": "tmp",
        "SECRET_KEY": "askdfjasd"
    }
finally:
    # set file destination
    application.config['UPLOADED_DATAFILES_DEST'] = configurations["SAVE_FILE_DESTINATION"]
    # set secret
    application.secret_key = configurations['SECRET_KEY']

# declare files for upload set
# DATA allows for only data extensions (".csv" etc)
datafiles = UploadSet('datafiles', DATA)
configure_uploads(application, datafiles)

# set max upload size to 500MB
patch_request_class(application, 500 * 1024 * 1024)

#### FUNCTIONS ####

# hashing function to be applied to pandas dataframe
# salt is prepended to string


def hashthis(string, salt):
    hash_string = salt+string
    sha = hashlib.sha256(hash_string.encode()).hexdigest()
    return sha

# pandas processing function to anonymise ids column


def anonymise(filename, column, salt=""):
    df = pd.read_csv(os.path.join('tmp', filename))

    # process salt
    df[column] = df[column].apply(hashthis, salt=salt)

    # save CSV with UUID to ensure no collision
    completed_filename = uuid.uuid4()
    df.to_csv('tmp/%s.csv' % completed_filename, index=False)

    # return filename so it can be passed as URL
    return completed_filename

# pandas processing to return html view


def returnhtmlview(filename):
    df = pd.read_csv(os.path.join('tmp', filename), nrows=50)
    return df.head(25).to_html(
        bold_rows=True,
        max_rows=50,
        max_cols=25,
        classes=['table', 'table-striped']
    )

# pandas processing to return list of colnames


def returncolnames(filename):
    df = pd.read_csv(os.path.join('tmp', filename), nrows=20)
    return list(df.columns.values)

#### ROUTES ####


@application.route('/')
def index():
    return render_template('index.html')


@application.route('/upload', methods=['POST', 'GET'])
def files_upload():
    if request.method == 'POST':

        # set file
        uploaded_file = request.files['datafile']

        # save file to UploadSet
        filename = datafiles.save(uploaded_file)

        # save to SESSION var to be accessed later
        session['filename'] = filename

        return redirect(url_for("selectcolumn", _scheme="https", _external=True))
    return render_template('upload.html')


@application.route('/processfile')
def processfile():

    filename = session['filename']
    salt = request.args['salt']
    column = request.args['column']

    # process file
    completed_filename = anonymise(
        filename,
        salt=salt,
        column=column)

    session['completed_filename'] = completed_filename

    # now that file is processed, remove the original upload from server
    os.remove(os.path.join('tmp', filename))

    # send flash to index
    flash("%s is processed.  Salt: %s" % (filename, salt), "msg")
    flash("%s" % completed_filename, "completed_filename")
    return redirect(url_for('index', _scheme="https", _external=True))


@application.route('/downloadfile_<completed_filename>')
def download_file(completed_filename):
    # since we want to REMOVE the file after sending this request with send_file,
    # but this is not possible
    # the workaround is to save it in memory, then serve the response
    path = os.path.join("tmp", completed_filename+".csv")

    def generate():
        with open(path) as f:
            yield from f
        os.remove(path)

    r = current_app.response_class(generate(), mimetype="text/csv")
    r.headers.set('Content-Disposition', 'attachment', filename='data.csv')
    return r


@application.route('/selectcolumn', methods=["POST", "GET"])
def selectcolumn():
    if request.method == "POST":
        column = request.form['column']
        salt = request.form['salt']
        return redirect(url_for('processfile',
                                column=column,
                                salt=salt, _scheme="https", _external=True))

    filename = session['filename']

    colnames = returncolnames(filename)
    html_view = returnhtmlview(filename)

    return render_template('selectcolumn.html',
                           colnames=colnames,
                           html_view=html_view)


if __name__ == "__main__":
    application.run(host="0.0.0.0", debug=True)
