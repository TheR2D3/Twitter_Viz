import pandas as pd
import numpy as np 
import tweepy
#from tweet_cleaner_rough import text_cleaner
from tweet_cleaner_rough import data_set_cleaner
from textblob import TextBlob
import json


#Function to calculate the sentiment
def senti_analyzer(sentence):
    blob1 = TextBlob(sentence)
    return(blob1.sentiment.polarity)


def dataframe_populator(screen_name):

    #Set the authorization keys and define the API
    auth = tweepy.OAuthHandler('PwIx3tXnoN6LNEjHMWtn2b7s2', '8vr859bsLSRyiijzMvFaACYqxnYNdLhcwTWhKEUPSrRSnrQziU')
    auth.set_access_token('150554502-Svlt33TXWClnGYpJ5G01SfVUYhXcEvXCaIfQW8nW', 'eiKA07ylhb5Y5dWWXTaRU09H39N8rVZMFQTOmNjD081n5')    
    
    api = tweepy.API(auth)

    #Get the input screen name and tweet object    
    tweet_object = api.user_timeline(screen_name = screen_name,count=10)

    #Get various items from tweet json and store it in tweet_object
    tweet_list=[]

    #for tweet in tweet_object:    
        #tweet_id = tweet.id # unique integer identifier for tweet
        #text = tweet.text # utf-8 text of tweet
        #favorite_count = tweet.favorite_count
        #retweet_count = tweet.retweet_count
        #created_at = tweet.created_at # utc time tweet created
        #source = tweet.source # utility used to post tweet
        #reply_to_status = tweet.in_reply_to_status_id # if reply int of orginal tweet id
        #reply_to_user = tweet.in_reply_to_screen_name # if reply original tweetes screenname
        #retweets = tweet.retweet_count # number of times this tweet retweeted
        #favorites = tweet.favorite_count # number of time this tweet liked
        # append attributes to list
        #tweet_list.append({'Tweet_id':tweet_id, 'Tweet':text, 'Favorite_count':favorite_count,'Retweet_count':retweet_count, 'Created_at':created_at, 'Source':source,
                                                #'Reply_to_status':reply_to_status, 'Reply_to_user':reply_to_user, 'Retweets':retweets, 'Favorites':favorites})

    #tweet_data_frame = pd.DataFrame(tweet_list, columns=['Tweet_id', 'Tweet',
                                            #'Favorite_count',
                                            #'Retweet_count',
                                            #'Created_at',
                                            #'Source',
                                            #'Reply_to_status',
                                            #'Reply_to_user',
                                            #'Retweets',
                                            #'Favorites'])

    for tweet in tweepy.Cursor(api.user_timeline, screen_name=screen_name, tweet_mode="extended").items(10):
        tweet_id=tweet.id        
        text = tweet.full_text
        favorite_count = tweet.favorite_count
        retweet_count = tweet.retweet_count
        created_at = tweet.created_at
        retweets = tweet.retweet_count
        favorites = tweet.favorite_count
        source = tweet.source
        tweet_list.append({'Tweet':text, 'Favourite_count':favorite_count,'Retweet_count':retweet_count, 'Created_at':created_at, 'Source':source, 'Retweets':retweets, 'Favorites':favorites})
    
    #Store the info from list to df
    tweet_data_frame = pd.DataFrame(tweet_list)

    #Clean the obtained dataset                                           
    cleaned_data_frame = data_set_cleaner(tweet_data_frame)

    #Drop the unwanted columns in the dataset
    cleaned_data_frame = cleaned_data_frame.drop(['Tweet_lower','No_Contractions','No_stop_words'], axis=1) 

    #Calculate and Populate the sentiments of the Tweets
    cleaned_data_frame['Sentiment'] = cleaned_data_frame['Stemmed_review'].apply(lambda x:senti_analyzer(x))

    #Form the hour column
    #cleaned_data_frame['Hour_of_tweet'] = cleaned_data_frame['Created_at'].apply(lambda x:x[11]+x[12])

    #Form the date column
    #cleaned_data_frame['Date'] = cleaned_data_frame['Created_at'].apply(lambda x:x[:10])

    #Form the Tweet/Re-tweet column
    #cleaned_data_frame['Is_retweet'] = cleaned_data_frame['Tweet'].apply(lambda x: 'Re-tweet' if (x[:2] == "RT") else "Tweet" )

    #Save the datafram
    #cleaned_data_frame.to_csv('saved_data.csv')

    #Return the dataset
    return(cleaned_data_frame)

def trend_name_populator(woe_id):

    #Initialize the APIs to extract trends
    auth = tweepy.OAuthHandler('PwIx3tXnoN6LNEjHMWtn2b7s2', '8vr859bsLSRyiijzMvFaACYqxnYNdLhcwTWhKEUPSrRSnrQziU')
    auth.set_access_token('150554502-Svlt33TXWClnGYpJ5G01SfVUYhXcEvXCaIfQW8nW', 'eiKA07ylhb5Y5dWWXTaRU09H39N8rVZMFQTOmNjD081n5')
    api = tweepy.API(auth)    
    
    #Load the location woe_id to populate trend object
    location_trend_obj = api.trends_place(woe_id) 
    trends = json.loads(json.dumps(location_trend_obj, indent=1))
    trend_list=[]
    
    for trend in trends[0]["trends"]:
        trend_list.append(trend["name"])

    return(trend_list[:5])

def trend_tweet_populator(hashtag):
    # The auth methods
    auth = tweepy.OAuthHandler('PwIx3tXnoN6LNEjHMWtn2b7s2', '8vr859bsLSRyiijzMvFaACYqxnYNdLhcwTWhKEUPSrRSnrQziU')
    auth.set_access_token('150554502-Svlt33TXWClnGYpJ5G01SfVUYhXcEvXCaIfQW8nW', 'eiKA07ylhb5Y5dWWXTaRU09H39N8rVZMFQTOmNjD081n5')
    api = tweepy.API(auth)

    tweet_string=[]
    hashtag_phrase= str(hashtag)


    for tweet in tweepy.Cursor(api.search, q= hashtag_phrase +' -filter:retweets', lang="en", tweet_mode="extended").items(10):
        tweet_string.append(tweet.full_text)
    
    return(tweet_string)


	


