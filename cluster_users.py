#%%
"""
cluster_users.py
ユーザごとのトピック別文書数を DB から読み込み、ユーザを分類する。
"""

#%%
from statistics import mean
from pymongo import MongoClient
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

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

#%%
# 確率のリスト (のリスト) にする
usr_tp_rates = []
for tp_cnts in [u['topic_counts'] for u in usr_tp_cnts]:
    total = sum(tp_cnts)
    tp_rates = [c/total for c in tp_cnts]
    usr_tp_rates.append(tp_rates)

#%%
# エルボー法でクラスタ数の見当を付ける
distortions = []
for i  in range(1,11):                # 1~10クラスタまで一気に計算
    km = KMeans(n_clusters=i, random_state=10).fit(usr_tp_rates)
    distortions.append(km.inertia_)

plt.plot(range(1,11),distortions,marker='o')
plt.xlabel('Number of clusters')
plt.ylabel('Distortion')
plt.show()

#%%
# 決めたクラスタ数
clst_cnt = 4

#%%
# 決めたクラスタ数で分類してデータを整形
km = KMeans(n_clusters=clst_cnt, random_state=10).fit(usr_tp_rates)

# rate をクラスタごとにまとめる
clusters = []
for i in range(clst_cnt):
    clusters.append([])

# label と rate をクラスタごとにまとめる
for label, tp_rates in zip(km.labels_, usr_tp_rates):
    clusters[label].append(tp_rates)

#%%
# ラベル (クラスタ ID) 、トピック分布を表示する
for i, group in enumerate(clusters):
    # グラフの描画
    xdata = range(4)
    
    for tp_rate in group:
        ydata = tp_rate
        plt.plot(xdata, ydata)

    # トピックごとの rate の平均値
    tp_rates = [r for r in zip(*group)]
    means = [mean(r) for r in tp_rates]
    # 小数点以下2桁に丸める
    means_str = ', '.join(['%.2f'% m for m in means])
    # タイトルとして表示
    plt.title('Cluster {}\n{}'.format(i, means_str))

    plt.show()
    plt.close()
    

#%%
