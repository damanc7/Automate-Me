from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

dayInput = input('What day do you want to input? ')

driver = webdriver.Firefox()
import time, csv, re
import pandas as pd
fileName = 'enames2.04.xls'
df = pd.read_excel(fileName)
# strip out spaces in Program Name
df['Program Name'] = df['Program Name'].str.strip()

#Dictionaries {'compass' : 'enames'}
shownamesDict = {'Best of Rip City Drive': 'BEST OF RIP CITY DRIVE',
 'Best of Rip City Mornings': 'BEST OF RIP CITY MORNINGS',
 'Best of The Brian Noe Show': 'BEST OF THE BRIAN NOE SHOW',
 'Blazers Outsiders': 'BLAZERS OUTSIDERS',
 'Blazers Outsiders Postgame': 'BLAZERS OUTSIDERS POSTGAME',
 'Blazers Outsiders Pregame': 'BLAZERS OUTSIDERS PREGAME',
 'Blazers Raw': 'BLAZERS RAW',
 'Blazers Warm-Up with Chad Doing': 'BLAZERS WARM-UP WITH CHAD DOING',
 'Outdoor GPS': 'OUTDOOR GPS',
 'Rip City Drive with Travis & Chad': 'RIP CITY DRIVE',
 'Rip City Mornings with Dan & Nigel': 'RIP CITY MORNINGS',
 "Talkin' Beavers": 'TALKIN BEAVERS',
 "Talkin' Ducks": 'TALKIN DUCKS',
 'The Brian Noe Show': 'BRIAN NOE SHOW,THE',
 'The Bridge': 'THE BRIDGE',
 'Trail Blazers Basketball': 'NBA BASKETBALL',
 'Trail Blazers Courtside': 'TRAILBLAZERS COURTSIDE',
 'Trail Blazers Postgame': 'BLAZERS PRE GAME SHOW',
 'Trail Blazers Pregame': 'BLAZERS POST GAME SHOW',
 'Paid Programming': 'PAID PROGRAM'}
teamsDict = {'Atlanta': 'ATLANTA HAWKS',
 'Boston': 'BOSTON CELTICS',
 'Brooklyn': 'BROOKLYN NETS',
 'Charlotte': 'CHARLOTTE HORNETS',
 'Chicago': 'CHICAGO BULLS',
 'Cleveland': 'CLEVELAND CAVALIERS',
 'Dallas': 'DALLAS MAVERICKS',
 'Denver': 'DENVER NUGGETS',
 'Detroit': 'DETROIT PISTONS',
 'Golden State': 'GOLDEN STATE WARRIORS',
 'Houston': 'HOUSTON ROCKETS',
 'Indiana': 'INDIANA PACERS',
 'L.A. Lakers': 'LOS ANGELES LAKERS',
 'LA Clippers': 'LOS ANGELES CLIPPERS',
 'Memphis': 'MEMPHIS GRIZZLIES',
 'Miami': 'MIAMI HEAT',
 'Milwaukee': 'MILWAUKEE BUCKS',
 'Minnesota': 'MINNESOTA TIMBERWOLVES',
 'New Orleans': 'NEW ORLEANS PELICANS',
 'New York': 'NEW YORK KNICKERBOCKERS',
 'Oklahoma City': 'OKLAHOMA CITY THUNDER',
 'Orlando': 'ORLANDO MAGIC',
 'Philadelphia': "PHILADELPHIA 76'ERS",
 'Phoenix': 'PHOENIX SUNS',
 'Sacramento': 'SACRAMENTO KINGS',
 'San Antonio': 'SAN ANTONIO SPURS',
 'Toronto': 'TORONTO RAPTORS',
 'Utah': 'UTAH JAZZ',
 'Washington': 'WASHINGTON WIZARDS',
 'Portland Trail Blazers': 'PORTLAND TRAILBLAZERS'}
daysofWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# LOGIN
driver.get(
    'https://answers.nielsen.com/portal/sso_portlet_audit.jsp?portlet=9b217689306c21baf4944b70e75072a0&url='
    'https://media.nielsen.com/lrsenam/enames/html/validatelogin.jsp')  # go to site
