from threading import Lock
from core.base.data.LSHBasedFixSizeHash import LSHBasedFixSizeHash
from datasketch import MinHash
from services.NLPService import NLPService
from core.Singleton import Singleton


class DistinctTask:

    def __init__(self):
        self.data = LSHBasedFixSizeHash()
        self.nlp_service = NLPService.instance()

    def add(self, data, min_score=0.7):
        docs = self.nlp_service.sentencesize(data)
        words = [word for doc in docs for word in self.nlp_service.seg_words(doc)]
        m = MinHash()
        for word in words:
            m.update(word.encode())
        m_score = self.data.get_max_similar(m)
        self.data.add(m)
        if m_score > min_score:
            return False
        else:
            return True

