import os
import smtplib as sm

import google.generativeai as palm
import requests
from flask import Flask, render_template, redirect, request, session, url_for
from ipstack import GeoLookup
from bs4 import BeautifulSoup
import lxml

# Use "pip install google-generativeai" to install the google.generativeai module
# Set up the palm AI module
palmApiKey = "AIzaSyBJEkrAln6h9yp5pfZyr15uauLBMlIOheA"

palm.configure(api_key=palmApiKey)

defaults = {
  'model': 'models/text-bison-001',
  'temperature': 0.3,
  'candidate_count': 1,
  'top_k': 40,
  'top_p': 0.95,
  'max_output_tokens': 200,
  'stop_sequences': [],
  'safety_settings': [{"category":"HARM_CATEGORY_DEROGATORY","threshold":1},
                      {"category":"HARM_CATEGORY_TOXICITY","threshold":1},
                      {"category":"HARM_CATEGORY_VIOLENCE","threshold":2},
                      {"category":"HARM_CATEGORY_SEXUAL","threshold":2},
                      {"category":"HARM_CATEGORY_MEDICAL","threshold":2},
                      {"category":"HARM_CATEGORY_DANGEROUS","threshold":2}],
}


def get_prompt(name):
    return (f"Give 12 bullet points of  political facts about {name} and their political views. "
            f"Put each bullet on a new line, most of which contain their view on many different policies."
            f"Also include their political party and their political position. Example ways to display political"
            f"view: 'Support/oppose $15 minimum wage. Support/oppose to abortion rights."
            f" Support/oppose school vouchers. Support/oppose universal health care. Support/oppose the death penalty."
            f"Support/oppose 2020 election fraud claims. Support/oppose the legalization of marijuana. "
            f"Support/oppose U.S. support for Israel. Support/oppose U.S. aid to Ukraine. "
            f"Support/oppose the U.S. withdrawal from Afghanistan. Support/oppose the U.S. withdrawal from Syria. "
            f"Support/oppose the U.S. withdrawal from the Paris Climate Agreement.'")


# Code for Google Civic API
# Call based on division, for each state
ocd_url = "https://www.googleapis.com/civicinfo/v2/representatives/ocdId"
apiKey = "AIzaSyC8JpyYJoet115Awj-hWWwlf74axIbI_UY"
header = {"Accept": "application/json"}
ocd_param = {
    "ocdId": "",
    "levels": "",
    "roles": "",
    "key": apiKey
}
# Call based on address, for each district
url = "https://www.googleapis.com/civicinfo/v2/representatives/"
param = {
    "address": "",
    "includedOffices": True,
    "levels": "",
    "roles": "",
    "key": apiKey
}

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
geo_lookup = GeoLookup("d769f3b499163fe5c76326aa2f29469b")


@app.route("/", methods=['GET', 'POST'])
def home():
    ip_addr = request.environ['REMOTE_ADDR']
    return render_template("index.html")


@app.route("/representative", methods=['GET', 'POST'])
def representative():
    if request.method == "POST":
        param["levels"] = "country"
        param["roles"] = "legislatorLowerBody"
        param["address"] = request.form["Address"]
        response = requests.get(url, params=param, headers=header).json()
        rep = response["officials"][0]
        session["rep"] = rep
        return redirect(url_for("your_representative"))
    return render_template("representative.html")


@app.route("/state/<state>")
def state(state):
    ocd_param["ocdId"] = f"ocd-division/country:us/state:{state}"

    # Senators
    ocd_param["levels"] = "country"
    ocd_param["roles"] = "legislatorUpperBody"
    response = requests.get(ocd_url, params=ocd_param, headers=header).json()
    sen1 = response["officials"][0]
    completion = palm.generate_text(
        **defaults,
        prompt=get_prompt("Senator " + sen1["name"])
    )
    sen1_desc = completion.result.replace("*", "")

    sen2 = response["officials"][1]
    completion = palm.generate_text(
        **defaults,
        prompt=get_prompt("Senator " + sen2["name"])
    )
    sen2_desc = completion.result.replace("*", "")

    # Governor
    ocd_param["levels"] = "administrativeArea1"
    ocd_param["roles"] = "headOfGovernment"
    response = requests.get(ocd_url, params=ocd_param, headers=header).json()
    gov = response["officials"][0]
    completion = palm.generate_text(
        **defaults,
        prompt=get_prompt("Governor " + gov["name"])
    )
    gov_desc = completion.result.replace("*", "")

    # Attorney General
    ocd_param["roles"] = "governmentOfficer"
    response = requests.get(ocd_url, params=ocd_param, headers=header).json()
    i = 0
    for office in response["offices"]:
        if "Attorney General" in office["name"] or "Attorney-General" in office["name"]:
            i = office["officialIndices"][0]
            break
    ag = response["officials"][i]
    completion = palm.generate_text(
        **defaults,
        prompt=get_prompt("Attorney General " + ag["name"])
    )
    ag_desc = completion.result.replace("*", "")

    return render_template("state.html", senator1=sen1, senator2=sen2, governor=gov, attorneyGeneral=ag
                           , senator1_desc=sen1_desc, senator2_desc=sen2_desc, governor_desc=gov_desc,
                           attorneyGeneral_desc=ag_desc)


@app.route("/your-representative")
def your_representative():
    rep = session.get('rep', None)
    completion = palm.generate_text(
        **defaults,
        prompt=get_prompt("Representative " + rep["name"])
    )
    rep_desc = completion.result.replace("*", "")

    # Get the image URL
    wikipedia_url = [x for x in rep["urls"] if "wikipedia" in x][0]
    response = requests.get(url=wikipedia_url)
    soup = BeautifulSoup(response.text, "lxml")
    images = soup.find_all('img')
    rep_image = [x for x in images if "jpg" in x or "jpeg" in x["src"]][0]["src"]

    return render_template("district.html", representative=rep, representative_desc=rep_desc,
                           representative_image=rep_image)


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
    app.run( debug=True)
