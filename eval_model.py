#%%
"""
eval_model.py
モデルの評価のため、以下の指標を算出する。
- coherence : トピック内の単語の類似度
- カルバック・ライブラー距離 : トピック間の距離
"""

#%%

from gensim import corpora, models
from gensim.matutils import kullback_leibler
import matplotlib.pyplot as plt
from lib.gensim_util import StreamCorpus
from statistics import mean

#%%

# モデル番号
model_no = '02'

# モデルの名前
model_name = 'data/' + model_no + '/lda_model'

# コーパスの名前 (拡張子なし)
corpus_name = 'data/' + model_no + '/corpus_training'

#%%

# モデルを読み込む
model = models.LdaMulticore.load(model_name)

# コーパスを読み込む
corpus_file_name = corpus_name + '.txt'
corpus = StreamCorpus(corpus_file_name)

#%%

# 各トピックの Coherence を算出し描画する (大きいほど良い)
tps = model.top_topics(corpus=corpus)
plt.title('Coherence')
plt.hist([tp[1] for tp in tps ])
plt.savefig('data/' + model_no + '/coherence.png')

# 平均値をテキスト保存
c_mean = mean([tp[1].astype(float) for tp in tps ])
print('Coherence: {}\n'.format(c_mean))
with open('data/' + model_no + '/evaluation.txt', 'w') as f:
    f.write('Coherence: {}\n'.format(c_mean))

#%%

# トピック間のカルバック・ライブラー距離を算出し描画する

# トピックごとの、辞書内の単語を含む文がそのトピックに分類される (事後) 確率
t = model.state.get_lambda()

# トピック同士の確率分布の距離を表示 (離れているほど良い)
ds = []
for i in range(model.num_topics):
    for j in range(model.num_topics):
        if i != j:
            kl = kullback_leibler(t[i], t[j])
            # print('{:02}-{:02}: {}'.format(i, j, kl))
            ds.append(kl)

# グラフを保存
plt.title('KL-divergence')
plt.hist(ds)
plt.savefig('data/' + model_no + '/kl-divergence.png')

# 平均値をテキスト保存
d_mean = mean([d.astype(float) for d in ds])
print('KL-divergence: {}\n'.format(d_mean))
with open('data/' + model_no + '/evaluation.txt', 'a') as f:
    f.write('KL-divergence: {}\n'.format(d_mean))
