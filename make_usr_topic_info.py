#%%
"""
make_usr_topic_info.py
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

# ユーザ ID を取得する
usr_ids = col_usrtweets.aggregate([
        {'$match': {
            'test_data': True,
            'topic_id': {'$exists': True},
            'topic_prob': {'$exists': True}}},
        {'$group': {'_id': '$user.id'}}
    ], allowDiskUse:True, corsor:{})
usr_ids = [d['_id'] for d in usr_ids]

#%%

# ユーザごとの各トピックの出現率を記録してゆく。
# トピック数は 4 であることが分かっている。

user_tp_rates = []
for id in user_ids:
    topic_cnt = [0] * 4
    tweets = col_usrtweets.find(
        {'user.id': id, 'topic_id': {'$exists': True},
        {'topic_id': 1}
    )
    # トピックを数える
    for t in tweets:
        tpid = t['topic_id']
        if tpid in range(4):
            topic_cnt[tpid] = topic_cnt[tpid] + 1
    
    # 確率に変える
    total = sum(topic_cnt)
    topic_rates = [c/total for c in topic_cnt]
    user_tp_rates.append(topic_rates)

#%%

# 実験

# from sklearn.cluster import KMeans
# import matplotlib.pyplot as plt
# import random

#%%

# グループ数
grp_cnt = 4

# 仮の値
# user_tp_rates = []
# for i in range(10):
#     user_tp_rates.append(random.sample([0.1, 0.2, 0.3, 0.4], 4))

#%%

# KMeans でクラスタリング
km = KMeans(n_clusters=grp_cnt, random_state=10).fit(user_tp_rates)

# user_tp_rates に対応するラベルのリスト
labels = km.labels_

# rate をグループごとにまとめる
groups = []
for i in range(grp_cnt):
    groups.append([])

for label, tp_rates in zip(labels, user_tp_rates):
    # 該当するグループに追加
    print('label: {}'.format(label))
    print('rates: {}'.format(tp_rates))
    groups[label].append(tp_rates)

# for i, label in enumerate(labels):
#     print('label: {}'.format(label))
#     print('rates: {}'.format(user_tp_rates[i]))
#     groups[label].append(user_tp_rates[i])

#%%

# ラベル (ユーザグループ ID) 、トピック分布を表示する

for i, group in enumerate(groups):
    plt.title('Group {}'.format(i))
    xdata = range(4)
    
    for tp_rate in group:
        ydata = tp_rate
        plt.plot(xdata, ydata)

    plt.show()
    plt.clf()










#%%
