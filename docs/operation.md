# 操作

## スクリプト

### サンプルツイートを取得する

1. 必要なら DB の tw_ana.tw_samples をクリアしておく。
1. `retrieve_tweets.py` を編集し、検索キーワードを指定する。
1. `retrieve_tweets.py` を実行する。
    - VSCode に仮想環境の設定をしていれば、最初のセルで Run Below で実行できる。
    - またはコマンドプロンプトで `pipenv run python retrieve_tweets.py` とする。

### サンプルツイートからユーザ情報を取得する

1. 必要なら DB の tw_ana.users をクリアしておく。
1. `update_users.py` を実行する。

### ランダムでユーザを選んでツイートを取得する

1. 必要なら DB の tw_ana.usr_tweets をクリアしておく。
    - クリアするなら、tw_ana.users の used_as_sample, tweet_count も。
1. `retrieve_usr_tweets.py` を編集し、選ぶユーザ数を指定する。
1. `retrieve_usr_tweets.py` を実行する。
    - 選ばれたユーザは、used_as_sample が true になり、次回から選ばれない。

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
