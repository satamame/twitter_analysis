#%%
"""
retrieve_usr_tweets.py
ユーザ collection からランダムでユーザを抽出し、
各ユーザの tweets を取得して DB に追加する。
"""

#%%

from pymongo import MongoClient
import lib.tw_connect as tw_connect
import random

#%%

# lib/token.py に、以下の変数を定義しておくこと
from lib.token import consumer_token, consumer_secret, access_token, access_secret

# Twitter API への接続の準備
twconn = tw_connect.TwConn(consumer_token, consumer_secret)
twconn.set_access_token(access_token, access_secret)

#%%

# データベースの準備
client = MongoClient()
# user 情報を保存した collection
col_users = client.tw_ana.users

# API で取ってきた tweets の情報を保存する collection
col_usrtweets = client.tw_ana.usr_tweets

#%%

# ユーザのサンプル数
sample_user_count = 10

# id をランダムに抽出 (ignore 列が True なら選ばない)
user_ids = [d['user']['id'] for d in col_users.find(
    {'ignore': {'$ne': True}}, {'user.id': 1}
)]
user_ids = random.sample(user_ids, sample_user_count)

#%%

# 抽出されたというフラグを更新
col_users.update_many({}, {'$set': {'used_as_sample': False}})
col_users.update_many(
    {'user.id': {'$in': user_ids}}, {'$set': {'used_as_sample': True}}
)

#%%

# collection の初期化
col_usrtweets.delete_many({})

# 抽出されたユーザごとの、tweets の取得と保存
for i, id in enumerate(user_ids):
    for results in twconn.user_timeline(user_id=id):
        ins_result = col_usrtweets.insert_many(results)

        ret_cnt = len(results)
        ins_cnt = len(ins_result.inserted_ids)

        print('User #{}: {} tweets retrieved and {} added to DB.'.format(i, ret_cnt, ins_cnt))

#%%

tweet_count = col_usrtweets.count_documents({})
print('{} tweets by {} users stored.'.format(tweet_count, sample_user_count))
