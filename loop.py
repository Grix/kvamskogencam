#Hyttecam 2.0 - This script takes a photo from two angles using a raspberry pi w/ camera and servo, and uploads them to a webserver.
#Author: Gitle Mikkelsen
#Version 0.1 14.01.18


from ftplib import FTP
import picamera
import time
from PIL import Image, ImageDraw
import RPi.GPIO as GPIO

SERVO_PIN = 4;

#Move servo, capture photos and repeat
try:
	#Init camera
	i = 10;
	camera = picamera.PiCamera();
	camera.resolution = (1280, 800);
	camera.vflip = 1;
	GPIO.setmode(GPIO.BCM);
	GPIO.setup(SERVO_PIN, GPIO.OUT);
	time.sleep(1);
	#Move servo to the left and capture left.jpg
	while (i):
		GPIO.output(SERVO_PIN, GPIO.HIGH);
		time.sleep(0.0010);
		GPIO.output(SERVO_PIN, GPIO.LOW);
		time.sleep(0.02);
		i -= 1;
	time.sleep(1);
	camera.capture('left.jpg');
	#Move servo to the right and capture right.jpg
	i = 10;
	while (i):
		GPIO.output(SERVO_PIN, GPIO.HIGH);
		time.sleep(0.0020);
		GPIO.output(SERVO_PIN, GPIO.LOW);
		time.sleep(0.02);
		i -= 1;
	time.sleep(1);
	camera.capture('right.jpg');
	camera.close();
	time.sleep(1);
	GPIO.cleanup();
except:	
	print "Unexpected error camera/servo:"
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
	imageright.save ('rightfinal.jpg', quality=75);
	imageleft.save ('leftfinal.jpg', quality=75);
	time.sleep(1);
except:	
	print "Unexpected error photo manipulation:"
	raise

#Upload photos to FTP server
try:
	#Open maniulated images
	photoleft = open("./leftfinal.jpg", "rb");
	photoright = open("./rightfinal.jpg", "rb");
	#Connect to FTP and store
	ftp = FTP('ftp.bitlasers.com', 'kvamskogen@bitlasers.com', '');
	ftp.storbinary("STOR right.jpg", photoright);
	ftp.storbinary("STOR left.jpg", photoleft);
except:	
	print "Unexpected error FTP:"
	raise
