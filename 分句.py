# -*- coding: utf-8 -*-
import re
from pyltp import SentenceSplitter

def split_sent(text,type='re'):
    if type == 're':# 使用正则分句
        sents = re.split('[,，;；。!！?？…\n\r\t]+', text)# 根据非字符分句
    elif type == 'ltp':
        sents = SentenceSplitter.split(text)# ltp分句:句号、问号、感叹号、分号、省略号
    else:
        print('输入错误')
    sents = [sent.strip() for sent in sents]
    sents = list(filter(lambda x: x != '', sents))
    return sents
if __name__ == '__main__':
    text = """
        2年前开始关注汽车方面的信息，最开始喜欢上吉利博越，配置齐全，外观漂亮，油耗没太在意，慢慢关注更多车型后就入不了眼了，
        油耗什么的都得开始考虑，然后就是GS4外观漂亮，油耗不错 ，试乘后，上下车容易刮脚，左右扶手让人不满意，因为在等居住证下来所以也没买，
        直到看到长安CS35PLUS，被彻底惊艳到配置，颜值，油耗，都是心里最满意的，2年前偶然间看到过长安CS35就被其外观打动过，
        现在全新升级了，就更加是我的菜了。
        """
    sents = split_sent(text,'re')
    for sent in sents:
        print(sent)