time.sleep(1) # get password
with open(r'C:\Users\206568682\PycharmProjects\eNames\python_login_info.csv') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            enamesUsername = row[0]
            enamesPassword = row[1]
elemUser = driver.find_element_by_css_selector('#USER')
elemUser.send_keys(enamesUsername)
elemPass = driver.find_element_by_css_selector('#PASSWORD')
elemPass.send_keys(enamesPassword)
elemPass.submit()

# BYPASS ALERT
time.sleep(10)
Alert = driver.find_element_by_css_selector('#btnAlert')
time.sleep(10) # not sure why it takes so long to register button
Alert.click()
time.sleep(2)

# GO TO DAY LINEUP
day = dayInput
# find start day based on day of week
for row in df.itertuples():
    if row[1] == day:
        dateofDay = df['Start Date'][row[0]]
dayLineup = dateofDay.strftime("%m/%d/%Y")
if day == 'All': #start at the first date on sheet
    dayLineup = df['Start Date'][1].strftime("%m/%d/%Y")
    day = 'Monday'
selectedDate = driver.find_element_by_css_selector('#selectedDate')
selectedDate.click()
ActionChains(driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
selectedDate.send_keys(dayLineup)
editLineup = driver.find_element_by_css_selector('.form-elem-title > button:nth-child(11)')
editLineup.click()
time.sleep(2)
# --------------------------------------First Day Start For Loop -----------------------------------------------
countofDays = df.groupby('Day Of Week').size() # number of Mondays, Tuesdays, etc
count = 0
threeAMprogram = 0

for row in df.itertuples():
    if row[1] == day:
        # INSERT EVENT
        insertEvent = driver.find_element_by_css_selector('#insertEvent')
        insertEvent.click()
        # START/END TIME
        eStarttime = driver.find_element_by_xpath('//*[@id="rowStartTime"]')
        startTime = row[2][:5] + ':00' + row[2][-3:]
        endTime = row[3][:5] + ':00' + row[3][-3:]
        eStarttime.send_keys(startTime)
        eEndtime = driver.find_element_by_xpath('//*[@id="rowEndTime"]')
        eEndtime.send_keys(endTime)
        # SOURCE
        if row[4] == 'Pro Football Weekly' or row[4] ==  'The Bridge':
            eSource = Select(driver.find_element_by_css_selector('#rowSource_O_L'))
            eSource.select_by_visible_text('Syndicated')
        # PROGRAM NAME
        eProgramname = driver.find_element_by_xpath('//*[@id="ynamelookup"]')
        programName = row[4]
        if programName in shownamesDict: #if in dictionary use it
            eProgramname.send_keys(shownamesDict[programName])
            time.sleep(2)
            eProgramname.send_keys(Keys.ENTER)
        else: # else just put in what the row has for Program Name
            eProgramname.send_keys(programName)
            time.sleep(2)
            eProgramname.send_keys(Keys.ENTER)
        # SUFFIX
        if row[5] == 'R':
            eSuffix = driver.find_element_by_css_selector('#rowSuffix')
            eSuffix.click()
            try: # This checks if the program entered above is new.  If new, there will be an alert
                WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#btnAlert')))
                button = driver.find_element_by_css_selector('#btnAlert')
                button.click()
                time.sleep(1)
                # Cancel suffix window
                driver.find_element_by_css_selector("[value='Cancel']").click()
                #CREATE NEW SHOW
                advancedSearch = driver.find_element_by_css_selector('#advancedSearchButton')
                advancedSearch.click()
                createNameButton = driver.find_element_by_css_selector('#namesOverlay > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > button:nth-child(3)')
                createNameButton.click()
                #enter create new name window
                selectLocal = Select(driver.find_element_by_css_selector('#sourceTypeList_O_L'))
                selectLocal.select_by_visible_text('Local')
                selectProgramType = Select(driver.find_element_by_css_selector('#programTypeList_O_L'))
                selectProgramType.select_by_visible_text('S - SPORTS EVENTS & COMMENTARY')
                createName = driver.find_element_by_css_selector('#programNameToCreate')
                createName.send_keys(programName)
                # short name
                shortName = driver.find_element_by_css_selector('#reportableNameToCreate')
                shortName.send_keys(programName[:13])
                createDuration = driver.find_element_by_css_selector('#durationField')
                createDuration.send_keys(Keys.BACK_SPACE)
                time.sleep(1)
                createDuration.send_keys('60')
                create_program_button = driver.find_element_by_css_selector('#createBtn')
                time.sleep(2)
                create_program_button.click()
                #add suffix for new program
                eSuffix.click()
                eSuffix = driver.find_element_by_css_selector('#rowSuffix')
                eSuffix.click()
                eSuffixr = driver.find_element_by_css_selector('#R')
                eSuffixr.click()
                driver.find_element_by_css_selector("[value='OK']").click()  # click ok in suffix menu
            except TimeoutException: # if no alert aka not a new show, check for R and place
                if row[5] == 'R':
                    eSuffixr = driver.find_element_by_css_selector('#R')
                    eSuffixr.click()
                    driver.find_element_by_css_selector("[value='OK']").click()  # click ok in suffix menu
            # TODO if previous program with same program name also had an 'R' in it, then it should be 'RB' then 'RB2' etc.
        # Back to main window
        #SUBTITLE
        if programName == 'Trail Blazers Basketball':
            eSubtitle = driver.find_element_by_css_selector('#rowSubtitle')
            eSubtitle.click()
            # select by visible text
            select = Select(driver.find_element_by_css_selector('#subtitleType_O_L'))
            select.select_by_visible_text('Sports')
            typeSport = driver.find_element_by_css_selector('#ysportstypelookup')
            typeSport.send_keys('Basketball-Professional')
            time.sleep(1)
            typeSport.send_keys(Keys.TAB)
            titleTeam = row[7] #find way to create regex with 2 groups
            #away team
            awayTeam = re.findall(r'(.*?) @', titleTeam) #everything before the ' @' symbol
            awayTeam = awayTeam[0]
            eAwayteam = driver.find_element_by_css_selector('#yteamawaylookup')
            eAwayteam.send_keys(teamsDict[awayTeam]) #lookup in dictionary
            time.sleep(3)
            eAwayteam.send_keys(Keys.ENTER)
            time.sleep(3)
            #home team
            homeTeam = re.findall(r'@ (.*)', titleTeam)  # everything after the '@ ' symbol
            time.sleep(3)
            homeTeam = homeTeam[0]
            eHometeam = driver.find_element_by_css_selector('#yteamhomelookup')
            eHometeam.send_keys(teamsDict[homeTeam]) #lookup in dictionary
            time.sleep(3)
            eHometeam.send_keys(Keys.ENTER)
            time.sleep(3)
            # TODO subtitleOK changes css selector - find another way to locate
            subtitleOK = driver.find_element_by_css_selector('#sportsSubtitleBox > div:nth-child(6) > input:nth-child(1)')
            subtitleOK.click()
        count += 1
        # CHECK IF PROGRAM SPANS 3AM then break into two programs
        if threeAMprogram == 0:
            if row[2][-2:] == 'AM': # if it is in the morning
                if int(row[2][:2]) < 3:  # if start time hour is less than 3am (2am, 1am, 12am) Doesn't work for 11pm or 10pm
                    if int(row[3][:2]) > 3 or row[3] == '03:30 AM': #and if end time is 3am, 4am, 5am, 6am, etc
                        # put endtime at 3am
                        endTime = '03:00:00 AM'
                        eEndtime = driver.find_element_by_xpath('//*[@id="rowEndTime"]')
                        eEndtime.clear()
                        time.sleep(2)
                        eEndtime.send_keys(endTime)
                        eEndtime.send_keys(Keys.TAB)
                        threeAMprogram += 1 # so I know if it is creating the first or second program
                        time.sleep(2)
        # ACCEPT creation of new event
        acceptButton = driver.find_element_by_xpath('//*[@id="acceptButton"]')
        acceptButton.click()
        # BYPASS ALERT - CONFIRM DELETION OF PRIOR PROGRAMS (if if pops up)
        try:
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btnConf"]')))
            driver.find_element_by_xpath('//*[@id="btnConf"]').click()
        except TimeoutException:
            continue
        if threeAMprogram == 1: # If it is creating the second program spanning 3am
            # check same conditions as above
            if row[2][-2:] == 'AM':
                if int(row[2][:2]) < 3:
                    if int(row[3][:2]) > 3 or row[3] == '03:30 AM':
                        # put start at 3am
                        startTime = '03:00:00 AM'
                        # run entire For Loop again but change starttime to 3am
                        # INSERT EVENT
                        insertEvent = driver.find_element_by_css_selector('#insertEvent')
                        insertEvent.click()
                        # START/END TIME
                        eStarttime = driver.find_element_by_xpath('//*[@id="rowStartTime"]')
                        endTime = row[3][:5] + ':00' + row[3][-3:]
                        eStarttime.send_keys('03:00:00 AM')
                        eEndtime = driver.find_element_by_xpath('//*[@id="rowEndTime"]')
                        eEndtime.send_keys(endTime)
                        # SOURCE
                        if row[4] == 'Pro Football Weekly' or row[4] ==  'The Bridge':
                            eSource = Select(driver.find_element_by_css_selector('#rowSource_O_L'))
                            eSource.select_by_visible_text('syndicated')
                        # PROGRAM NAME
                        eProgramname = driver.find_element_by_xpath('//*[@id="ynamelookup"]')
                        programName = row[4]
                        if programName in shownamesDict: #if in dictionary use it
                            eProgramname.send_keys(shownamesDict[programName])
                            time.sleep(2)
                            eProgramname.send_keys(Keys.ENTER)
                        else: # else just put in what the row has for Program Name # programName in newShowsList: #if already added use it
                            eProgramname.send_keys(programName)
                            time.sleep(2)
                            eProgramname.send_keys(Keys.ENTER)
                        # SUFFIX click on suffix and select 'R' if scheduling type has an 'R' in it
                        # TODO if alert comes up saying no program then create new program
                        if row[5] == 'R':
                            eSuffix = driver.find_element_by_css_selector('#rowSuffix')
                            eSuffix.click()
                            try:
                                WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#btnAlert')))
                                button = driver.find_element_by_css_selector('#btnAlert')
                                print("alert accepted start to create a new program")
                                button.click()
                                time.sleep(1)
                                #Get out of Suffix workspace
                                driver.find_element_by_css_selector("[value='Cancel']").click()
                                #CREATE NEW SHOW
                                #click 'Advanced Search' button
                                advancedSearch = driver.find_element_by_css_selector('#advancedSearchButton')
                                advancedSearch.click()
                                #click on 'Create Name' button
                                createNameButton = driver.find_element_by_css_selector('#namesOverlay > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > button:nth-child(3)')
                                createNameButton.click()
                                #enter create new name window
                                selectLocal = Select(driver.find_element_by_css_selector('#sourceTypeList_O_L'))
                                selectLocal.select_by_visible_text('Local')
                                selectProgramType = Select(driver.find_element_by_css_selector('#programTypeList_O_L'))
                                selectProgramType.select_by_visible_text('S - SPORTS EVENTS & COMMENTARY')
                                createName = driver.find_element_by_css_selector('#programNameToCreate')
                                createName.send_keys(programName)
                                # short name
                                shortName = driver.find_element_by_css_selector('#reportableNameToCreate')
                                shortName.send_keys(programName[:13])
                                createDuration = driver.find_element_by_css_selector('#durationField')
                                createDuration.send_keys(Keys.BACK_SPACE)
                                time.sleep(1)
                                createDuration.send_keys('60')
                                create_program_button = driver.find_element_by_css_selector('#createBtn')
                                time.sleep(2)
                                create_program_button.click()  # new program name created
                                newShowsList.append(programName)  # add program name to list
                                eSuffix.click()
                                eSuffix = driver.find_element_by_css_selector('#rowSuffix')
                                eSuffix.click()
                                eSuffixr = driver.find_element_by_css_selector('#R')
                                eSuffixr.click()
                                driver.find_element_by_css_selector("[value='OK']").click()  # click ok in suffix menu
                            except TimeoutException:
                                if row[5] == 'R':
                                    eSuffixr = driver.find_element_by_css_selector('#R')
                                    eSuffixr.click()
                                    driver.find_element_by_css_selector("[value='OK']").click()  # click ok in suffix menu
                            # TODO if previous program with same program name also had an 'R' in it, then it should be 'RB' then 'RB2' etc.
                            #If error says "Please pick a program name before applying suffixes" then create new show
                        # Back to main create event window
                        #SUBTITLE
                        if programName == 'Trail Blazers Basketball':
                            eSubtitle = driver.find_element_by_css_selector('#rowSubtitle')
                            eSubtitle.click()
                            # select by visible text
                            select = Select(driver.find_element_by_css_selector('#subtitleType_O_L'))
                            select.select_by_visible_text('Sports')
                            typeSport = driver.find_element_by_css_selector('#ysportstypelookup')
                            typeSport.send_keys('Basketball-Professional')
                            time.sleep(1)
                            typeSport.send_keys(Keys.TAB)
                            titleTeam = row[7] #find way to create regex with 2 groups
                            #away team
                            awayTeam = re.findall(r'(.*?) @', titleTeam) #everything before the ' @' symbol
                            awayTeam = awayTeam[0]
                            eAwayteam = driver.find_element_by_css_selector('#yteamawaylookup')
                            eAwayteam.send_keys(teamsDict[awayTeam]) #lookup in dictionary
                            time.sleep(1)
                            eAwayteam.send_keys(Keys.TAB)
                            #home team
                            homeTeam = re.findall(r'@ (.*)', titleTeam)  # everything after the '@ ' symbol
                            homeTeam = homeTeam[0]
                            eHometeam = driver.find_element_by_css_selector('#yteamhomelookup')
                            eHometeam.send_keys(teamsDict[homeTeam]) #lookup in dictionary
                            time.sleep(1)
                            eHometeam.send_keys(Keys.TAB)
                            # TODO subtitleOK changes css selector - find another way to locate
                            subtitleOK = driver.find_element_by_css_selector('#sportsSubtitleBox > div:nth-child(6) > input:nth-child(1)')
                            subtitleOK.click()
                        threeAMprogram -= 1
                        # ACCEPT creation of new event
                        acceptButton = driver.find_element_by_xpath('//*[@id="acceptButton"]')
                        acceptButton.click()
                        # CONFIRM DELETION OF PRIOR PROGRAMS (if if pops up)
                        try:
                            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btnConf"]')))
                            driver.find_element_by_xpath('//*[@id="btnConf"]').click()
                        except TimeoutException:
                            continue
        if count == int(countofDays[day]):  # if it has done all loops of current day
            day = daysofWeek[daysofWeek.index(day) + 1]  # change day to next day and continue loop
            nextDayInput = input('Would you like to submit and do the next day? ')
            if nextDayInput == 'Yes':
                submitLineup = driver.find_element_by_css_selector('#submitLineupDetails')
                submitLineup.click()
                #reset count to keep track of days
                count = 0
                time.sleep(7)
                #accept alert: Submit Successful
                submitOK = driver.find_element_by_css_selector('#btnAlert')
                submitOK.click()
                time.sleep(2)
                #Navigate to next date
                for row in df.itertuples():
                    if row[1] == day:
                        dateofDay = df['Start Date'][row[0]]
                dayLineup = dateofDay.strftime("%m/%d/%Y")
                selectedDate = driver.find_element_by_css_selector('#selectedDate')
                selectedDate.click()
                time.sleep(1)
                ActionChains(driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
                selectedDate.send_keys(dayLineup)
                time.sleep(1)
                editLineup = driver.find_element_by_css_selector('#editLineupDetails')
                editLineup.click()
                time.sleep(2)
            else: break

# --------------------------------------Second Day Start For Loop -----------------------------------------------
# submitLineup = driver.find_element_by_css_selector('#submitLineupDetails')
# nextDayInput = input('Would you like to submit and do the next day? ')
# if nextDayInput == 'Yes':
#     submitLineup.click()
#     # change day to next day
#     day = daysofWeek[daysofWeek.index(day)+1]
#     # run above loop with new day

# if dayInput == 'All' then loop through Monday - Sunday
    #otherwise ask if I want to submit the day and do the next day
    #if it has just filled in Sunday then don't ask and end program


print('IT WORKED')