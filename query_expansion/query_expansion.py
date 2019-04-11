import json
import os.path
import numpy as np
import nltk
from sklearn.metrics import jaccard_similarity_score
from models import  model
class QueryExpansion:
    def __init__(self, dictionary, inverted_index):
        self.dictionary=dictionary
        self.inverted_index=inverted_index
    def unique_words(self):
        result=set()
        for doc in self.dictionary:
            for word in self.dictionary[doc]:
                result.add(word)
        return result


    def build_thesaurus(self):
        theaurous={}
        word_set=self.unique_words()
        doclist=[]
        for i in range(19043):
            doclist.append(str(i))

        for word in word_set:
            theaurous[word]=self.get_word_sim(word,word_set, doclist)

    def get_word_sim(self, word, word_set, doclist):
        result=[]
        couter=0
        for elem in word_set:
            sim=self.get_sim(word, elem, doclist)
            result.append((elem,sim))
            couter+=1
            # print(couter)
            # print(sim)
            if couter%1000==0:
                print(couter)
        print(result)
        return result

    def get_sim(self, word1, word2, doclst):
        if word1==word2:
            return 1
        lst1=[]
        lst2=[]
        for elem in self.inverted_index:
            if elem[0][0]==word1:
                wlist = set([i[0] for i in elem[1]])
                for docid in doclst:

                    if docid not in wlist:
                        lst1.append(False)
                    else:
                        lst1.append(True)
                break

        for elem in self.inverted_index:

            if elem[0][0]==word2:
                wlist = set([i[0] for i in elem[1]])
                for docid in doclst:

                    if docid not in wlist:
                        lst2.append(False)
                    else:
                        lst2.append(True)
                break

        # print(len(lst1),len(lst2))
        return self.jaccard(lst1,lst2)


    def get_doc_vector(self):
        word_set = self.unique_words()
        vec={}
        doclst=[]
        for i in range(19043):
            doclst.append(str(i))
        for word in word_set:
            lst=[]
            for elem in self.inverted_index:
                if elem[0][0] == word:
                    wlist = set([i[0] for i in elem[1]])
                    for docid in doclst:

                        if docid not in wlist:
                            lst.append(False)
                        else:
                            lst.append(True)
                    break
            vec[word]=lst
            print(word, lst)
        return vec

    @staticmethod
    # def jaccard(lst1, lst2):
    #     count=0
    #     diff=0
    #     for i in range(19043):
    #         if lst1[i] and lst2[i]: #same and 1
    #             count+=1
    #         elif (not lst1[i] and lst2[i]) or (lst1[i] and not lst2[i]): #one of them has 1 and diff
    #             diff+=1
    #     return count/diff
    def jaccard(lst1, lst2):
        lst1=np.asarray(lst1)
        lst2=np.asarray(lst2)
        return np.double(np.bitwise_and(lst1, lst2).sum())/ np.double(np.bitwise_or(lst1, lst2).sum())



if __name__ == '__main__':
    reuterdicpath = os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))) + "\\dictionaryBuilding\\reutersdic.json"
    with open(reuterdicpath, 'r') as f:
        dic=json.load(f)
        inverted_index=model.Model('vsm').buildIndex(dic)
        expander=QueryExpansion(dic, inverted_index)

    # with open('docvec.json', 'w') as f:
    #     json.dump(expander.get_doc_vector(), f)
    print(expander.build_thesaurus())
    # print(expander.build_thesaurus())
    # with open('reuters_theaurus.json', 'w') as f:
    #
    #     json.dump(expander.build_thesaurus(),f, indent=4)

