import pymongo
from datetime import datetime

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
    for d in col_twsamples.find({}, {'user':1}):
        # 同じ id のユーザがすでに DB にあれば、更新する
        existing = [e for e in col_users.find({'user.id': d['user']['id']})]
        if len(existing) > 0 and existing[0]['updated'] != now:
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
