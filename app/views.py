# -*- coding: utf-8 -*-

import psycopg2
import psycopg2.extras
from flask import g, request, render_template, session
from app import app
#from flask_sqlalchemy import SQLAlchemy
#from flask.ext.uploads import UploadSet, configure_uploads, IMAGES
#from werkzeug.utils import secure_filename
from datetime import date
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/static/images'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Connect database
# g = http://flask.pocoo.org/docs/1.0/api/#flask.g
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

conn = psycopg2.connect("dbname=instagram user=postgres password=flasknao host=127.0.0.1")
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

now = date.now()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if (request.method == 'POST'):
        account = request.form['account']
        username = request.form['username']
        password = request.form['password']
        cur.execute("INSERT INTO client(account, username, password) VALUES ('%s', '%s', '%s')" %(account, username, password))
        conn.commit()
        return render_template('login.html')
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if (request.method == 'POST'):
        cur.execute("SELECT * FROM client;")
        accounts = cur.fetchall()
        username = request.form['username']
        password = request.form['password']
        for x in accounts:
            if x['username'] == username and x['password'] == password:
                session['name'] = username
                return render_template('feed.html')
        return render_template('login.html', error='usuario nao existe')
    return render_template('login.html')

@app.route('/comment', methods=['GET', 'POST'])
def comment():
    if (request.method == 'POST'):
        cur.execute("INSERT INTO comment(id, date_c, comment, id_photo) VALUES (id, now, comment, id_photo)")
        conn.commit()
    return render_template('home.html')
'''
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['inputFile']
    return file.filename

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        return filename
    return render_template('upload.html')
'''
@app.route('/post', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        session[''] = request.form['']
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filename)
            cur.execute("INSERT INTO photo(description, way) VALUES ('%s', '%s')" %(description, filename))
            conn.commit()
            return redirect(url_for('uploaded_file', filename=filename))
