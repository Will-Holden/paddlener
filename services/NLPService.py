import re
from zhon import hanzi
import string
from threading import Lock
from services.tool_services.JiebaService import JiebaService


class NLPService:
    _instance = None
    _lock = Lock()

    @classmethod
    def instance(cls):
        if NLPService._instance is None:
            with NLPService._lock:
                if NLPService._instance is None:
                    NLPService._instance = cls()
        return NLPService._instance

    def __init__(self):
        self.stop_words = {}
        self.word_list = []
        self.nlp_core = JiebaService.instance()

    def seg_words(self, doc):
        return [word for word in self.nlp_core.segment(doc)]

    def tag_words(self, words):
        return [tag for tag in self.nlp_core.postag(words)]

    def recongize(self, words, tags):
        return [entity_tag for entity_tag in self.nlp_core.recognize(words, tags)]

    def sentencesize(self, doc):
        """
        分割文本为一个个的句子
        :param doc:
        :return:
        """
        if not type(doc) == str:
            return
        doc_origin = re.sub(r' +|	+|　+', '', doc.replace('\n', ' '))
        doc_origin = re.sub(r"[%s]+" % (hanzi.non_stops + string.punctuation), "", doc_origin)
        docs = [doc for doc in re.split(r'[%s]+' % (hanzi.stops), doc_origin) if len(doc) >= 1]
        return docs
