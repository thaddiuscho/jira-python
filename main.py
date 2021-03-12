# library modules
from jira import JIRA
import re
import pandas as pd
import os
import csv

user = 'mcho@assurance.com'
apikey = 'UXEJt33uqlgiu6arvFV9200A'
server = 'http://assuranceiq.atlassian.net/'

options = {
 'server': server
}

jira = JIRA(options, basic_auth=(user,apikey) )




#Testing issues
issue = jira.issue("SUP-11124")
transitions = jira.transitions(issue)

jira.transition_issue(issue, 901)


for items in transitions:
   print(items)
    


#Declare Regex compiler
emailRegex = re.compile(r'''(
    [a-zA-Z0-9._%+-]+
    @
    [a-zA-Z0-9.-]+
    (\.[a-zA-Z]{2,4})
    )''', re.VERBOSE)




#pulls 50 of the latest issues the issue #'s from that filter
def pull_aws_keys(filter_id):
    temp_arr = []
    for i in jira.search_issues('filter='+filter_id):
        #print(i.key)
        temp_arr.append(i.key)
    return temp_arr
                                

def pull_status_str(arr):
    temp_arr = []
    for i in arr:
        raw_desc = jira.issue(i).raw["fields"]["description"]
        temp_arr.append(raw_desc)
        #print(raw_desc)
    return temp_arr

#Takes an iterable
def find_email_regex(in_series):
    matches = []
    for items in in_series:
        for groups in emailRegex.findall(items):
            matches.append(groups[0])
    return matches

#tokenize ret_issue by \r\n
def ret_issue_descriptions(issues):
    temp_arr = []
    for items in issues:
        ret_arr = items.split("\r\n")
        ret_arr[4]
        temp_arr.append(ret_arr[4])
    return temp_arr



pulled_issue = pull_aws_keys("10364") #returns the keys
ret_issue = pull_status_str(pulled_issue)
jira_description = ret_issue_descriptions(ret_issue)
find_email_regex(jira_description)
#Create DF
init_df = pd.DataFrame()
init_df["Jira Key"] = pulled_issue
init_df["Description"] = jira_description
init_df["Email"] = find_email_regex(jira_description) #redundant, create csv method already implements this.