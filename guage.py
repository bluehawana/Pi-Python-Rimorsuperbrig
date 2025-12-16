import time
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from PIL import Image, ImageDraw, ImageFont
from guizero import App
import os
import PIL
import requests

time.sleep(5)
# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1015(i2c)

chan = AnalogIn(ads, ADS.P3)

while True:
    print("ADC Data: ","{:>5}\t{:>5.3f}".format(chan.value, chan.voltage),"volts")
    voltage=float(chan.voltage)-1.122 #empty tank voltage
    percent=voltage/1.842*100 #full tank minus empty tank voltage
    percentage=voltage/1.842*100
    print("Fuel Percentage Remaining: ","{0:.3f}".format(percent),"%")
    output_file_name = '/home/pi/fuel/new_gauge.png'

    # X and Y coordinates of the center bottom of the needle starting from the top left corner
    #   of the image
    x = 412.5
    y = 412.5
    loc = (x, y)

    percent = percent / 100
    rotation = 180 * percent  # 180 degrees because the gauge is half a circle
    rotation = 90 - rotation  # Factor in the needle graphic pointing to 50 (90 degrees)

    dial = Image.open('/home/pi/fuel/needle.png')
    dial = dial.rotate(rotation, resample=PIL.Image.BICUBIC, center=loc)  # Rotate needle

    gauge = Image.open('/home/pi/fuel/gauge.png')
    gauge.paste(dial, mask=dial)  # Paste needle onto gauge
    gauge.save(output_file_name)



    # get an image
    base = Image.open('/home/pi/fuel/new_gauge.png').convert('RGBA')
    # make a blank image for the text, initialized to transparent text color
    txt = Image.new('RGBA', base.size, (255,255,255,0))
    # get a font
    fnt = ImageFont.truetype('/usr/share/fonts/truetype/lato/Lato-Medium.ttf', 40)
    # get a drawing context
    d = ImageDraw.Draw(txt)

    # draw text, full opacity
    d.text((210,10), "{0:.3f}".format(percentage), font=fnt, fill=(0,0,0,255))
    d.text((340,10), "% Fuel Remaining", font=fnt, fill=(0,0,0,255))

    out = Image.alpha_composite(base, txt)
    out.save(output_file_name)
    #app = App(title="Hello world")
    #guage = Picture(app, image="new_guage.png")
    os.system('pcmanfm --set-wallpaper /home/pi/fuel/new_gauge.png --wallpaper-mode=center')

    remurl = 'http://myurl.co.uk/pi/fuel/guage.php'
    myobj = {'fuelpercent': percent}

    x = requests.post(remurl, data = myobj)

    time.sleep(10)
