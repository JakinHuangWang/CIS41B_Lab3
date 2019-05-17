"""LAB 3 Back
Author: Jakin Wang
OS: Mac OSX
IDE: Wings IDE
Date: 05/17/2019
Description: This file scrapes the web, creates a json file, and uses the json file to construct a database
"""
import urllib.request as ur
import requests
from bs4 import BeautifulSoup 
import re
import time
import collections
import json
import sqlite3

#For checking if a string is a valid number, including the negative sign
def is_number(n):
    try:
        int(n)
    except ValueError:
        return False
    return True

#This portion is to create a json file by scraping the web
'''
page = requests.get("https://www.bls.gov/ooh/computer-and-information-technology/home.htm")
soup = BeautifulSoup(page.content, "lxml")
lstOfLinks = [link["href"] for link in soup.select("h4 a")]
titleContentdd = {}

for link in lstOfLinks:
    page = requests.get("https://www.bls.gov" + link)
    soup = BeautifulSoup(page.content, "lxml")
    titleLst = soup.select("tbody tr th a")
    contentLst = soup.find_all("td")    
    titleContentdd[soup.find_all("h1")[0].text.strip()] = {titleLst[i].text.strip() : contentLst[i].text.strip().split("  ")[0].split("%")[0].strip("$").replace(",", "")
                                                           for i in range(7)}
for v in titleContentdd.values():
    for i, j in v.items():
        if is_number(j):v[i] = int(j)
        if j == 'See How to Become One':v[i] = 'Certificate'
        
with open('dataLab3.json', 'w', True) as fh:
    json.dump(titleContentdd, fh, indent=3)
'''

#This portion is to create a database based on the json file we have created
with open('dataLab3.json', 'r') as fh:
    datadd = json.load(fh)
    
conn = sqlite3.connect("Lab3.db")
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS FIELDNAMES")      
cur.execute('''CREATE TABLE FIELDNAMES(
               ID INTEGER NOT NULL PRIMARY KEY UNIQUE,
               C1 TEXT,
               C2 TEXT,
               C3 TEXT,
               C4 TEXT,
               C5 TEXT,
               C6 TEXT,
               C7 TEXT)''')
cur.execute('''INSERT INTO FIELDNAMES (C1, C2, C3, C4, C5, C6, C7)
               VALUES (?, ?, ?, ?, ?, ?, ?)''', tuple(datadd["Computer and Information Research Scientists"].keys()))
cur.execute("DROP TABLE IF EXISTS DATA")      
cur.execute('''
            CREATE TABLE DATA(
            ID INTEGER NOT NULL PRIMARY KEY UNIQUE, 
            Name TEXT UNIQUE ON CONFLICT IGNORE,
            MedianPay INTEGER,
            EntryLevel INT,
            WorkExperience TEXT,
            Training TEXT,
            Jobs INTEGER,
            Outlook INTEGER,
            Change INTEGER )''')
cur.execute("DROP TABLE IF EXISTS EDUCATION")
cur.execute('''
            CREATE TABLE EDUCATION(
            ID INTEGER NOT NULL PRIMARY KEY UNIQUE,
            NAME TEXT UNIQUE ON CONFLICT IGNORE)''')

for name, d in datadd.items():
    v = tuple(d.values())
    cur.execute("INSERT INTO EDUCATION (NAME) VALUES(?)", (v[1], ))
    cur.execute("SELECT ID FROM EDUCATION WHERE NAME = ?", (v[1], ))
    degree_id = cur.fetchone()[0]
    
    cur.execute('''INSERT INTO DATA
                   (Name, MedianPay, EntryLevel, WorkExperience, Training, Jobs, Outlook, Change)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (name, v[0], degree_id, v[2], v[3], v[4], v[5], v[6]))
conn.commit()
conn.close()
