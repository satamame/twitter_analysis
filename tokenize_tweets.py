#%%
"""
tokenize_tweets.py
サンプルツイートを形態素解析して同じ DB に格納する。
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
# 重複を削除した サンプルツイートの Collection
col_twsamples = client.tw_ana.tw_text

#%%

if clear:
    col_twsamples.update_many({}, {'$unset': {'words': ''}})

# 実行
mongo_util.add_tokenized_words(col_twsamples, 'full_text', 'words', count)
