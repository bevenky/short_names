from flask import Flask
from flask import render_template, url_for, redirect
from flask import request

import sqlite3
from flask import g

import json
import string
from collections import defaultdict


app = Flask(__name__)
app.debug = True

domains = defaultdict(list)

char_set = map(chr, range(97, 123))

secret_key = string.ascii_uppercase


@app.route("/")
def index():
    global domains
    domains = defaultdict(list)
    
    temp_file = open("Urls.txt", "r")
    for url in sorted(temp_file, key = str.lower):
        domains[url[:1]].append(url)
    temp_file.close()

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
    if 'auth' in request.form:
        auth = request.form['auth']
        if auth == secret_key:
            domains = defaultdict(list)
            temp_file = open("Urls.txt", "r")
            for url in sorted(temp_file, key = str.lower):
                domains[url[:1]].append(url)

            temp_file.close()
            return "OK"
    return "ERR"


if __name__ == "__main__":
    app.run(host='0.0.0.0')