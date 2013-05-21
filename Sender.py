import smtplib, poplib, email

class EmailServer:
  def __init__(self,smtp,pop):
		self._SMTPServer = smtplib.SMTP(smtp)
		self._POPServer = poplib.POP3(pop)

	def login(self,user,psw):
		self._From = user
		self._Psw = psw
		self._SMTPServer.login(self._From,self._Psw)
		return True

	def sendMail(self,to,subject,body):
		self._Msg = email.message_from_string(body)
		self._Msg['To'] = to
		self._Msg['From'] = self._From
		self._Msg['Subject'] = subject
		self._SMTPServer.sendmail(self._From,to,self._Msg.as_string())
		self._SMTPServer.quit()
		return True

	def recvMail(self):
		self._POPServer.user(self._From)
		self._POPServer.pass_(self._Psw)
		print self._POPServer.getwelcome()

		if self._POPServer.stat()[1]:
			print 'you have new email'
		else:
			print 'No incoming email'
			return False

		emailList = self._POPServer.list()[1]
		for item in emailList:
			emailNo, emailSize = item.split(' ')
			#print emailNo, '--', emailSize
			emailContent = self._POPServer.retr(emailNo)[1]
			#print emailContent
			mail = email.message_from_string('\n'.join(emailContent))

			for k,v in mail.items():
				if k in ('From','To','Subject'):
					print k,':',v

			print 'body: \n', mail.get_payload()[0]


			break


smtp = 'smtp.qq.com'
pop = 'pop.qq.com'
user = 'xxxxxx@qq.com'
psw = 'xxxxx'
to = 'xxxx@hotmail.com'
subject = 'test email server 2'
body = 'this is the body'

svr = EmailServer(smtp,pop)
svr.login(user,psw)
"""if svr.login(user,psw):
	if svr.sendMail(to,subject,body):
		print 'sent'
	else:
		print 'sent failed'
else:
	print 'login failed' """

svr.recvMail()
