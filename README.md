# SI 507 Final Project
## Requirements
`requests`, `flask` and `pandas` are required to run this project, as listed in requirements.txt. To install, run
```
pip install -r requirements.txt
```
## File Structure
```
│  preprocess.py            # preprocessed code
│  README.md
│  tree.py                  # tree related code, including building, saving, loading trees
│  ui.py                    # flask related code
│
├─cache                     # cached data
│      cache.json
│      data.json
│      language.json
│      movies.csv
│      ratingGroup.json
│      runtimeGroup.json
│      yearGroup.json
│
├─data_kaggle               # kaggle data set
│      keywords.csv
│      movies_metadata.csv
│
├─templates                 # flask templates
│      index.html
│      tables.html
│
└─trees                     # json files of the trees
       language.json
       ratingGroup.json
       runtimeGroup.json
       yearGroup.json
```
## How to Run
As is shown above, there are 3 .py files in this project: 
* `ui.py` builds the flask application that enables user interaction and data presentation. To start the application, run `python ui.py`. Then a local server will start, and the homepage will be shown at http://127.0.0.1:5000/. Select from different year of release groups, language groups, rating groups and runtime groups, and the selected movies will be displayed in HTML tables at http://127.0.0.1:5000/tables.
* `tree.py` includes functions that could builds, saves, and loads the trees.
* `preprocess.py` includes 5 functions that could preprocess the data. A command-line interface is provided to select data preprocess steps from the 5 functions. The api key is included, but if you would like to get an api key yourself, please visit https://www.omdbapi.com/apikey.aspx. 
## Data Structure
The movies are organized into 4 trees based on year of release, language, rating or runtime respectively. The tree node is defined as a class, which could be found at https://github.com/tcy1999/SI507/blob/master/tree.py#L3. There are 2 kinds of nodes in a tree, a groups node and a movies node. A groups node is an internal node, whose `groups` attribute represents the possible groups that its children might fall into. A movies node is a leaf node, whose `groups` attribute has length of 1, only containing a specific group, and the `movies` attribute represents the movies of this group. 

Basically, the tree is built by dividing groups into two halves to create internal nodes, and finally store movies at the leaf nodes.
