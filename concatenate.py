#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import os

path = os.getcwd() + "/output/second/"
files = os.listdir(path)

df_list = []

for file in files:
    df = pd.read_csv(path + file, index_col=None)
    df_list.append(df)

tweets_raw = pd.concat(df_list, axis=0, ignore_index=True)

tweets_raw.to_csv("tweets_v2.csv")

