import json
import nltk
import operator
import os.path
from collections import  Counter

class bigrammodel:

    def __init__(self, bigramsCollection):
        self.bigramsCollection = bigramsCollection

    # to get last word in user query
    # def getCondition(self, query):
    #     queryList = list(query.split(" "))
    #     condition = queryList[len(queryList) - 1]
    #     return condition.lower()

    # to get all recommandations
    def getRecommandations(self, token, n):
        if token in self.bigramsCollection:
            return [elem[0] for elem in self.bigramsCollection[token]][:n]

    # to get a specific number of words as recommandations based on a threshold
    # def getNrecommandation(self, N, query):
    #     recommandations = self.getRecommandations(query)
    #     recList = []
    #     i = 0
    #     for w in recommandations:
    #         if i < N:
    #             recList.append(w[0])
    #             i += 1
    #         else:
    #             break
    #     return recList

    @staticmethod
    def generate_bigram(path):
        bigram={}
        with open(path, 'r')as f:
            collection=json.load(f)
        for doc in collection:
            setOfbigrams=list(nltk.bigrams(collection[doc]))

            for e in setOfbigrams:
                if e[0] in bigram:
                    bigram[e[0]].append(e[1])
                else:
                    bigram[e[0]]=[e[1]]
        for key in bigram:
            bigram[key] = bigrammodel.sort_bigram(bigram[key])

        print(bigram)

        with open('csbigram.json', 'w') as f:
            json.dump(bigram, f)

    @staticmethod
    def sort_bigram(bigram):
        c= Counter(bigram)
        return Counter.most_common(c)


def main():
    # path=os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "\\dictionaryBuilding\\reutersdic.json"
    # cspath = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "\\dictionaryBuilding\\csdic.json"
    # bigrammodel.generate_bigram(cspath)

    # load biragm.json
    with open("reutersbigram.json","r") as f:
        bigramsCollection = json.load(f)
    bigramModel = bigrammodel(bigramsCollection)
    print(bigramModel.getRecommandations('coffee',15))


if __name__ == '__main__':
    main()