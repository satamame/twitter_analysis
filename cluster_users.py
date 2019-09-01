#%%
"""
cluster_users.py
ユーザごとのトピック別文書数を DB から読み込み、ユーザを分類する。
"""

#%%

from pymongo import MongoClient

#%%

# データベースの準備
client = MongoClient()
# ユーザごとのトピック別文書数の Collection
col_usrtopics = client.tw_ana.user_topics

#%%

# ユーザごとのトピック別文書数を DB から取得
usr_tp_cnts = col_usrtopics.find({'topic_counts': {'$exists': True}},
    {'topic_counts': 1}
)

# 確率のリスト (のリスト) にする
usr_tp_rates = []
for tp_cnts in [u['topic_counts'] for u in usr_tp_cnts]:
    total = sum(tp_cnts)
    tp_rates = [c/total for c in tp_cnts]
    usr_tp_rates.append(tp_rates)

#%%

from sklearn.cluster import KMeans
# import matplotlib.pyplot as plt
# import random

#%%

# グループ数
grp_cnt = 4

# 仮の値
# usr_tp_rates = []
# for i in range(10):
#     usr_tp_rates.append(random.sample([0.1, 0.2, 0.3, 0.4], 4))

#%%

# KMeans でクラスタリング
km = KMeans(n_clusters=grp_cnt, random_state=10).fit(usr_tp_rates)

# usr_tp_rates に対応するラベルのリスト
labels = km.labels_

# rate をグループごとにまとめる
groups = []
for i in range(grp_cnt):
    groups.append([])

for label, tp_rates in zip(labels, usr_tp_rates):
    # 該当するグループに追加
    print('label: {}'.format(label))
    print('rates: {}'.format(tp_rates))
    groups[label].append(tp_rates)

# for i, label in enumerate(labels):
#     print('label: {}'.format(label))
#     print('rates: {}'.format(usr_tp_rates[i]))
#     groups[label].append(usr_tp_rates[i])

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
