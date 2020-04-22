#!/usr/bin/env python
# coding: utf-8

# In[8]:


import mysql.connector
import pickle
import numpy as np


with open('modelclf.pkl',"rb") as saved_processing:
        m,classes = pickle.load(saved_processing)
        saved_processing.close()
count_vect = pickle.load(open('count_vect', 'rb'))

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="21margesh",
  db="ichat"
    
)

mycursor = mydb.cursor()

def get_final_output(pred, classes):
    predictions = pred[0]
    #print(predictions)
    classes = np.array(classes)
    #print(classes)
    ids = np.argsort(-predictions)
    classes = classes[ids]
    print(classes)
    predictions = -np.sort(-predictions)
    print(predictions)
    return classes[0],predictions[0],classes[1],predictions[1]  

def predict(msg):    
    pred=m.predict_proba(count_vect.transform([msg]))
    firstIntent,firstprob,secondIntent,secondprob=get_final_output(pred, classes)   
    return firstIntent,firstprob,secondIntent,secondprob
    #return myresult[0][0]
    

def get_url(msg, region):
    firstcategory,firstprob,secondcategory,secondprob=predict(msg)
    sql = """SELECT url FROM url_mapping WHERE Category = '%s' AND Region = '%s'""" % (firstprob, region)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    url=myresult[0][0]
    url2 = {"url" : url}

    return url2



msg="Find the nearest CCAC? LHIN? OHT?"
# firstcategory,firstprob,secondcategory,secondprob=predict(msg)
# print(firstcategory)
# print(firstprob)
# print(secondcategory)
# print(secondprob)

print(get_url(msg), 'Oshawa')

# #fetching URL
# sql = """SELECT url FROM url_mapping WHERE Category = '%s' AND Region = '%s'""" % (firstcategory, 'Oshawa')
# mycursor.execute(sql)
# myresult = mycursor.fetchall()
# url=myresult[0][0]
# print(url)


# In[ ]:




