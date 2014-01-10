from ftplib import FTP;
from time import sleep;

photo = open("./current.jpg", "rb");


ftp = FTP('ftp.bitlasers.com', 'kvamskogen@bitlasers.com', 'G0liates_ftp');
ftp.storbinary("STOR current.jpg", photo);