from indexing import indexer
import os.path
from dictionaryBuilding import dictionaryBuilding

class BooleanIndexer(indexer.Indexer):
    def __init__(self):
        super().__init__('boolean')

    def buildIndex(self, dictionary):
        boolean_index=[]
        sorted=self.parseIndex(dictionary)
        i=0
        j=0
        while i <len(sorted):
            while j<len(sorted):
                if sorted[i][0]!=sorted[j][0]:
                    boolean_index.append((sorted[i][0], j-i))
                    i=j
                    break
                if j==len(sorted)-1:
                    boolean_index.append((sorted[j][0], j-i+1))

                    return boolean_index

                j += 1
            # print(boolean_index)




def main():
    path = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "\\parsed\\ComputerScience(CSI)uOttawa.json"
    builder = dictionaryBuilding.DictionaryBuilding(path, True, True, True)
    indexer = BooleanIndexer()
    print(indexer.buildIndex(builder.build()))

if __name__ == '__main__':
    main()