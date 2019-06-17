# Tuning history

## model_01
be6c9e6e852144f53271d1c68c11468e5250512d

### 条件

|項目|値|
|-|-|
|品詞|'名詞', '動詞', '形容詞', '形容動詞'|
|ノイズ除去|RT, URL, mention|
|stop_words|(See stop_words.py)|
|訓練データ数|50,000|
|no_below|20|
|no_above|0.2|
|num_topics|8|
|alpha|default (1 / num_topics)|

### 結果

|項目|値|
|-|-|
|Coherence|-4.103670646845522|
|KL-divergence|0.808693450476442|

