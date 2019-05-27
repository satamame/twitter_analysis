#%%
"""
tokenize_tweets.py
ユーザごとのツイートを形態素解析して同じ DB に格納する。
"""

#%%

from pymongo import MongoClient
import lib.mongo_util as mongo_util

#%%

# 何件処理するか (0 なら、words が未セットのもの全て)
count = 0

#%%

# データベースの準備
client = MongoClient()
# ユーザごとのツイートの Collection
col_usrtweets = client.tw_ana.usr_tweets
# 実行
mongo_util.add_tokenized_words(col_usrtweets, 'text', 'words', count)
