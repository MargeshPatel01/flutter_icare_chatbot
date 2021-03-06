#!/usr/bin/env python
# coding: utf-8

# In[16]:


import pandas as pd
import pickle
df1 = pd.read_csv('module2data.csv')
df1.head()


# In[17]:


from io import StringIO
col = ['Target', 'Reviews']
df1 = df1[col]
df1 = df1[pd.notnull(df1['Reviews'])]
df1.columns = ['Target', 'Reviews']
df1['category_id'] = df1['Target'].factorize()[0]
category_id_df = df1[['Target', 'category_id']].drop_duplicates().sort_values('category_id')
category_to_id = dict(category_id_df.values)
id_to_category = dict(category_id_df[['category_id', 'Target']].values)
#df.head(100)
df1.info


# In[18]:


import matplotlib.pyplot as plt
fig = plt.figure(figsize=(8,6))
df1.groupby('Target').Reviews.count().plot.bar(ylim=0)
plt.show()


# In[19]:


from sklearn.feature_extraction.text import TfidfVectorizer
tfidf1 = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2', encoding='latin-1', ngram_range=(1, 2), stop_words='english')
#tfidf = TfidfVectorizer(sublinear_tf=True, stop_words='english')
features1 = tfidf1.fit_transform(df1.Reviews).toarray()
labels = df1.category_id
features1.shape


# In[20]:


from sklearn.feature_selection import chi2
import numpy as np
N = 2
for Target, category_id in sorted(category_to_id.items()):
    features_chi2 = chi2(features1, labels == category_id)
    indices = np.argsort(features_chi2[0])
    feature_names = np.array(tfidf1.get_feature_names())[indices]
    unigrams = [v for v in feature_names if len(v.split(' ')) == 1]
    bigrams = [v for v in feature_names if len(v.split(' ')) == 2]
    print("# '{}':".format(Target))
    print("  . Most correlated unigrams:\n. {}".format('\n. '.join(unigrams[-N:])))
    print("  . Most correlated bigrams:\n. {}".format('\n. '.join(bigrams[-N:])))


# ### Naive Bayes Classifier ###
# 
# 

# In[21]:


from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
X_train, X_test, y_train, y_test = train_test_split(df1['Reviews'], df1['Target'], random_state = 0)
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(X_train)
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
clf = MultinomialNB().fit(X_train_tfidf, y_train)


# In[22]:


# Saving model to disk
# pickle.dump(clf, open('modelclf.pkl','wb'))


# In[28]:


#Testing Prediction

# print(clf.predict(count_vect.transform(["I am very happy customer "])))


# In[29]:


import mysql.connector

# infile=open('modelclf.pkl',"rb")
# m=pickle.load(infile)

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="21margesh",
  db="ichat"
    
)

mycursor = mydb.cursor()

def return_url(msg,region):    
    pred=clf.predict(count_vect.transform([msg]))
    if(pred[0]=='Negative'):
        cat='Suicide'
    elif(pred[0]=='Positive'):
        cat='Depression'
    elif(pred[0]=='Neutral'):
        cat='Dementia'
        
    sql = """SELECT url FROM url_mapping WHERE Category = '%s' AND Region = '%s'""" % (cat, region)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()    
    return myresult[0][0]
    

msg="I am very happy customer"
url=return_url(msg,'Oshawa')
print(url)







