#%%
"""
tokenize_tweets.py
ユーザごとのツイートを形態素解析して同じ DB に格納する。
あらかじめ mark_usr_tweets_to_cluster を実行しておく。
"""

#%%

from pymongo import MongoClient
import lib.mongo_util as mongo_util

#%%

# words をクリアするか
clear = True

# 何件処理するか (0 なら、words が未セットのもの全て)
count = 0

#%%

# データベースの準備
client = MongoClient()
# ユーザごとのツイートの Collection
col_usrtweets = client.tw_ana.usr_tweets

if clear:
    col_usrtweets.update_many({}, {'$unset': {'words': ''}})

#%%

# 実行
mongo_util.add_tokenized_words(col_usrtweets, 'text', 'words',
                                count=count, test_data_only=True)

#%%
