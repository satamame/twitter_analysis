import pymongo
from datetime import datetime
from janome.tokenizer import Tokenizer

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

    # サンプルツイートの全ユーザをチェック
    for d in col_twsamples.find({}, {'user': 1}):
        # 同じ id のユーザがすでに DB にあれば、更新する
        existing = [e for e in col_users.find({'user.id': d['user']['id']})]
        if len(existing) > 0 and existing[0]['updated'] != now:
            # 1個しか存在しないはずだが、ロジックとしては条件に合うもの全て更新
            col_users.update_many(
                {'user.id': d['user']['id']}, 
                {'$set': {'user': d['user'], 'updated': now}}
            )
        # なければ追加
        else:
            col_users.insert({
                'user': d['user'],
                'updated': now,
                'used_as_sample': False,
                'ignore': False,
                'tweet_count': 0
            }, {})

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
