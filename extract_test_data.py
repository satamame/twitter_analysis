#%%

# このスクリプトは作るのをやめて、
# DB 上で直に分類することにする。


"""
extract_test_data.py
DB から test_data としてマークされているデータを
取り出し、本文とコーパスをファイルに保存する。
"""

#%%

from pymongo import MongoClient
from gensim import corpora
from lib.mongo_util import StreamWords

#%%

# サンプルツイートから取り出す (0) か、ユーザツイートから取り出す (1) か
source = 0

# 保存する時の名前 (拡張子なし)
tweets_name = 'data/tweets_test'
corpus_name = 'data/corpus_test'

#%%

# データベースの準備
client = MongoClient()
if source == 1:
    collection = client.tw_ana.usr_tweets
else:
    collection = client.tw_ana.tw_samples

#%%

# test_data の id を抽出
ids = [d['id'] for d in collection.find(
    {'words': {'$exists': True}, 'test_data': True},
    {'id': 1}
)]



