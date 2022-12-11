import json

class TreeNode():
  def __init__(self, groups=[], left=None, right=None, movies=[]):
    self.groups = groups  # for leaf nodes, this attribute.length == 1
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
    """
    TODO: write comments
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

def saveTree(root, treeFile):
    """
    TODO: write comments
    """
    if root.left is None and root.right is None:
        print("Leaf\n{}\n{}".format(','.join(root.groups), json.dumps(root.movies)), file=treeFile)
    else:
        print("Internal Node\n{}".format(','.join(root.groups)), file=treeFile)
        saveTree(root.left, treeFile)
        saveTree(root.right, treeFile)

def loadTree(treeFile):
    """
    TODO: write comments
    """
    line = treeFile.readline().strip()
    groups = treeFile.readline().strip().split(',')
    root = TreeNode(groups)
    if line == 'Leaf':
        root.movies = json.loads(treeFile.readline().strip())
        return root
    else:
        root.left = loadTree(treeFile)
        root.right = loadTree(treeFile)
        return root

def main():
    for treeType, groups in treeGroups.items():
        root = buildTree(treeType, groups)
        treeFile = open('trees/{}.txt'.format(treeType), "w")
        saveTree(root, treeFile)
        treeFile.close()
    # for treeType in treeGroups:
    #     treeFile = open('trees/{}.txt'.format(treeType), "r")
    #     print(loadTree(treeFile).groups)
    #     treeFile.close()

if __name__ == '__main__':
    main()