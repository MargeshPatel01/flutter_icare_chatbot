#!/usr/bin/env python
# coding: utf-8

# In[1]:


import mysql.connector
import pickle
import json
from flask import jsonify# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

infile=open('modelclfsvm.pkl',"rb")
m=pickle.load(infile)
count_vect = pickle.load(open('count_vect_svm', 'rb'))

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

    data = {"category":cat, "process":"identification", "Question" : "What is your postal code?"}

    return data
    # return myresult[0][0]
    


driver = webdriver.Chrome(executable_path='C:/Users/patel/Documents/chromedriver.exe')
def get_url(postal_code):
    driver.get("https://www.thehealthline.ca/")
    user_input_postal = driver.find_elements_by_xpath('//*[@id="ctl00_ContentPlaceHolder2_txtPostalCodeSearch"]')[0]
    #print(user_input_postal)
    user_input_postal.send_keys(postal_code)
    user_input_postal.send_keys(Keys.ENTER)
    retrieved_url = driver.current_url
    url = {"url" : retrieved_url, "process": "postal_code"}
    return url

msg="I am very happy customer"
url=return_url(msg,'Oshawa')
print(url)


# In[ ]:




