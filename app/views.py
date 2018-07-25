# -*- coding: utf-8 -*-

import psycopg2
import psycopg2.extras
from flask import g, request, redirect, render_template, session
from app import app
from datetime import date
import base64
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
    session['username'] = None
    return render_template('home.html')

@app.route('/profile/<path:username>', methods=['GET', 'POST'])
def home(username):
    user = username
    cur.execute("SELECT id, date_p, description, client_p, way FROM photo WHERE client_p = '%s'" %(user))
    posts = cur.fetchall()
    cur.execute("SELECT follower FROM followers WHERE followed = '%s'" %(user))
    foll = cur.fetchall()
    nfoll = len(foll)
    cur.execute("SELECT followed FROM followers WHERE follower = '%s'" %(user))
    full = cur.fetchall()
    nfull = len(full)
    for post in posts:
        cur.execute("SELECT COUNT(*) FROM lik WHERE photo = '%s'" % post[0])
        likes = cur.fetchone()
        post.append(likes[0])
        cur.execute("SELECT * FROM comment WHERE id_photo = '%s'" % post[0])
        comments = cur.fetchall()
        post.append(comments)
    return render_template('profile.html', posts=posts, foll=foll, seguidores=nfoll, seguindo=nfull, user = username)

@app.route('/feed', methods=['GET'])
def feed():
    username = session['username']
    cur.execute("SELECT id, date_p, description, client_p, way FROM photo WHERE client_p <> '%s'" %(username))
    posts = cur.fetchall()
    for post in posts:
        cur.execute("SELECT COUNT(*) FROM lik WHERE photo = '%s'" % post[0])
        likes = cur.fetchone()
        post.append(likes[0])
        cur.execute("SELECT * FROM comment WHERE id_photo = '%s'" % post[0])
        comments = cur.fetchall()
        post.append(comments)
    return render_template('feed_aut.html', username=session['username'], posts=posts)

@app.route('/logout', methods=['GET'])
def logout():
    session['username'] = None
    return redirect('feed')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if (request.method == 'POST'):
        account = request.form['account']
        username = request.form['username']
        password = request.form['password']
        cur.execute("INSERT INTO client(account, username, password) VALUES ('%s', '%s', '%s')" %(account, username, password))
        conn.commit()
        return redirect('login')
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if (request.method == 'POST'):
        cur.execute("SELECT * FROM client;")
        accounts = cur.fetchall()
        #username = session['username']
        username = request.form['username']
        password = request.form['password']
        for x in accounts:
            if x['username'] == username and x['password'] == password:
                session['username'] = request.form['username']
                return redirect('feed')
        return render_template('login.html', error='usuario nao existe')
    return render_template('login.html')


@app.route('/comment', methods=['GET', 'POST'])
def comment():
    if (request.method == 'POST'):
        now = date.today()
        id_photo = request.form['idPhoto']
        comment = request.form['comment']
        username = session['username']
        cur.execute("INSERT INTO comment(date_c, comment, id_photo, username) VALUES ('%s', '%s', '%s', '%s')" %(now, comment, id_photo, username))
        conn.commit()
    if 'username' in session:
        return redirect('feed')
    return render_template('feed_aut.html')

@app.route('/post', methods=['GET', 'POST'])
def upload_file():
    now = date.today()
    if request.method == 'POST':
        file = request.files['file']
        if file == None:
            return redirect('feed')
        photo =  base64.b64encode(file.read()).decode('utf-8').replace('\n', '')
        username = session['username']
        description = request.form['description']
        cur.execute("INSERT INTO photo(date_p, description, client_p, way) VALUES ('%s', '%s', '%s', '%s')" %(now, description, username, photo))
        conn.commit()
        return redirect('feed')

@app.route('/like/<idPhoto>', methods=['GET', 'POST'])
def like(idPhoto):
    now = date.today()
    if request.method == 'GET':
        id_photo = idPhoto
        username = session['username']
        cur.execute("SELECT COUNT(*) FROM lik WHERE photo = '%s' and u_user = '%s'" %(id_photo, username))
        quantidadeLikes = cur.fetchone()
        if quantidadeLikes[0] == 1 :
            return redirect('feed')
        else :
            cur.execute("INSERT INTO lik(u_user, photo) VALUES ('%s', '%s')" %(session['username'], id_photo))
            conn.commit()
        return redirect('feed')
