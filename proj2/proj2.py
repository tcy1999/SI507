#
# Name: Chenyun Tao
#

from Proj2_tree import printTree

#
# The following two trees are useful for testing.
#
smallTree = \
    ("Is it bigger than a breadbox?",
        ("an elephant", None, None),
        ("a mouse", None, None))
mediumTree = \
    ("Is it bigger than a breadbox?",
        ("Is it gray?",
            ("an elephant", None, None),
            ("a tiger", None, None)),
        ("a mouse", None, None))

def main():
    """
    * Prints a welcome message
    * Asks the user if they would like to load a tree from a file
    * If the user didn't want to load from a file, the initial tree should be the smallTree
    * Plays the game
    * Asks the user if they would like to play again, in which case we play again with
    the new tree
    * When the user is done playing, asks the user if they would like to save the file, in
    which case the user is queried for a file name and the file is saved
    """
    # Write the "main" function for 20 Questions here.  Although
    # main() is traditionally placed at the top of a file, it is the
    # last function you will write.
    print("Welcome to 20 Questions!")
    tree = smallTree
    if yes("Would you like to load a tree from a file?"):
        fileName = input("What's the name of the file? ").strip()
        treeFile = open(fileName, "r")
        tree = loadTree(treeFile)
        treeFile.close()
    while True:
        tree = play(tree)
        if not yes("Would you like to play again?"):
            break
    if yes("Would you like to save this tree for later?"):
        fileName = input("Please enter a file name: ").strip()
        treeFile = open(fileName, "w")
        tree = saveTree(tree, treeFile)
        treeFile.close()
        print("Thank you! The file has been saved.")
    print("Bye!")

def isLeaf(tree):
    """returns True if the tree is a leaf and False if it is an internal node.

    Parameters
    ----------        
    tree: 
        a tree or a sub-part of a tree

    Returns
    -------
    Boolean
        whether the tree is a leaf 
    """
    _, left, right = tree
    return left is None and right is None

def yes(prompt):
    """uses the prompt to ask the user a yes/no question

    Parameters
    ----------        
    prompt: string
        input prompt for the user

    Returns
    -------
    Boolean
       True if the answer is yes, False if it is no
    """
    answer = input(prompt + ' ')
    if answer.strip().lower() in ['yes', 'y', 'yup', 'sure']:
        return True
    return False

def simplePlay(tree):
    """plays the game once by using the tree to guide its questions,
    and returns True if the computer guessed the answer

    Parameters
    ----------        
    tree: 
        a tree or a sub-part of a tree

    Returns
    -------
    Boolean
        whether the computer guessed the answer
    """
    text, left, right = tree
    if isLeaf(tree):
        return yes("Is it {}?".format(text))
    else:
        if yes(text):
            return simplePlay(left)
        return simplePlay(right)
    
def play(tree):
    """plays the game once by using the tree to guide its questions,
    and returns a new tree that is the result of playing the game on the original tree 
    and learning from the answers

    Parameters
    ----------        
    tree: 
        a tree or a sub-part of a tree

    Returns
    -------
    tree
        a new tree that is the result of playing the game on the original tree 
        and learning from the answers
    """
    text, left, right = tree
    if isLeaf(tree):
        if yes("Is it {}?".format(text)):
            print("I got it!")
            return tree
        newObject = input("Drats! What was it? ").strip()
        question = input("What's a question that distinguishes between {} and {}? ".format(newObject, text)).strip()
        if yes("And what's the answer for {}?".format(newObject)):
            return (question, (newObject, None, None), tree)
        return (question, tree, (newObject, None, None))
    else:
        if yes(text):
            left = play(left)
        else:
            right = play(right)
        return (text, left, right)
    
def saveTree(tree, treeFile):
    """saves the tree to a file

    Parameters
    ----------        
    tree: 
        a tree or a sub-part of a tree
    treeFile:
        a handle of a file that is open for writing

    Returns
    -------
    None
    """
    text, left, right = tree
    if isLeaf(tree):
        print("Leaf\n{}".format(text), file = treeFile)
    else:
        print("Internal Node\n{}".format(text), file = treeFile)
        saveTree(left, treeFile)
        saveTree(right, treeFile)

def loadTree(treeFile):
    """loads a tree from a given file

    Parameters
    ----------        
    treeFile:
        a handle of a file that is open for reading

    Returns
    -------
    tree
    """
    line = treeFile.readline().strip()
    text = treeFile.readline().strip()
    if line == 'Leaf':
        return (text, None, None)
    else:
        left = loadTree(treeFile)
        right = loadTree(treeFile)
        return (text, left, right)

#
# The following two-line "magic sequence" must be the last thing in
# your file.  After you write the main() function, this line it will
# cause the program to automatically play 20 Questions when you run
# it.
#
if __name__ == '__main__':
    main()
