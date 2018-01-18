import urllib2, base64, smtplib, datetime
from email.mime.text import MIMEText

#Put your email and password
EMAIL = ''
PASSWORD = ''

#dd-wrt info
DDWRT_USER = ''
DDWRT_PASSWORD = ''
DDWRT_IP = ''


def is_ip_changed(curIP):
	lastIP = "";

	try:
		with open("ip.txt","r") as file:
			lastIP = file.read()

		if curIP == lastIP:
			print "The IP continues the same: %s" % curIP
			return False

	except:
		pass
		
	with open("ip.txt","w") as file:
		print "The IP changed: %s" % curIP
		file.write(curIP)
		return True

 

def checkIP():
	result = "";

	username = DDWRT_USER 
	password = DDWRT_PASSWORD
	auth_encoded = base64.encodestring('%s:%s' % (username, password))[:-1]

	req = urllib2.Request('http://{}/Status_Internet.live.asp'.format(DDWRT_IP))
	req.add_header('Authorization', 'Basic %s' % auth_encoded)

	response = urllib2.urlopen(req)
	result = filter(None, response.read().split('\n'))[-1].split(' ')[-1].replace('}','');
	return result;

def mail(message):
	to = EMAIL
	gmail_user = EMAIL
	gmail_password = PASSWORD
	smtpserver = smtplib.SMTP('smtp.gmail.com', 587)
	smtpserver.ehlo()
	smtpserver.starttls()
	smtpserver.ehlo
	smtpserver.login(gmail_user, gmail_password)
	today = datetime.date.today()
	msg = MIMEText(message)
	msg['Subject'] = 'IP Config: %s' % today.strftime('%b %d %Y')
	msg['From'] = gmail_user
	msg['To'] = to
	smtpserver.sendmail(gmail_user, [to], msg.as_string())
	smtpserver.quit()

def check_ddwrt_config():
    if not DDWRT_USER or not DDWRT_PASSWORD or not DDWRT_IP:
        print("Check you ddwrt config.")
        return False

    return True

def check_email_config():
    if not EMAIL or not PASSWORD:
        print("Check your email config.")
        return False
    return True

if __name__ == '__main__':
    if not check_ddwrt_config() or not check_email_config():
        exit()

    ip = "Current WAN IP is: %s" % checkIP()
    print(ip)
    if is_ip_changed(ip):
        mail(ip)
	print "Mail Sended!"
