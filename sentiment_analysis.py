#!/usr/bin/env python
# coding: utf-8

# In[5]:


import nltk 
import pandas as pd

from nltk.corpus import sentiwordnet as swn

df = pd.read_csv("tweets_clean.csv")

display(df.head())


# In[6]:


df.drop(columns=["Unnamed: 0"], axis=1, inplace=True)

display(df.head())


# In[7]:


nltk.download('averaged_perceptron_tagger')
from nltk.tokenize import word_tokenize

pd.set_option('display.max_colwidth', None)

df["Pos"] = df["Clean"].astype(str).str.replace('\[|\]|\'|\,', '')

pos = []

for words in df["Pos"]:
    list = word_tokenize(words)
    pos.append(nltk.pos_tag(list))

    
df["Pos"] = pos    


# In[8]:


display(df.head())


# In[9]:


from nltk.corpus import wordnet as wn

#convert the tags to wordnet equivalent
def pos_to_wordnet(tag):
    if tag.startswith('N'):
        return wn.NOUN
    elif tag.startswith('J'):
        return wn.ADJ
    elif tag.startswith('V'):
        return wn.VERB
    elif tag.startswith('R'):
        return wn.ADV
    return ''


# In[10]:


from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

def calculate_sentiment(word,tag):
    wordnet_tag = pos_to_wordnet(tag)
    
    if wordnet_tag not in (wn.NOUN, wn.ADJ, wn.ADV):
        return []

    lemma = lemmatizer.lemmatize(word, pos=wordnet_tag)
    if not lemma:
        return []

    synsets = wn.synsets(word, pos=wordnet_tag)
    if not synsets:
        return []

    synset = synsets[0]
    swn_synset = swn.senti_synset(synset.name())

    return [synset.name(), swn_synset.pos_score(),swn_synset.neg_score(),swn_synset.obj_score()]


# In[11]:


senti_score = []

pos=neg=obj=count=0

for pos_val in df["Pos"]:
    senti_val = [calculate_sentiment(x,y) for (x,y) in pos_val]
    for score in senti_val:
        try:
            pos = pos + score[1]  #positive score is stored at 2nd position
            neg = neg + score[2]  #negative score is stored at 3rd position
        except:
            continue
    senti_score.append(pos - neg)
    pos=neg=0    
    
df["Polarity"] = senti_score

display(df.head())


# In[12]:


display(df.tail())


# In[13]:


score=[]

for i in range(len(df)):
    if df["Polarity"][i]>= 0.05:
        score.append('Positive')
    elif df["Polarity"][i]<= -0.05:
        score.append('Negative')
    else:
        score.append('Neutral')
df["Sentiment"] = score


# In[14]:


display(df.head())


# In[15]:


df.to_csv("sentiment.csv")


# In[16]:


count = df['Sentiment'].value_counts()
count


# In[17]:


import matplotlib.pyplot as plt

plt.figure(figsize=(10, 7))
plt.pie(count.values, labels = count.index, explode = (0.05, 0.05, 0.05), autopct='%1.1f%%', shadow=False)


# In[26]:


df['Clean'] = df['Clean'].str.replace("[']", "")


# In[27]:


display(df['Clean'])


# In[29]:


from wordcloud import WordCloud
wc = WordCloud()
img = wc.generate_from_text(' '.join(df.loc[df['Sentiment'] == 'Positive', 'Clean']))

fig=plt.figure(figsize=(15, 8))
plt.imshow(img, interpolation='bilinear')
plt.axis("off")
plt.show()


# In[30]:


wc = WordCloud()
img = wc.generate_from_text(' '.join(df.loc[df['Sentiment'] == 'Negative', 'Clean']))

fig=plt.figure(figsize=(15, 8))
plt.imshow(img, interpolation='bilinear')
plt.axis("off")
plt.show()


# In[ ]:




