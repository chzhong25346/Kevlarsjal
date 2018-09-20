import smtplib
import logging
import yaml,os
import sys
logger = logging.getLogger('main.mail')


def sendMail(sub,cont):
    try:
        with open("config.yaml", 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
    except Exception as e:
        logger.error('No config.yaml file, unable to send email')
        logger.error(e)
        sys.exit(1)

    # start talking to the SMTP server for Gmail
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.ehlo()
    # now login as my gmail user
    username = cfg['gmail']['username']
    password = cfg['gmail']['password']
    recipient = cfg['gmail']['recipient']
    s.login(username,password)
    # the email objects
    replyto=username # where a reply to will go
    sendto=[recipient] # list to send to
    sendtoShow=recipient# what shows on the email as send to
    subject=sub # subject line
    content=cont # content
    # compose the email. probably should use the email python module
    mailtext='From: '+replyto+'\nTo: '+sendtoShow+'\n'
    print(content)
    mailtext=mailtext+'Subject:'+subject+'\n'+content
    # send the email
    s.sendmail(replyto, sendto, mailtext)
    # we're done
    rslt=s.quit()
