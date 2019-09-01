# 操作

## ツイートの分類

### サンプルツイートを取得する

1. Twitter アプリ作成時に取得したトークンを `lib/token.py` に設定しておく。
1. 必要なら DB の tw_ana.tw_samples をクリアしておく。
1. `retrieve_tweets.py` を開く。
1. 必要なら編集して、検索キーワードを指定する。
1. `retrieve_tweets.py` を実行する。
    - (それなりに時間がかかります。)

### テキストのみの Collection を作る (任意だが推奨)

1. `gen_text_only.py` を開く。
1. 必要なら編集して、元となるサンプルツイート Collection や、作成するテキストのみの Collection を指定する。
1. `gen_text_only.py` を実行する。
    - full_text というフィールドを持つ Collection が作成/上書きされる。
    - 同じ full_text を持つ Document があった場合は追加しません (これにより重複するツイートを削除できます)。
1. このステップをした場合は、以下の手順の "サンプルツイート" として、テキストのみの Collection が使えます。

### サンプルツイートを形態素解析する
**mongo_util.py で使う品詞などを変更した場合はここからやり直す**

1. `tokenize_tweets.py` を開く。
1. 必要なら編集して、何件処理するか指定する。
1. `tokenize_tweets.py` を実行する。

### サンプルツイートから訓練データを選ぶ

1. `mark_training_data.py` を開く。
1. 必要なら編集して、訓練データの数を指定する。
1. `mark_training_data.py` を実行する。
    - すべてのツイートの training_data が初期化される。
    - ランダムで選ばれたツイートの training_data が true になる。

### 訓練データから辞書とコーパスを作る
**ストップワードを更新した場合はここからやり直す**

1. `extract_training_data.py` を開く。
1. 必要なら編集して以下のパラメタを決める。
    - no_below, no_above (辞書に採用する単語の基準)
    - 辞書とコーパスの名前（拡張子はつけなくて良い)
1. `extract_training_data.py` を実行する。

### 辞書とコーパスを基に LDA モデルを作る

1. `make_model.py` を開く。
1. 何個のトピックに分類するかを設定する。
1. 辞書とコーパスの名前（上で保存したもの）を設定する。
1. 保存するモデルの名前を設定する。
1. `make_model.py` を実行する。

### 分類の基準となる単語を見る

1. `print_model_topics` を開く。
1. 読み込むモデルの名前を指定する。
1. `print_model_topics` を実行する。
1. 特徴っぽくない単語があれば、ストップワードに追加してやり直す。

### 訓練データの分類結果を見る

1. `cluster_training_data` を開く。
1. 読み込むモデルの名前を指定する。
1. 必要なら編集して閾値やファイル名を決める。
1. `cluster_training_data` を実行する。
1. 指定したフォルダ内に、トピックごとに分類されたテキストファイルが作られる。
1. 人間が見て、何のトピックか想像がつかなければ、モデルを改良する。

### モデルの評価を描画・保存する

1. `eval_model.py` を開く。
1. 評価するモデルの名前を指定する。
1. `eval_model.py` を実行する。
1. Coherence のヒストグラムが描画され、平均値が保存される。
1. カルバック・ライブラー距離のヒストグラムが描画され、平均値が保存される。

### サンプルツイートからテストデータを選ぶ

1. `mark_test_data.py` を開く。
1. 必要なら編集して、テストデータの数を指定する。
1. `mark_test_data.py` を実行する。
    - すべてのツイートの test_data が初期化される。
    - training_data 以外のツイートからランダムで選ばれたものの test_data が true になる。

### テストデータの分類結果を見る

1. `cluster_test_data` を開く。
1. 必要なら編集して閾値やファイル名を決める。
1. `cluster_test_data` を実行する。
1. 指定したフォルダ内に、トピックごとに分類されたテキストファイルが作られる。

---
## ユーザツイートの分類

### サンプルツイートからユーザ情報を取得する

1. 必要なら DB の tw_ana.users をクリアしておく。
1. `update_users.py` を実行する。
    - (1件ずつループするので、時間がかかります。)

### ランダムでユーザを選んでツイートを取得する

1. 必要なら DB の tw_ana.usr_tweets をクリアしておく。
    - クリアするなら、tw_ana.users の used_as_sample, tweet_count もクリアすること。
1. `retrieve_usr_tweets.py` を開く。
1. 必要なら編集して、選ぶユーザ数を指定する。
1. `retrieve_usr_tweets.py` を実行する。
    - 選ばれたユーザは、used_as_sample が true になり、二度選ばれない。
    - (私の環境では、100ユーザ分を取得するのに、2～3時間かかりました。)

### ユーザツイートからテストデータを選ぶ

1. `mark_usr_tweets_to_cluster.py` を開く。
1. 必要なら編集して、テストデータとして使うユーザ数を指定する。
1. `mark_usr_tweets_to_cluster.py` を実行する。
    - tw_ana.usr_tweets の、ランダムで選ばれたユーザのツイートに test_data フラグが付く。

### ユーザツイートを形態素解析する

1. `tokenize_usr_tweets.py` を開く。
1. 必要なら編集して、何件処理するか指定する (通常は 0 (すべて))。
1. 形態素解析の品詞や方法が変わった場合は `clear = True` にする。
    - すでにある形態素解析の結果を削除したくない場合は `True` にしないよう、注意してください。
1. `tokenize_tweets.py` を実行する。
    - (私の環境では、1000件処理するのに10～15分くらいかかりました。)

### ユーザツイートを分類する

1. `cluster_usr_tweets.py` を開く。
1. 必要なら編集して、モデル番号や閾値を決める。
1. 必要なら実行前に `topic_id`, `topic_prob` フィールドをクリアしておく。
    ```
    col_usrtweets.update_many({}, {'$unset': {'topic_id': '', 'topic_prob': ''}})
    ```
1. `cluster_usr_tweets.py` を実行する。
    - テストデータとしてマークされたユーザツイートに、topic_id と topic_prob がセットされる。

### ユーザごとのトピック別文書数をカウントする

1. `count_usr_topics.py` を開いて実行する。
    - `col_usrtopics` で指定された Collection に、ユーザごとのトピック別文書数が格納される。

### ユーザを分類する



---
## NoSQLBooster for MongoDB

### Collection の全 documents をクリアする

1. 右上の (+) ボタンを押して Shell Tab を開く。
1. `db.<collection 名>.deleteMany({})` と入力する。  
    例
    ```
    db.tw_samples.deleteMany({})
    ```
1. Tool Bar の Run ボタンを押す（または Ctrl + Enter）。

### Collection の列にインデックスを追加する

1. 右上の (+) ボタンを押して Shell Tab を開く。
1. `db.<collection 名>.createIndex({<列名>: 1}, {<options>})` と入力する。  
    例1 - ユニークなインデックス
    ```
    db.tw_samples.createIndex({id: 1}, {unique: true})
    ```
    例2 - 降順ソートのためのインデックス
    ```
    db.tw_samples.createIndex({topic_prob: -1})
    ```
1. Tool Bar の Run ボタンを押す（または Ctrl + Enter）。

### DB を Export する

1. DB (tw_ana) を選択した状態で Export > Mongodump... 。
1. ダイアログで Export する Collection を選んで 'Dump'。
1. mongodump.exe の場所を聞かれたら、インストール先を選択する。
1. 出力先を指定する。

### DB を Import する

1. Import > Mongorestore... 。
1. mongorestore.exe の場所を聞かれたら、インストール先を選択する。
1. 読み込むフォルダを指定する。
    - 注意: Dump folder を指定する場合は、DB フォルダの上のフォルダを指定する。
