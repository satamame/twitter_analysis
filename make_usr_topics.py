#%%
"""
make_usr_topics.py
ユーザツイートの Collection から分類結果を取得し、
ユーザ ID ごとのトピック別文書数を DB に記録する。
"""

#%%
from pymongo import MongoClient

#%%
# データベースの準備
client = MongoClient()
# ユーザツイートの Collection
col_usrtweets = client.tw_ana.usr_tweets
# 出力先の Collection
col_usrtopics = client.tw_ana.user_topics

#%%
# カウントする条件としての最低構成比
minp = 0.5

#%%
# ユーザ ID を取得する
pipe = [
    {'$match': {
        'test_data': True,
        'topic_id': {'$exists': True},
        'topic_prob': {'$exists': True}}},
    {'$group': {'_id': '$user.id'}}
]
usr_ids = col_usrtweets.aggregate(pipeline=pipe, allowDiskUse=True)
usr_ids = [d['_id'] for d in usr_ids]

print('{} users on DB.'.format(len(usr_ids)))

#%%
# ユーザごとの各トピックの出現数を記録してゆく。
# トピック数は 4 であることが分かっている。

usr_tp_cnts = []
for i, id in enumerate(usr_ids):
    tp_cnts = [0] * 4
    for tp_id in range(len(tp_cnts)):
        tp_cnt = col_usrtweets.count_documents(
            {
                'user.id': id,
                'topic_id': tp_id,
                'topic_prob': {'$gte': minp}
            }
        )
        tp_cnts[tp_id] = tp_cnt
    
    usr_tp_cnts.append(tp_cnts)
    
    # DB に書き込む (更新または user_id がなければ追加)
    col_usrtopics.replace_one({'user_id': id},
        {'user_id': id, 'topic_counts': tp_cnts}, True # upsert
    )
    if (i + 1) % 50 == 0:
        print('{} users processed.'.format(i + 1))
    
print('Done.')


#%%
