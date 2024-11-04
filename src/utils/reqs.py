import requests

# Define the URL for the Flask app (adjust the port if necessary)
url = 'http://127.0.0.1:5000/'

def sendGetReq(relative_url, params):
    response = requests.get(url+relative_url, params=params)
    return response