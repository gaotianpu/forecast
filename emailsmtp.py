#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''it's a python script to get the pv,then send email to managers.'''
import os
import sys
sys.path.insert(0, os.path.join('..'))
import da
import web
import smtplib,time
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from datetime import datetime,date,timedelta

def sendmail(subject,content,tousrs):
    hostname ='smtp.163.com'
    from_usr ='name@163.com'
    from_usr_pwd='poss'
    msg = MIMEText(content,'html','utf-8')
    msg['Subject']= subject
    msg['To'] = ','.join(tousrs)
    server = smtplib.SMTP(hostname)
    server.set_debuglevel(1)
    server.login(from_usr, from_usr_pwd)
    server.sendmail(from_usr, tousrs, msg.as_string())
    server.quit()

def sendmail_attach(subject,content,tousrs,attchfiles):
    msg = MIMEMultipart()
    txt = MIMEText(content,'html','utf-8')
    msg.attach(txt)
    for attchfile in attchfiles:
        att = MIMEText(open(attchfile,'rb').read(),'base64','utf-8')
        att["Content-Type"] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        att["Content-Disposition"] = 'attachment;filename="%s"' %(os.path.basename(attchfile))
        msg.attach(att)

    msg['Subject']= subject
    msg['To'] ='tgao@airizu.com'
    server = smtplib.SMTP(hostname)
    server.set_debuglevel(1)
    server.login(from_usr, from_usr_pwd)
    server.sendmail(from_usr, tousrs, msg.as_string())
    server.quit()

if __name__ == "__main__":
    sendmail('helloword','test','aa@qq.com')
