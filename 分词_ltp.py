# -*- coding: utf-8 -*-
import os
from pyltp import Segmentor # 分词
path = r'D:\PycharmProjects\NLP\model_package'
LTP_DATA_DIR = r'D:\PycharmProjects\NLP\model_package\models\pyltp'  # ltp模型目录的路径
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
stopwords = [i.strip('\n') for i in open(os.path.join(path,'stopwords.txt'),encoding='utf-8')] + ['\n']
def seg_ltp(text,withstopwords=False):
    segmentor = Segmentor()  # 初始化分词实例
    segmentor.load(cws_model_path)  # 加载分词模型
    segmentor.load_with_lexicon(cws_model_path, os.path.join(os.path.dirname(os.path.dirname(LTP_DATA_DIR)),
                                                             'user_dict2_pyltp.txt'))  # 加载外部分词词典
    words = list(segmentor.segment(text))  # 分词
    segmentor.release()  # 释放分词模型
    if withstopwords:
        words = list(filter(lambda x:x not in set(stopwords),words))
    return words
if __name__ == '__main__':
    # text = '股价上涨得很快。'
    text = '奔驰的操控性很好'
    words = seg_ltp(text)
    print(words)
    # ['股价', '上涨', '得', '很', '快', '。']
