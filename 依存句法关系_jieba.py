# -*- coding: utf-8 -*-
import os
import pandas as pd
import jieba
import jieba.posseg as pseg
path = r'D:\PycharmProjects\NLP\model_package'
jieba.load_userdict(os.path.join(path,'user_dict2_jieba.txt'))
from pyltp import Parser
LTP_DATA_DIR = r'D:\PycharmProjects\NLP\model_package\models\pyltp'  # ltp模型目录的路径
par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')  # 依存句法分析模型路径，模型名称为`parser.model`
jieba_ltp = pd.read_csv(r'D:\PycharmProjects\NLP\model_package\pos_jieba_ltp.txt')
jieba_ltp_dict = dict(zip(jieba_ltp['jieba'],jieba_ltp['ltp']))

def arcs_jieba(text):
    words = [w.word for w in pseg.cut(text)]
    postags = [jieba_ltp_dict[w.flag] if w.flag in jieba_ltp_dict else w.flag for w in pseg.cut(text)]
    parser = Parser() # 初始化实例
    parser.load(par_model_path)  # 加载模型
    arcs = parser.parse(words, postags)  # 句法分析
    parser.release()  # 释放模型
    print(words)
    print(postags)
    return arcs
if __name__ == '__main__':
    text = '股价上涨得很快。'
    arcs = arcs_jieba(text)
    print(["%d:%s" % (arc.head, arc.relation) for arc in arcs])
