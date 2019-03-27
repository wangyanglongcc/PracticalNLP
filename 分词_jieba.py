# -*- coding: utf-8 -*-
import os
import jieba
path = r'D:\PycharmProjects\NLP\model_package'
jieba.load_userdict(r'D:\PycharmProjects\NLP\model_package\user_dict2_jieba.txt')
stopwords = [i.strip('\n') for i in open(os.path.join(path,'stopwords.txt'),encoding='utf-8')] + ['\n']
def seg_jieba(text,withstopwords=False):# jieba分词
    words = [word for word in jieba.cut(text)]
    if withstopwords:
        words = list(filter(lambda x:x not in set(stopwords),words))
    return words
if __name__ == '__main__':
    text = '股价上涨得很快。'
    words = seg_jieba(text)
    print(words)
    # ['股价', '上涨', '得', '很快', '。']
