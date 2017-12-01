#-*-coding:utf-8-*-
from gensim.models import Word2Vec
class PrefixQuery(object):
    def __init__(self, words={}):

        self.prefix_dict = {}
        self.label_dict = {}
        self._init(words)
        # print(self.prefix_dict)

    def _init(self, words):
        for word in words:
            self.insert(word)

    def insert(self, word, label=''):
        len_w = len(word)
        for i in range(1, len_w + 1):
            w = word[:i]
            if i == len_w:
                self.prefix_dict[w] = 1
                if label:
                    self.label_dict[w] = label
            elif w not in self.prefix_dict:
                self.prefix_dict[w] = 0

    def query_words(self, text):
        t_len = len(text)
        matchs = []
        i = 0
        result_word = ""
        result_index = -1
        while i < t_len - 1:
            for j in range(i + 1, t_len + 1):
                word = text[i:j]
                
                if word not in self.prefix_dict:
                    if result_word:
                        matchs.append([result_word + '_' + self.label_dict[result_word], (result_index, result_index + len(result_word) - 1)])
                        i = result_index + len(result_word) - 1
                        result_word = ""
                        result_index = -1
                    break
                if self.prefix_dict.get(word) == 1:
                    result_word = word
                    result_index = i
                    # print(result_word + '\t' + str(result_index))
            i += 1
        if result_word:
            matchs.append([result_word + '_' + self.label_dict[result_word], (result_index, result_index + len(result_word) - 1)])
        #print(matchs)
        return matchs



#query = PrefixQuery()
#query.insert(u"心态浮躁", "label")
#print(query.prefix_dict)

#text = u"珍格格心态浮躁"
#res = query.query_words(text)
#print(res)
