import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import serial
import picamera as c
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

GPIO.setwarnings(False)

sensor = Adafruit_DHT.DHT11
pin = 3
ch=2

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin,GPIO.IN)
GPIO.setup(ch,GPIO.IN)
cred=credentials.Certificate('/home/pi/Desktop/conver-e6a68.json')
firebase_admin.initialize_app(cred,{'storageBucket':'conver-e6a68.appspot.com'})
bucket = storage.bucket('gs://conver-e6a68.appspot.com')
num=0;

def main():
		time.sleep(2)
               	pic()
		num=num+1
                	image_url='/home/pi/Desktop/image.jpg'
                	try:
                    		blob=bucket.blob('new_cool_image'+str(num)+'.jpg')
                   		blob.upload_from_filename(image_url)
			time.sleep(2)
                    		print('image stored')
		except:
			print('Image uploadation failed')
                
def sounddetected():
        sound=IO.add_event_detect(ch,IO.BOTH,bouncetime=300)
        if sound is None:
                return False
        else:
                return True
def heatdetected():
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

        if humidity is not None and temperature is not None:
                print 'Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity)
                return True
        else:
                print 'Failed to get reading. Try again!'
                return False
        time.sleep(0.1)

def pic():
        camera=c.PiCamera()
        try:
		camera.start_preview()
		time.sleep(2)
            	camera.capture('image.jpg')
		camera.stop_preview()
            	camera.vflip = True
            	camera.hflip = True
            	camera.brightness=80
    

try:
        while True:
                if sounddetected() or heatdetected():
                        main()
except:
	print('Exception')					

