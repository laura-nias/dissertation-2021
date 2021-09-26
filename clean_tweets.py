#!/usr/bin/env python
# coding: utf-8

# In[18]:


import re
import numpy as np
import pandas as pd

pd.set_option('display.max_colwidth', None)

tweets_raw = pd.read_csv("tweets_v2.csv")

print(tweets_raw.info())


# In[19]:


tweets_raw.drop(columns=["Unnamed: 0", "Unnamed: 0.1", "Location", "Username"], axis=1, inplace=True)

print(tweets_raw.info())


# In[20]:


tweets_raw.drop_duplicates(inplace=True)

tweets_raw.to_csv("tweets_final_v2.csv")

display(tweets_raw.head())

print(tweets_raw.info())


# In[21]:


tweets_raw['Clean'] = tweets_raw['Content'].str.lower()

display(tweets_raw.head())


# In[22]:


ori = tweets_raw['Clean'].apply(str)

tweets_raw['Clean'] = ori.apply(lambda x: re.sub("@[\w]*", '', x))

clean = tweets_raw['Clean'].apply(str)

tweets_raw['Clean'] = clean.apply(lambda x: re.sub(r'http\S+|www\S+|https\S+', '', x))

display(tweets_raw.tail())


# In[23]:


tweets_raw['Clean'] = tweets_raw['Clean'].str.replace("[^a-zA-Z]", " ")
display(tweets_raw.head())


# In[24]:


tweets_raw['Clean'] = tweets_raw['Clean'].apply(lambda x: ' '.join([w for w in x.split() if len(w)>2]))

display(tweets_raw.head())


# In[25]:


tweets_raw['Clean'] = tweets_raw['Clean'].apply(lambda x: re.split('\W+', x))

display(tweets_raw.head())


# In[26]:


display(tweets_raw.head())


# In[27]:


import nltk
from nltk.corpus import stopwords

tweets_raw['Clean'] = tweets_raw['Clean'].apply(lambda x: [word for word in x if word not in stopwords.words('english')])

display(tweets_raw.head())


# In[28]:


display(tweets_raw.tail())


# In[29]:


tweets_raw.to_csv("tweets_clean.csv")


# In[30]:


from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

tweets_raw['Clean'] = tweets_raw['Clean'].apply(
                    lambda x:[lemmatizer.lemmatize(word) for word in x])


# In[31]:


display(tweets_raw.head())


# In[32]:


tweets_raw.to_csv("tweets_clean.csv")


# In[ ]:




