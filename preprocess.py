import json
import requests
import pandas as pd
from ast import literal_eval
from tree import treeGroups

def kaggleProcess():
    """randomly sample 1500 records, and merge the 2 csvs from the kaggle dataset

    Parameters
    ----------        
    None

    Returns
    -------
    None
    """
    movies = pd.read_csv('data_kaggle/movies_metadata.csv').drop_duplicates(subset=['imdb_id'])
    keywords = pd.read_csv('data_kaggle/keywords.csv').drop_duplicates(subset='id')
    keywords['keywords'] = keywords['keywords'].map(lambda keyword: ', '.join([x['name'] for x in literal_eval(keyword)]))
    samples = movies.sample(1500, random_state=42)[['id', 'overview', 'popularity', 'revenue', 'status', 'production_countries', 'release_date', 'imdb_id', 'original_language']]
    samples['id'] = samples['id'].astype('int64')
    samples = samples.merge(keywords, on='id')
    samples.to_csv('cache/movies.csv', index=False)

def apiProcess():
    """access api data, join the data with csv data, and cache the joined data

    Parameters
    ----------        
    None

    Returns
    -------
    None
    """
    # open movie database api has a limit of 1000 requests/day/api key; for ease, just change the index here
    sample = pd.read_csv('cache/movies.csv')[1000:]
    key = '1dee52ff'
    try:
        with open('cache/cache.json') as file:
            cache = json.load(file)
    except:
        cache = {}   # initialization for the first request chunk
    for _, row in sample.iterrows():
        imdb_id = row['imdb_id']
        cache[imdb_id] = {
            'overview': row['overview'], 'popularity': row['popularity'], 
            'status': row['status'], 'revenue': row['revenue'], 
            'production_countries': row['production_countries'], 'language': row['original_language']
        }
        result = requests.get('http://www.omdbapi.com/?i={}&apikey={}'.format(imdb_id, key)).json()
        cache[imdb_id]['title'] = result['Title']
        cache[imdb_id]['year'] = result['Year']
        cache[imdb_id]['runtime'] = result['Runtime']
        cache[imdb_id]['genre'] = result['Genre']
        cache[imdb_id]['director'] = result['Director']
        cache[imdb_id]['writer'] = result['Writer']
        cache[imdb_id]['actor'] = result['Actors']
        cache[imdb_id]['rating'] = result['imdbRating']
    with open('cache/cache.json', 'w') as file:
        json.dump(cache, file)

def eda():
    """Exploratory Data Analysis of the data, in order to create reasonable groups

    Parameters
    ----------        
    None

    Returns
    -------
    None
    """
    with open('cache/cache.json') as file:
        cache = json.load(file)
    runtime = []
    rating = []
    year = []
    language = []
    for key in cache:
        if cache[key]['runtime'] != 'N/A':
            runtime.append(int(cache[key]['runtime'].split(' ')[0]))
        if cache[key]['rating'] != 'N/A':
            rating.append(float(cache[key]['rating']))
        year.append(int(cache[key]['year'][:4]))
        language.append(cache[key]['language'])
    print(pd.Series(language).value_counts())
    rating = pd.Series(rating)
    print(rating.describe())
    runtime = pd.Series(runtime)
    print(runtime.describe())
    year = pd.Series(year)
    print(year.describe())

def process():
    """convert the raw cached data into processed data, 
    e.g., label the data into year of release groups, rating groups and runtime groups

    Parameters
    ----------        
    None

    Returns
    -------
    None
    """
    commonLanguage = ['en', 'fr', 'it', 'ja', 'de']  # top 5 languages from EDA
    languageMap = {'en': 'English', 'fr': 'French', 'it': 'Italian', 'ja': 'Japanese', 'de': 'German'}
    with open('cache/cache.json') as file:
        cache = json.load(file)
    for key in cache:
        language = cache[key]['language']
        if language not in commonLanguage:
            cache[key]['language'] = 'Other'
        else:
            cache[key]['language'] = languageMap[language]
        year = cache[key]['year'][:4]
        if int(year) < 1970:
            cache[key]['yearGroup'] = 'Before 1970'
        else:
            cache[key]['yearGroup'] = '{} - {}'.format(int(year) // 10 * 10, int(year) // 10 * 10 + 9)
        rating = cache[key]['rating']
        if rating == 'N/A':
            cache[key]['ratingGroup'] = rating
        else:
            rating = float(rating)
            if rating < 5:
                cache[key]['ratingGroup'] = '< 5.0'
            else:
                cache[key]['ratingGroup'] = '{} - {}'.format(int(rating), int(rating) + 0.9)
        runtime = cache[key]['runtime']
        if runtime == 'N/A':
            cache[key]['runtimeGroup'] = runtime
        else:
            runtime = int(cache[key]['runtime'].split(' ')[0])
            if runtime < 85:
                cache[key]['runtimeGroup'] = '< 85 min'
            elif runtime < 95:
                cache[key]['runtimeGroup'] = '< 95 min'
            elif runtime < 105:
                cache[key]['runtimeGroup'] = '< 105 min'
            else:
                cache[key]['runtimeGroup'] = '>= 105 min'
        cache[key]['production_countries'] = ' | '.join([x['name'] for x in literal_eval(cache[key]['production_countries'])])
    with open('cache/data.json', 'w') as file:
        json.dump(cache, file)

def groupMovies():
    """based on the processed cache/data.json, group the data by different groups according to each tree type,
    and save to cache/{treeType}.json

    Parameters
    ----------        
    None

    Returns
    -------
    None
    """
    with open('cache/data.json') as file:
        cache = json.load(file)
    for treeType, groups in treeGroups.items():
        temp = {}
        for group in groups:
            temp[group] = []
        for key in cache:
            group = cache[key][treeType]
            if len(temp[group]) == 50:
                continue
            temp[group].append(cache[key])
        with open('cache/{}.json'.format(treeType), 'w') as file:
            json.dump(temp, file)

def main():
    option = input("Input 1, 2, 3, 4, 5 to select whether you would like to process kaggle data, \
    \nor the open movie database api data, \nor see EDA result, \nor process the raw data, \
    \nor group the movies: ").strip()
    if option == '2':
        apiProcess()
    elif option == '3':
        eda()
    elif option == '4':
        process()
    elif option == '5':
        groupMovies()
    else:
        kaggleProcess()

if __name__ == '__main__':
    main()
