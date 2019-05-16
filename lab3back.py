#importing modules
import urllib.request as ur
import requests
from bs4 import BeautifulSoup 
import re
import time
import collections
import json
import sqlite3

#page = requests.get("https://www.bls.gov/ooh/computer-and-information-technology/home.htm")
#soup = BeautifulSoup(page.content, "lxml")
#lstOfLinks = [link["href"] for link in soup.select("h4 a")]
#titleContentdd = {}

#for link in lstOfLinks:
    #page = requests.get("https://www.bls.gov" + link)
    #soup = BeautifulSoup(page.content, "lxml")
    #titleLst = soup.select("tbody tr th a")
    #contentLst = soup.find_all("td")    
    #titleContentdd[soup.find_all("h1")[0].text.strip()] = {titleLst[i].text.strip() :
                                                           #contentLst[i].text.strip().split("  ")[0].split("%")[0].strip("$").replace(",", "") 
                                                           #for i in range(7)}
#for v in titleContentdd.values():
    #for i, j in v.items():
        #if j.isdigit():
            #v[i] = int(j)
#with open('dataLab3.json', 'w', True) as fh:
    #json.dump(titleContentdd, fh, indent=3)

conn = sqlite3.connect("Lab3.db")
cur = conn.cursor()

with open('dataLab3.json', 'r') as fh:
    data = json.load(fh)
print(data)

cur.execute("DROP TABLE IF EXISTS FIELDNAMES")      
cur.execute('''CREATE TABLE FIELDNAMES(
               N1 TEXT,
               N2 TEXT,
               N3 TEXT,
               N4 TEXT,
               N5 TEXT,
               N6 TEXT,
               N7 TEXT)''')
cur.execute('''INSERT INTO FIELDNAMES 
            VALUES (?, ?, ?, ?, ?, ?, ?)''', 
            tuple(data["Computer and Information Research Scientists"].keys()))
cur.execute("DROP TABLE IF EXISTS DATA")      
cur.execute("""
            CREATE TABLE DATA(
            Name TEXT UNIQUE ON CONFLICT IGNORE,
            MedianPay INTEGER,
            EntryLevel TEXT,
            WorkExperience TEXT,
            Training TEXT,
            Jobs INTEGER,
            Outlook INTEGER,
            Change INTEGER )""")
cur.execute("DROP TABLE IF EXISTS EDUCATION")
cur.execute("""
            CREATE TABLE EDUCATION(
            EDUCATION TEXT UNIQUE ON CONFLICT IGNORE)""")
for k, v in data.items():
    cur.execute('''INSERT INTO DATA (Name, MedianPay, EntryLevel, WorkExperience, Training, Jobs, Outlook, Change)
                 VALUES(?, ?, ?, ?, ?, ?, ?, ?)''', (k, ) + tuple(v.values()))   
    for key, value in v.items():
        if key == "Typical Entry-Level Education" and value != "None":
            cur.execute("INSERT INTO EDUCATION (EDUCATION) VALUES (?)", (value, ))
       
conn.commit()
conn.close()

