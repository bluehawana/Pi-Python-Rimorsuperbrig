#!/usr/bin/env python
import os
import requests
import json
import smtplib
import time
from time import sleep
import RPi.GPIO as GPIO

time.sleep(10)
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("myemail@gmail.com", "mypassword")

sent_from = 'myemail@gmail.com'
to = ['destinationemail@gmail.com']
subject = 'Don Vito alarm has been triggered'
body = 'Don Vito Alarm has been triggered'

email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)


API_KEY = 'myAPIkey'



def pushMessage(title, body):
    data = {
        'type':'note',
        'title':title,
        'body':body
        }
    resp = requests.post('https://api.pushbullet.com/api/pushes',data=data, auth=(API_KEY,''))



GPIO.setmode(GPIO.BOARD)
GPIO.setup(15, GPIO.IN)

LOOP_TIME_MS = 5000
activeTimeMs = 0
while True:
  time.sleep(LOOP_TIME_MS / 1000.0)
  if GPIO.input(15):
    activeTimeMs = activeTimeMs + LOOP_TIME_MS
    if activeTimeMs == 3000:
      print("Input no longer active")
  else:
    if activeTimeMs >= 5000:
      print("Input has been active for 5 seconds")
    pushMessage("Don Vito Alarm has been Triggered", "Alarm has been triggered")

    server.sendmail(sent_from, to, email_text)



    sleep(10)
    activeTimeMs = 0
