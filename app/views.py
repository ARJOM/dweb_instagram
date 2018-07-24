# -*- coding: utf-8 -*-

import psycopg2
import psycopg2.extras
from flask import g, request, render_template, session
from app import app
from datetime import date
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/static/images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

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
        return login()
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
                session['username'] = request.form['username']
                return render_template('feed_aut.html')
        return render_template('login.html', error='usuario nao existe')
    return render_template('login.html')


@app.route('/', methods=['GET', 'POST'])
def comment():
    if (request.method == 'POST'):
        now = date.today()
        comment = request.form['comment']
        cur.execute("INSERT INTO comment(date_c, comment, id_photo) VALUES (now, comment, id_photo)")
        conn.commit()
    if 'username' in session:
        return render_template('feed_aut.html')
    return render_template('feed_naut.html')

#@app.route('/upload', methods=['POST'])
#def upload():
#    file = request.files['inputFile']
#    return file.filename


#@app.route('/upload', methods=['GET', 'POST'])
#def upload():
#    if request.method == 'POST' and 'photo' in request.files:
#        filename = photos.save(request.files['photo'])
#        return filename
#    return render_template('upload.html')

@app.route('/post', methods=['GET', 'POST'])
def upload_file():
    now = date.today()
    if request.method == 'POST':

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
            description = request.form['description']
            file.save(filename)
            cur.execute("INSERT INTO photo(date_p, description, client_p, way) VALUES ('%s', '%s', '%s', '%s')" %(now, description, username, filename))
            conn.commit()
            return redirect(url_for('uploaded_file', filename=filename))

@app.route('/', methods=['GET', 'POST'])
def like():
    now = date.today()
    if request.method == 'POST':
        cur.execute("INSERT INTO lik(u_user, photo) VALUES ('%s', '%s')" %(u_user, photo))
        conn.commit()
