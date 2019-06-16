#%%
"""
make_model.py
辞書とコーパスのファイルを読み込んで
「潜在的ディリクレ配分法」による分類モデルを作る
"""

#%%

from gensim import corpora, models
from gensim.test.utils import datapath
from lib.gensim_util import StreamCorpus
import logging

logging.getLogger('smart_open').setLevel(logging.ERROR)

#%%

# 出来たモデルの、トピックごとのパラメタを表示するか？
verbose = True

# 何個のトピックに分類するか
num_topics = 5

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
corpus_file_name = corpus_name + '.txt'
corpus = StreamCorpus(corpus_file_name)

#%%

# モデルにする
model = models.LdaMulticore(
    corpus=corpus, id2word=dict, num_topics=num_topics)

#%%

# Save model to disk.
model.save(model_name)
if verbose:
    for topic in model.print_topics(-1):
        print(topic)
print('Model saved as {}.'.format(model_name))
