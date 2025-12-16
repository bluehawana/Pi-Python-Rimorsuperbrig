#! /usr/bin/python

import os
from gps import *
from time import *
import time
import threading
import mysql.connector
from mysql.connector import Error
from datetime import datetime
from mysql.connector import errorcode



time.sleep(10)

connection = mysql.connector.connect(host='mysqlserver.com',
                                 database='dbname',
                                 user='username',
                                 password='password!')


gpsd = None

os.system('clear')
os.system('sudo systemctl stop serial-getty@ttyAMA0.service')
print("Stopping tty")
os.system('sudo systemctl disable serial-getty@ttyAMA0.service')
print("Disabling tty")
os.system('sudo gpsd /dev/ttyAMA0 -F /var/run/gpsd.sock')
print("Starting gpsd daemon")



class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd
    gpsd = gps(mode=WATCH_ENABLE)
    self.current_value = None
    self.running = True

  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next()
if __name__ == '__main__':
  gpsp = GpsPoller()
  try:
    gpsp.start()
    print("Starting GPS poller")
    while True:


      while gpsd.fix.longitude > 0 and gpsd.fix.longitude != 'nan':

          os.system('clear')
          dateTimeObj = datetime.now()
          print
          print 'latitude    ' , gpsd.fix.latitude
          print 'longitude   ' , gpsd.fix.longitude

          cursor = connection.cursor()

          cursor.execute("""INSERT INTO location (id,time,longitude,latitude) VALUES (%s,%s,%s,%s) """,(" ",dateTimeObj,gpsd.fix.longitude,gpsd.fix.latitude))
          connection.commit()
          print("Record inserted successfully into location table")
          cursor.close()
          time.sleep(10)
      else:
          print("No GPS Fix")
  except mysql.connector.ProgrammingError as err:
      if err.errno == errorcode.ER_SYNTAX_ERROR:
        print("Check your syntax!")
        time.sleep(5)
        os.execv('/home/pi/gps/gpsdb.py',  [''])

      else:
        print("Error: {}".format(err))
        time.sleep(5)
        os.execv('/home/pi/gps/gpsdb.py',  [''])

  except mysql.connector.OperationalError as e:
      time.sleep(5)
      os.execv('/home/pi/gps/gpsdb.py',  [''])

  except mysql.connector.InterfaceError as e:
      time.sleep(5)
      os.execv('/home/pi/gps/gpsdb.py',  [''])

  except (KeyboardInterrupt, SystemExit):
      print "\nKilling Thread..."
      gpsp.running = False
      gpsp.join()
      print "Done.\nExiting."
