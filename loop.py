from ftplib import FTP
import picamera
import time
from PIL import Image, ImageDraw
import RPi.GPIO as GPIO

#Move servo, capture photos and repeat
try:
	#Init camera
	i = 10;
	camera = picamera.PiCamera();
	camera.resolution = (800, 600);
	GPIO.setup(4, GPIO.OUT);
	time.sleep(1);
	#Move servo to the left and capture left.jpg
	while (i):
		GPIO.output(4, GPIO.HIGH);
		time.sleep(0.0010);
		GPIO.output(4, GPIO.LOW);
		time.sleep(0.02);
		i -= 1;
	time.sleep(1);
	camera.capture('left.jpg');
	#Move servo to the right and capture right.jpg
	while (i):
		GPIO.output(4, GPIO.HIGH);
		time.sleep(0.0020);
		GPIO.output(4, GPIO.LOW);
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
	drawright.text( (300, 50), ts);
	drawleft.text( (300, 50), ts);
	#Save manipulated photos to rightfinal.jpg/leftfinal.jpg
	imageright.save ('rightfinal.jpg', quality=85);
	imageleft.save ('leftfinal.jpg', quality=85);
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
