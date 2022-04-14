from re import I
from bs4 import BeautifulSoup
import requests
import sqlite3
import json
import os

def setUpDatabase(db_name):

    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn
def bs2():
    resp=requests.get('https://firstsportz.com/top-100-highest-paid-athletes-conor-mcgregor/')
    soup = BeautifulSoup(resp.content, 'html.parser')
    players = soup.find_all('tr' )
    lst_of_tup=[]
    for player in players[1:]:
        player.find_all('td')
        lst=[]
        for item in player:
            lst.append(item.text)
        # print(lst)
        rank = lst[0]
        name = lst[1]
        team = lst[2]
        earnings=lst[5]
        # print((rank,name))
        lst_of_tup.append((rank,name, team, earnings))
    # print(lst_of_tup)     
    return lst_of_tup       
   
    

def table(cur, conn, lst_of_tup):
    """
    creates the database for the menu and puts the foods into it. 
    """
    cur.execute("CREATE TABLE IF NOT EXISTS Earnings (id INTEGER UNIQUE PRIMARY KEY, name TEXT UNIQUE, team TEXT, earnings TEXT)")
    count = 0
#     #need to limit this to 25 per time
    for lst in lst_of_tup:

        cur.execute("INSERT OR IGNORE INTO Earnings (id, name, team, earnings) VALUES (?, ?, ?, ?)", (lst[0],lst[1],lst[2],lst[3]))
    conn.commit()
def main():
#     # SETUP DATABASE AND TABLE
    cur, conn = setUpDatabase('DATABASE.db')
    table(cur,conn,bs2())
    # database(cur, conn, bs2(),ranks(), names(), teams(),earnings(()))
#     #api("https://v6.exchangerate-api.com/v6/44aa98a04162992c430b491c/latest/USD?")
#    #api(cur, conn, "https://api.nal.usda.gov/fdc/v1/foods/search?api_key=zUkvK46coqpfOMJbl3SfFLBUAfS4Fhnt8SOKgu5X&query=")
#     #api2(cur , conn)
if __name__ == "__main__":
    main()