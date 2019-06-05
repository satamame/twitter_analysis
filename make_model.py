#%%
"""
make_model.py
辞書とコーパスを読み込んで「潜在的ディリクレ配分法」による
分類モデルを作る
"""

#%%

from gensim import corpora, models
from gensim.test.utils import datapath
from lib.gensim_util import StreamCorpus

#%%

num_topics = 3

# 辞書とコーパスの名前 (拡張子なし)
dict_name = 'data/dictionary'
corpus_name = 'data/corpus_training'

# 保存するモデルの名前
model_name = 'data/lda_model'

#%%

# 辞書を読み込む
dict_file_name = dict_name + '.dict'
dict = corpora.Dictionary.load(dict_file_name)

# コーパスを読み込む
corpus = StreamCorpus(corpus_name + '.txt')

#%%

# モデルにする
m = models.LdaModel(
    corpus=corpus, id2word=dict, num_topics=num_topics)

#%%

# Save model to disk.
m.save(model_name)
print('Model saved as {}.'.format(model_name))
