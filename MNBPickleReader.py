#!/usr/bin/env python
# coding: utf-8

# In[8]:


import pickle
import numpy as np


with open('modelclf.pkl',"rb") as saved_processing:
        m,classes = pickle.load(saved_processing)
        saved_processing.close()
count_vect = pickle.load(open('count_vect', 'rb'))

# mydb = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   password="21margesh",
#   db="ichat"
    
# )

# mycursor = mydb.cursor()

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

def predict(msg, Region):    
    print(msg)
    pred=m.predict_proba(count_vect.transform([msg]))
    firstIntent,firstprob,secondIntent,secondprob=get_final_output(pred, classes)   
    # sql = """SELECT url FROM url_mapping WHERE Category = '%s' AND Region = '%s'""" % (firstprob, 'Oshawa')
    # mycursor.execute(sql)
    # myresult = mycursor.fetchall()
    # url=myresult[0][0]
    response = ""
    valid = False



    if firstprob > 0.5:
        process = "postal_code"
        valid = True
        print("In if")
        response = "To get relative suggestions please enter your postal code:"
    else :
        process = "identification"
        valid = False
        print("In else")
        response =  "Can you please elaborate your question? The bot is unable to understand."
        pass
    

    urltwo = {"message" : response, "process" : process,"processValid" : valid, "probability" : firstprob}

    return urltwo
    # return firstIntent,firstprob,secondIntent,secondprob
    #return myresult[0][0]
    

def get_url(firstcategory, Region):
    sql = """SELECT url FROM url_mapping WHERE Category = '%s' AND Region = '%s'""" % (firstcategory, Region)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    url=myresult[0][0]
    

    return url
# firstcategory,firstprob,secondcategory,secondprob=predict(msg)
# print(firstcategory)
# print(firstprob)
# print(secondcategory)
# print(secondprob)
# print(msg)
# output = predict(msg)

# print(output)
# print(predict(msg))

# #fetching URL
# sql = """SELECT url FROM url_mapping WHERE Category = '%s' AND Region = '%s'""" % (firstcategory, 'Oshawa')
# mycursor.execute(sql)
# myresult = mycursor.fetchall()
# url=myresult[0][0]
# print(url)


# In[ ]:




