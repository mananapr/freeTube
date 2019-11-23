from flask import render_template, request, session, redirect, url_for
from app import app
import requests
import json
from bs4 import BeautifulSoup

SERVER_DOMAIN_NAME = 'http://127.0.0.1:8000'
API_ADDR = 'http://127.0.0.1'
API_PORT = '5000'
API_URL = API_ADDR + ":" + API_PORT + "/api/v1/"

def getChannelLink(userLink):
    ytURL = "https://youtube.com"+userLink+"/videos"
    response = requests.get(ytURL)
    soup = BeautifulSoup(response.text, "html5lib")
    channelLink = soup.find('meta', {'property':'og:url'})['content'][23:]
    return channelLink

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
    return render_template('search.html', title='Search', page=page, results=results, query=query, prev_page="/search?search={}&page={}".format(query,str(page-1)), next_page="/search?search={}&page={}".format(query,str(page+1)), baseaddr=SERVER_DOMAIN_NAME)

@app.route('/watch', methods=['GET'])
def watch():
    print(session['subscribedChannelsURLs'])
    videoID = request.args.get('v', default="error")
    if videoID == "error":
        return "Please specify a valid video"
    ytURL = "https://youtube.com/watch?v=" + videoID
    payload = {'url':ytURL}
    response = requests.post(API_URL+"urlinfo", json=payload)
    results = json.loads(response.text)
    return render_template("video.html", title=results["title"], video=results, baseaddr=SERVER_DOMAIN_NAME, videoID=videoID)

@app.route('/user/<id>', methods=['GET'])
def user(id):
    return redirect(SERVER_DOMAIN_NAME + getChannelLink('/user/'+str(id)))
@app.route('/channel/<id>', methods=['GET'])
def channel(id):
    ytURL = "https://youtube.com/channel/" + str(id)
    payload = {'url':ytURL}
    response = requests.post(API_URL+"channelinfo", json=payload)
    results = json.loads(response.text)
    return render_template("channel.html", channelLink="/channel/{}".format(id), title=results["channelName"], results=results["videos"], baseaddr=SERVER_DOMAIN_NAME, channelName=results["channelName"], subCount=results["channelSubCount"])

@app.route('/subscribe', methods=['GET'])
def subscribe():
    redirectURL = request.args.get('redirect', default='/index')
    channelURL = request.args.get('channelURL')
    if session.get('subscribedChannelsURLs') == None:
        session['subscribedChannelsURLs'] = []
    if channelURL in session['subscribedChannelsURLs']:
        tempList = []
        for channel in session['subscribedChannelsURLs']:
            if channel != channelURL:
                tempList.append(channel)
        session['subscribedChannelsURLs'] = tempList
    else:
        session['subscribedChannelsURLs'] = session['subscribedChannelsURLs'] + [channelURL]
    return redirect(redirectURL)

@app.route('/subscriptions', methods=['GET'])
def subscriptions():
    videos = []
    print(session['subscribedChannelsURLs'])
    if session.get('subscribedChannelsURLs') is not None:
        for channelURL in session.get('subscribedChannelsURLs'):
            ytURL = "https://youtube.com" + channelURL
            payload = {'url':ytURL}
            response = requests.post(API_URL+"channelinfo", json=payload)
            results = json.loads(response.text)["videos"]
            results[0]["channelName"] = json.loads(response.text)["channelName"]
            results[0]["channelLink"] = channelURL
            videos.append(results[0])
    return render_template("subscriptions.html", title="Subscriptions", results=videos, baseaddr=SERVER_DOMAIN_NAME)
