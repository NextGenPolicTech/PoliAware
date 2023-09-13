from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, SelectField)
from wtforms.validators import DataRequired, URL

app = Flask(__name__)
Bootstrap5(app)
lol = "AIzaSyBs2A9UzhTy0WXwfGeUriHMJngaKkeBxc4"

# all Flask routes below
@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        print(request.form["Address"])
        return render_template("page.html")
    return render_template("page.html")

if __name__ == "__main__":
    app.run(debug=True)