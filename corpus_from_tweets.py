#%%
"""
corpus_from_tweets.py
サンプルツイートからランダムでサンプリングしてコーパスにする。
中間生成物として特徴語辞書を生成する。
"""

#%%

from pymongo import MongoClient
from gensim import corpora
import random
import re

#%%

# ランダムサンプリングするツイートの数
sample_count = 1000
# 使われてるツイートが no_berow 個以下の単語は無視
no_below = 5
# 使われてるツイートの割合が no_above 以上の単語は無視
no_above = 0.3

# 保存する時の名前 (拡張子なし)
dict_name = 'dictionary'
corpus_name = 'corpus'

# ストップワード
stop_words = [
    r'\d+',
    r'RT',
    r'https?',
    r'[0-9:;/\\!?@#$%^&*()\-_=+*.,\'"\[\]｀´ー…～＃｢｣「」]+',
]

#%%

# データベースの準備
client = MongoClient()
# API で適当に取ってきた サンプルツイートの Collection
col_twsamples = client.tw_ana.tw_samples

#%%

# id をランダムに抽出
ids = [d['id'] for d in col_twsamples.find({}, {'id': 1})]
ids = random.sample(ids, sample_count)

#%%

# 単語リストのリスト
words_list = []
for id in ids:
    words = col_twsamples.find_one({'id': id}, {'words': 1})['words']
    for sw in stop_words:
        words = [w for w in words if not re.fullmatch(sw, w, flags=re.IGNORECASE)]
    words_list.append(words)

#%%

# 辞書作成
dict = corpora.Dictionary(words_list)
dict.filter_extremes(no_below=no_below, no_above=no_above)

# 保存
dict_file_name = dict_name + '.dict'
dict.save(dict_file_name)
print('Dictionary saved as {}.'.format(dict_file_name))
dict.save_as_text(dict_name + '.txt')

# コーパス作成 & 保存
corpus_file_name = corpus_name + '.mm'
corpus = [dict.doc2bow(words) for words in words_list]
corpora.MmCorpus.serialize(corpus_file_name, corpus)
print('Corpus saved as {}.'.format(corpus_file_name))
