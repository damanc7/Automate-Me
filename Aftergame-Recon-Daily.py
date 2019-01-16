import re
import pprint
import pyperclip

# curently text is taken from clipboard but in the future
#   the report should be read from my email the morning after a game
text = pyperclip.paste()

# regex to find time
eventTimeRegex=re.compile(r'\d*\d:\d\d:\d\d')
eventTime = eventTimeRegex.findall(text)
pprint.pprint(eventTime) # printing only to debug
# regex to find title
eventNameRegex = re.compile(r'.*?\d\d:\d\d:\d\d(.*)\.*')
eventName = eventNameRegex.findall(text)
pprint.pprint(eventName) # printing only to debug

# print out schedule only to confirm program is accurate
blazersStart = input('What time(ET) did the Blazers game start? ')
blazersStartindex = eventTime.index(blazersStart)

print('Game Start: ' + eventTime[blazersStartindex])
print('Game End: ' + eventTime[blazersStartindex+2])
print('Blazers Post Game Start: ' + eventTime[blazersStartindex+2])
print('Blazers Post Game End: ' + eventTime[blazersStartindex+4])
print('Blazers Outsiders Start: ' + eventTime[blazersStartindex+4])
print('Blazers Outsiders End: ' + eventTime[blazersStartindex+6])
print('Blazers Raw Start: ' + eventTime[blazersStartindex+6])
print('Blazers Raw End: ' + eventTime[blazersStartindex+8])
print('Filler Start: ' + eventTime[blazersStartindex+8])
print('Filler End and on-time: ' + eventTime[blazersStartindex+12])

# TODO login to enames
# TODO navigate to yesterday's lineup
# TODO edit events or create new event for game, post, outsiders post, raw, and add filler
# TODO submit


# issues so far:
#   recon report is inconsistent - solution: ask operators to use template
#   Games can go long or short above is if the game is short.
