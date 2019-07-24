import os
import platform
import jieba
import jieba.posseg as pseg
from utils.Logger import logging
from settings import BASE_DIR

class Jieba:
    def __init__(self, user_dict = None):
        user_dict_path = os.path.join(BASE_DIR, 'resources', 'lexicon')
        if user_dict is not None:
            self.verify_dict(user_dict_path, user_dict)
            jieba.set_dictionary(user_dict_path)

    def segment(self, doc):
        return jieba.cut(doc)

    def postag(self, doc):
        return pseg.cut(doc)


    def verify_dict(self, user_dict_path, user_dict):
        with open(user_dict_path, 'w+', encoding='utf-8') as f:
            word_list = f.read().split('\n')
            word_not_in_dict = set(user_dict) - set(word_list)
            if word_not_in_dict:
                logging.warning("there is {0}s word not in dict, adding them".format(len(word_not_in_dict)))
                f.write("\n".join(word_not_in_dict))
        pass
