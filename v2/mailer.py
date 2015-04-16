#!/usr/bin/python
# -*- coding: utf-8 -*-
import smtplib, mimetypes  
from email.mime.text import MIMEText  
from email.mime.multipart import MIMEMultipart  
from email.mime.image import MIMEImage   
import config

def send(title,body):
    s = smtplib.SMTP()  
    s.connect(config.smtp_host)  
    s.login(config.smtp_usr,config.smtp_pass)  
    
    msg = MIMEMultipart()  
    msg['From'] = config.smtp_from 
    msg['To'] =  ','.join(config.smtp_mailto)  
    msg['Subject'] = title  
    msg.attach(MIMEText( body ) )   

    s.sendmail(config.smtp_from,config.smtp_mailto,msg.as_string())  
    s.quit()  
    s.close()  


if __name__ == "__main__":
    send("hi","xx")