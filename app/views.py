from flask import render_template, request
from app import app
import requests
import json

SERVER_DOMAIN_NAME = 'http://127.0.0.1:8000'
API_ADDR = 'http://127.0.0.1'
API_PORT = '5000'
API_URL = API_ADDR + ":" + API_PORT + "/api/v1/"

@app.route('/')
@app.route('/index')
def index():
    response = requests.get(API_URL+"explore")
    results = json.loads(response.text)["videos"]
    return render_template('index.html', title='Home', results=results, baseaddr=SERVER_DOMAIN_NAME)

@app.route('/search', methods=['GET'])
def search():
    page = request.args.get('page', default=1, type=int)
    if page <= 0:
        page = 1
    query = request.args.get('search')
    payload = {'query':query}
    response = requests.post(API_URL+"search?page="+str(page), json=payload)
    results = json.loads(response.text)['videos']
    return render_template('search.html', title='Search', page=page, results=results, prev_page="/search?search={}&page={}".format(query,str(page-1)), next_page="/search?search={}&page={}".format(query,str(page+1)), baseaddr=SERVER_DOMAIN_NAME)

@app.route('/watch', methods=['GET'])
def watch():
    videoID = request.args.get('v', default="error")
    if videoID == "error":
        return "Please specify a valid video"
    ytURL = "https://youtube.com/watch?v=" + videoID
    payload = {'url':ytURL}
    response = requests.post(API_URL+"urlinfo", json=payload)
    results = json.loads(response.text)
    return render_template("video.html", title=results["title"], video=results, baseaddr=SERVER_DOMAIN_NAME)

@app.route('/user/<id>', methods=['GET'])
def user(id):
    ytURL = "https://youtube.com/user/" + str(id)
    payload = {'url':ytURL}
    response = requests.post(API_URL+"channelinfo", json=payload)
    results = json.loads(response.text)
    return render_template("channel.html", title=results["channelName"], results=results["videos"], baseaddr=SERVER_DOMAIN_NAME, channelName=results["channelName"], subCount=results["channelSubCount"])
@app.route('/channel/<id>', methods=['GET'])
def channel(id):
    ytURL = "https://youtube.com/channel/" + str(id)
    payload = {'url':ytURL}
    response = requests.post(API_URL+"channelinfo", json=payload)
    results = json.loads(response.text)
    return render_template("channel.html", title=results["channelName"], results=results["videos"], baseaddr=SERVER_DOMAIN_NAME, channelName=results["channelName"], subCount=results["channelSubCount"])
