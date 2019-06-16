#%%
"""
トピック間のカルバック・ライブラー距離を確認する。
"""

#%%

from gensim import corpora, models
from gensim.matutils import kullback_leibler
import matplotlib.pyplot as plt

#%%

# 使うモデルの名前
model_name = 'data/lda_model'

#%%

# モデルを読み込む
model = models.LdaMulticore.load(model_name)

#%%

# トピックごとの、辞書内の単語を含む文がそのトピックに分類される (事後) 確率
t = model.state.get_lambda()

#%%

# トピック間のカルバック・ライブラー距離 (離れているほど良い)
ds = []
for i in range(model.num_topics):
    for j in range(model.num_topics):
        if i != j:
            kl = kullback_leibler(t[i], t[j])
            print('{:02}-{:02}: {}'.format(i, j, kl))
            ds.append(kl)

#%%
plt.hist(ds)


#%%
