import os.path
import sys
import json
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re

class DictionaryBuilding:

    def __init__(self, path, stopwords=False, stemming=False, normalization=False):
        self.path=path
        self.stopwords = stopwords
        self.stemming = stemming
        self.normalization = normalization

    @staticmethod
    def remove_stopwords(tokens):
        stoplist = set(stopwords.words('english')+stopwords.words('french'))
        filtered=[]
        for token in tokens:
            if token not in stoplist:
                filtered.append(token)
        return filtered

    @staticmethod
    def stem(tokens):
        ps = PorterStemmer()
        stemmed=[]
        for token in tokens:
            stemmed.append(ps.stem(token))
        return stemmed

    @staticmethod
    def normalize(tokens):
        normalized=[]
        for token in tokens:
            normalized.extend(re.split('[-.]',token))
        return normalized

    def build(self):
        file = open(self.path, 'r')
        collection = json.load(file)
        file.close()
        dictionary = {}

        for doc in collection['documents']:
            tokenized=list(filter(None, re.split('[ .,/()_&#!@?;:]', str(doc['description']).lower())))
            if self.normalization:
                tokenized=self.normalize(tokenized)
            if self.stopwords:
                tokenized=self.remove_stopwords(tokenized)
            if self.stemming:
                tokenized=self.stem(tokenized)

            dictionary[doc['docID']] = tokenized

        return dictionary


def main():
    path = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "\\parsed\\ComputerScience(CSI)uOttawa.json"
    builder = DictionaryBuilding(path, True, True, True)
    print(builder.build())


if __name__ == '__main__':
    main()
