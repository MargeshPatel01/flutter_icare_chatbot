#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 14:21:59 2020

@author: dilsher
"""

from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google_chrome'
CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'
chrome_options = webdriver.ChromeOptions()
options_headless = Options()
options_headless.add_argument('--disable-gpu')
options_headless.add_argument('--headless')
  # Last I checked this was necessary.
# chrome_options.add_argument('--no-sandbox')
browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, option_headless=chrome_options)    

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
