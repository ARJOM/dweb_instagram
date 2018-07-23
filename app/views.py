# -*- coding: utf-8 -*-

import psycopg2
import psycopg2.extras
from flask import g, request, render_template
from app import app
'''from flask_sqlalchemy import SQLAlchemy'''
'''from flask.ext.uploads import UploadSet, configure_uploads, IMAGES'''
'''from werkzeug.utils import secure_filename'''
from datetime import datetime

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Connect database
# g = http://flask.pocoo.org/docs/1.0/api/#flask.g
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''
photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)
'''
conn = psycopg2.connect("dbname=instagram user=postgres password=flasknao host=127.0.0.1")
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

now = datetime.now()

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
