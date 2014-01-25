# -*- coding: utf-8 -*-

import json
import pymongo
json_data=open('ader.json')

data = json.load(json_data)
json_data.close()

connection_string = "mongodb://localhost"
connection = pymongo.MongoClient(connection_string)
database = connection.meps
country_queried = "Romania"
for mep in data["meps"]:
    country = mep["Constituencies"][0]["country"]
    if country == country_queried:
        print mep["Name"]["full"]
        database.meps.insert(mep)
