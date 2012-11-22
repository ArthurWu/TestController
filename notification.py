import smtplib
from email.mime.text import MIMEText
subject = 'Runing tests result for build %s'
sender = 'svc-SPbuild-Zhuhai@quest.com'
pwd = 'Pa$$word'
domain = 'prod'

receivers = ['arthur.wu@quest.com']
cc = ['175040128@qq.com']

body = '''
Dear all,

	Warrior and blade's tests are ok.

'''

def send_mail(sender, receivers, subject, body, cc=None):
	msg = MIMEText(body)
	msg['Subject'] = subject
	msg['From'] = sender
	msg['To'] = ', '.join(receivers)
	msg['CC'] = ', '.join(cc or [])
	
	s = smtplib.SMTP('10.1.0.160')
	s.sendmail(sender, receivers, msg.as_string())
	s.quit()

if __name__ == '__main__':
	send_mail(sender, receivers, subject, body, cc)