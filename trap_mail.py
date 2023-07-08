import smtplib

def generate_mail(message):
    sender_name = "SNMP Trap Receiver"
    sender_email = 'sample.mail.for.work.inline@gmail.com'
    recipient_emails = ['sample.mail.for.work.inline@gmail.com']
    subject = "Sample mail generated from python script"
    email_text = """\
From: %s <%s>
To: %s
Subject: %s

%s
""" % (sender_name, sender_email, ", ".join(recipient_emails), subject, message)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(sender_email, 'fdozznwebwrmkfpk')
        server.sendmail(sender_email, recipient_emails, email_text)
        server.close()

        print('>>> Email sent!')
    except Exception as exception:
        print("Error: %s!\n\n" % exception)

