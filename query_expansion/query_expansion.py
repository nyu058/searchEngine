import json
import os.path
import numpy as np
import nltk
# from sklearn.metrics import jaccard_similarity_score
from models import  model
import  time
class QueryExpansion:
    def __init__(self, dictionary, inverted_index):
        self.dictionary=dictionary
        self.inverted_index=inverted_index
    def unique_words(self):
        result=set()
        for doc in self.dictionary:
            for word in self.dictionary[doc]:
                result.add(word)
        return list(result)


    def build_thesaurus(self):
        theaurous={}
        word_set=self.unique_words()
        print(len(word_set))
        word_set.sort()
        doclist=[]
        for i in range(19043):
            doclist.append(str(i))

        for word in word_set:
            start=time.time()
            theaurous[word]=self.get_word_sim(word,word_set, doclist)
            end=time.time()
            print(end-start)
    def get_word_sim(self, word, word_set, doclist):
        result={}
        couter=0

        wlist2=[]
        for elem in inverted_index:
            if elem[0][0]==word:
                wlist2 = set([i[0] for i in elem[1]])
                break
        for i in range(len(word_set)-1):
            wlist1 = set([i[0] for i in inverted_index[i][1]])
            sim=self.get_sim(word_set[i], word, wlist1, wlist2, doclist)
            result[word_set[i]]=sim
            couter+=1
            # print(couter)
            # print(sim)
            if couter%1000==0:
                print(couter)
        print(result)
        return result

    def get_sim(self, word1, word2, wlist1, wlist2, doclst):
        if word1==word2:
            return 1
        lst1=[]
        lst2=[]
        for docid in doclst:

            if docid not in wlist1:
                lst1.append(False)
            else:
                lst1.append(True)
            if docid not in wlist2:
                lst2.append(False)
            else:
                lst2.append(True)
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
        print(len(inverted_index))
        expander=QueryExpansion(dic, inverted_index)

    # with open('docvec.json', 'w') as f:
    #     json.dump(expander.get_doc_vector(), f)
    expander.build_thesaurus()
    # print(expander.build_thesaurus())
    with open('reuters_theaurus.json', 'w') as f:

        json.dump(expander.build_thesaurus(),f, indent=4)

