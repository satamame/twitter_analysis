#%%
"""
update_users.py
サンプルツイートを元に、DB の ユーザ collection を更新する。
"""

#%%

from pymongo import MongoClient
import lib.mongo_util as mongo_util

#%%

# データベースの準備
client = MongoClient()
# API で適当に取ってきた tweets は、tw_samples に入っている
col_twsamples = client.tw_ana.tw_samples

# tw_samples から抜き出した user 情報を保存する collection
col_users = client.tw_ana.users

#%%

# サンプルツイートからユーザを取り出して、ユーザ collection を更新する
mongo_util.update_users(col_users, col_twsamples)

#%%

print('Total: {} users stored.'.format(col_users.count_documents({})))
