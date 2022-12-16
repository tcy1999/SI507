from flask import Flask, render_template
from NYTSecrets import api_key
import requests

app = Flask(__name__)

def getData(hasImage=False):
    try:
        resp = requests.get('https://api.nytimes.com/svc/topstories/v2/technology.json?api-key={}'.format(api_key)).json()
        results = resp['results'][:5]
        if hasImage:
            articles = [(x['title'], x['url'], [img['url'] for img in x['multimedia'] if img['format'] == 'Large Thumbnail'][0]) for x in results]
        else:
            articles = [(x['title'], x['url'])for x in results]
    except:
        articles = []
    return articles

@app.route('/')
def index():
    return "<h1>Welcome!</h1>"

@app.route('/name/<name>')
def name(name):
    return render_template('name.html', name=name)

@app.route('/headlines/<name>')
def headlines(name):
    articles = getData()
    return render_template('headlines.html', name=name, articles=articles)

@app.route('/links/<name>')
def links(name):
    articles = getData()
    return render_template('links.html', name=name, articles=articles)

@app.route('/images/<name>')
def images(name):
    articles = getData(True)
    return render_template('images.html', name=name, articles=articles)

if __name__ == "__main__":
    app.run(debug=True)