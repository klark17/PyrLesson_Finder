from pyramid.session import JSONSerializer
from pyramid.session import PickleSerializer


class JSONSerializerWithPickleFallback(object):
    def __init__(self):
        self.json = JSONSerializer()
        self.pickle = PickleSerializer()

    def dumps(self, value):
        return self.pickle.dumps(value)

    def loads(self, value):
        return self.pickle.loads(value)