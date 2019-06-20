#%%

from gensim import models

# モデル番号
model_no = '04'

# モデルの名前
model_name = 'data/' + model_no + '/lda_model'

# 出力先
f_out = 'data/' + model_no + '/topics.txt'

# モデルを読み込む
model = models.LdaModel.load(model_name)

# トピックの基準となっている単語を出力する
with open(f_out, 'w', encoding='utf-8') as f:
    for topic in model.print_topics(num_topics=-1, num_words=100):
        print(topic, file=f)
