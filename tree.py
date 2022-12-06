import json

class TreeNode():
  def __init__(self, group=None, movies=[], left=None, right=None):
    self.group = group
    self.movies = movies
    self.left = left
    self.right = right

def buildTree(treeType, groups):
    with open('data.json') as file:
        cache = json.load(file)
    temp = {}
    for group in groups:
        temp[group] = []
    for key in cache:
        group = cache[key][treeType]
        if len(temp[group]) == 50:
            continue
        temp[group].append(cache[key])
    root = TreeNode(groups[0], left=TreeNode(None, temp[groups[0]]))
    cur = root
    for group in groups[1:]:
        cur.right = TreeNode(group, left=TreeNode(None, temp[group]))
        cur = cur.right
    return root

def saveTree(root, fileName):
    pass

def loadTree(fileName):
    pass

def main():
    buildTree('language', ['English', 'French', 'Italian', 'Japanese', 'German', 'Other'])
    buildTree('year', ['Before 1970'] + ['{} - {}'.format(x, x + 9) for x in range(1970, 2020, 10)])
    buildTree('rating', ['N/A', '< 5.0'] + ['{} - {}'.format(x, x + 0.9) for x in range(5, 10)])
    buildTree('runtime', ['N/A', '< 85 min', '< 95 min', '< 105 min', '>= 105 min'])
