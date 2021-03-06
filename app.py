#import lyricsgenius as genius
import requests
import urllib.request
import json
from bs4 import BeautifulSoup
import re
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

# Genius API Information 
client_id = ""
client_secret = ""
client_access_token = ""

# Flask Information 
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Format a request URI for the Genius API
_URL_API = "https://api.genius.com/"
_URL_SEARCH = "search?q="


def search_helper(term):
    querystring = _URL_API + _URL_SEARCH + urllib.request.quote(term)
    #print(querystring)
    request = urllib.request.Request(querystring)
    request.add_header("Authorization", "Bearer " + client_access_token)
    request.add_header("User-Agent", "")
    response = urllib.request.urlopen(request, timeout=3).read().decode('UTF-8')
    json_obj = json.loads(response)
    return json_obj


def search_for_song(song_name):
    ret = search_helper(song_name)
    string = ret['response']['hits'][0]['result']['full_title']
    artwork = ret['response']['hits'][0]['result']['song_art_image_thumbnail_url']
    genius_url = ret['response']['hits'][0]['result']['url']
    url = ret['response']['hits'][0]['result']['url']
    return url, string, artwork, genius_url

def get_song_info(url):
    page = requests.get(url)
    html = BeautifulSoup(page.text, 'html.parser')
    lyrics = html.find('div', class_='lyrics')
    return lyrics

def parse_lyrics(lyrics_html, url):
    dict = {}
    values = []

    annotated = lyrics_html.find_all('a')
    # TODO: Develop a way to evaluate the quality of annotations
    # for a in annotated:
    #     # temp = a['href']
    #     # temp = temp[temp.find('note-')+5:]
    #     # querystring = _URL_API + 'annotations/' + temp
    #     # request = urllib.request.Request(querystring)
    #     # request.add_header("Authorization", "Bearer " + client_access_token)
    #     # request.add_header("User-Agent", "")
    #     # response = urllib.request.urlopen(request, timeout=3).read().decode('UTF-8')
    #     # json_obj = json.loads(response)
    #     # try:
    #     #     annotation = json_obj['response']['annotation']['body']['dom']['children']
    #     #     if len(annotation) >= 5:
    #     #         values.append(1)
    #     #     else:
    #     #         values.append(len(annotation)/5)
    #     # except:
    #     values.append(1)

    #Get all the lyrics that are annotated and add them to the dict
    for x in range(len(annotated)):
        temp = annotated[x].get_text().rstrip("\n\r")
        temp = re.sub('\s+',' ',temp)
        dict.update({temp:1})
    full_text = lyrics_html.get_text()
    temp = ""
    #now we have to add all the lyrics that are not annotated
    for x in range(len(full_text)):
        temp += full_text[x]
        #loop through all the lines until we find a new line
        if full_text[x] == "\n":
            if len(temp) > 2:
                if temp[0] == "[":
                    temp = ""
                    continue
                else:
                    if temp.rstrip("\n\r") in dict:
                        pass
                    else:
                        dict.update({temp:0})
                    temp = ""
            else:
                temp = ""

    result = {}

    for key,value in dict.items():
        if key not in result.keys():
            # We want to assign a value of 0.5 to annotated lyrics that are repeated
            if key in result.keys() and value == 1:
                result[key] = 0.5
            else:
                result[key] = value

    return result

def evaluate(result_dict):
    annotated_score = 0
    empty_score = 0
    for key,value in result_dict.items():
        # if we have a value greater than 0, add it the annotated score
        temp = len(key)
        if value > 0:
            annotated_score += value * temp
        # always add it to the empty score
        empty_score += temp
    temp = float(annotated_score)/float(empty_score)
    return temp

def driver(song_name):
    query,string,artwork, genius_url = search_for_song(song_name)
    lyrics = get_song_info(query)
    result_dict = parse_lyrics(lyrics, query)
    score = evaluate(result_dict)
    return score, string, artwork, genius_url

@app.route('/query', methods= ['POST'])
def create():
    query = request.args['query']
    score, string, artwork, genius_url = driver(query)
    return jsonify({"score":score, "string":string, "artwork":artwork, "genius_url":genius_url})
