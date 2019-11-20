from flask import render_template, request
from app import app
import requests
import json

API_ADDR = 'http://127.0.0.1'
API_PORT = '5000'
API_URL = API_ADDR + ":" + API_PORT + "/api/v1/"

@app.route('/')
@app.route('/index')
def index():
    response = requests.get(API_URL+"explore")
    results = json.loads(response.text)["videos"]
    return render_template('index.html', title='Home', results=results)

@app.route('/search', methods=['GET'])
def search():
    page = request.args.get('page', default=1, type=int)
    if page <= 0:
        page = 1
    query = request.args.get('search')
    print(query)
    payload = {'query':query}
    response = requests.post(API_URL+"search?page="+str(page), json=payload)
    results = json.loads(response.text)['videos']
    return render_template('search.html', title='Search', page=page, results=results, prev_page="/search?search={}&page={}".format(query,str(page-1)), next_page="/search?search={}&page={}".format(query,str(page+1)))
