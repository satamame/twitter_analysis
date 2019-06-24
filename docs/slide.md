---
marp: true
---

# トピックモデルによる短文の分類

by 佐田和也 (kazuya.sada@leadinge.co.jp)

---

# 目次

1. 当初の目標
1. データセットの収集
    1. Tweepy
    1. MongoDB
1. LDA モデル
1. チューニング
1. 成果
1. 振り返り

---

<!-- header: 当初の目標 -->

# 当初の目標
- 短文の分類をしたい
- データセットを自分で作りたい
    - Twitter から取得
- 余力があれば、ユーザごとのトピックの分布のパターンも調べてみたい
    - このトピックを発信する人は、あのトピックを発信しない、等

## 当初の懸念点
- 教師ラベルが無い
- 分類精度の決め方が分からない

---

<!-- header: データセットの収集 -->

# データセットの収集
## Tweepy
- Tweepy : Twitter API を扱うためのパッケージ
### Twitter API を使って、検索結果 (JSON) を取得
- 検索キーワードを決める必要があった
    - q = 'です OR ます OR でした OR ました OR でしょう OR ましょう'
- ユーザごとのタイムラインも保存しておいて、余力があれば分析する

---

<!-- header: データセットの収集 -->

## MongoDB
- PyMongo : MongoDB にアクセスするためのパッケージ
- NoQSLBooster for MongoDB : GUI ツール

### Collections
- tw_samples : 検索で取得したツイート (112,284 件)
- users : 検索で取得したツイート (96,895 件)
    - このうち 1,000 件くらいを、タイムラインを取得する対象とする
- usr_tweets : 選んだユーザのタイムラインから取得したツイート (2,043,636 件)

---

<!-- header: LDA モデル -->

# LDA モデル
- 「ある単語を含む文書は、ある確率であるトピックを持つ」という表現
- ベイズ推定によって直接的な単語でなくても予測できる
    - 短文の分類に向いているのではないか
- 一個の文書について、複数のトピックの「構成比」を予測する
- トピック ＝「文書に潜んでいる主題」  
    - 「経済」「エンタメ」などの「ジャンル」とはちょっと違う

---

<!-- header: LDA モデル -->

## gensim
- gensim : トピックモデリングのためのパッケージ
    - 辞書を作る
    - Bow 表現を作る
    - LDA モデルを作る

---

<!-- header: チューニング -->

# チューニング
## 指標
- Perplexity : 今回は使いません。
- Coherence : モデルを表す単語に一貫性があるか
- KL-divergence : トピック間の距離

---

<!-- header: チューニング -->

## パラメタ
- num_topics : トピックの数
- alpha : トピックの構成比がどうなっていると予測するか
    - 例 : すべてのトピックが同じ割合で出現
- no_below : 出現する文書が少ない単語をカット
- no_above : 出現する文書が多い単語をカット
- ストップワード（コーパス取得時の実装による）

---

<!-- header: 成果 -->

# 成果
## 最初のモデルによる分類
- 訓練データをそのまま分類にかけた結果
    - [topic 00](../data/01/topics_training/00.txt)
    - [topic 01](../data/01/topics_training/01.txt)
    - [topic 02](../data/01/topics_training/02.txt)
    - [topic 03](../data/01/topics_training/03.txt)
    - [topic 04](../data/01/topics_training/04.txt)
    - [topic 05](../data/01/topics_training/05.txt)
    - [topic 06](../data/01/topics_training/06.txt)
    - [topic 07](../data/01/topics_training/07.txt)

特にトピックごとの特徴、トピック間の違いがわかりませんでした。
