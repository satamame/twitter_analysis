#%%
"""
mark_usr_tweets_to_cluster.py
ユーザツイートの Collection の中からランダムでユーザ ID を選ぶ。
選んだユーザのツイートにマークを（既存のマークをクリアしてから）つける。
"""

#%%

from pymongo import MongoClient
import random

#%%

# 選ぶユーザの数
usr_count = 100

#%%

# データベースの準備
client = MongoClient()
# ユーザツイートの Collection
col_usrtweets = client.tw_ana.usr_tweets

#%%

# 初期化
col_usrtweets.update_many(
    {'test_data': True}, {'$set': {'test_data': False}}
)

#%%

# ユーザ ID を取得
usr_ids = col_usrtweets.aggregate(
    [{'$group': {'_id': '$user.id'}}],
    allowDiskUse=True
)
# ランダムに選択
usr_ids = random.sample([d['_id'] for d in usr_ids], usr_count)

#%%

cnt = 0
# マークをセット
for usr_id in usr_ids:
    col_usrtweets.update_many(
        {'user.id': usr_id},
        {'$set': {'test_data': True}}
    )
    cnt += 1
    if cnt % 10 == 0:
        print('{} users processed.'.format(cnt))

print('Done.')
print('Totally {} users processed.'.format(cnt))

#%%
