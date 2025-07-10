import pandas as pd
import numpy as np
import json
import tweepy
#Date
from datetime import datetime
import datetime as dt
from dateutil.relativedelta import relativedelta

class data_twitter:
    
    def __init__(self):
        with open(r'C:\Users\dylan\OneDrive\Documentos\Git\Codes\Cryptos\Credentials\twitter_credentials.json', 'r') as fp:
            access_params = json.load(fp)
        #assert "crypto" in access_params.keys(), "access_params must have a crypto"
        #assert "days_back" in access_params.keys(), "consumer_secret must have a days_back"
        #assert "time" in access_params.keys(), "access_token must have a time"
        assert "api_key" in access_params.keys(), "access_token_secret must have a api_key"
        assert "api_secret_key" in access_params.keys(), "access_token_secret must have a api_secret"
        assert "access_token" in access_params.keys(), "access_token_secret must have a access_token"
        assert "access_token_secret" in access_params.keys(), "access_token_secret must have a access_token_secret"
        #self.crypto = access_params["crypto"]
        #self.days_back = access_params["days_back"]
        #self.time = access_params["time"]
        self.api_key = access_params["api_key"]
        self.api_secret_key = access_params["api_secret_key"]
        self.access_token = access_params["access_token"]
        self.access_token_secret = access_params["access_token_secret"]
        
    def twitter_download(self, params):
        ################################################Elon Tweets################################################
        screen_name = params["screen_name"]
        try:
            # Create The Authenticate Object
            authenticate = tweepy.OAuthHandler(self.api_key, self.api_secret_key)
            # Set The Access Token & Access Token Secret
            authenticate.set_access_token(self.access_token, self.access_token_secret)
            # Create The API Object
            api = tweepy.API(authenticate, wait_on_rate_limit = True)
            #200 tweets es el maximo que se puede descargar
            tweets = api.user_timeline(screen_name = params["screen_name"], count = 200, lang = "en", tweet_mode = "extended")

            return(tweets)
        except Exception as e:
            if str(e) == """'created_at'""":
                print('*******Error: No hay tweets con esa palabra********')
            else:
                print(e)