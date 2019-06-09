# 操作

## スクリプト

### サンプルツイートを取得する

1. 必要なら DB の tw_ana.tw_samples をクリアしておく。
1. `retrieve_tweets.py` を開く。
1. 必要なら編集して、検索キーワードを指定する。
1. `retrieve_tweets.py` を実行する。
    - (それなりに時間がかかります。)

### サンプルツイートからユーザ情報を取得する

1. 必要なら DB の tw_ana.users をクリアしておく。
1. `update_users.py` を実行する。
    - (1件ずつループするので、時間がかかります。)

### ランダムでユーザを選んでツイートを取得する

1. 必要なら DB の tw_ana.usr_tweets をクリアしておく。
    - クリアするなら、tw_ana.users の used_as_sample, tweet_count も。
1. `retrieve_usr_tweets.py` を開く。
1. 必要なら編集して、選ぶユーザ数を指定する。
1. `retrieve_usr_tweets.py` を実行する。
    - 選ばれたユーザは、used_as_sample が true になり、二度選ばれない。
    - (環境にもよりますが、2～3時間かかります。)

### サンプルツイートから訓練データを選ぶ

1. `mark_training_data.py` を開く。
1. 必要なら編集して、訓練データの数を指定する。
1. `mark_training_data.py` を実行する。
    - すべてのツイートの training_data が初期化される。
    - ランダムで選ばれたツイートの training_data が true になる。

### 訓練データから辞書とコーパスを作る

1. `extract_training_data.py` を開く。
1. 必要なら編集して以下のパラメタを決める。
    - no_below, no_above (辞書に採用する単語の基準)
    - 辞書とコーパスの名前（拡張子はつけなくて良い)
1. `extract_training_data.py` を実行する。

### 辞書とコーパスを基に分類モデルを作る

1. `make_model.py` を開く。
1. 辞書とコーパスの名前（上で保存したもの）を設定する。
1. 保存するモデルの名前を設定する。
1. `make_model.py` を実行する。
1. 分類の基準となる単語を見るには、`print_model_topics` を実行する。

### 訓練データの分類結果を見る

1. `cluster_training_data` を開く。
1. 必要なら編集して閾値やファイル名を決める。
1. `cluster_training_data` を実行する。
1. 指定したフォルダ内に、トピックごとに分類されたテキストファイルが作られる。

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
1. `db.<collection 名>.createIndex({<列名>: 1}, {unique: true})` と入力する。  
    例
    ```
    db.tw_samples.createIndex({id: 1}, {unique: true})
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
