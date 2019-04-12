import json
import os.path
import numpy as np
import nltk
# from sklearn.metrics import jaccard_similarity_score
from models import model
import time
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
        doclen = len(doclist)
        wlist2=[]
        for elem in inverted_index:
            if elem[0][0]==word:
                wlist2 = set([i[0] for i in elem[1]])
                break
        lst1 = bytearray(doclen)
        for i in range(doclen):
            if doclist[i] in wlist2:
                lst1[i] = 1
        for i in range(len(word_set)-1):
            wlist1 = set([i[0] for i in inverted_index[i][1]])
            if word_set[i]==word:
                sim=1
            else:
                sim=self.get_sim(lst1, wlist1, doclist)
            if sim>0:
                result[word_set[i]]=sim
            couter+=1
            # print(couter)
            # print(sim)
            if couter%1000==0:
                print(couter)
        print(result)
        return result

    def get_sim(self, lst1, wlist2, doclst):
        doclen=len(doclst)
        lst2=bytearray(doclen)
        for i in range(doclen):
            if doclst[i] in wlist2:
                lst2[i] = 1

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
    with open('unique_words.json', 'w')as f:
        words=expander.unique_words()
        json.dump(words,f)
    # with open('docvec.json', 'w') as f:
    #     json.dump(expander.get_doc_vector(), f)
    # expander.build_thesaurus()
    # print(expander.build_thesaurus())
    # with open('reuters_theaurus.json', 'w') as f:
    #
    #     json.dump(expander.build_thesaurus(),f, indent=4)

