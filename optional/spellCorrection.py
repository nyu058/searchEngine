from nltk.corpus import words
import os.path
from models import booleanmodel
from dictionaryBuilding import dictionaryBuilding
'''
modified from: http://norvig.com/spell-correct.html
'''



def edits(word, index):
    "All edits that are two edits away from `word`."
    dic={}
    mindist=999
    for elem in index:
        if elem[0][0][0]==word[0]:
            curdist=minDistance(elem[0][0], word)
            dic[elem[0][0]]=curdist
            if curdist<mindist:
                mindist=curdist

    result=[]
    for elem in dic:
        if dic[elem]==mindist:

            result.append(elem)
    return result

'''
modified from: https://leetcode.com/problems/edit-distance/discuss/159295/Python-solutions-and-intuition
'''
def minDistance(word1, word2):
    """Naive recursive solution"""
    if not word1 and not word2:
        return 0
    if not word1:
        return len(word2)
    if not word2:
        return len(word1)
    if word1[0] == word2[0]:
        return minDistance(word1[1:], word2[1:])
    insert = 1 + minDistance(word1, word2[1:])
    delete = 1 + minDistance(word1[1:], word2)
    replace = 1 + minDistance(word1[1:], word2[1:])
    return min(insert, replace, delete)


def main():
    path = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "\\parsed\\ComputerScience(CSI)uOttawa.json"
    builder = dictionaryBuilding.DictionaryBuilding(path, True, False, True)
    indexer = booleanmodel.BooleanModel()
    index=indexer.buildIndex(builder.build())
    print(edits('operatng', index))

if __name__ == '__main__':
    main()