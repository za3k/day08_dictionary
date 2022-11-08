#!/bin/python3
import flask, flask_login
from flask_login import current_user
import json
from datetime import datetime
from base import app,load_info,ajax,DBDict

# -- Info for every Hack-A-Day project --
load_info({
    "project_name": "Hack-A-Dictionary",
    "source_url": "https://github.com/za3k/day08_dictionary",
    "subdir": "/hackaday/dictionary"
})

# -- Routes specific to this Hack-A-Day project --
histories = DBDict("history")
with open("dictionary.json") as f:
    webster = json.load(f)

def get_picture():
    pass

@app.route("/")
def index():
    return flask.render_template('index.html')

@app.route("/w")
def word_redir():
    word = flask.request.args.get("word")
    return flask.redirect(flask.url_for("word", word=word))

@app.route("/history")
@flask_login.login_required
def history():
    history = [(word, word in webster) for word in histories.get(current_user.id, [])]
    return flask.render_template("history.html", history=history)

@app.route("/<word>")
def word(word):
    definition = webster.get(word)
    if current_user.is_authenticated:
        history = histories.get(current_user.id, [])
        history.append(word)
        histories[current_user.id] = history
    print(word, definition)
    return flask.render_template("word.html", word=word, definition=definition)
