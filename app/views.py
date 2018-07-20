# -*- coding: utf-8 -*-

import psycopg2
import psycopg2.extras
from flask import g, request, render_template
from app import app

'''lista_filmes = ['Star Wars', 'Toy Story', 'Taxi Driver']'''

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
                return render_template('signup.html')
            else:
                pass
    return render_template('login.html')
'''
    if request.method == 'GET':
        return render_template('login.html')
    else:
        if request.form['user'] == 'gustavo':
            return render_template('login.html', error='usuario nao existe')
        else:
            print( request.form['user'], request.form['password'] )
            return redirect(url_for('filmes'))
'''
