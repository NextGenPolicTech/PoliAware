import sys

from flask import Flask, render_template, app
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, SelectField)
from wtforms.validators import DataRequired, URL
from flask import request
from flask import jsonify
from ipstack import GeoLookup



app = Flask(__name__)
Bootstrap5(app)

geo_lookup = GeoLookup("d769f3b499163fe5c76326aa2f29469b")

@app.route("/",methods=['GET', 'POST'])
def home():
    ip_addr = request.environ['REMOTE_ADDR']
    print(geo_lookup.get_location(ip_addr),file=sys.stderr)
    return render_template("index.html")
@app.route("/", )
def get_my_ip():
    ip = request.remote_addr
    print(ip, file=sys.stderr)
    print(request.environ['REMOTE_ADDR'], file=sys.stderr)
    app.logger.info('testing info log')

@app.route("/page")
def page():
    return render_template("page.html")

if __name__ == '__main__':
    app.run(debug=True)
