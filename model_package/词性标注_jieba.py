# -*- coding: utf-8 -*-
import os
import jieba
import jieba.posseg as pseg
path = r'D:\PycharmProjects\NLP\model_package'
jieba.load_userdict(os.path.join(path,'user_dict2_jieba.txt'))
def pos_jieba(text):
    word = [w.word for w in pseg.cut(text)]
    postags = [w.flag for w in pseg.cut(text)]
    return word,postags
if __name__ == '__main__':
    text = '股价上涨得很快。'
    word,postags = pos_jieba(text)
    print(word,postags)
    # ['股价', '上涨', '得', '很快', '。']['v', 'v', 'ud', 'a', 'x']
