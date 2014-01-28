KvamskogenCam
=============

This is a python script designed to run on a raspberry pi with the camera addon attached to a servo,
It takes two photos from different angles, processes them and uploads them to a webserver.

INSTRUCTIONS:
Get a raspberry pi, the official camera add-on, and a simple servo motor.
Attach and set up the camera to the r-pi as per instructions in the box.
Attach the servo signal wire to your GPIO pins.
	You can either solder the wires on or cut the servo female servo lead connector into three pieces.
	Use google to find a r-pi GPIO pinout diagram.
	Connect the power leads to 5V and GND, and the signal lead to your desired GPIO pin (default is 4).
Set up an FTP user with home folder located to your choosing, or edit the script to upload to a different folder.
Place loop.py in a folder on your raspberry pi, adjust settings.
Use cron to set the script to run every x amount of time.