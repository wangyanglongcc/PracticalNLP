# -*- coding: utf-8 -*-
import os
from pyltp import Parser
from collections import defaultdict
LTP_DATA_DIR = r'D:\PycharmProjects\NLP\model_package\models\pyltp'  # ltp模型目录的路径
par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')  # 依存句法分析模型路径，模型名称为`parser.model`
def arcs_ltp(words,postags):
    parser = Parser()  # 初始化实例
    parser.load(par_model_path)  # 加载模型
    arcs = parser.parse(words, postags)  # 句法分析
    parser.release()  # 释放模型
    return arcs
# 为句子中的每个词语维护一个保存句法依存子节点的字典
# words: 分词列表   arcs: 句法依存列表
def parse_child_dict(words,arcs):
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
    '让 车子 充满 了 肌肉感'
    words = ['奔驰', '的', '操控性', '很', '好']
    postags = ['nz', 'u', 'n', 'd', 'a']
    arcs = arcs_ltp(words,postags)
    child_dict_list = parse_child_dict(words,arcs)
    print(words)
    print(postags)
    print(["%d:%s" % (arc.head, arc.relation) for arc in arcs])
    print(child_dict_list)