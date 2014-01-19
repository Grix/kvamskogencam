#loop.py
#This script takes two photos from separate angles via a raspberry pi 
#/w camera add-on and a servo, and uploads the photos to a webserver
#Author: GrixM - Gitle Mikkelsen

from ftplib import FTP
import picamera
import time
from PIL import Image, ImageDraw
import RPi.GPIO as GPIO

SERVO_PIN = 4;
FTP_SERVER = 'ftp.bitlasers.com';
FTP_USER = 'kvamskogen@bitlasers.com';
FTP_PASSWORD = '';
IMAGE_QUALITY = 80;


if (time.localtime().tm_hour < 7):
	exit(0);

#Move servo, capture photos and repeat
try:
	#Init camera
	camera = picamera.PiCamera();
	camera.resolution = (1280, 800);
	camera.vflip = 1;
	camera.hflip = 1;
	GPIO.setmode(GPIO.BCM);
	GPIO.setup(SERVO_PIN, GPIO.OUT);
	time.sleep(1);
	#Move servo to the left and capture left.jpg
	i = 10;
	while (i):
		GPIO.output(SERVO_PIN, GPIO.HIGH);
		time.sleep(0.0007);
		GPIO.output(SERVO_PIN, GPIO.LOW);
		time.sleep(0.02);
		i -= 1;
	time.sleep(1);
	camera.capture('left.jpg');
	#Move servo to the right and capture right.jpg
	i = 10;
	while (i):
		GPIO.output(SERVO_PIN, GPIO.HIGH);
		time.sleep(0.0023);
		GPIO.output(SERVO_PIN, GPIO.LOW);
		time.sleep(0.02);
		i -= 1;
	time.sleep(1);
	camera.capture('right.jpg');
	camera.close();
	time.sleep(1);
	GPIO.cleanup();
except:	
	print "Unexpected error in camera/servo section"
	raise

#Append timestamp to and compress photos
try:
	#Get timestamp
	ts = time.strftime("%Y-%m-%d %H:%M:%S");
	#Open photos for manipulation
	imageright = Image.open("./right.jpg");
	imageleft = Image.open("./left.jpg");
	drawright = ImageDraw.Draw(imageright);
	drawleft = ImageDraw.Draw(imageleft);
	#Draw the timestamp
	drawright.text( (1100, 770), ts);
	drawleft.text( (1100, 770), ts);
	#Save manipulated photos to rightfinal.jpg/leftfinal.jpg
	imageright.save ('rightfinal.jpg', quality=IMAGE_QUALITY);
	imageleft.save ('leftfinal.jpg', quality=IMAGE_QUALITY);
	time.sleep(1);
except:	
	print "Unexpected error in photo manipulation section"
	raise

#Upload photos to FTP server
try:
	#Open maniulated images
	photoleft = open("./leftfinal.jpg", "rb");
	photoright = open("./rightfinal.jpg", "rb");
	#Connect to FTP and store
	ftp = FTP(FTP_SERVER, FTP_USER, FTP_PASSWORD);
	ftp.storbinary("STOR right.jpg", photoright);
	ftp.storbinary("STOR left.jpg", photoleft);
except:	
	print "Unexpected error in FTP section"
	raise
