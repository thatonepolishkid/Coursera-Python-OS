import re
import operator
import csv
import sys

#establishes an Error dictionary and User statistics dictionary to input and iterate information into
errors_dict = {}
user_statistics = {}

#Declare two files with which to write into, for errors and statistics respectively
error_csv = 'error_message.csv'
user_csv = 'user_statistics.csv'

#declares and opens the log file that we wish to process
logfile = 'syslog.log'
log_report = open(logfile, 'r')

#Regex for finding and placing into groups the Errors/Info and usernames
pattern = r"ticky: ([\w' ]*):? ([\w' ]*) [\[[0-9#]*\]?]? ?\((.*)\)$"

#opens and itterates through the log file, then counts the occurances of each ticket that was produced
for log in log_report:
    result = re.search(pattern, log)
    if result.group(2) not in errors_dict.keys():
        errors_dict[result.group(2)] = 0
    errors_dict[result.group(2)] += 1
    if result.group(3) not in user_statistics.keys():
        user_statistics[result.group(3)] = {}
        user_statistics[result.group(3)]["INFO"] = 0
        user_statistics[result.group(3)]["ERROR"] = 0
        
    if result.group(1) == "INFO":
        user_statistics[result.group(3)] += 1
    elif result.group(1) == "ERROR":
        user_statistics[result.group(3)] += 1

#Sorts the Error dictionary from most to least
errors_dict = sorted(errors_dict.items(), key = operator.itemgetter(1), reverse = True)
#Sorts the User statistics dictionary by name
user_statistics = sorted(user_statistics.items())

log_report.close()

#Establishes the Header for the table in the Errors Dictionary
errors_dict.insert(0, ("Error", "Count"))

#Formats and writes into the csv file to be placed in the html page
error_file = open(error_csv, 'w')
for error in errors_dict:
    a,b = error
    error_file.write(str(a)+','+str(b)+'\n')
error_file.close()

#Formats and writes into the csv file to be placed into the html page
user_file = open(user_csv, 'w')
user_file.write("username, INFO, ERROR\n")
for stat in user_statistics:
    a,b = stat
    user_file.write(str(a) + ',' + str(b["INFO"]) + ',' + str(b["ERROR"])+ '\n')
user_file.close()