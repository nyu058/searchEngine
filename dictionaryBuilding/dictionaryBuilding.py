import os.path
import sys
import json
from nltk.corpus import stopwords, words
from nltk.stem import PorterStemmer
import re

class DictionaryBuilding:

    def __init__(self, path, stopwords=False, stemming=False, normalization=False):
        self.path = path
        self.stopwords = stopwords
        self.stemming = stemming
        self.normalization = normalization

    @staticmethod
    def remove_stopwords(tokens):
        stoplist = set(stopwords.words('english') + stopwords.words('french'))
        filtered = []
        for token in tokens:
            if token not in stoplist:
                filtered.append(token)
        return filtered

    @staticmethod
    def stem(tokens):
        ps = PorterStemmer()
        stemmed = []
        for token in tokens:
            stemmed.append(ps.stem(token))
        return stemmed

    @staticmethod
    def normalize(tokens):
        normalized = []
        for token in tokens:
            normalized.extend(filter(None, re.split('[-.]', token)))
        return normalized

    def build(self):
        file = open(self.path, 'r')
        collection = json.load(file)
        file.close()
        dictionary = {}
        engword = set(words.words())
        for doc in collection['documents']:
            tokenized = list(filter(None, re.split('[ .,/()_&#!@?;:""]', str(doc['description']).lower())))

            if self.normalization:
                tokenized = self.normalize(tokenized)
            if self.stopwords:
                tokenized = self.remove_stopwords(tokenized)
            if self.stemming:
                tokenized = self.stem(tokenized)

            dictionary[doc['docID']] = [token for token in tokenized if token.isalpha() and (token not in engword) and (len(token)<16)]

        return dictionary


def main():
    path = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "\\parsed\\ComputerScience(CSI)uOttawa.json"
    pathreuter = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "\\parsed\\reuters_parsed.json"
    builder = DictionaryBuilding(pathreuter, True, True, False)
    csdic_path =os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "\\dictionaryBuilding\\csdic.json"
    reutersdic_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "\\dictionaryBuilding\\reutersdic.json"
    with open(reutersdic_path, 'w') as f:
        dic=builder.build()
        json.dump(dic, f)

if __name__ == '__main__':
    main()
