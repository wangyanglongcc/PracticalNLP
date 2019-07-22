# -*- coding: utf-8 -*-
import os
import pandas as pd
from collections import defaultdict
import jieba
import jieba.posseg as pseg
from multiprocessing import Pool
import numpy as np
from collections import Counter

path = r'D:\PycharmProjects\nlpData\yuqing_sgm\doc'
jieba.load_userdict(os.path.join(path, 'user_dict2.txt'))
from pyltp import Parser

LTP_DATA_DIR = r'D:\PycharmProjects\nlpData\yuqing_bmw_v2\models\pyltp'  # ltp模型目录的路径
par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')  # 依存句法分析模型路径，模型名称为`parser.model`
jieba_ltp = pd.read_csv(r'D:\GitHub\PracticalNLP\pos_jieba_ltp.txt')
jieba_ltp_dict = dict(zip(jieba_ltp['jieba'], jieba_ltp['ltp']))


def arcs_jieba(text):
    text = str(text)
    words = [w.word for w in pseg.cut(text)]
    postags = [jieba_ltp_dict[w.flag] if w.flag in jieba_ltp_dict else w.flag for w in pseg.cut(text)]
    parser = Parser()  # 初始化实例
    parser.load(par_model_path)  # 加载模型
    arcs = parser.parse(words, postags)  # 句法分析
    parser.release()  # 释放模型
    return words, postags, arcs


def parse_child_dict(words, arcs):
    child_dict_list = []
    for index in range(len(words)):
        child_dict = defaultdict(list)
        for arc_index in range(len(arcs)):
            if arcs[arc_index].head == index + 1:
                child_dict[arcs[arc_index].relation].append(arc_index)
        child_dict_list.append(child_dict)
    child_dict_list = [dict(child_dict) for child_dict in child_dict_list]
    return child_dict_list


def fun(words, postags, child_dict_list):
    '''
    :param words:
    :param postags:
    :param child_dict_list:
    :return: (修饰词,核心词,rule) 即 (实体词,描述词,rule)
    '''
    _relations = [key for child_dict in child_dict_list for key, value in child_dict.items()]
    for index in range(len(words)):
        child_dict = child_dict_list[index]
        # rule1
        if 'SBV' in child_dict and postags[index] == 'a':
            # rule11
            if set(_relations) == set(['SBV']):
                es = words[child_dict['SBV'][0]]
                o = words[index]
                return (es, o, 'rule11')
            # rule12
            if 'COO' in set(_relations):
                es = []
                for i in child_dict['SBV']:
                    es.append(words[i])
                    if 'COO' in child_dict_list[i]:
                        for j in child_dict_list[i]['COO']:
                            es.append(words[j])
                o = words[index]
                return ('|'.join(es), o, 'rule12')
        else:
            return (0, 0, 'rule13')


def rule(texts):
    rules = []
    for index, text in enumerate(texts):
        words, postags, arcs = arcs_jieba(text)
        child_dict_list = parse_child_dict(words, arcs)
        _, _, rule = fun(words, postags, child_dict_list)
        rules.append(rule)
        if index % 1000 == 0:
            print(index, Counter(rules))
    return rules


def main(texts):
    texts = list(texts)
    pool = Pool(3)
    max_rows = 17000
    res = []
    for i in range(int(np.ceil(len(texts) / max_rows))):
        text = texts[i * max_rows:i * max_rows + max_rows]
        res.append(pool.apply_async(func=rule, args=(text,)))
    pool.close()
    pool.join()
    res = [i.get() for i in res]
    print(Counter(res))


if __name__ == '__main__':
    texts = ['刹车满分', '刹车和车身都很稳', '推背十足', '动力十足']
    # texts = ['刹车很稳','安全感非常足','很没有安全感','刹车满分','自动驻车需要加装']
    # texts = ['我喜欢黑白两色','个人感觉电子手刹的位置不习惯','亚洲龙音响异响']
    file = r'\\192.168.1.4\数据分析组数据存储\王杨龙\ty_201906\口碑评论表头.pl'
    import pickle

    with open(file, 'rb') as f:
        df = pickle.load(f)
    texts = set(df['word'])
    print(len(texts))
    main(texts)
    # rules = []
    # for index,text in enumerate(texts):
    #     words,postags,arcs = arcs_jieba(text)
    #     child_dict_list = parse_child_dict(words,arcs)
    #     heads = [arc.head for arc in arcs]
    #     relations = [arc.relation for arc in arcs]
    #     _,_,rule = fun(words,postags,child_dict_list)
    #     rules.append(rule)
    #     if index % 1000 == 0:
    #         print(index,Counter(rules))
    # print(index, Counter(rules))
    # print(["%d:%s" % (arc.head, arc.relation) for arc in arcs])
