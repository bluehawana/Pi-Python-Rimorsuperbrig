import os
import glob
import picamera
import RPi.GPIO as GPIO
import smtplib
from time import sleep
import datetime as dt

# Importing modules for sending mail
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

sender = 'account@gmail.com'
password = 'password'
receiver = 'receiver@gmail.com'

DIR = './Database/'
FILE_PREFIX = 'image'

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)   # Read output from PIR motion sensor
sleep(5)
def send_mail():
    print 'Sending E-Mail'
    # Create the directory if not exists
    if not os.path.exists(DIR):
        os.makedirs(DIR)
    # Find the largest ID of existing images.
    # Start new images after this ID value.
    files = sorted(glob.glob(os.path.join(DIR, FILE_PREFIX + '[0-9][0-9][0-9].jpg')))
    count = 0

    if len(files) > 0:
        # Grab the count from the last filename.
        count = int(files[-1][-7:-4])+1

    # Save image to file
    filename = os.path.join(DIR, FILE_PREFIX + '%03d.jpg' % count)
    # Capture the face
    with picamera.PiCamera() as camera:
        camera.rotation = 180
        #camera.start_preview()
        camera.annotate_background = picamera.Color('black')
        camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sleep(10)
        pic = camera.capture(filename)
        camera.stop_preview()
    # Sending mail
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = 'Movement Detected'

    body = 'Picture is Attached.'
    msg.attach(MIMEText(body, 'plain'))
    attachment = open(filename, 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename= %s' % filename)
    msg.attach(part)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, password)
    text = msg.as_string()
    server.sendmail(sender, receiver, text)
    server.quit()

while True:
    i = GPIO.input(11)
    if i == 0:  # When output from motion sensor is LOW
        print "No intruders", i
        sleep(0.3)
    elif i == 1:  # When output from motion sensor is HIGH
        print "Intruder detected", i
        send_mail()
