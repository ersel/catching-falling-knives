import json
import os
import requests

def shorten(longUrl):
    query_params = {
        'longUrl': longUrl,
        'access_token': os.environ['BITLY_ACCESS_TOKEN']
    }

    endpoint = 'https://api-ssl.bitly.com/v3/shorten'
    response = requests.get(endpoint, params=query_params, verify=False)

    response = json.loads(response.content)
    return response['data']['url']
