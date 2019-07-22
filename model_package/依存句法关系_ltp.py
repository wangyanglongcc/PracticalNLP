# -*- coding: utf-8 -*-
import os
import jieba
import jieba.posseg as pseg
from pyltp import Parser
from collections import defaultdict

CURRENTFILE = os.path.abspath(__file__)
CURRENTPATH = os.path.dirname(CURRENTFILE)
FATHERPATH = os.path.dirname(CURRENTPATH)
jieba.load_userdict(os.path.join(FATHERPATH, 'doc/user_dict2.txt'))
pos_jieba_ltp_file = os.path.join(FATHERPATH, 'doc/pos_jieba_ltp.txt')
pos_jieba_ltp_dict = dict([line.strip().split(',') for line in open(pos_jieba_ltp_file, 'r+', encoding='utf-8')])
LTP_DATA_DIR = '/Users/ryan/PycharmProjects/nlpData/yuqing_bmw_v2/models/pyltp'  # ltp模型目录的路径
par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')  # 依存句法分析模型路径，模型名称为`parser.model`


def pseg_text(text):
    word = [w.word for w in pseg.cut(text)]
    postags = [w.flag for w in pseg.cut(text)]
    postags = [pos_jieba_ltp_dict[w] if w in pos_jieba_ltp_dict else w for w in postags]
    return word, postags


def arcs_ltp(words, postags):
    '''
    根据分词和词性获取依存句法树
    :param words: 分词后list
    :param postags: 词性list
    :return:
    '''
    parser = Parser()  # 初始化实例
    parser.load(par_model_path)  # 加载模型
    arcs = parser.parse(words, postags)  # 句法分析
    parser.release()  # 释放模型
    return arcs


def parse_child_dict(words, arcs):
    '''
    为句子中的每个词语维护一个保存句法依存子节点的字典
    :param words: 分词列表 index从0开始
    :param arcs: 句法依存列表 .head从1开始
    :return:
    '''
    child_dict_list = []
    for index in range(len(words)):
        child_dict = defaultdict(list)
        for arc_index in range(len(arcs)):
            if arcs[arc_index].head == index + 1:
                child_dict[arcs[arc_index].relation].append(arc_index)
        child_dict_list.append(child_dict)
    child_dict_list = [dict(child_dict) for child_dict in child_dict_list]
    return child_dict_list


if __name__ == '__main__':
    texts = ['股价上涨得很快', '奔驰的操控性很好', '宝马的外观很有肌肉感', '翻倍的净利润', '音响的声音小了一点', '收入增长 ３５％ ， 佣金率下降趋缓，份额继续上升']
    for text in texts[:1]:
        words, postags = pseg_text(text)
        words, postags = ['股价','上涨','得','很','快'],['n','v','u','d','n']
        arcs = arcs_ltp(words, postags)
        heads = [arc.head for arc in arcs]  # 提取依存父节点id
        relation = [arc.relation for arc in arcs]  # 提取依存关系
        targ = ['ROOT' if i == 0 else words[i - 1] for i in heads]  # 匹配依存父节点短语
        word_pos_dict = dict(zip(words, postags))
        for i in range(len(words)):
            pos = word_pos_dict[targ[i]] if targ[i] in word_pos_dict else ''
            print(relation[i], words[i], postags[i], targ[i], heads[i], pos)
        print(heads)
        child_dict_list = parse_child_dict(words, arcs)
        print(words, postags, sep='\n')
        print(["%d:%s" % (arc.head, arc.relation) for arc in arcs])
        print(child_dict_list)
