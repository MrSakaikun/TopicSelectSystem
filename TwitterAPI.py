import sys
import os

from requests_oauthlib import OAuth1Session
import settings


class TwitterAPI(object):
    def __init__(self,screen_name=''):
        # 環境変数から認証情報を取得する。
        CONSUMER_KEY = settings.CONSUMER_KEY
        CONSUMER_SECRET = settings.CONSUMER_SECRET
        ACCESS_TOKEN = settings.ACCESS_TOKEN
        ACCESS_TOKEN_SECRET = settings.ACCESS_TOKEN_SECRET

        # 認証情報を使ってOAuth1Sessionオブジェクトを得る。
        self.twitter = OAuth1Session(CONSUMER_KEY,
                        client_secret=CONSUMER_SECRET,
                        resource_owner_key=ACCESS_TOKEN,
                        resource_owner_secret=ACCESS_TOKEN_SECRET)
        #screen_nameを取得
        if screen_name == '':
            self.screen_name = settings.SCREEN_NAME
        else:
            self.screen_name = screen_name

    #user_idを取得
    def get_screen_name(self):
        return self.screen_name

    #ユーザのツイートを表示する関数
    def print_tweet_from_usertimeline(self):
        #url
        url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
        #パラメータ
        params = {'screen_name':self.screen_name,'lang':'ja','count':200,'exclude_replies':False,'include_rts':False}
        #ユーザーのタイムラインを取得する。
        response = self.twitter.get(url,params=params)
        # APIのレスポンスはJSON形式の文字列なので、response.json()でパースしてlistを取得できる。
        # statusはツイート（Twitter APIではStatusと呼ばれる）を表すdict。
        if response.status_code==200:
            statuses = response.json()
            for status in statuses:
                tweet = status['text']
                print(tweet)  #ツイートを表示する。
                print("\n")
        else:
            print("error")

    #ユーザのツイートを取得する関数
    def get_tweet_from_usertimeline(self):
        #url
        url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
        #パラメータ
        params = {'screen_name':self.screen_name,'lang':'ja','count':200,'exclude_replies':False,'include_rts':False}
        #ユーザーのタイムラインを取得する。
        response = self.twitter.get(url,params=params)
        # APIのレスポンスはJSON形式の文字列なので、response.json()でパースしてlistを取得できる。
        # statusはツイート（Twitter APIではStatusと呼ばれる）を表すdict。
        if response.status_code==200:
            statuses = response.json()
            #リストにして返す
            return [status['text'] for status in statuses]
        else:
            print('Error')
            return []

    #キーワード検索結果を表示する関数
    def print_tweet_from_keyword(self,keyword):
        #url
        url = 'https://api.twitter.com/1.1/search/tweets.json'
        #パラメータ
        params = {'q':keyword, 'lang':'ja','result_type':'mixed','count':100}
        #キーワード検索結果を取得
        response = self.twitter.get(url,params=params)
        # APIのレスポンスはJSON形式の文字列なので、response.json()でパースしてlistを取得できる。
        # statusはツイート（Twitter APIではStatusと呼ばれる）を表すdict。
        if response.status_code == 200:
            statuses = response.json()
            for status in statuses['statuses']:
                print('@' + status['user']['screen_name'], status['text'])  # ユーザー名とツイートを表示する。
        else:
            print('Error')

    #キーワード検索結果を取得する関数
    def get_tweet_from_keyword(self,keyword):
        #url
        url = 'https://api.twitter.com/1.1/search/tweets.json'
        #パラメータ
        params = {'q':keyword, 'lang':'ja','result_type':'mixed','count':100}
        #キーワード検索結果を取得
        response = self.twitter.get(url,params=params)
        # APIのレスポンスはJSON形式の文字列なので、response.json()でパースしてlistを取得できる。
        # statusはツイート（Twitter APIではStatusと呼ばれる）を表すdict。
        if response.status_code == 200:
            statuses = response.json()
            #ツイートをlistにして返す
            return [status['text'] for status in statuses['statuses']]
        else:
            print('Error')
