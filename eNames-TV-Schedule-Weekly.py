from selenium import webdriver
from selenium.webdriver import ActionChains
import time
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import csv
import pandas as pd
import xlrd
from selenium.webdriver.support.ui import Select
driver = webdriver.Firefox()

import os
os.chdir(r'C:\Users\206568682\AppData\Local\Programs\Python\Python37-32')

#Dictionary {'compass' : 'enames'}
showNames = {'Rip City Mornings with Dan & Nigel ' : 'RIP CITY MORNINGS',
             'Paid Programming ' : 'PAID PROGRAM',
             'Dew Tour. ' : 'DEW ACTION SPORTS TOUR',
             'Mecum Top 10 ' : 'MECUM TOP 10',
             'The Brian Noe Show' : 'BRIAN NOE SHOW,THE',
             'The Bridge ' : 'THE BRIDGE',
             'Trail Blazers Courtside ' : 'TRAILBLAZERS COURTSIDE',
             "Talkin' Beavers " : 'TALKIN BEAVERS',
             "Talkin' Huskies " : 'TALKIN HUSKIES',
             'UCI Track Cycling World Cup ' : 'UCI TRACK WORLD CYCLING CHAMPIONSHIP',
             'Best of The Brian Noe Show ' : 'BEST OF THE BRIAN NOE SHOW'}

#Login/Pass
with open(r'C:\Users\206568682\PycharmProjects\eNames\python_login_info.csv') as file:
    csv_reader = csv.reader(file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            enamesUsername = row[0]
            enamesPassword = row[1]

# login to eNames website
driver.get(
    'https://answers.nielsen.com/portal/sso_portlet_audit.jsp?portlet=9b217689306c21baf4944b70e75072a0&url=https://media.nielsen.com/lrsenam/enames/html/validatelogin.jsp')  # go to site
elemUser = driver.find_element_by_css_selector('#USER')
elemUser.send_keys(enamesUsername)
elemPass = driver.find_element_by_css_selector('#PASSWORD')
elemPass.send_keys(enamesPassword)
elemPass.submit()

#bypass internet explorer popup alert
time.sleep(5)
Alert = driver.find_element_by_css_selector('#btnAlert')
time.sleep(10) # not sure why it takes so long to register button
Alert.click()
time.sleep(2)


# Go to worksheet's first date (Monday)
selectedDate = driver.find_element_by_css_selector('#selectedDate')
startofWeek = '12/31/2018' # this should be taken from worksheet The first Monday
selectedDate.click()
ActionChains(driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
selectedDate.send_keys(startofWeek)
editLineup = driver.find_element_by_css_selector('.form-elem-title > button:nth-child(11)')
editLineup.click()
time.sleep(2)


# open excel file and add Start Time and Start Date into a column called "Combined Start" and "Combined End"
# import excel file

fileName = 'eNames12.31.xlsx'
df = pd.read_excel(fileName)

#strip out trailing spaces in Program Name
df['Program Name'] = df['Program Name'].str.strip()


# --------------------------------------MONDAY-----------------------------------------------
day = 'Monday'

# search worksheet for Monday program that starts at 3am
firstEventrow = df.loc[(df['Day Of Week'] == day) & (df['Start Time'] == '03:00 AM')]
#if there are no 3am starts, search for program that starts before 3am and ends after 3am
if firstEventrow.empty == True:
    firstEventrow = df.loc[(df['Day Of Week'] == day) & (df['Combined Start'].dt.hour < 3) & (
                df['Combined End'].dt.hour >= 3)]
startTime = '3am'
endTime = firstEventrow['End Time'].item()
# Enter For Loop
for row in df.itertuples():
    # insert event
    insertEvent = driver.find_element_by_css_selector('#insertEvent')
    insertEvent.click()
    #enter start and end time
    eStarttime = driver.find_element_by_xpath('//*[@id="rowStartTime"]')
    startTime = row[2]
    eStarttime.send_keys(startTime)
    eStarttime.send_keys(Keys.TAB)
    eEndtime = driver.find_element_by_xpath('//*[@id="rowEndTime"]')
    endTime = row[3]
    eEndtime.send_keys(endTime)
    eEndtime.send_keys(Keys.TAB)
    #source if program is Pro Football Weekly or The Bridge then change source
    if index[4] == 'Pro Football Weekly ' or 'The Bridge ':
        eSource = Select(driver.find_element_by_css_selector('#rowSource_O_L'))
        eSource.select_by_visible_text('syndicated')
    # Program name should be same as worksheet name except in eNames dictionary
    eProgramname = driver.find_element_by_xpath('//*[@id="ynamelookup"]')
    programName = row[4]
    if programName [-1:] == ' ': # minus the last character if it is a space
    programName = programName[:-1] #program name minus end space
    #use dictionary here
    eProgramname.send_keys(programName)
    eProgramname.send_keys(Keys.ENTER)
# Suffix click on suffix and select 'R' if scheduling type has an 'R' in it
if firstEventrow['Scheduling Type'].item() == 'R':
  eSuffix = driver.find_element_by_css_selector('#rowSuffix')
  eSuffix.click()
  eSuffixr = driver.find_element_by_css_selector('#R')
  eSuffixr.click()
  eSuffixOK = driver.find_element_by_css_selector('#suffixBox > fieldset:nth-child(1) > div:nth-child(4) > input:nth-child(1)')
  eSuffixOK.click()


# if NBA Basketball enter into subtitle menu

import re
if firstProgramname == 'NBA Basketball':
    eSubtitle = driver.find_element_by_css_selector('#rowSubtitle')
    eSubtitle.click()
    # select by visible text
    select = Select(driver.find_element_by_css_selector('#subtitleType_O_L'))
    select.select_by_visible_text('Sports')
    typeSport = driver.find_element_by_css_selector('#ysportstypelookup')
    typeSport.send_keys('Basketball-Professional')
    typeSport.send_keys(Keys.TAB)
    titleName = firstEventrow['Title Name'].item() #everything before the '@' symbol
    m = re.findall(r'(.+(?=@))', text)
    awayTeam = m[0] # has an ending space

    eAwayteam = driver.find_element_by_css_selector('#yteamawaylookup')
    #create a dictionary for all teams
    select.all_selected_options






# accept
acceptButton = driver.find_element_by_xpath('//*[@id="acceptButton"]')
acceptButton.click()


# continue to next program and so on
