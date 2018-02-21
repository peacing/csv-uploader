from flask import Flask, render_template, session, redirect, url_for, flash, request, send_from_directory, g
from werkzeug.utils import secure_filename
import os, csv
import io
import sqlite3

UPLOAD_FOLDER = '/tmp'
DATABASE = 'csv.db'
ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'super secret key'

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    g.db = connect_db()
    if request.method == 'POST':
    # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            try:
                filename = secure_filename(file.filename)
                #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
                csv_input = csv.reader(stream)
           
                for row in csv_input:
                    g.db.execute('INSERT INTO data VALUES (?,?,?,?,?,?,?,?,?,?,?)', row)
                    g.db.commit()
                g.db.close()
                flash('File uploaded successfully!')
                return render_template('base.html')
            except Exception:
                flash('Error saving data, try again')
                return render_template('base.html')

    return render_template('base.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
