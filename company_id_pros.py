# -*- coding: UTF-8 -*-
import codecs
import os
import re
from multi_match import PrefixQuery
from snownlp import SnowNLP
from collections import Counter
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import chardet

class get(object):
    
    def __init__(self):
        self.pattern = re.compile(r',|，|\\.|。|\\?|？|:|：|!|！|、|.|')
        
          
    def cut_words(self,text):
        pattern = self.pattern
        result = re.split(pattern,text)
        for data in result:
            if ' ' in data:
                cut_data = data
                result.remove(data)
                cut_data = cut_data.split(' ')
                result.append('\t'.join(cut_data))
        if '<br>' in result:
            result = re.sub(r'<br>','',result) 
        if '</br>' in result:
            result = re.sub(r'</br>','',result)
        if '<br/>' in result:
            result = re.sub(r'<br/>','',result)
        save = '\t'.join(result)
        return save

    
    
    def read_dictionary(self,f_position,label):
        dictionary = []
        f_read = open(f_position)
        for data in f_read.readlines():
            data = data.strip()
            dictionary.append(data)
        
        seacher = PrefixQuery(dictionary)
        
        for word in dictionary:
            seacher.insert(word,label)
        return dictionary,seacher
                                                        
    
    
    def get_emotion_words(self,text):
        
        dictionary_emotion_high,seacher_emotion_high = self.read_dictionary('./tag_high_review_emotion.txt','emotion_high')
        dictionary_emotion_low,seacher_emotion_low = self.read_dictionary('./tag_low_review_emotion.txt','emotion_low')
        dictionary_review,seacher_review = self.read_dictionary('./tag_review.txt','review')
#        for word in dictionary_emotion_low:
#            print(word)
#            print(type(word))
        line = text
        word_low_emotion  = []  #存储低方面词所在句子的情感值
        word_high_emotion = []  #存储高方面词所在句子情感值
        dictionary_high_emotion = [] #存储词典方面词+情感词为高兴的词
        dictionary_low_emotion  = [] #存储词典方面词+情感词为低落的词
        line = line.strip().split('\t')
        
        for data in line:
            words = data         
            data = data.decode('utf-8')
            try:
                if data != '':
                    s = SnowNLP(data)
                    print(data + '\t' + str(s.sentiments))
                    if len(seacher_emotion_high.query_words(words)) >= 1:
                        for detail_word in seacher_emotion_high.query_words(words): 
                            dictionary_high_emotion.append(detail_word[0].split('_')[0] + '\t' + str(s.sentiments) + '\t' + str(data))
                    
                
                    elif len(seacher_emotion_low.query_words(words)) > 0:
                        for detail_word in seacher_emotion_low.query_words(words):
                            dictionary_low_emotion.append(detail_word[0].split('_')[0] + '\t' + str(1-s.sentiments) + '\t' + str(data))
                            #词典部分数据处理


                    elif s.sentiments <= 0.2 and len(data) <= 50:
                        if len(seacher_review.query_words(words)) >= 1:   #判断有没有方面词
                            for detail_word in seacher_review.query_words(words):
                                word_low_emotion.append(detail_word[0].split('_')[0] + '\t' + str(1-s.sentiments) + '\t' + str(data))
                    
                    elif s.sentiments >= 0.8 and len(data) <= 50: #分句词数小于25比较准确
                        if len(seacher_review.query_words(words)) >= 1 :             #判断有没有方面词
                            for detail_word in seacher_review.query_words(words):
                                word_high_emotion.append(detail_word[0].split('_')[0] + '\t' + str(s.sentiments) + '\t' + str(data))
            except Exception as e:
                print(e)

            
        result_high = []
        result_low  = []
        
        for data in dictionary_low_emotion:
            print(data)


        if len(dictionary_high_emotion) >= 1:
            for line in dictionary_high_emotion:
                line = line.split('\t')
                result_high.append(line[0] +'\t' + str(0.8*(float(line[1]))) + '\t' + line[2])
        if len(word_high_emotion) >= 1:
            for line in word_high_emotion:
                line = line.split('\t')
                result_high.append(line[0] + '\t' + str(0.4*(float(line[1]))) + '\t' + line[2])
        #得到情感词正向的情感和分值以及在句子中的位置
        if len(dictionary_low_emotion) >= 1:
            #print('1')
            for line in dictionary_low_emotion:
                line = line.split('\t')
                result_low.append(line[0] + '\t' + str(0.8*(float(line[1])))  + '\t' + line[2])
        
        if len(word_low_emotion) >= 1:
            for line in word_low_emotion:
                line = line.split('\t')
                result_low.append(line[0] + '\t' + str(0.4*(float(line[1]))) + '\t' + line[2])
        #得到负向的情感词和分值以及在句子中的位置
        
        print('-----------以下是正向的情感词以及得分')
        if len(result_high) >= 1:
            for data in list(set(result_high)):
                print(data)

        print('-----------以下是负向的情感词以及得分')
    

        if len(result_low) >= 1:
            for data in list(set(result_low)):
                print(data)
        



if __name__ == '__main__':
    text = '本科基本工资是4000  研究生是5000  还有其他补助 稍微不爽的是没有住房补贴  总得来说还不错'
    get_word = get()
    word = get().cut_words(text)
    print(word)
    get_word.get_emotion_words(word)





