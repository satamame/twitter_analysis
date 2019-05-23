#%%
"""
retrieve_tweets.py
ツイートを取得して、DB に追加していく。
これを繰り返し実行して良い。
"""

#%%

from pymongo import MongoClient
import lib.tw_connect as tw_connect
import lib.mongo_util as mongo_util

#%%

# lib/token.py に、以下の変数を定義しておくこと
from lib.token import consumer_token, consumer_secret, access_token, access_secret

# Twitter API への接続の準備
twconn = tw_connect.TwConn(consumer_token, consumer_secret)
twconn.set_access_token(access_token, access_secret)

#%%

# データベースの準備
client = MongoClient()
# API で適当に取ってきた tweets は、tw_samples に入れる
col_twsamples = client.tw_ana.tw_samples

# 次に取得する最小 id (取得した最大 id + 1 または None)
since_id = mongo_util.next_id(col_twsamples)

#%%

q = 'です OR ます OR でした OR ました OR でしょう OR ましょう'

count = 0
try:
    for results in twconn.search(q, since_id=since_id):
        ins_result = col_twsamples.insert_many(results)
        
        ret_cnt = len(results)
        ins_cnt = len(ins_result.inserted_ids)

        print('{} tweets retrieved and {} added to DB.'.format(ret_cnt, ins_cnt))
        count += ins_cnt
except Exception as e:
    print('Error: {}'.format(e))

print('Total: {} tweets added and {} stored.'.
    format(count, col_twsamples.count_documents({})))
