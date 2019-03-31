from models import model
import os.path
from dictionaryBuilding import dictionaryBuilding

class BooleanModel(model.Model):
    def __init__(self):
        super().__init__('boolean')

    '''
    modified from: http://interactivepython.org/runestone/static/pythonds/BasicDS/InfixPrefixandPostfixExpressions.html
    '''
    @staticmethod
    def toPostFix(tokens):
        operators = {'and', 'or', 'not'}
        brackets = {'(', ')'}
        prec = {'(': 1, 'and': 2, 'or': 2, 'not': 3}
        opstack = []
        result = []
        for token in tokens:

            if token not in operators | brackets:
                result.append(token)
            elif token == '(':
                opstack.append(token)
            elif token == ')':
                top = opstack.pop()
                while top != '(':
                    result.append(top)
                    top = opstack.pop()
            else:
                while opstack and (prec[opstack[-1]] >= prec[token]):
                    result.append(opstack.pop())
                opstack.append(token)
        while opstack:
            result.append(opstack.pop())
        return result

    def query_processor(self, query, index):
        tokenized = list(filter(None, query.lower().split(' ')))
        # tokenized = dictionaryBuilding.DictionaryBuilding.stem(
        #     dictionaryBuilding.DictionaryBuilding.normalize(tokenized))
        for i in range(len(tokenized)):

            if tokenized[i][-1]=='*':
                wc=self.wildcard(tokenized[i][0:-1], index)
                tokenized[i]=wc
        tokenized=list(self.flatten(tokenized))
        return self.toPostFix(tokenized)

    def wildcard(self, token, index):
        result=[]
        count=0
        for word in index:
            if word[0][0][:len(token)] == token:
                result.append('(')
                result.append(word[0][0])
                result.append('or')
                count+=1
        result.pop()
        for i in range(count):
            result.append(')')
        return result

    def search(self, query, options, dic):

        index = self.buildIndex(dic)
        print(dic)
        processed = self.query_processor(query, index)
        print(processed)
        operators = {'and', 'or', 'not'}
        tojoin = []
        for elem in processed:

            if elem not in operators:
                tojoin.append(self.getDocList(index, elem))
            elif elem == 'and':
                joined = self.intersect(tojoin[-1], tojoin[-2])
                tojoin.pop()
                tojoin.pop()
                tojoin.append(joined)
            elif elem == 'or':
                joined = self.union(tojoin[-1], tojoin[-2])
                tojoin.pop()
                tojoin.pop()
                tojoin.append(joined)
            else:
                joined = self.negation(tojoin[-1], dic)
                tojoin.pop()
                tojoin.append(joined)
                print(joined)


        return tojoin[0]


    def getDocList(self, index, token):
        result=[]
        for elem in index:
            if elem[0][0] == token:
                for docid in elem[1]:
                    result.append(docid[0])
                return result
    @staticmethod
    def negation(lst, dic):
        result=[]
        lst=set(lst)
        for elem in dic.keys():
            if elem not in lst:
                result.append(elem)
        return result

    @staticmethod
    def union(l1, l2):
        ptr1 = 0
        ptr2 = 0
        result = []
        if not l2:
            return l1
        if not l1:
            return l2
        if l1 and l2:
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


    @staticmethod
    def intersect(l1, l2):
        if not l2:
            return l1
        if not l1:
            return l2
        result = []
        if l1 and l2:
            for elem in l1:
                if elem in l2:
                    result.append(elem)
        return result
    '''
    from :https://stackoverflow.com/questions/2158395/flatten-an-irregular-list-of-lists
    '''
    @staticmethod
    def flatten(alist):
        for item in alist:
            if isinstance(item, list):
                for subitem in item: yield subitem
            else:
                yield item


def main():
    path = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "\\parsed\\ComputerScience(CSI)uOttawa.json"
    builder = dictionaryBuilding.DictionaryBuilding(path, True, True, True)
    indexer = BooleanModel()
    #print(indexer.buildIndex(builder.build()))
    #print(indexer.query_processor('not thread and ( Operating or system )'))
    print(indexer.search(' graphics or ( not opera* and system )', [True, False, True]))


if __name__ == '__main__':
    main()
