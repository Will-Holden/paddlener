from threading import Lock
from tools.Jieba import Jieba

class JiebaService:
    _instance = None
    _lock = Lock()

    @classmethod
    def instance(cls):
        if JiebaService._instance is None:
            with JiebaService._lock:
                if JiebaService._instance is None:
                    JiebaService._instance = cls()
        return JiebaService._instance

    def __init__(self):
        self.jieba = Jieba()

    def segment(self, doc):
        return self.jieba.segment(doc)

    def postag(self, doc):
        if type(doc) == list:
            doc = "".join(doc)
        words = self.jieba.postag(doc)
        tags = [flag for word, flag in words]
        return tags

