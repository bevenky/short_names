from flask import Flask
from flask import render_template, url_for, redirect
from flask import request

import sqlite3
from flask import g

import json
import string

app = Flask(__name__)
app.debug = True

domains = {
            "a" : ["aa.com", "aka.com", "aa.com", "aka.com", "aa.com", "aka.com"],
            "b" : ["ba.com", "bka.com"],
}

char_set = map(chr, range(97, 123))

secret_key = string.ascii_uppercase


DATABASE = 'urls.db'

def connect_db():
    return sqlite3.connect(DATABASE)

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


@app.route("/")
def index():
    return show_domains("a")


@app.route("/<alphabet>/")
def show_domains(alphabet):
    print "comes here"
    global domains
    if not alphabet:
        alphabet = "a"
    filtered_domains = []
    if alphabet in domains:
        filtered_domains = domains[alphabet]
    return render_template('index.html', domains=filtered_domains, char_set=char_set, current=alphabet)


@app.route("/hard_to_guess_url/setdata/", methods=['POST'])
def set_data():
    global secret_key
    global domains
    if 'data' in request.form and 'auth' in request.form:
        data = request.form['data']
        auth = request.form['auth']
        if auth == secret_key:
            domains = json.loads(data)
            return "OK"
    
    return "ERR"


if __name__ == "__main__":
    app.run(host='0.0.0.0')