from collections import deque

nodeTypes = {0: 'movie', 1: 'actor'}

class Node:
    def __init__(self, val, nodeType=0):    # nodeType: see nodeTypes
        self.val = val
        self.nodeType = nodeType
        self.neighbors = set()

def loadData(fileName):
    """load movie and actor data from a given file and build the actor-movie 
    relationships as a graph

    Parameters
    ----------        
    fileName: string
        name of the file to be read

    Returns
    -------
    graph:
        a graph representing actor-movie relationships
    """
    graph = {}
    with open(fileName, 'r', encoding='iso-8859-1') as file:
        while True:
            line = file.readline()
            if line == '':          
                break
            line = line.strip().split('/')
            movie, actors = line[0], line[1:]
            graph[movie] = Node(movie)
            for actor in actors:
                if actor not in graph:
                    graph[actor] = Node(actor, 1)
                graph[movie].neighbors.add(graph[actor])
                graph[actor].neighbors.add(graph[movie])
    return graph

def calculateBaconNumber(graph, nameA, nameB):
    """find the A-number of B (that is, a shortest path from A to B) and display the movie-actor
    chain to A

    Parameters
    ----------        
    graph:
        a graph representing actor-movie relationships
    nameA: string
        actor name A
    nameB: string
        actor name B

    Returns
    -------
    int
        A-number of B
    """
    queue = deque()
    visited = set()
    queue.append((graph[nameB], [nameB + ' [' + nodeTypes[1] + ']'], 0))
    visited.add(graph[nameB])
    while len(queue) > 0:
        cur, path, distance = queue.popleft()
        if cur.val == nameA:
            print(' -> '.join(path))
            return distance
        for neighbor in cur.neighbors:
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor.val + ' [' + nodeTypes[neighbor.nodeType] + ']'], distance + 1 if neighbor.nodeType == 1 else distance))
                visited.add(neighbor)

def averageBaconNumber(graph, nameA='Bacon, Kevin'):
    """run bfs to find the average A-number (by default, Kevin-Bacon-number) of all the other actors 
    and display the movie-actor chain to A whenever find anohter actor

    Parameters
    ----------        
    graph:
        a graph representing actor-movie relationships
    nameA: string
        actor name A

    Returns
    -------
    int
        average A-number (by default, Kevin-Bacon-number)
    """
    queue = deque()
    visited = set()
    queue.append((graph[nameA], 0))
    visited.add(graph[nameA])
    distances = 0
    actorCount = 0
    while len(queue) > 0:
        cur, distance = queue.popleft()
        if cur.nodeType == 1:
            distances += distance
            actorCount += 1
        for neighbor in cur.neighbors:
            if neighbor not in visited:
                queue.append((neighbor, distance + 1 if neighbor.nodeType == 1 else distance))
                visited.add(neighbor)
    return distances / (actorCount - 1)

def main():
    fileList = ['ActionCast.txt', 'BaconCastFull.txt', 'BaconCast_00_06.txt', 'Bacon_06.txt', 'PopularCast.txt']
    fileName = None
    while fileName not in fileList:
        fileName = input('Please input the name of the file to be used from [{}]: '.format(', '.join(fileList))).strip()
    graph = loadData('./BaconData/' + fileName)
    option = None
    while option not in ['1', '2']:
        option = input('Please input 1 or 2 to select from the following options: 1) find the shortest path from actor A to actor B, 2) find the average shortest path of all actors to Kevin Bacon: ').strip()
    if option == '1':
        actors = []
        while len(actors) < 2 or actors[0] not in graph or actors[1] not in graph:
            actors = input('Please input 2 actor names occurred in {}, and split them by /, for example, "Bacon, Kevin/Smith, Will (I)":\n'.format(fileName)).strip().split('/')
        baconNum = calculateBaconNumber(graph, actors[0], actors[1])
        print('The {}-number of {} is: {}'.format(actors[0], actors[1], baconNum))
    else:
        avgBaconNum = averageBaconNumber(graph)
        print('The average Kevin-Bacon-number is: {}'.format(avgBaconNum))

if __name__ == '__main__':
    main()
