# -*- coding: utf-8 -*-
import os
import jieba
import jieba.posseg as pseg
from pyltp import Parser
from collections import defaultdict
from nltk.parse import DependencyGraph

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

def graph_tree(words,postags,arcs,show=True):
    conlls = ''
    for i in range(len(words)):
        if show:
            tmp_text = words[i] + '(' + '-'.join((str(i), postags[i], arcs[i].relation)) + ')'
        else:
            tmp_text = words[i]
        conll = '\t'.join((tmp_text, postags[i], str(arcs[i].head)))
        conlls += '\n' + conll
    conlltree = DependencyGraph(conlls)
    tree = conlltree.tree()
    tree.draw()


if __name__ == '__main__':
    # words, postags = ['股价', '上涨', '得', '很', '快'], ['n', 'v', 'u', 'd', 'n']
    text = '宝马的外观很有肌肉感'
    words, postags = pseg_text(text)
    arcs = arcs_ltp(words, postags)
    print(words,postags,[(arc.head,arc.relation) for arc in arcs],sep='\n')
    graph_tree(words,postags,arcs,True)