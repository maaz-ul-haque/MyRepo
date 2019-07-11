#!/usr/bin/env python
import re
import getpass, imaplib
import datetime
import base64


TODAYSDATE = datetime.date.today().strftime("%d-%b-%Y").strip()
ONEDAYAGO = (datetime.date.today() - datetime.timedelta(days=30)).strftime("%d-%b-%Y").strip()
aws_list = []

M = imaplib.IMAP4_SSL("imap.gmail.com", 993)
M.login("cloudways.maazulhaq@gmail.com", "**************")
M.select('"maaz.haq@cloudways.com/Amazon Abuses"')

typ, data = M.search(None, '(FROM "ec2-abuse@amazon.com" SUBJECT "Your Amazon EC2 Abuse Report" since %s before %s)' % (ONEDAYAGO, TODAYSDATE) )

for num in data[0].split():
    typ, data = M.fetch(num, '(RFC822)')
    email=data[0][1]

    subject = re.search('Subject: (.*)', email)
    ticket_id = re.search('Your Amazon EC2 Abuse Report (.*) \[', subject.group(1))
    date = re.search('Date: (.*)', email)
    body = re.search('Hello(.*)\n', email, re.DOTALL)
    instance_id = re.search('i-(.*)', body.group())

    if ('Re:' or 'RE:') not in subject.group():

        if "spam" in body.group(0) or "Spam" in body.group(0):
            abuse_type = "Email Spamming"
        else:
            abuse_type = "NA"

        if "EC2 Instance Id:" in body.group():
            print '\n' + str(instance_id.group())
        else:
            print "\nInstance ID is not available"

        print str(subject.group(0))
        print ticket_id.group(1)
        print str(date.group(1))
        print("Abuse type is: "+abuse_type)

M.close()
M.logout()
