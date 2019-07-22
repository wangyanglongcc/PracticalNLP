# -*- coding: utf-8 -*-
import os
from pyltp import Segmentor # 分词
from pyltp import Postagger # 词性标注
path = r'D:\PycharmProjects\NLP\model_package'
LTP_DATA_DIR = r'D:\PycharmProjects\NLP\model_package\models\pyltp'  # ltp模型目录的路径
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
def seg_ltp(text):
    segmentor = Segmentor()  # 初始化分词实例
    segmentor.load(cws_model_path)  # 加载分词模型
    words = list(segmentor.segment(text))  # 分词
    segmentor.release()  # 释放分词模型
    return words
def pos_ltp(words):
    postagger = Postagger()  # 初始化词性标注实例
    postagger.load(pos_model_path)  # 加载词性标注模型
    postags = list(postagger.postag(words))  # 词性标注
    postagger.release()  # 释放词性标注模型
    return postags
if __name__ == '__main__':
    text = '股价上涨得很快。'
    text = '奔驰的操控性很好'
    words = seg_ltp(text)
    postags = pos_ltp(words)
    print(words,postags)
    # ['股价', '上涨', '得', '很', '快', '。']
