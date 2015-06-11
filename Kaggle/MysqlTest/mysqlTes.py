'''
Created on 2015/06/03

@author: Daytona
'''


import mysql.connector
from mysql.connector import cursor
import pandas as pd

print ("hello")

cnx = mysql.connector.connect(user='PengJiang', password='jiangpengjun',
                              host='149.171.37.73',
                              database='sydneyexchange')

cursor = cnx.cursor()
query = ("SELECT Country, Local_Code, Name_English, Date, Open, High from aac_historicalquotes_sydney")

cursor.execute(query)


for (Country, Local_Code, Name_English, Date, Open, High) in cursor:
    print("{}, {}, {}, {}, {}, {}".format(Country, Local_Code, Name_English, Date, Open, High))

cursor.close()
cnx.close()

print ("finish")
