import smtplib
import ssl
from email.message import EmailMessage

# Define email sender and receiver
email_sender = 'biblefaithchurchit@gmail.com'
email_password = 'khcbdkeyxyqcvbcz'
email_receiver = 'pysirikwa@gmail.com'

# Set the subject and body of the email
subject = 'Check out my new video!'
body = """
I've just published a new video on YouTube: https://youtu.be/2cZzP9DLlkg
"""

em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = subject
em.set_content(body)

# Add SSL (layer of security)
context = ssl.create_default_context()

# Log in and send the email
with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender, email_receiver, em.as_string())

# import smtplib

# sender = 'from@fromdomain.com'
# receivers = ['pysirikwa@gmail.com']

# message = """From: From Person <from@fromdomain.com>
# To: To Person <to@todomain.com>
# Subject: SMTP e-mail test

# This is a test e-mail message.
# """

# try:
#    smtpObj = smtplib.SMTP('localhost')
#    smtpObj.sendmail(sender, receivers, message)         
#    print ("Successfully sent email")
# except SMTPException:
#    print ("Error: unable to send email")