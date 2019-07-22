# -*- coding: utf-8 -*-
import os
import jieba
CURRENTFILE = os.path.abspath(__file__)
CURRENTPATH = os.path.dirname(CURRENTFILE)
FATHERPATH = os.path.dirname(CURRENTPATH)
from collections import Counter
jieba.load_userdict(os.path.join(FATHERPATH,'doc/user_dict2.txt'))
stopwords = [i.strip('\n') for i in open(os.path.join(FATHERPATH,'doc/stopwords.txt'),encoding='utf-8')] + ['\n']

def seg_jieba(text,withstopwords=False):# jieba分词
    words = [word for word in jieba.cut(text)]
    if withstopwords:
        words = list(filter(lambda x:x not in set(stopwords),words))
    return words
def words_count(words):# 统计词频
    word_count = Counter(words)
    word_count = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
    return word_count
if __name__ == '__main__':
    text = """2年前开始关注汽车方面的信息，最开始喜欢上吉利博越，配置齐全，外观漂亮，油耗没太在意，慢慢关注更多车型后就入不了眼了，
    油耗什么的都得开始考虑，然后就是GS4外观漂亮，油耗不错 ，试乘后，上下车容易刮脚，左右扶手让人不满意，因为在等居住证下来所以也没买，
    直到看到长安CS35PLUS，被彻底惊艳到配置，颜值，油耗，都是心里最满意的，2年前偶然间看到过长安CS35就被其外观打动过，
    现在全新升级了，就更加是我的菜了。"""
    words = seg_jieba(text,True)
    word_c = words_count(words)
    for word in word_c:
        print(word)
