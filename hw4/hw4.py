import requests
import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib.patches import Polygon
from matplotlib.path import Path
import random as random
import json
import re
from collections import Counter

# Step 1
RedliningData = requests.get('https://dsl.richmond.edu/panorama/redlining/static/downloads/geojson/MIDetroit1939.geojson').json()['features']

# Step 2
HolcColorMap = {'A': 'darkgreen', 'B': 'cornflowerblue', 'C': 'gold', 'D': 'maroon'}

class DetroitDistrict():
    def __init__(self, Coordinates, HolcGrade, Name, QualitativeDescription):
        self.Coordinates = Coordinates
        self.HolcGrade = HolcGrade
        self.HolcColor = HolcColorMap[self.HolcGrade]
        self.Name = Name
        self.QualitativeDescription = QualitativeDescription

# Step 3
Districts = [DetroitDistrict(x['geometry']['coordinates'][0][0], x['properties']['holc_grade'], str(index), x['properties']['area_description_data']['8']) for index, x in enumerate(RedliningData)]
fig, ax = plt.subplots()
for District in Districts:
    ax.add_patch(Polygon(xy=np.array(District.Coordinates), facecolor=District.HolcColor, edgecolor='black'))
    ax.autoscale()
    plt.rcParams["figure.figsize"] = (15,15) 
plt.show()

# Step 4 - 7
cacheFile = 'cache.json'
try:
    with open(cacheFile, 'r') as file:
        cache = json.load(file)
        for j in Districts:
            j.RandomLong = cache[j.Name]['RandomLong']
            j.RandomLat = cache[j.Name]['RandomLat']
            j.CensusTract = cache[j.Name]['CensusTract']
            j.MedianIncome = cache[j.Name]['MedianIncome']
except:
    random.seed(17)
    xgrid = np.arange(-83.5,-82.8,.004) 
    ygrid = np.arange(42.1, 42.6, .004)
    xmesh, ymesh = np.meshgrid(xgrid,ygrid)
    points = np.vstack((xmesh.flatten(),ymesh.flatten())).T
    for j in Districts:
        # j.Coordinates instead of j.Coordinates[0] here since Coordincates I defined above is a 2D array
        p = Path(j.Coordinates)
        grid = p.contains_points(points) 
        # print(j," : ", points[random.choice(np.where(grid)[0])]) 
        point = points[random.choice(np.where(grid)[0])]
        j.RandomLong = point[0]
        j.RandomLat = point[1]
        areaUrl = 'https://geo.fcc.gov/api/census/area?lat={}&lon={}&censusYear=2010&format=json'.format(j.RandomLat, j.RandomLong)
        j.CensusTract = requests.get(areaUrl).json()['results'][0]['block_fips'][2:11]  # county_fips and tract code

    key = '364ecb717064b86c438ff1c227a88fa1a8c8bdf9'
    state= 26  # MI
    url = 'https://api.census.gov/data/2018/acs/acs5?get=B19013_001E&for=tract:*&in=state:{}&key={}'.format(state, key)
    MIMedian = requests.get(url).json()
    cache = {}
    for j in Districts:
        j.MedianIncome = int([x[0] for x in MIMedian if x[2] == j.CensusTract[0:3] and x[3] == j.CensusTract[3:]][0])
        cache[j.Name] = {}
        cache[j.Name]['RandomLong'] = j.RandomLong
        cache[j.Name]['RandomLat'] = j.RandomLat
        cache[j.Name]['CensusTract'] = j.CensusTract
        cache[j.Name]['MedianIncome'] = j.MedianIncome
    with open(cacheFile, 'w') as file:
        json.dump(cache, file)
    
# Step 8
AMedian = [j.MedianIncome for j in Districts if j.HolcGrade == 'A']
BMedian = [j.MedianIncome for j in Districts if j.HolcGrade == 'B']
CMedian = [j.MedianIncome for j in Districts if j.HolcGrade == 'C']
DMedian = [j.MedianIncome for j in Districts if j.HolcGrade == 'D']
A_mean_income = np.mean(AMedian)
A_median_income = np.median(AMedian)
B_mean_income = np.mean(BMedian)
B_median_income = np.median(BMedian)
C_mean_income = np.mean(CMedian)
C_median_income = np.median(CMedian)
D_mean_income = np.mean(DMedian)
D_median_income = np.median(DMedian)
print('A_mean_income: {}, A_median_income: {}'.format(A_mean_income, A_median_income))
print('B_mean_income: {}, B_median_income: {}'.format(B_mean_income, B_median_income))
print('C_mean_income: {}, C_median_income: {}'.format(C_mean_income, C_median_income))
print('D_mean_income: {}, D_median_income: {}'.format(D_mean_income, D_median_income))

# Step 9
ADescription = ' '.join([j.QualitativeDescription for j in Districts if j.HolcGrade == 'A'])
BDescription= ' '.join([j.QualitativeDescription for j in Districts if j.HolcGrade == 'B'])
CDescription = ' '.join([j.QualitativeDescription for j in Districts if j.HolcGrade == 'C'])
DDescription = ' '.join([j.QualitativeDescription for j in Districts if j.HolcGrade == 'D'])
AWords = re.findall(r'[\w]+', ADescription)
BWords = re.findall(r'[\w]+', BDescription)
CWords = re.findall(r'[\w]+', CDescription)
DWords = re.findall(r'[\w]+', DDescription)
# in order to remove the words that are common to all 4 categories, I include a stop word list on GitHub
stopWords = requests.get('https://raw.githubusercontent.com/Alir3z4/stop-words/master/english.txt').text.split('\n')[:-1]
# turn into lower case
ANoStop = [word.lower() for word in AWords if word.lower() not in stopWords]
BNoStop = [word.lower() for word in BWords if word.lower() not in stopWords]
CNoStop = [word.lower() for word in CWords if word.lower() not in stopWords]
DNoStop = [word.lower() for word in DWords if word.lower() not in stopWords]
ACounter = Counter(ANoStop)
BCounter = Counter(BNoStop)
CCounter = Counter(CNoStop)
DCounter = Counter(DNoStop)
A_10_Most_Common = [word for word, _ in ACounter.most_common(10)]
B_10_Most_Common = [word for word, _ in BCounter.most_common(10)]
C_10_Most_Common = [word for word, _ in CCounter.most_common(10)]
D_10_Most_Common = [word for word, _ in DCounter.most_common(10)]
print('A_10_Most_Common: {}'.format(A_10_Most_Common))
print('B_10_Most_Common: {}'.format(B_10_Most_Common))
print('C_10_Most_Common: {}'.format(C_10_Most_Common))
print('D_10_Most_Common: {}'.format(D_10_Most_Common))

# Bonus 2
"""
The results in Step 6 or 7 actually didn't surprise me as I have been provided the redlining background
information in Step 6. However, I will be surprised if not given the background. The results show that 
the household income data is quite different in districts with various grades, which implicates that 
inequality does exist.
"""
