import smtplib

YOUR_GOOGLE_EMAIL = 'mvg7486@gmail.com'  # The email you setup to send the email using app password
sent_to = 'mikegamarnik@gmail.com'
YOUR_GOOGLE_EMAIL_APP_PASSWORD = 'rxtk ixgl ltlb fuod'  # The app password you generated

smtpserver = smtplib.SMTP_SSL('smtp.gmail.com', 465)
smtpserver.ehlo()
smtpserver.login(YOUR_GOOGLE_EMAIL, YOUR_GOOGLE_EMAIL_APP_PASSWORD)

# Test send mail
sent_from = YOUR_GOOGLE_EMAIL
email_text = 'This is a test'
email_subj = 'Todays Stocks'
message = 'Subject: {}\n\n{}'.format(email_subj, email_text)
smtpserver.sendmail(sent_from, sent_to, message)
print("email sent")
# Close the connection
smtpserver.close()
# from datetime import datetime

# # Get the current time
# current_time = datetime.now()
# print(current_time)