import re
from pyltp import SentenceSplitter


def split_sent_word_byrule(text='', flag='re'):
    text = str(text)
    text = re.sub("[^\w0-9]{25,}", '', text)  # 特殊字符重复10次以上替换掉
    if flag == 'ltp':
        temp_sents = SentenceSplitter.split(text)  # ltp分句:句号、问号、感叹号、分号、省略号
    elif flag == 're':
        temp_sents = re.split('[,，;；。!！?？…\n\r\t]+', text)  # re分句:使用非字符类符号进行分句
    # 对包含.的句子利用正则二次分句
    sents = []
    for sent in temp_sents:
        if '.' in sent:
            temp_sent = re.split(r'(?<![0-9a-zA-Z])\.', sent)
            sents.extend(temp_sent)  # temp_sent是一个列表，所以不能用append,要用extend
        else:
            sents.append(sent)
    # 对包含空格的句子进行三次分句
    temp_sents = sents
    sents = []
    for sent in temp_sents:
        sent = sent.strip()
        if ' ' in sent:
            temp_sent = sent.split(' ')
            mean_length = 0
            for sec_sent in temp_sent:
                mean_length += len(sec_sent)
            mean_length = mean_length / len(temp_sent)
            # 如果用空格分句后长度大于6则用空格分句，否则使用crf分句
            if mean_length > 6.5:
                sents.extend(temp_sent)
            else:
                print('fdsfasd')
                # temp_sent2 = sent_split.predict(sent)
        #             sents.extend(temp_sent2)
        else:
            sents.append(sent)
    # # 对长句利用进行分句
    # temp_sents = sents
    # sents = []
    # for sent in temp_sents:
    #     sent = sent.strip()
    #     if (len(sent) > 50):  # or (' ' in sent) or ('.' in sent):
    #         temp_sent = sent_split.predict(sent)
    #         sents.extend(temp_sent)
    #     else:
    #         sents.append(sent)
    return sents


if __name__ == '__main__':
    text = """2年前开始关注汽车方面的信息，最开始喜欢上吉利博越，配置齐全，外观漂亮，油耗没太在意，慢慢关注更多车型后就入不了眼了，
    油耗什么的都得开始考虑，然后就是GS4外观漂亮，油耗不错 ，试乘后，上下车容易刮脚，左右扶手让人不满意，因为在等居住证下来所以也没买，
    直到看到长安CS35PLUS，被彻底惊艳到配置，颜值，油耗，都是心里最满意的，2年前偶然间看到过长安CS35就被其外观打动过，
    现在全新升级了，就更加是我的菜了。"""
    sents = split_sent_word_byrule(text, flag='ltp')
    for index, sent in enumerate(sents):
        print(index, sent)
