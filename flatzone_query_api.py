import requests
from requests.auth import HTTPBasicAuth
import os, sys, json


def download_flatzone():
    EMAIL= os.environ["EMAIL"]
    PASSWD= os.environ["PASSWD"]



    url = "https://api.flatzone.cz/graphql"

    mutation = {
        "query":"mutation Login {"+
                " login(usernameOrEmail: \""+EMAIL+"\", password: \""+PASSWD+"\") {"+
                    "token"+
                "  }"+
                "}",
        "variables":"null",
        "operationName":"Login"
    }

    r=requests.post(url=url, json=mutation)
    print(r)
    jr = json.loads(r.text)
    token = jr['data']['login']['token']


    query = {
        "token":token,
        "query":"query test {"+
                "searchByDistance(location: {lat: 50.093894,lon: 14.390144}, radius: 5000, offset: 0, size: 100) {"+
                "estates{"+
                      "developer,"+
                      "locality,"+
                      "gps{"+
                        "lat,"+
                        "lon"+
                      "},"+
                      "price,"+
                      "floorArea"+
                "}"+
            "}"+
        "}",
        "variables":None,
        "operationName":"test"
        }

    r=requests.post(url, json=query)

    return json.loads(r.text)


