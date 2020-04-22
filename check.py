#!/usr/bin/env python
# coding: utf-8

import mysql.connector
import pickle
import sklearn
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
count_vect = CountVectorizer()
infile=open('modelclf.pkl',"rb")
m=pickle.load(infile)

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
    pred=m.predict(count_vect.transform([msg]))
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