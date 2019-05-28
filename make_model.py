#%%
"""
make_model.py
辞書とコーパスを読み込んで「潜在的ディリクレ配分法」による
分類モデルを作る
"""

#%%

from gensim import corpora, models
from gensim.test.utils import datapath

#%%

# 辞書とコーパスの名前 (拡張子なし)
dict_name = 'dictionary'
corpus_name = 'corpus'

# 保存するモデルの名前
model_name = 'lda_model'


#%%

# 辞書を読み込む
dict_file_name = dict_name + '.dict'
dict = corpora.Dictionary.load(dict_file_name)

# コーパスを読み込む
corpus_file_name = corpus_name + '.mm'
corpus = corpora.MmCorpus(corpus_file_name)

#%%

# モデルにする
m = models.LdaModel(corpus=corpus, id2word=dict, num_topics=3)

#%%

# Save model to disk.
m.save(model_name)
print('Model saved as {}.'.format(model_name))
