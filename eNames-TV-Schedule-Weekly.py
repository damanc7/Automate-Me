from selenium import webdriver
from selenium.webdriver import ActionChains
import time
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import csv
driver = webdriver.Firefox()

import os
os.chdir(r'C:\Users\206568682\AppData\Local\Programs\Python\Python37-32')

#Login/Pass
with open(r'C:\Users\206568682\Documents\python_login_info.csv') as file:
    csv_reader = csv.reader(file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            user = row[0]
            password = row[1]

# login to eNames website
driver.get(
    'https://answers.nielsen.com/portal/sso_portlet_audit.jsp?portlet=9b217689306c21baf4944b70e75072a0&url=https://media.nielsen.com/lrsenam/enames/html/validatelogin.jsp')  # go to site
elemUser = driver.find_element_by_css_selector('#USER')
elemUser.send_keys(user)
elemPass = driver.find_element_by_css_selector('#PASSWORD')
elemPass.send_keys(password)
elemPass.submit()

# bypass internet explorer popup alert
time.sleep(5)
okButton = driver.find_element_by_css_selector('#btnAlert')
time.sleep(10) # not sure why it takes so long to register button
okButton.click()

time.sleep(2)

# MONDAY
# Go to worksheet's first date (Monday)
selectedDate = driver.find_element_by_css_selector('#selectedDate')
startofWeek = '12/31/2018' # this should be taken from worksheet
selectedDate.click()
ActionChains(driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
selectedDate.send_keys(startofWeek)
editLineup = driver.find_element_by_css_selector('.form-elem-title > button:nth-child(11)')
editLineup.click()
time.sleep(2)

# search worksheet for Monday program that starts at 3am
# 	or program that starts before 3am and ends after 3am
workday = 'Monday'

with open(r'C:\Users\206568682\Documents\eNames12.31.csv') as file:
    csv_reader = csv.reader(file, delimiter=',')
    count = 0
    for row in csv_reader:
        if count == 0:
            count += 1
            continue
        day = row[0]
        startTime = row[1]
        endTime = row[2]
        programName = row[3]
        suffix = row[4]
        date = row[5]
        combined = date + ' ' + startTime
        dt_object = datetime.strptime(combined)
        print(dt_object)
        if all(day == workday, startTime == '03:00 AM'):
            firstEvent = programName
            firstEventendtime = endTime
        count += 1
      #  elif all(day == workday, startTime < 3am, endTime > 3am:
         #   firstEvent = programName


# enter first event for Monday
insertEvent = driver.find_element_by_css_selector('#insertEvent')
insertEvent.click()
eStarttime = driver.find_element_by_xpath('//*[@id="rowStartTime"]')
eStarttime.send_keys('3am')
eEndtime = driver.find_element_by_xpath('//*[@id="rowEndTime"]')
# firstEventendtime = one column over from startTime
eEndtime.send_keys(firstEventendtime)

# Source should stay on 'local' for all shows except: "Pro Football Weekly" and "The Bridge"

# Program name should be same as worksheet name except in eNames dictionary
eProgramname = driver.find_element_by_xpath('//*[@id="ynamelookup"]')
eProgramname.send_keys(firstEventname)  # minus the last character if it is a space

# Suffix click on suffix and select 'R' if scheduling type has an 'R' in it

# accept
acceptButton = driver.find_element_by_xpath('//*[@id="acceptButton"]')
acceptButton.click()

# set suffix according to excel (R) or (none)
# enter suffix window
# navigate to "R"checkbox and click
# click "ok"
# click "Accept"
# continue to next program and so on
# if programName = 'Trail Blazers Basketball' then it needs to enter subtitle as "basketball-professional"
#   and needs to enter away team and home team
