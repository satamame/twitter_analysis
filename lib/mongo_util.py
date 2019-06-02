import pymongo
from datetime import datetime
from janome.tokenizer import Tokenizer
import re

def next_id(collection):
    """
    与えられた collection の id フィールドを見て最大値 + 1 を返す

    collection にドキュメントが無ければ、None を返す。
    すべてのドキュメントに id フィールドがある事が前提。

    Parameters
    ----------
    collection : pymongo.collection.Collection

    Returns
    -------
    next_id : int
        None if collection doesn't have document.
    """
    if not isinstance(collection, pymongo.collection.Collection):
        raise TypeError(
            'Argument "collection" should be a pymongo.collection.Collection object. '
        )
    
    # DB のデータを id で降順にソートして id のリストを得る
    sorted = [d['id'] for d in collection.find({}, {'id': 1}).sort([('id', -1)])]

    # 結果があれば、最初の値 (最大値) + 1 を返す
    if len(sorted) > 0:
        return sorted[0] + 1
    else:
        return None

def update_users(col_users, col_twsamples):
    """
    サンプルツイートからユーザを取り出して、ユーザ collection を更新する

    Parameters
    ----------
    col_users : pymongo.collection.Collection
        更新するユーザの collection
    col_twsamples : pymongo.collection.Collection
        サンプルツイートの collection
    """
    # タイムゾーンなしの現在の UTC 日時
    now = datetime.utcnow()

    uids = col_twsamples.distinct('user.id')
    upd_count = 0
    add_count = 0
    # サンプルツイートの全ユーザ ID を重複なく取り出す
    for uid in uids:
        # ユーザ情報を取得
        user = col_twsamples.find_one({'user.id': uid})['user']
        # 同じ id のユーザがすでに DB にあれば、更新する
        existing = [e for e in col_users.find({'user.id': uid})]
        if len(existing) > 0:
            # 1個しか存在しないはずだが、ロジックとしては条件に合うもの全て更新
            col_users.update_many(
                {'user.id': uid}, {'$set': {'user': user, 'updated': now}}
            )
            upd_count += 1
        # なければ追加
        else:
            col_users.insert({
                'user': user,
                'updated': now,
                'used_as_sample': False,
                'ignore': False,
                'tweet_count': 0
            }, {})
            add_count += 1

        count = upd_count + add_count
        if count % 100 == 0:
            print('{}/{} users processed.'.format(count, len(uids)))

    print('{} users updated and {} users added.'.format(upd_count, add_count))

def add_tokenized_words(collection, text_field, words_field, count=0):
    """
    text_filed を形態素解析して words_field に単語列をセットする

    未処理の document が対象となる。
    やり直したい場合は document から words_field を削除しておく。

    Parameters
    ----------
    collection : pymongo.collection.Collection
        対象とする collection
    text_field : str
        形態素解析の対象とするテキストのフィールド名
    words_field : str
        形態素解析の結果をセットするフィールド名
    count : int
        処理する件数。0 なら未処理のもの全て
    """

    # 件数分の id を document (words_field が未セットのもの) から取得
    if count == 0:
        tweets = collection.find({words_field: {'$exists': False}}, {'id': 1})
    else:
        tweets = collection.find({words_field: {'$exists': False}},{'id': 1}).limit(count)
    ids = [d['id'] for d in tweets]

    t = Tokenizer()
    pos_to_pick = ['名詞', '動詞', '形容詞', '形容動詞']

    progress = 0
    progress_unit = 1000
    for i, id in enumerate(ids):
        tweet = collection.find_one({'id': id})
        text = tweet[text_field]
        words = [tk.base_form for tk in t.tokenize(text)
            if tk.part_of_speech.split(',')[0] in pos_to_pick]
        collection.find_one_and_update({'id': id},
            {'$set': {words_field: words}}
        )

        if i + 1 >= progress_unit * (progress + 1):
            print(i + 1)
            progress += 1
    
    print('{} tweets were tokenized.'.format(len(ids)))


class StreamWords(object):

    # ストップワード (クラス変数)
    stop_words = [
        r'\d+',
        r'RT',
        r'https?',
        r'[0-9:;/\\!?@#$%^&*()\-_=+*.,\'"\[\]｀´ー…～＃｢｣「」]+',
    ]

    def __init__(self, collection, words_field, used_field=''):
        """
        コンストラクタ

        parameters
        ----------
        collection : pymongo.collection.Collection
            対象とする collection
        words_field : str
            単語列が格納されているフィールド名
        used_field : str
            コーパスとして使われたという bool 値を記録するフィールド名。
            空なら記録しない。
        """
        self.collection = collection
        self.words_field = words_field
        self.used_field = used_field
    
    def words_from_col(self, ids, init_used_field=True):
        """
        DB の Collection から 単語列を取り出すジェネレータ

        parameters
        ----------
        ids : list
            id のリスト。一致する Document から単語列を取り出す。
        init_used_field : bool
            self.used_field で指定されたフィールドを最初に初期化するか。
        """
        coll = self.collection
        wrd_f = self.words_field
        usd_f = self.used_field

        # コーパスとして使われた記録をクリア
        if len(usd_f) > 0 and init_used_field:
            coll.update_many({}, {'$set': {usd_f: False}})

        for id in ids:
            # DB から words を取得
            words = coll.find_one({'id': id}, {wrd_f: 1})[wrd_f]
            # ストップワードを除外する
            for sw in StreamWords.stop_words:
                words = [w for w in words if not re.fullmatch(sw, w, flags=re.IGNORECASE)]

            yield words

            # フラグを立てる
            if len(usd_f) > 0:
                coll.update_one({'id': id}, {'$set': {usd_f: True}})
