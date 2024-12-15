class Item:
    """Classe générale des objets"""
    nbr = 0

    def __init__(self, targs, stat):
        self._name = targs['name']
        self._type = targs['type']
        self._space = targs['space']
        self._stat = stat
        Item.nbr += 1

    def __str__(self):
        return self._name


class Equipment(Item):
    """Classe pour gérer les équipements"""
    def __init__(self, targs, stat):
        super().__init__(targs, stat)
        self._lClasses = targs['classList']
        self._place = targs['place']


class Bag:
    """Classe pour gérer le sac des objets"""
    def __init__(self, args):
        self._sizeMax = args['sizeMax']
        self._lItems = args['items']
        self._size = len(self._lItems)

    def addItem(self, item):
        if self._size < self._sizeMax:
            self._lItems.append(item)
            self._size += 1
        else:
            return False

    def delItem(self, index):
        self._lItems.pop(index)
        self._size -= 1

    def __str__(self):
        output = ""
        for item in self._lItems:
            output += str(item) + " "
        return output.strip()
