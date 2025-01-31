
# importing dependencies:-
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import email.encoders

import requests
import schedule
from datetime import datetime
import time
import pandas as pd

def send_mail(subject, body, filename):

    #smtp_server = "smtp.google.com"
    smtp_server ="mail.goutamg245@gmail.com"
    smtp_port =587
    sender_mail ="djononon245@gmail.com"
    email_password ="admin@234"
    receiver_mail ="busniess.naj@gamil.com"

    # compose the mail
    message = MIMEMultipart()
    message['From'] =sender_mail
    message['To'] =receiver_mail
    message['Subject'] = subject

    # attaching body
    message.attach(MIMEText(body, 'plain'))

    # attach csv file
    with open(filename, 'rb') as file:
        part =MIMEBase('application', 'octet-stream')
        part.set_payload(file.read())
        email.encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
        message.attach(part)

    # start server
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls() # secure connection
            server.login(sender_mail, email_password) # login

            # sending mail
            server.sendmail(sender_mail, receiver_mail, message.as_string())
            print("Email send successful")

    except Exception as e:
        print(f'Unable to send mail {e}')


# Getting crypto data:-
def get_crypto_data():
    # Api requests:-
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    param = {
        'vs_currency' : 'usd',
        'order' : 'market_cap_desc',
        'per_page': 250,
        'page': 1
    }



    # sending requests
    response = requests.get(url, params=param)

    if response.status_code == 200:
        print('Connection Successfull! \nGetting the data...')
    
        # storing the response into data
        data = response.json()
    
        # creating df dataframe
        df = pd.DataFrame(data)

        #Selecting only columns we need data cleaning
        df = df[[
        'id','current_price', 'market_cap', 'price_change_percentage_24h',
        'high_24h' , 'low_24h' , 'ath', 'atl' 
        ]]

        print(df.columns)
    
        #creating new columns
        today =  datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        df['time_stamp'] = today
    
        # getting top 10
        top_negative_10 = df.nsmallest(10, 'price_change_percentage_24h')
    
        # positive top
        top_positive_10 = df.nlargest(10, 'price_change_percentage_24h')
    
        # saving the data
        file_name = f'crypto_data {today}.csv'
        df.to_csv(file_name, index=False)

    
        print("Data saved successfully as {file_name}!")

        # Call email function to create the reports

        subject= f"Top 10 crypto currency data tyo invest for {today}"
        body =f"""
        Good Morning,\n\n

        your crypto report is here!\n\n
        
        Top 10 crypto with highest price increase in last 24 hour!\n
        {top_positive_10}\n\n\n

        Top 10 crypto with highest price decrease in last 24 hour!\n
        {top_negative_10}\n\n\n

        Attached 250 plus crypto currency latest reports\n

        Regards!\n
        see you tomorrow!\n
        Your crypto python application

        """
        send_mail(subject, body, file_name)
    
    else:
        print(f"Connection Failed Error Code {response.status_code}")
    
#this get executed only if we run this function
if __name__ == '__main__':
    #call the function
    get_crypto_data()
