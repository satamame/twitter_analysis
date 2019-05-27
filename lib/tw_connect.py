import tweepy
from datetime import datetime
import time

class TwConn:
    """
    Twitter に接続するためのクラス
    """
    def __init__(self, consumer_token=None, consumer_secret=None):
        """
        コンストラクタ

        Parameters
        ----------
        consumer_token : str
        consumer_secret : str
        """
        if consumer_token and consumer_secret:
            self.set_consumer_token(consumer_token, consumer_secret)
        elif consumer_token or consumer_secret:
            raise ValueError('consumer_token and consumer_secret should be specified together.')
    
    def set_consumer_token(self, consumer_token, consumer_secret):
        """
        consumer_token と consumer_secret を指定して OAuthHandler を用意する

        Parameters
        ----------
        consumer_token : str
        consumer_secret : str
        """
        self.auth = tweepy.OAuthHandler(consumer_token, consumer_secret)

    def set_access_token(self, access_token, access_secret):
        """
        access_token と access_secret をセットする

        Parameters
        ----------
        access_token : str
        access_secret : str
        """
        if not isinstance(self.auth, tweepy.auth.OAuthHandler):
            raise TypeError(
                'Instance variable "auth" should be a tweepy.auth.OAuthHandler object.'
            )
        self.auth.set_access_token(access_token, access_secret)
    
    def search(self, q, *, max_id=None, since_id=None, count=None, pages=100):
        """
        ツイートの検索結果リストを繰り返し取り出すジェネレータ

        Parameters
        ----------
        q : str
            Search keyword.
        max_id : int
            Newest tweet id where the search start from.
        since_id : int
            Oldest tweet id where the search stops at.
        count : int
            Number of tweets to retrieve at a time. 100 at maximum.
        pages : int
            Limit of repetitions
        
        Yields
        ------
        results : list
            List of tweet info in json
        """
        api = tweepy.API(self.auth)
        page = 1
        while True:
            try:
                statuses = api.search(
                    q, max_id=max_id, since_id=since_id, count=count, tweet_mode='extended'
                )
            # API から RateLimitError が返ったら15分待って続行する
            except tweepy.RateLimitError:
                print('RateLimitError. Waiting for 15 minutes.')
                time.sleep(60 * 15)
                continue
            # その他のエラーなら再送出
            except Exception:
                raise
            
            if statuses:
                results = []
                for status in statuses:
                    # ツイートの作成日時を datetime 型に変換
                    dt = status._json['created_at']
                    dt = datetime.strptime(dt, "%a %b %d %H:%M:%S %z %Y")
                    status._json['created_at'] = dt

                    # ユーザの作成日時を datetime 型に変換
                    dt = status._json['user']['created_at']
                    dt = datetime.strptime(dt, "%a %b %d %H:%M:%S %z %Y")
                    status._json['user']['created_at'] = dt

                    # 次の検索は、最後に取得したツイートの id - 1 から
                    max_id = status._json['id'] - 1
                    
                    # JSON を結果リストに追加する
                    results.append(status._json)

                # 結果リストをイテレータの要素として返却
                yield results
            else:
                # All done
                break
            page += 1  # next page
            if page > pages:
                break

    def user_timeline(self, user_id, *, max_id=None, since_id=None, count=None, pages=100):
        """
        ユーザのツイートのリストを繰り返し取り出すジェネレータ

        Parameters
        ----------
        user_id : int
            User's id.
        max_id : int
            Newest tweet id where the search start from.
        since_id : int
            Oldest tweet id where the search stops at.
        count : int
            Number of tweets to retrieve at a time. 100 at maximum.
        pages : int
            Limit of repetitions
        
        Yields
        ------
        results : list
            List of tweet info in json
        """
        api = tweepy.API(self.auth)
        page = 1
        while True:
            try:
                statuses = api.user_timeline(
                    user_id=user_id, max_id=max_id, since_id=since_id, count=count
                )
            # API から RateLimitError エラーが返ったら15分待って続行する
            except tweepy.RateLimitError:
                print('RateLimitError. Waiting for 15 minutes.')
                time.sleep(60 * 15)
                continue
            # その他のエラーなら再送出
            except Exception:
                raise
            
            if statuses:
                results = []
                for status in statuses:
                    # ツイートの作成日時を datetime 型に変換
                    dt = status._json['created_at']
                    dt = datetime.strptime(dt, "%a %b %d %H:%M:%S %z %Y")
                    status._json['created_at'] = dt

                    # ユーザ情報を id のみにする
                    status._json['user'] = {'id': user_id}

                    # 次の検索は、最後に取得したツイートの id - 1 から
                    max_id = status._json['id'] - 1

                    # JSON を結果リストに追加する
                    results.append(status._json)

                # 結果リストをイテレータの要素として返却
                yield results
            else:
                break
            page += 1  # next page
            if page > pages:
                break
