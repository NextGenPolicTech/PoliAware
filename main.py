import os
import smtplib as sm

import urllib.parse
from bing_image_urls import bing_image_urls

import openai
from PIL import Image

import google.generativeai as palm
import requests
from flask import Flask, render_template, redirect, request, session, url_for
from ipstack import GeoLookup
from bs4 import BeautifulSoup
from googlesearch import search
from gnews import GNews
import lxml

gn = GNews(language='en', country='US', period='7d', max_results = 9)



# Use "pip install google-generativeai" to install the google.generativeai module
# Set up the palm AI module
palmApiKey = "AIzaSyBJEkrAln6h9yp5pfZyr15uauLBMlIOheA"

openai.api_key = "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"

messages = [
    {"role": "system", "content":"You are a generative AI who's only role is to utilize links found on the web to "
                                 "generate a description of a politician. You are not allowed to use any other "
                                 "information other than the links provided."},]

palm.configure(api_key=palmApiKey)

defaults = {
  'model': 'models/text-bison-001',
  'temperature': 0.3,
  'candidate_count': 1,
  'top_k': 40,
  'top_p': 0.95,
  'max_output_tokens': 130,
  'stop_sequences': [],
  'safety_settings': [{"category":"HARM_CATEGORY_DEROGATORY","threshold":1},
                      {"category":"HARM_CATEGORY_TOXICITY","threshold":1},
                      {"category":"HARM_CATEGORY_VIOLENCE","threshold":2},
                      {"category":"HARM_CATEGORY_SEXUAL","threshold":2},
                      {"category":"HARM_CATEGORY_MEDICAL","threshold":2},
                      {"category":"HARM_CATEGORY_DANGEROUS","threshold":2}],
}

def retrieve_information(query):
    results = []
    for result in search(query, num_results=3):
        results.append(result)
    results = ', '.join(results)
    return results

def generate_response(results, name):
    messages.append({"role": "user", "content": "Please generate a short (3 sentences) description of " + name + " based on the following links: " + results + ". Please be sure to give a short summary of their political views and their stance on major policies. You MUST provide the summary and cannot state that there is no information to be found. If necessary, you may use what you know and fabricate believable information."})
    completions = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages
        )
    messages.pop((len(messages) - 1))
    return completions.choices[0].message.content

def get_prompt(name):
    return (f"Give exactly 6 bullet points of  political facts about {name} and their political views, "
            f"most of which contain their view on many different policies."
            f"Include their positions on top policies such as: Gay marriage, abortion, gun control, death penalty"
            f", legalization of marijuana, minimum wage, universal health care, drug price regulations, and free"
            f"college tuition.")


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

        param["levels"] = "locality"
        param["roles"] = "headOfGovernment"
        response = requests.get(url, params=param, headers=header).json()
        mayor = response["officials"][0]
        session["mayor"] = mayor
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
    results = retrieve_information(sen1["name"])
    response = generate_response(results, sen1["name"])
    sen1_desc = response

    news = gn.get_news(sen1["name"])
    sen1_link = news[0]["title"] + "\n\n" + news[1]["title"]

    sen2 = response["officials"][1]
    results = retrieve_information(sen2["name"])
    response = generate_response(results, sen2["name"])
    sen2_desc = response

    news = gn.get_news(sen2["name"])
    sen2_link = news[0]["title"] + "\n\n" + news[1]["title"]

    # Governor
    ocd_param["levels"] = "administrativeArea1"
    ocd_param["roles"] = "headOfGovernment"
    response = requests.get(ocd_url, params=ocd_param, headers=header).json()
    gov = response["officials"][0]
    results = retrieve_information(gov["name"])
    response = generate_response(results, gov["name"])
    gov_desc = response

    news = gn.get_news(gov["name"])
    gov_link = news[0]["title"] + "\n\n" + news[1]["title"]

    # Attorney General
    ocd_param["roles"] = "governmentOfficer"
    response = requests.get(ocd_url, params=ocd_param, headers=header).json()
    i = 0
    for office in response["offices"]:
        if "Attorney General" in office["name"] or "Attorney-General" in office["name"]:
            i = office["officialIndices"][0]
            break
    ag = response["officials"][i]
    results = retrieve_information(ag["name"])
    response = generate_response(results, ag["name"])
    ag_desc = response

    news = gn.get_news(ag["name"])
    ag_link = news[0]["title"] + "\n\n" + news[1]["title"]

    return render_template("state.html", senator1=sen1, senator2=sen2, governor=gov, attorneyGeneral=ag
                           , senator1_desc=sen1_desc, senator2_desc=sen2_desc, governor_desc=gov_desc,
                           attorneyGeneral_desc=ag_desc, senator1_links = sen1_link, senator2_links = sen2_link, governor_links = gov_link, attorneyGeneral_links = ag_link)


@app.route("/your-representative")
def your_representative():
    rep = session.get('rep', None)
    mayor = session.get('mayor', None)
    results = retrieve_information(rep["name"])
    response = generate_response(results, rep["name"])
    rep_desc = response

    results = retrieve_information(mayor["name"])
    response = generate_response(results, mayor["name"])
    mayor_desc = response

    #Representative News
    news = gn.get_news(rep["name"])
    print(news)
    rep_link = news[0]["title"]

    # Representative Image
    query = rep["name"]
    query = urllib.parse.quote_plus(query)
    image = bing_image_urls(query, limit=1)
    rep_image = image[0]

    # Mayor Image
    query = mayor["name"]
    query = urllib.parse.quote_plus(query)
    image = bing_image_urls(query, limit=1)
    mayor_image = image[0]

    #Mayor News
    news = gn.get_news(mayor["name"])
    mayor_link = news[0]["title"]


    return render_template("district.html", representative=rep, representative_desc=rep_desc,
                           representative_image=rep_image, mayor_image=mayor_image, mayor=mayor,
                           mayor_description=mayor_desc, representative_links = rep_link, mayor_links = mayor_link)

@app.route("/news", methods=['GET'])
def news():
    news = gn.get_news("USA politics")

    query = news[0]["title"]
    image = bing_image_urls(query, limit=1)
    first_image_link = image[0]
    news[0]["image"] = first_image_link

    query = news[1]["title"]
    query = urllib.parse.quote_plus(query)
    image = bing_image_urls(query, limit=1)
    second_image_link = image[0]
    news[1]["image"] = second_image_link

    query = news[2]["title"]
    query = urllib.parse.quote_plus(query)
    image = bing_image_urls(query, limit=1)
    third_image_link = image[0]
    news[2]["image"] = third_image_link

    query = news[3]["title"]
    query = urllib.parse.quote_plus(query)
    image = bing_image_urls(query, limit=1)
    fourth_image_link = image[0]
    news[3]["image"] = fourth_image_link


    print(news)
    return render_template("news.html", news=news)


@app.route("/elections")
def elections():
    return render_template("elections.html")

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
