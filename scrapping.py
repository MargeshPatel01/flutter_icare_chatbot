#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 14:21:59 2020

@author: dilsher
"""


from selenium import webdriver 
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome(executable_path='./chromedriver.exe')
    

def get_url(postal_code):

    driver.get("https://www.thehealthline.ca/")
    
    user_input_postal = driver.find_elements_by_xpath('//*[@id="ctl00_ContentPlaceHolder2_txtPostalCodeSearch"]')[0]
    #print(user_input_postal)
    user_input_postal.send_keys(postal_code)
    
    user_input_postal.send_keys(Keys.ENTER)
    
    
    err_msg_path=driver.find_elements_by_xpath('//*[@id="ctl00_ContentPlaceHolder2_lblComingSoon"]')
    #print(err_msg)    
    
    if(len(err_msg_path)>0):
        err_msg = err_msg_path[0].text 
        # return (driver.current_url, False, err_msg)
        return {"url" : driver.current_url, "status" : False , "response" : err_msg}
    
    else:
        url = driver.current_url
        area = driver.find_elements_by_xpath('//*[@id="ctl00_ctlRegionTabNav_rptNavBar_ctl00_lnkRegion"]')[0].text
        return {"url" : url, "status" : True , "response" : area}
