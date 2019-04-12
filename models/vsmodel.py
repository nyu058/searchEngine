from models import model
import math
import os.path
from dictionaryBuilding import dictionaryBuilding as db


class VSModel(model.Model):
    def __init__(self):
        super().__init__('vs')

    def calculate_weight(self, index, n):
        for term in index:
            for i in range(len(term[1])):
                term[1][i] = (term[1][i][0], term[1][i][1], self.weight(term[1][i][1], term[0][1], n))

        return index

    @staticmethod
    def weight(tf, df, n):

        return math.log(1 + tf, 10) * math.log(n / df, 10)

    def search(self, query, dic):

        index = VSModel()
        result = []
        index = self.calculate_weight(index.buildIndex(dic), len(dic))
        processedQuery = self.query_processor(query)
        queryweight = []
        for elem in processedQuery:
            queryweight.append(processedQuery.count(elem))

        docVec = self.getDocVec(processedQuery, index)
        for doc in docVec:
            result.append((doc[0], self.innerProduct(queryweight, doc[1])))
        result.sort(key=lambda x: x[1], reverse=True)
        return result

    def query_processor(self, query):

        tokenized=list(filter(None, query.lower().split(' ')))
        return db.DictionaryBuilding.stem(db.DictionaryBuilding.remove_stopwords(tokenized))

    def getDocVec(self, query, index):
        qdoclist = []
        for token in query:
            doclist = self.binarySearch(index, token)

            qdoclist.append(doclist)
        docset = self.unionSet(qdoclist)
        allDocVec = []
        for doc in docset:
            docVec = []
            for qdocs in qdoclist:
                appended = False
                for qdoc in qdocs:
                    if doc == qdoc[0]:
                        docVec.append(qdoc[2])
                        appended = True
                if not appended:
                    docVec.append(0)
            allDocVec.append((doc, docVec))
        return allDocVec

    def innerProduct(self, queryvec, docvec):
        ip = 0
        for i in range(len(queryvec)):
            ip += queryvec[i] * docvec[i]
        return round(ip, 3)

    def binarySearch(self, index, term):
        result = self.binarySearchIter(index, 0, len(index), term)
        if result == -1:
            return []
        else:
            return index[result][1]

    def unionSet(self, lst):
        result = []
        for i in range(len(lst)):
            result = self.union(result, lst[i])
        for i in range(len(result)):
            result[i] = result[i][0]
        seen = set()
        seen_add = seen.add
        return [x for x in result if not (x in seen or seen_add(x))]

    @staticmethod
    def union(l1, l2):
        ptr1 = 0
        ptr2 = 0
        result = []
        while ptr1 < len(l1) and ptr2 < len(l2):
            if l1[ptr1] > l2[ptr2]:
                result.append(l2[ptr2])
                ptr2 += 1
            else:
                result.append(l1[ptr1])
                ptr1 += 1
        while ptr1 < len(l1):
            result.append(l1[ptr1])
            ptr1 += 1
        while ptr2 < len(l2):
            result.append(l2[ptr2])
            ptr2 += 1
        return result

    '''
    modified from: https://www.geeksforgeeks.org/binary-search/
    '''
    @staticmethod
    def binarySearchIter(arr, l, r, x):
        while l <= r:
            mid = l + (r - l) // 2

            if arr[mid][0][0] == x:
                return mid
            elif arr[mid][0][0] < x:
                l = mid + 1
            else:
                r = mid - 1
        return -1


def main():
    path = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "\\parsed\\reuters_parsed.json"
    # path = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "\\parsed\\ComputerScience(CSI)uOttawa.json"
    builder = db.DictionaryBuilding(path, True, False, False)
    indexer = VSModel()
    dic = builder.build()
    i=indexer.buildIndex(dic)
    print(print(len(i)))

    # print(indexer.search('China', dic))


if __name__ == '__main__':
    main()
