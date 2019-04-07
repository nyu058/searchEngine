from dictionaryBuilding import dictionaryBuilding
import os.path


class Model:

    def __init__(self, model):
        self.model = model

    @staticmethod
    def parseIndex(dictionary):
        index = []
        for key in dictionary:
            for term in dictionary[key]:
                index.append((term, key))
        index.sort(key= lambda x: x[0])
        return index

    def buildIndex(self, dictionary):
        boolean_index = []
        sorted = self.parseIndex(dictionary)
        i = 0
        j = 0
        while i < len(sorted):
            docarr = []
            tf = 1
            while j < len(sorted):
                if j == len(sorted) - 1:
                    boolean_index.append(((sorted[j][0], len(docarr)), docarr))
                    return boolean_index
                if sorted[i][0] != sorted[j][0]:
                    boolean_index.append(((sorted[i][0], len(docarr)), docarr))
                    i = j
                    break
                else:
                    if sorted[j][1] != sorted[j + 1][1]:
                        docarr.append((sorted[j][1], tf))
                        tf = 1
                    else:
                        tf += 1
                j += 1

def main():
    path = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "\\parsed\\ComputerScience(CSI)uOttawa.json"
    builder = dictionaryBuilding.DictionaryBuilding(path, True, True, True)
    index=Model('boolean')
    for elem in index.buildIndex(builder.build()):
        print(elem)


if __name__ == '__main__':
    main()
