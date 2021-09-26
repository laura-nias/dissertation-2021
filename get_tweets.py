#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tweepy
import pandas as pd
import numpy as np
import os

with open('twitter_api.txt') as file:
    consumer_key, consumer_key_secret, access_token, access_token_secret = [line.strip('\n').split('=')[1] for line in file.readlines()]

auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


# In[2]:


hashtags = ["#distancelearning", "#onlinelearning","#virtuallearning",
            "#onlineclasses","#digitallearning","#elearning","#onlineteaching","#blendedlearning"]

search_terms = ["distance learning","online learning","virtual learning","online classes",
              "digital learning","e learning","e-learning","online teaching","blended learning"]

def get_tweets(search, isHashtag):
    
    df_temp = pd.DataFrame(columns=["Content","Location","Username","Created at"])
    
    tweets = tweepy.Cursor(api.search, q=search+" -filter:retweets", lang="en",since="2020-05-24", tweet_mode='extended').items(3000)
    
    for tweet in tweets:
        content = tweet.full_text
        username = tweet.user.screen_name
        location = tweet.user.location
        created_at = tweet.created_at
        
        retrieved = [content, location, username, created_at]
        
        df_temp.loc[len(df_temp)] = retrieved
        
    path = os.getcwd()
    
    if isHashtag:
        filename = path + '/output/' + search[1:] + '_hashtag_v2.csv'
    else:
        filename = path + '/output/' + search.replace(" ", "") + '_keywords_v2.csv'
    
    df_temp.to_csv(filename)
    
for hashtag in hashtags:
    get_tweets(hashtag, isHashtag=True)

for search in search_terms:
    get_tweets(search, isHashtag=False)
    


# In[ ]:




