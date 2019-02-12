from dictionaryBuilding import dictionaryBuilding
import os.path

class Indexer:

    def __init__(self, model):
        self.model=model


    @staticmethod
    def parseIndex(dictionary):
        index = []
        for key in dictionary:
            for term in dictionary[key]:
                pos=len(index)
                for i in range(len(index)):
                    if index[i][0]>term:
                        pos=i
                        break
                index.insert(pos, (term,key))

        return index

def main():
    path = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "\\parsed\\ComputerScience(CSI)uOttawa.json"
    builder = dictionaryBuilding.DictionaryBuilding(path, True, True, True)
    print(Indexer.parseIndex(builder.build()))


if __name__ =='__main__':
    main()