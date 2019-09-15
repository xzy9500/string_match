# -*- coding: UTF-8 -*- #
import difflib
import Levenshtein
import pandas as pd
import math
import jieba
jieba.load_userdict('stopword.txt')
import re

def create_rep_dict(txt):
    with open(txt, encoding='utf-8') as f:
        text = f.read()
    dic = {}
    for each in text.split('\n'):
        dic[each] = ''
    return dic

def multi_replace(text, rep_dict):
    rx = re.compile('|'.join(map(re.escape, rep_dict)))
    def one_xlat(match):
        return rep_dict[match.group(0)]
    return rx.sub(one_xlat, text)




rep_dict = {'指数型':'', '发起式':''}
multi_replace('中证全指证券公司指数型发起式', rep_dict)

data = pd.read_csv('fundreg_data.csv')

word_list = []

for each in data['申请事项']:
    seg_list = list(jieba.cut(each))
    word_list += seg_list

word_df = pd.DataFrame(word_list, columns=['word'])
word_df['cnt'] = 1
word_cnt = word_df.groupby('word')['cnt'].sum()

que_cnt = math.ceil(len(data)/3)

tar_data = data.iloc[0]

matching_data = data.loc[(data['基金管理人'] == tar_data['基金管理人']) & (data['申请材料接收日'] == tar_data['申请材料接收日']) & (data.index != 0)]

if len(matching_data):
    result_data = []
    for i in range(len(matching_data)):
        result_set = {}
        ratio = Levenshtein.ratio(tar_data['申请事项'], matching_data.iloc[i]['申请事项'])
        result_set['相似度'] = ratio
        result_set['匹配名称'] = matching_data.iloc[i]['申请事项']
        result_data.append(result_set)
else:
    pass

result_data = pd.DataFrame(result_data)
max_data = result_data.max()

seq = difflib.SequenceMatcher(None, '惠弘定期开放纯债债券型', '惠享定期开放纯债债券型')
cut_data = seq.find_longest_match(0, len('惠弘定期开放纯债债券型'), 0, len('惠享定期开放纯债债券型'))


# 若长度一致且相同字段超过60%,则先去掉相同的字段,再比较相似度,否则直接比较