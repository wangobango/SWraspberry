import serial
import time
import sqlite3
import signal
import sys

dane = serial.Serial('/dev/ttyUSB0', 9600)
db = sqlite3.connect('/home/pi/testDB.db')
cursor = db.cursor()

cursor.execute('''
SELECT MAX(id) FROM pomiary;
''')

pom = cursor.fetchone()

id = int(pom[0]) + 1

while 1:
   try:
      dane.write('S')
      if(dane.inWaiting()>0):
         myData = dane.readline()
         cursor.execute('''
            INSERT INTO pomiary (id,value)
            VALUES (?,?);
         ''', (id,int(myData)))
         id+=1
         db.commit()
         cursor.execute('''
         SELECT * FROM pomiary ORDER BY id DESC LIMIT 1;
         ''')
         print(cursor.fetchone())
   except KeyboardInterrupt:
      db.close()
      sys.exit()

