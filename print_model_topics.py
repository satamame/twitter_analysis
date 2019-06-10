#%%

from gensim import models

# モデルの名前
model_name = 'data/lda_model'

# モデルを読み込む
model = models.LdaMulticore.load(model_name)

# トピックの基準となっている単語を表示する
model.print_topics(num_topics=-1, num_words=50)
