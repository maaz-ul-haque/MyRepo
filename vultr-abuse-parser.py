#!/usr/bin/env python
import re
import getpass, imaplib
import datetime
import base64


TODAYSDATE = datetime.date.today().strftime("%d-%b-%Y").strip()
ONEDAYAGO = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%d-%b-%Y").strip()

M = imaplib.IMAP4_SSL("imap.gmail.com", 993)
M.login("cloudways.maazulhaq@gmail.com", "***********")
M.select('"maaz.haq@cloudways.com/Vultr"')

typ, data = M.search(None, '(since %s before %s)' % (ONEDAYAGO, TODAYSDATE))

for num in data[0].split():
    typ, data = M.fetch(num, '(RFC822)')
    email=data[0][1]
    subject = re.search('Subject:(.*)\n', email)
    date = re.search('Date:(.*)', email)
    body = re.search('base64(.*)', email, re.DOTALL)
    if "Ticket" in subject.group(1) and not 'Vultr.com: Cloud Server Activated' in subject.group(1):
        print("\n"+subject.group(1))   

#        ticketid = re.search('\[(.*?)\]' , result.group(1))
#        if "Ticket" in str(ticketid.group(1)):
#    	print("TickedID: "+str(ticketid.group(0)))
        print("Date is:"+date.group(1))
        print(base64.b64decode(body.group(1)))
#        print body.group(1)
#
M.close()
M.logout()
