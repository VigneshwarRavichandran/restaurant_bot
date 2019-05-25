import smtplib
from email.mime.text import MIMEText
import datetime

def send_email(booking_date, booking_time, booking_email):
	smtp_ssl_host = 'smtp.gmail.com'
	smtp_ssl_port = 465
	username = '16jecit119@gmail.com'
	password = 'user@123'
	sender = '16jecit119@gmail.com'
	# contents for the message
	booking_date = booking_date[0:10]
	booking_time = booking_time[11:16]
	msg = MIMEText('FOODIEE RESTAURANT WELCOMES YOU\n Booking Date : {0}\n Booking Time : {1}\n Your reservation is confirmed on the above date and time.'.format(booking_date, booking_time))
	msg['Subject'] = 'Booking Confirmation'
	msg['From'] = sender
	msg['To'] = booking_email
	# email connection establishment and execution
	server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
	server.login(username, password)
	server.sendmail(sender, booking_email, msg.as_string())
	server.quit()