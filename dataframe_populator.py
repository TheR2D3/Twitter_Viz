import pandas as pd
import numpy as np 
import tweepy
from tweet_cleaner import text_cleaner

def dataframe_populator(input_name):
    auth = tweepy.OAuthHandler('PwIx3tXnoN6LNEjHMWtn2b7s2', '8vr859bsLSRyiijzMvFaACYqxnYNdLhcwTWhKEUPSrRSnrQziU')
    auth.set_access_token('150554502-Svlt33TXWClnGYpJ5G01SfVUYhXcEvXCaIfQW8nW', 'eiKA07ylhb5Y5dWWXTaRU09H39N8rVZMFQTOmNjD081n5')

    data_set = pd.DataFrame()    
    api = tweepy.API(auth)