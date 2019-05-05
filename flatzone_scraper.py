import json
import os
import requests


def download_flatzone():
    email = os.environ["EMAIL"]
    passwd = os.environ["PASSWD"]

    url = "https://api.flatzone.cz/graphql"

    mutation = {
        "query": "mutation Login {" +
                 " login(usernameOrEmail: \"" + email + "\", password: \"" + passwd + "\") {" +
                 "token" +
                 "  }" +
                 "}",
        "variables": "null",
        "operationName": "Login"
    }

    r = requests.post(url=url, json=mutation)

    jr = json.loads(r.text)
    token = jr['data']['login']['token']

    query = {
        "token": token,
        "query": "query test {" +
                 "searchByDistance(location: {lat: 50.093894,lon: 14.390144}, radius: 5000, offset: 0, size: 100) {" +
                 "estates{" +
                 "developer," +
                 "locality," +
                 "gps{" +
                 "lat," +
                 "lon" +
                 "}," +
                 "price," +
                 "floorArea," +
                 "detailUrl" +
                 "}" +
                 "}" +
                 "}",
        "variables": None,
        "operationName": "test"
    }

    r = requests.post(url, json=query)

    return json.loads(r.text)
