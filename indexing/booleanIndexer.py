from .indexer import Indexer
import os.path
from dictionaryBuilding import dictionaryBuilding

class BooleanIndexer(Indexer):
    def __init__(self,):
        super().__init__('boolean')

    def buildIndex(self, dictionary):
        boolean_index=[]
        for tuple in self.parseIndex(dictionary):




def main():
    path = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "\\parsed\\ComputerScience(CSI)uOttawa.json"
    builder = dictionaryBuilding.DictionaryBuilding(path, True, True, True)
    indexer = BooleanIndexer()
    print(indexer.buildIndex(builder.build()))

if __name__ == '__main__':
    main()