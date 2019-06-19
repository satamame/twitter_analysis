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
|alpha|default (symmetric)|

### 結果

Coherence: -4.103670646845522  
![Coherence](../data/01/coherence.png)

KL-divergence: 0.808693450476442  
![KL-divergence](../data/01/kl-divergence.png)

---
## model_02
25fe30fc69c8869c14bcc4f874232e09f51760dd

### 条件

|項目|値|
|-|-|
|品詞|'名詞', '動詞', '形容詞', '形容動詞'|
|ノイズ除去|RT, URL, mention|
|stop_words|**追加した** (See stop_words.py)|
|訓練データ数|50,000|
|no_below|20|
|no_above|0.2|
|num_topics|8|
|alpha|default (symmetric)|

### 結果
Coherence: -5.036905587315074  
![Coherence](../data/02/coherence.png)

KL-divergence: 0.8286949076822826  
![KL-divergence](../data/02/kl-divergence.png)

---
## model_03
2fbeb09304bb02f3d46ba7d37046f4fa5dd8d827

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
|alpha|**auto**|

### 結果
Coherence: -5.491802105728876  
![Coherence](../data/03/coherence.png)

KL-divergence: 4.820552068097251  
![KL-divergence](../data/03/kl-divergence.png)
