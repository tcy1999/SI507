#########################################
##### Name:     Chenyun Tao         #####
##### Uniqname: cyuntao             #####
#########################################

import json
import webbrowser
import requests


class Media:

    def __init__(self, title="No Title", author="No Author", release_year="No Release Year", url="No URL", json=None):
        if json:
            if "trackName" in json:
                self.title = json['trackName']
            elif "collectionName" in json:
                self.title = json["collectionName"]
            else:
                self.title = "No Title"
            self.author = json["artistName"]
            self.release_year = json["releaseDate"][:4]
            if 'trackViewUrl' in json:
                self.url = json["trackViewUrl"]
            elif 'collectionViewUrl' in json:
                self.url = json["collectionViewUrl"]
            else:
                self.url = "No URL"
        else:
            self.title = title
            self.author = author
            self.release_year = release_year
            self.url = url

    
    def info(self):
        return "{} by {} ({})".format(self.title, self.author, self.release_year)


    def length(self):
        return 0


class Song(Media):

    def __init__(self, title="No Title", author="No Author", release_year="No Release Year", url="No URL", album="No Album", genre="No Genre", track_length=0, json=None):
        super().__init__(title, author, release_year, url, json)
        if json:
            self.album = json["collectionName"]
            self.genre = json["primaryGenreName"]
            self.track_length = json["trackTimeMillis"]
        else:
            self.album = album
            self.genre = genre
            self.track_length = track_length


    def info(self):
        return "{} [{}]".format(super().info(), self.genre)

    def length(self):
        return round(self.track_length / 1000)


class Movie(Media):

    def __init__(self, title="No Title", author="No Author", release_year="No Release Year", url="No URL", rating="No Rating", movie_length=0, json=None):
        super().__init__(title, author, release_year, url, json)
        if json:
            self.rating = json["contentAdvisoryRating"]
            self.movie_length = json["trackTimeMillis"]
        else:
            self.rating = rating
            self.movie_length = movie_length


    def info(self):
        return "{} [{}]".format(super().info(), self.rating)

    def length(self):
        return round(self.movie_length / 60000)


# fetch iTunes API data
def fetchItunesData(term):
    res = requests.get("https://itunes.apple.com/search?term=" + term).text
    return json.loads(res)


# create media lists from iTunes API
def createMediaFromItunes(term):
    jsonData = fetchItunesData(term)["results"]
    songList = []
    movieList = []
    otherList = []
    
    for x in jsonData:
        otherMedia = True
        if x["wrapperType"] == "track":
            if x["kind"] == "song":
                otherMedia = False
                songList.append(Song(json=x))
            elif x["kind"] == "feature-movie":
                otherMedia = False
                movieList.append(Movie(json=x))
        if otherMedia:
            otherList.append(Media(json=x))
    return songList, movieList, otherList


# print a media list line by line
def printList(mediaList, mediaType, num):
    if len(mediaList):
        print(mediaType.upper())
        for media in mediaList:
            print('{} {}'.format(num, media.info()))
            num += 1
    else:
        print('No {} for the term'.format(mediaType))
    return num


if __name__ == "__main__":
    # your control code for Part 4 (interactive search) should go here
    term = input('Enter a search term, or "exit" to quit: ')
    while True:
        # a try-catch block in case of other unexpected errors not handled in the code
        try:
            if term == 'exit':
                print('Bye!')
                break
            else:
                songList, movieList, otherList = createMediaFromItunes(term)
                songLen, movieLen, otherLen = len(songList), len(movieList), len(otherList)
                totalLen = songLen + movieLen + otherLen
                if totalLen == 0:
                    term = input('No results for the term. Please enter another search term, or exit: ')
                    continue
                num = printList(songList, 'songs', 1)
                num = printList(movieList, 'movies', num)
                printList(otherList, 'other media', num)
                term = input('Enter a number for more info, or another search term, or exit: ')
                while term.isnumeric():
                    inputNum = int(term) - 1
                    if inputNum < 0 or inputNum > totalLen - 1:
                        print('This number is out of range.')
                    else:
                        if inputNum < songLen:
                            url = songList[inputNum].url
                        elif inputNum < songLen + movieLen:
                            url = movieList[inputNum - songLen].url
                        else:
                            url = otherList[inputNum - songLen - movieLen].url
                        if url == "No URL":
                            print(url)
                        else:
                            print('Launching {} in web browser...'.format(url))
                            webbrowser.open(url)
                    term = input('Enter a number for more info, or another search term, or exit: ')
        except:
            term = input('Enter a number for more info, or another search term, or exit: ')
