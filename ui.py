from flask import Flask, request, render_template, session
import os
from tree import treeGroups, loadTree

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    return render_template(
        'index.html', 
        language=treeGroups['language'],
        year=treeGroups['yearGroup'],
        rating=treeGroups['ratingGroup'],
        runtime=treeGroups['runtimeGroup']
    )

@app.route('/', methods = ["POST"])
def data():
    data = request.get_json()
    session['data'] = data
    return data

@app.route('/tables')
def tables():
    treeType, group = session.get('data', None).split(',')
    headers = ['Title', 'Language', 'Year', 'Rating', 'Runtime', 'Genre', 'Director', 'Writer', 
    'Actor', 'Popularity', 'Revenue', 'Status', 'Keywords', 'Overview', 'Production Countries']
    attributes = [h.lower() for h in headers[1:-1]] + ['production_countries']
    treeFile = open('trees/{}.txt'.format(treeType), "r")
    root = loadTree(treeFile)
    treeFile.close()
    cur = root
    while cur.left and cur.right:
        if group in cur.left.groups:
            cur = cur.left
        else:
            cur = cur.right
    movies = cur.movies
    return render_template('tables.html', movies=movies, headers=headers, attributes=attributes)

if __name__ == "__main__":
    app.run(debug=True)