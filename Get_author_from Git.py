from git import Repo
from datetime import datetime
from operator import itemgetter
import time
import os
import urllib.request
import zipfile
import sys
import re
import openpyxl


YEAR = 0
WEEK = 1
DAY = 2
TIME = 3
SHA = 4
DATE = 5
AUTHOR = 6

repo = Repo('D:/sonarqube/projects/trafficserver-qa')
commits = list(repo.iter_commits('master'))

commits_in_week = {}
list_all = []
list_eachday = []
for each in commits:
    each_time = datetime.fromtimestamp(each.committed_date)
    each_date = datetime.date(each_time)
    each_hour = datetime.time(each_time)
    hash = each.hexsha
    author = each.author

    list_each = [each_time.isocalendar()[YEAR], each_time.isocalendar()[WEEK], each_time.isocalendar()[DAY], each_hour,
                 hash, each_date, author]
    list_all.append(list_each)

list_all.sort(key=itemgetter(YEAR, WEEK, DAY, TIME))
len_list_all = len(list_all)

list_eachday.sort(reverse=False)
for each in list_eachday:
    print(each)

print(len(list_all))

wb = openpyxl.load_workbook('D:\PhD Groningen\Publications\TechDebt2020\\trafficserver-qa_author.xlsx')
sheet = wb.get_sheet_by_name('all_author')
row1 = ('Date','Commit','Author',	'Email')
sheet.append(row1)

for each in list_all:
#    print(each)
    commit_hash = str(each[SHA])
    commit_author = str(each[AUTHOR])
    commit_date = str(each[DATE])
    author_all = repr(each[AUTHOR])
    author = str(author_all)
    commit_email = re.split('<|>',author)[-3]
    row = (commit_date, commit_hash, commit_author, commit_email)
    print(row)
    sheet.append(row)

wb.save('D:\PhD Groningen\Publications\TechDebt2020\\trafficserver-qa_author.xlsx')

