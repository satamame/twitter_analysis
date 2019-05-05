# やったことの記録

## Twitter API 準備

- https://dev.twitter.com/apps へ行く。
- Application を作るか開くかして、以下の文字列を手元に保存しておく。
    - Consumer Key
    - Consumer Secret
    - Access Token
    - Access Token Secret

参考
- [PHP+OAuthでTwitter](https://sdn-project.net/labo/oauth.html)

---
## Tweepy インストール

- Project フォルダで
    ```
    > pipenv install tweepy
    ```
- 入ったバージョンは `3.7.0` でした。

---
## Twitter API 接続用クラス作成

**File:** lib/tw_connect.py  
**Class:** TwConn

- 検索結果を繰り返し取り出すジェネレータを作成。  
    **Method:** search
- Key や Token をハードコードしたスクリプトを作って、動作確認しました。

参考
- [API Reference - tweepy 3.7.0 documentation](http://docs.tweepy.org/en/3.7.0/api.html)
- [python - Tweepy "page parameter is invalid" error - Stack Overflow](
    https://stackoverflow.com/questions/31958964/tweepy-page-parameter-is-invalid-error)

---
## MongoDB インストール

- [MongoDB Download Center | MongoDB](https://www.mongodb.com/download-center/community) からインストーラをダウンロードする。
    - インストーラに従えば、インストールとサービス化までできます。
- インストールしたバージョンは `4.0.9` でした。
- インストールされたパスは `C:\Program Files\MongoDB\Server\4.0` です。

参考
- [PythonからMongoDB(DocumentStore)を使ってみる](
    https://hytmachineworks.hatenablog.com/entry/2018/08/03/230503)
- [pythonでMongoDB入門しよう](https://qiita.com/Syoitu/items/db192385a4b2e4884ed5)

---
## NoSQLBooster for MongoDB インストール

NoSQLBooster for MongoDB は、MongoDB を GUI で操作できるクライアントです。  
便利なので入れておきます。

- [Download NoSQLBooster for MongoDB](https://nosqlbooster.com/downloads) からインストーラをダウンロードする。
    - インストーラに従えば、普通にインストールできます。
- インストールしたバージョンは `5.1.7` でした。

参考
- [Windowsで使えるMongoDBのGUIクライアントソフトをまとめてみた - エンジニアステップ](
    https://www.engineer-step.com/entry/mongodb-client)

---
## PyMongo インストール

- Project フォルダで
    ```
    > pipenv install pymongo
    ```
- 入ったバージョンは `3.8.0` でした。

---
## サンプルツイート取得スクリプト作成

**File:** retrieve_tweets.py

- Twitter API 接続用クラス を使って取得した tweets を、PyMongo で DB に保存します。
- 一度に取得できる tweets に限りがあるので、繰り返し実行します。
- すでに取得済みの tweets より新しいもののみ取得するようにします。
    - そのため id でソートするオペレーションが入るので、id にインデックスをつけておきます。
- DB から最新の id を取得するメソッドは、`lib/mongo_util.py` に作りました。

サンプルツイートの Collection の id 列にインデックスをつける。
- これをしないと、ソート時にメモリ不足になります。
- `tw_samples` という Collection がまだない場合は作ります。
    - このスクリプトを一度実行すれば作られます。
- NoSQLBooster for MongoDB で Shell Tab を開いて実行するのが楽です。
    ```
    db.tw_samples.createIndex({id: 1}, {unique: true})
    ```

参考
- [MongoDB CRUD Operations](https://docs.mongodb.com/manual/crud/)
- [MongoDBにpythonのdatetimeオブジェクトを保存した時の挙動](
    https://qiita.com/TeraBytes/items/d9360bf908f3080f6af0)

---
## ユーザ情報抽出スクリプト作成

**File:** update_users.py

- 保存したサンプルツイートから、ユーザ情報のみ重複がないように抽出し、別の Collection に保存します。
- あとでこの Collection からユーザを選んでツイートを取得するので、サンプルとして選ばれたかどうかの列 (`used_as_sample`) を設けます。
- 実際の処理は `lib/mongo_util.py` に作って、呼び出すようにしました。

---
## ユーザツイート取得スクリプト作成

**File:** retrieve_usr_tweets.py

- DB のユーザ情報の Collection からランダムにユーザを選んで、各ユーザのツイートを取れるだけ取ってきて、DB に保存します。
- サンプルツイートでトピックモデルが作れたら、トピックの頻度を特徴量としてユーザを分類してみたいので、そのためのデータです。
