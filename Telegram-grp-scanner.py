from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import PeerChannel
from telethon.tl.types import MessageMediaPhoto
import csv
import time
from pytz import timezone
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

# use this to install before run:  pip install telethon
# Replace these with your own API ID, hash, and phone number
api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
phone = 'YOUR_PHONE_NUMBER'
# You need to get your own Telegram API ID and hash by registering an application on my.telegram.org.

group_url = 'https://t.me/H1B_H4_Visa_Dropbox_slots'
# mentioned the grp url

to_email_list = ["recipient1@example.com", "recipient2@example.com"]
bcc_list = ["bcc1@example.com", "bcc2@example.com"]
from_email = "your_email@gmail.com"
app_password = "your_app_password"
# this you need to get the App passwords, by following the below mentioned steps

# Generating an App-Specific Password
# Go to your Google Account Security Settings.
# Under "Signing in to Google," select "App passwords."
# Enter your Google account password if prompted.
# Select "Mail" as the app and "Other" as the device.
# Generate the password and use it in your script.

client = TelegramClient('session_name', api_id, api_hash)


async def send_email(subject, body, to_email_list, bcc_list, from_email, password, isImage = False, message = None, smtp_server='smtp.gmail.com', smtp_port=587):
    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = ", ".join(to_email_list)
    msg['Bcc'] = ", ".join(bcc_list)
    msg['Subject'] = subject

    if isImage:
        # Attach the body with the msg instance
        msg.attach(MIMEText(body, 'plain'))
        image = await client.download_media(message.media)
        with open(image, 'rb') as img_file:
            img_data = img_file.read()
        mime_image = MIMEImage(img_data)
        mime_image.add_header('Content-Disposition', 'attachment', filename='image.jpg')
        msg.attach(mime_image)

    # Attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Set up the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection
        server.login(from_email, password)

        # Send the email
        text = msg.as_string()
        server.sendmail(from_email, to_email_list + bcc_list, text)

        # Close the connection
        server.quit()

        print(f"Email successfully sent to {to_email_list}")

    except Exception as e:
        print(f"Failed to send email. Error: {e}")

async def download_image(message):
    image = await client.download_media(message.media)
    with open(image, 'rb') as img_file:
        img_data = img_file.read()
    return MIMEImage(img_data)

async def main():
    await client.start(phone)

    # Getting the group details
    group = await client.get_entity(group_url)
    myData = set()
    pst = timezone('US/Pacific')
    while(True):  # Replace NUMBER_OF_ITERATIONS with how many times you want to repeat
        messages = await client(GetHistoryRequest(
            peer=PeerChannel(group.id),
            offset_id=0,
            offset_date=None,
            add_offset=0,
            limit=3, # to set the number of recent messages to get from the api call, here the last 3 messages are been fetched.
            max_id=0,
            min_id=0,
            hash=0
        ))

        # Save messages to CSV file
        with open('telegram_messages.csv', 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'date', 'message']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            for message in messages.messages:
                if(message.id not in myData):
                    myData.add(message.id)
                    date_pst = message.date.astimezone(pst)
                    date_pst_formatted = date_pst.strftime('%a, %b %d %I:%M:%S %p')
                    msg = {'id': message.id, 'date': date_pst_formatted, 'message': message.message}
                    print(msg)
                    if ('na' not in message.message.lower()) and (message.message.lower() != ''):
                        print("--:got msg:--")
                        await send_email("Got new msg in visa grp", str(msg), to_email_list, bcc_list, from_email, password, False, message)
                    if isinstance(message.media, MessageMediaPhoto):
                        print("got image")
                        await send_email("Got new img in visa grp", str(msg), to_email_list, bcc_list, from_email, password, True, message)
                    writer.writerow({'id': message.id, 'date': date_pst_formatted, 'message': message.message})

        time.sleep(10) # Delay for 10 sec to trigger the api again.



with client:
    client.loop.run_until_complete(main())


