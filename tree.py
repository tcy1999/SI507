import json

class TreeNode():
  def __init__(self, groups=[], left=None, right=None, movies=[]):
    self.groups = groups  # for leaf nodes, len(groups) == 1
    self.left = left
    self.right = right
    self.movies = movies  # only leaf nodes have this attribute

treeGroups = {
    'language': ['French', 'Italian', 'Japanese', 'English',  'German', 'Other'],
    'yearGroup': ['Before 1970'] + ['{} - {}'.format(x, x + 9) for x in range(1970, 2020, 10)], 
    'ratingGroup': ['N/A', '< 5.0'] + ['{} - {}'.format(x, x + 0.9) for x in range(5, 10)], 
    'runtimeGroup': ['N/A', '< 85 min', '< 95 min', '< 105 min', '>= 105 min']
}

def buildTree(treeType, groups):
    """build a tree given the type of the tree
    for each internal node, the groups are divided into two halves,
    for each leaf node, the attribute movies contains the movies of a specific group

    Parameters
    ----------        
    treeType: 
        the type of a tree, possible values: ['language', 'yearGroup', 'ratingGroup', 'runtimeGroup']
    groups:
        the possible groups given the treeType, treeGroups[treeType]

    Returns
    -------
    TreeNode
    """
    with open('cache/{}.json'.format(treeType)) as file:
        cache = json.load(file)
    def buildHelper(curGroups):
        mid = len(curGroups) // 2
        if len(curGroups) > 1:
            left = buildHelper(curGroups[:mid])
            right = buildHelper(curGroups[mid:])
        else:
            left = right = None
        root = TreeNode(curGroups, left, right)
        if len(curGroups) == 1:
            root.movies = cache[curGroups[0]]
        return root
    return buildHelper(groups)

def serialize(cur):
    """serialize a tree to a dictionary

    Parameters
    ----------        
    cur: 
        a TreeNode

    Returns
    -------
    a dictionary representing the tree
    """
    if cur.left is None and cur.right is None:
        return {
            'nodeType': 'leaf', 
            'groups': cur.groups, 
            'movies': cur.movies
        }
    else:
        return {
            'nodeType': 'internal', 
            'groups': cur.groups, 
            'left': serialize(cur.left),
            'right': serialize(cur.right)
        }

def saveTree(root, treeFile):
    """save the tree to a file

    Parameters
    ----------        
    root: 
        the root node of a tree
    treeFile:
        filename of a file that will be open for writing

    Returns
    -------
    None
    """
    treeDict = serialize(root)
    with open(treeFile, 'w') as file:
        json.dump(treeDict, file)

def deserialize(treeDict):
    """deserialize a tree from a dictionary

    Parameters
    ----------        
    treeDict: 
        a dictionary representing the tree

    Returns
    -------
    TreeNode
    """
    if treeDict['nodeType'] == 'leaf':
        return TreeNode(treeDict['groups'], None, None, treeDict['movies'])
    else:
        return TreeNode(treeDict['groups'], deserialize(treeDict['left']), deserialize(treeDict['right']))

def loadTree(treeFile):
    """load a tree from a given file

    Parameters
    ----------        
    treeFile:
        filename of a file that will be open for reading

    Returns
    -------
    TreeNode
    """
    with open(treeFile) as file:
        tree = json.load(file)
    return deserialize(tree)

def main():
    for treeType, groups in treeGroups.items():
        root = buildTree(treeType, groups)
        saveTree(root, 'trees/{}.json'.format(treeType))
    # for treeType in treeGroups:
    #     print(loadTree('trees/{}.json'.format(treeType)).groups)

if __name__ == '__main__':
    main()