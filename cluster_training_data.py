#%%
"""
cluster_training_data.py
モデルをファイルから読み込んで、訓練データを分類する。
結果をトピックごとのテキストファイルに保存（上書き）する。
"""

#%%

from pymongo import MongoClient, DESCENDING
from gensim import corpora, models
from lib.mongo_util import StreamWords
import os
import shutil
import re

#%%

# probability の閾値（これより小さい場合は無視）
minp = 0.5

# 保存先のフォルダ名
save_folder_name = 'data/topics_training'

# モデルの名前
model_name = 'data/lda_model'

# 辞書の名前
dict_name = 'data/dictionary'

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

# サンプルツイートから単語列を取得するイテラブル
stream = StreamWords(col_twsamples, 'words')

#%%

# モデルを読み込む
model = models.LdaMulticore.load(model_name)

# 辞書を読み込む
dict_file_name = dict_name + '.dict'
dict = corpora.Dictionary.load(dict_file_name)

#%%

# DB 上で 分類し、構成率が最大であるトピックの ID を記録する
# ファイルへの書き出しは、DB を読みながらおこなう
stream.label_topics(ids, model, dict, minp)

#%%

# 出力先フォルダが存在し、空であること
if os.path.exists(save_folder_name):
    shutil.rmtree(save_folder_name)
os.mkdir(save_folder_name)

#%%

# テキスト中の空白文字を置き換えるための正規表現
regex = re.compile(r'\s')

#%%

# トピック ID のリスト
topic_ids = col_twsamples.find({'topic_id': {'$exists': True}}).distinct('topic_id')

# ファイルに書き出す
for topic_id in topic_ids:
    results = col_twsamples.find({'topic_id': topic_id}, {
        'full_text': 1,
        'topic_id': 1,
        'topic_prob': 1
    }).sort('topic_prob', DESCENDING)

    full_path = ('{}/{:02}.txt'.format(save_folder_name, topic_id))
    with open(full_path, 'w', encoding='utf-8') as f:
        for result in results:
            f.write('{}\t{}\n'.format(
                result['topic_prob'], regex.sub(' ', result['full_text']))
            )
