#%%
"""
mark_test_data.py
サンプルツイートの Collection の中からランダムでテストデータを決めて、
テストデータであることを示すマークを（既存のマークをクリアしてから）つける。
"""

#%%

from pymongo import MongoClient
import random

#%%

# テストデータの件数
test_data_count = 10000

#%%

# データベースの準備
client = MongoClient()
# API で適当に取ってきた tweets は、tw_samples に入っている
col_twsamples = client.tw_ana.tw_samples

#%%

# 初期化
col_twsamples.update_many(
    {'test_data': True}, {'$set': {'test_data': False}}
)

#%%

# id をランダムに抽出 (training_data でないもの)
ids = [d['id'] for d in col_twsamples.find(
    {'words': {'$exists': True}, 'training_data': {'$ne': True}},
    {'id': 1}
)]
ids = random.sample(ids, test_data_count)

#%%

# マークをセット
for id in ids:
    col_twsamples.update_one({'id': id},
        {'$set': {'test_data': True}})

print('{} tweets marked as test data.'.format(len(ids)))
