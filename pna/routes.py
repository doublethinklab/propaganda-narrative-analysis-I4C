import flask
from flask import current_app as app


@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def index():
    return flask.redirect('/propaganda_analysis/')
