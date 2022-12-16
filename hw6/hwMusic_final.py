from timeit import default_timer

rows = 296
cols = 3

# step 1
def initialize():
    return [[None] * cols for _ in range(rows)]

# step 2
def readFile(music, csvName):
    with open(csvName, encoding='iso8859') as file:
        for i, line in enumerate(file.readlines()):
            artist, album, track = line.strip().split(',')
            music[i] = [artist, int(album), int(track)] 
    return music

# step 3
def printData(music):
    print(('{:<30} | {:<10} | {:<10}').format('Artist Name', '#Album', '#Track'))
    for line in music:
        print(('{:<30} | {:<10} | {:<10}').format(line[0], line[1], line[2]))

# step 4.a
def biSearchArtist(music, artist):
    low, high = 0, len(music) - 1
    while low <= high:
        mid = low + (high - low) // 2
        if music[mid][0] == artist:
            return mid + 1
        elif music[mid][0] < artist:
            low = mid + 1
        else:
            high = mid - 1
    return -1

# step 4.b
def seqSearchArtist(music, artist):
    for i, line in enumerate(music):
        if line[0] == artist:
            return i + 1
    return -1

# step 4.c
def timeBiSearchArtist():
    start = default_timer()
    for _ in range(100000):
        biSearchArtist(music, 'Usher')
    return default_timer() - start

def timeSeqSearchArtist():
    start = default_timer()
    for _ in range(100000):
        seqSearchArtist(music, 'Usher')
    return default_timer() - start

# step 5.a
def bubbleSortAlbums(music):
    for i in range(len(music) - 1):
        for j in range(len(music) - 1 - i):
            if music[j][1] < music[j+1][1]:
                music[j+1], music[j] = music[j], music[j+1]
    return music

# step 5.b
def merge(left, right):
    res = []
    i, j = 0, 0
    while i < len(left) and j < len(right):
        if left[i][1] >= right[j][1]:
            res.append(left[i])
            i += 1
        else:
            res.append(right[j])
            j += 1
    if i < len(left):
        res += left[i:]
    if j < len(right):
        res += right[j:]
    return res

def altSortAlbums(music):
    """
    The alternate sort method implemented here is merge sort.
    """
    if len(music) < 2:
        return music
    mid = len(music) // 2
    return merge(altSortAlbums(music[:mid]), altSortAlbums(music[mid:]))

# step 5.c
def timeBubbleSortAlbums():
    start = default_timer()
    for _ in range(1000):
        bubbleSortAlbums(music.copy())
    return default_timer() - start

def timeAltSortAlbums():
    start = default_timer()
    for _ in range(1000):
        altSortAlbums(music.copy())
    return default_timer() - start

# step 6.a
def inSortTracks(music):
    for i in range(1, len(music)):
        temp = music[i]
        j = i - 1
        while j >= 0 and music[j][2] < temp[2]:
            music[j+1] = music[j]
            j -= 1
        music[j+1] = temp
    return music

# step 6.b
def partition(array, left, right):
    pivot = right
    i = left
    for j in range(left, right):
        if array[j][2] > array[pivot][2]:
            array[i], array[j] = array[j], array[i]
            i += 1
    array[i], array[pivot] = array[pivot], array[i]
    return i

def quickSort(array, left, right):
    if left < right:
        pivot = partition(array, left, right)
        quickSort(array, left, pivot - 1)
        quickSort(array, pivot + 1, right)
    return array

def altSortTracks(music):
    """
    The alternate sort method implemented here is quick sort.
    """
    return quickSort(music, 0, len(music) - 1)

# step 6.c
def timeInSortTracks():
    start = default_timer()
    for _ in range(1000):
        inSortTracks(music.copy())
    return default_timer() - start

def timeAltSortTracks():
    start = default_timer()
    for _ in range(1000):
        altSortTracks(music.copy())
    return default_timer() - start

# step 7
"""
Based on this project, I could say that binary search is more efficient than a sequential search, as it
takes much less time than sequential search. This is not surprising as the average time complexity of 
binary search is O(log n), while the time complexity of sequential search is O(n).

For sorting albums, merge sort is obviously more efficient than bubble sort. This is not surprising as
the average time complexity of bubble sort is O(n^2), while the average time complexity of merge sort 
is O(nlog n).

For sorting tracks, quick sort is obviously more efficient than insertion sort. This is not surprising 
as the average time complexity of insertion sort is O(n^2), while the average time complexity of quick 
sort is O(nlog n).
"""

music = initialize()
music = readFile(music, 'music.csv')

def main():
    print('Original music data (first 10 rows)')
    print('-'*60)
    printData(music[:10])
    print('-'*60)
    print('Binary search sample output: Nas was found at row number {}'.format(biSearchArtist(music, 'Nas')))
    print('Sequential search sample output: Nas was found at row number {}'.format(seqSearchArtist(music, 'Nas')))
    print('Binary search time: {}'.format(timeBiSearchArtist()))
    print('Sequential search time: {}'.format(timeSeqSearchArtist()))
    print('-'*60)
    print('Bubble sort albums result (first 10 rows)')
    print('-'*60)
    printData(bubbleSortAlbums(music.copy())[:10])
    print('-'*60)
    print('Merge sort albums result (first 10 rows)')
    print('-'*60)
    printData(altSortAlbums(music.copy())[:10])
    print('-'*60)
    print('Bubble sort time: {}'.format(timeBubbleSortAlbums()))
    print('Merge sort time: {}'.format(timeAltSortAlbums()))
    print('-'*60)
    print('Insertion sort tracks result (first 10 rows)')
    print('-'*60)
    printData(inSortTracks(music.copy())[:10])
    print('-'*60)
    print('Quick sort tracks result (first 10 rows)')
    print('-'*60)
    printData(altSortTracks(music.copy())[:10])
    print('-'*60)
    print('Insertion sort time: {}'.format(timeInSortTracks()))
    print('Quick sort time: {}'.format(timeAltSortTracks()))
    print('-'*60)

if __name__ == '__main__':
    main()