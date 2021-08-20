import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from getpass import getpass
from easygui import passwordbox
import matplotlib.pyplot as plot
from datetime import date


def GenerateCSVFromLastMonth():
    df = pd.read_json("https://api.coindesk.com/v1/bpi/historical/close.json")
    cleanData = df.iloc[0:31, 0:1]
    print(cleanData)
    cleanData.to_csv('outCSV.csv', index=True)
    return cleanData


def SendCSVToEmail():
    mail_content = "Siin on viimase 31 päeva bitcoini hinnaajalugu"
    #The mail addresses and password
    sender_address = input("Kirjuta oma e-mail.")
    sender_pass = passwordbox("Kirjuta oma parool.")
    receiver_address = input("Kellele tahad meili saata?")
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Bitcoin prices for the last 31 days'   #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.ehlo()
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password

    part = MIMEBase('application', "octet-stream")
    part.set_payload(open("outCSV.csv", "rb").read())
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="Bitcoin_prices.csv"')
    text = message.as_string()

    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Email saadetud!')


def MakeLineChart():
    df = GenerateCSVFromLastMonth()
    today = date.today()
    todayFormaat = today.strftime("%d/%m/%Y")

    df.plot.line(title="31 päeva BTC hinnaajalugu ( " + todayFormaat + " )")

    plot.show(block=True)

#-----------------------------------------Skripti algus-------------------------------------------

GenerateCSVFromLastMonth()

MakeLineChart()

SendCSVToEmail()