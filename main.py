from flask import Flask, render_template, app, redirect
from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, SelectField)
from wtforms.validators import DataRequired, URL
from flask import request
from flask import jsonify
from ipstack import GeoLookup
import smtplib as sm
import sys
import os


app = Flask(__name__)
geo_lookup = GeoLookup("d769f3b499163fe5c76326aa2f29469b")


@app.route("/", methods=['GET', 'POST'])
def home():
    ip_addr = request.environ['REMOTE_ADDR']
    print(geo_lookup.get_location(ip_addr),file=sys.stderr)
    return render_template("index.html")


"""@app.route("/", )
def get_my_ip():
    ip = request.remote_addr
    print(ip, file=sys.stderr)
    print(request.environ['REMOTE_ADDR'], file=sys.stderr)
    app.logger.info('testing info log')
"""

@app.route("/representative", methods=['GET', 'POST'])
def representative():
    if request.method == "POST":
        print(request.form["Address"])
        return redirect("/state")
    return render_template("representative.html")

@app.route("/state")
def state():
    return render_template("state.html")

@app.route("/news")
def news():
    return render_template("news.html")

@app.route("/contact")
def contact():
    if request.method == "GET":
        return render_template("contact.html")
    else:
        email = request.form["email"]
        name = request.form["name"]
        phone = request.form["phone"]
        message = request.form["message"]
        with sm.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user="josephle2005@gmail.com", password=os.environ["EMAIL_PASSWORD"])
            connection.sendmail(
                from_addr="josephle2005@gmail.com",
                to_addrs="umikikh@gmail.com",
                msg=f"Subject: New Website Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}")
        return render_template("contact.html")

if __name__ == '__main__':
    app.run(debug=True)
