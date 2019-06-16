#%%
"""
mark_training_data.py
サンプルツイートの Collection の中からランダムで訓練データを決めて、
訓練データであることを示すマークを（既存のマークをクリアしてから）つける。
"""

#%%

from pymongo import MongoClient
import random

#%%

# 訓練データの件数
training_data_count = 50000

#%%

# データベースの準備
client = MongoClient()
# API で適当に取ってきた tweets は、tw_samples に入っている
col_twsamples = client.tw_ana.tw_samples

#%%

# 初期化
col_twsamples.update_many(
    {'training_data': True}, {'$set': {'training_data': False}}
)

#%%

# id をランダムに抽出
ids = [d['id'] for d in col_twsamples.find(
    {'words': {'$exists': True}}, {'id': 1}
)]
ids = random.sample(ids, training_data_count)

#%%

# マークをセット
for id in ids:
    col_twsamples.update_one({'id': id},
        {'$set': {'training_data': True}})

print('{} tweets marked as training data.'.format(len(ids)))
