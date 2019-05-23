#%%
"""
tokenize_tweets.py
サンプルツイートを形態素解析して同じ DB に格納する。
"""

#%%

from pymongo import MongoClient
import lib.mongo_util as mongo_util
from janome.tokenizer import Tokenizer

#%%

# 何件処理するか
count = 10

#%%

# データベースの準備
client = MongoClient()
# API で適当に取ってきた サンプルツイートの Collection
col_twsamples = client.tw_ana.tw_samples

#%%

# 件数分の id をサンプルツイート (words が未セットのもの) から取得
tweets = col_twsamples.find({'words': {'$exists': False}}, {'id': 1}).limit(count)
ids = [d['id'] for d in tweets]

t = Tokenizer()
pos_to_pick = ['名詞', '動詞', '形容詞', '形容動詞']

for id in ids:
    tweet = col_twsamples.find_one({'id': id})
    text = tweet['full_text']
    words = [tk.base_form for tk in t.tokenize(text)
        if tk.part_of_speech.split(',')[0] in pos_to_pick]
    print(words)
