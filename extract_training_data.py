#%%
"""
extract_training_data.py
サンプルツイートから training_data としてマークされているデータを
取り出し、特徴語辞書とコーパスを作る。
"""

#%%

from pymongo import MongoClient
from gensim import corpora
from lib.mongo_util import StreamWords

#%%

# 使われてるツイートが no_below 個以下の単語は無視
no_below = 2
# 使われてるツイートの割合が no_above 以上の単語は無視
no_above = 0.3

# 保存する時の名前 (拡張子なし)
dict_name = 'data/dictionary'
corpus_name = 'data/corpus_training'

#%%

# データベースの準備
client = MongoClient()
# API で適当に取ってきた サンプルツイートの Collection
col_twsamples = client.tw_ana.tw_samples

#%%

# training_data の id を抽出
ids = [d['id'] for d in col_twsamples.find(
    {'words': {'$exists': True}, 'training_data': True},
    {'id': 1}
)]

#%%

# サンプルツイートから単語列を取得するイテラブル
stream = StreamWords(col_twsamples, 'words')

# 辞書作成
dict = corpora.Dictionary(stream.words_from_col(ids))
dict.filter_extremes(no_below=no_below, no_above=no_above)

# 保存
dict_file_name = dict_name + '.dict'
dict.save(dict_file_name)
print('Dictionary saved as {}.'.format(dict_file_name))
dict.save_as_text(dict_name + '.txt')

#%%

# コーパス作成 & 保存
corpus_file_name = corpus_name + '.txt'
with open(corpus_file_name, 'w') as f:
    for words in stream.words_from_col(ids):
        print(dict.doc2bow(words), file=f)
print('Corpus saved as {}.'.format(corpus_file_name))
