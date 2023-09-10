from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, SelectField)
from wtforms.validators import DataRequired, URL

app = Flask(__name__)
Bootstrap5(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/page")
def page():
    return render_template("page.html")

if __name__ == '__main__':
    app.run(debug=True)
