import requests

url = "https://www.googleapis.com/civicinfo/v2/representatives/"
apiKey = "AIzaSyC8JpyYJoet115Awj-hWWwlf74axIbI_UY"

header = {"Accept": "application/json"}
param = {
    "address": "2821 Townbluff Drive Apartment",
    "includedOffices": True,
    "levels": "",
    "roles": "",
    "key": apiKey
}

#Senator
param["levels"] = "country"
param["roles"] = "legislatorUpperBody"
response = requests.get(url, params=param, headers=header).json()

senator1 = response["officials"][0]
senator2 = response["officials"][1]

print(f"Your first Senator is {senator1['name']}, from the {senator1['party']}. Here's their image: {senator1['photoUrl']}.\n"
     f"Their political website: {senator1['urls'][0]}. Their wikipedia: {senator1['urls'][1]}.")
print(f"Your second Senator is {senator2['name']}, from the {senator2['party']}. Here's their image: {senator2['photoUrl']}.\n"
      f"Their political website: {senator2['urls'][0]}. Their wikipedia: {senator2['urls'][1]}.")

#Representative
param["levels"] = "country"
param["roles"] = "legislatorLowerBody"
response = requests.get(url, params=param, headers=header).json()

rep = response["officials"][0]
print(f"Your Representative is {rep['name']}, from the {rep['party']}.\n"
     f"Their political website: {rep['urls'][0]}. Their wikipedia: {rep['urls'][1]}.")

#Mayor
param["levels"] = "locality"
param["roles"] = "headOfGovernment"
response = requests.get(url, params=param, headers=header).json()
major = response["officials"][0]

print(f"Your major is {major['name']}, from the {major['party']}.\n"
      f"Their political website: {major['urls'][0]}.")