#%%
"""
cluster_usr_tweets.py
モデルをファイルから読み込んで、ユーザツイートを分類する。
DB に topic_id と topic_prob を書き込み、ファイルには書き出さない。
"""

#%%

from pymongo import MongoClient, DESCENDING
from gensim import corpora, models
from lib.mongo_util import StreamWords
import os
import shutil
import re

#%%

# モデル番号
model_no = '07'

# probability の閾値（これより小さい場合はどのトピックにも入れない）
minp = 0.5

# 使うモデルの名前
model_name = 'data/' + model_no + '/lda_model'

# 使う辞書の名前
dict_name = 'data/' + model_no + '/dictionary'

#%%

# データベースの準備
client = MongoClient()
# ユーザツイートの Collection
col_usrtweets = client.tw_ana.usr_tweets

#%%

# test_data の id を抽出 (未処理のもの)
ids = [d['id'] for d in col_usrtweets.find(
    {'words': {'$exists': True}, 'test_data': True,
        '$or': [{'topic_id': {'$exists': False}}, {'topic_prob': {'$exists': False}}]
    },
    {'id': 1}
)]

#%%

# ユーザツイートから単語列を取得するイテラブル
stream = StreamWords(col_usrtweets, 'words')

#%%

# モデルを読み込む
model = models.LdaModel.load(model_name)

# 辞書を読み込む
dict_file_name = dict_name + '.dict'
dict = corpora.Dictionary.load(dict_file_name)

#%%

# DB 上で分類し、構成率が最大であるトピックの ID を記録する
# ファイルへの書き出しは、DB を読みながらおこなう
stream.label_topics(ids, model, dict, minp)

print('Done.')
