import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders

#from my_password import my_password

email_user = 'even311379@hotmail.com'
email_send = 'masusalmon.yang@gmail.com'
subject = 'GPS 總整理最後版'

msg = MIMEMultipart()
msg['From'] = email_user
msg['To'] = email_send
msg['Subject'] = subject
body = '''
An email send from python!!
'''

msg.attach(MIMEText(body,'plain'))

def attach_an_image(filename):
    img_data = open(filename,'rb').read()
    image = MIMEImage(img_data,name=os.path.basename(filename))
    msg.attach(image)

def attach_a_file(filename):
    attachment = open(filename, 'rb')
    part = MIMEBase('application','octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition',"attachment; filename= "+filename)
    msg.attach(part)


##attach_an_image('email_attachment_test.jpg')
##attach_an_image('houghcircles2.jpg')
attach_a_file('20161108_Updated_GPS_ALL_refine.csv')

text = msg.as_string()

server = smtplib.SMTP('smtp.live.com',587)

server.ehlo()
server.starttls()
server.login(email_user,'???')

server.sendmail(email_user,email_send,text)
server.close()
