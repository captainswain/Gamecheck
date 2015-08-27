import time, requests, smtplib, urllib2
from pushbullet import Pushbullet
pb = Pushbullet("Pushbullet API")

starttime=time.time()
def send_email(user, pwd, recipient, subject, body):
    import smtplib

    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print 'successfully sent the mail'
    except:
        print "failed to send mail"
def Check_ID(id):
    apiurl = "http://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key=12A1D1DE83F9932934EDD6DF2BA00463&steamids=76561198000020858"
    PlayerData = requests.get(apiurl).json()
    isbanned = PlayerData['players'][0]['VACBanned']

    if isbanned == False:
        print "Check Complete: Account is Clean."
        #send_email("username", "password", "recepi@gmail.com", "Everything is looking good Chief.", "Looks like Everything is going good!")
    elif isbanned == True:
        print "Check Complete: Account is Dirty."
        push = pb.push_note("Looks Like someone is dirty", "Hey there, It looks like that account is dirty!")
        send_email("username", "password", "recepi@gmail.com", "Looks like we are taking a vacation Chief.", "Hey there ! Looks like that account is dirty!")
while True:
  print "Activating Check...."
  Check_ID(1)
  time.sleep(60.0 - ((time.time() - starttime) % 60.0))
