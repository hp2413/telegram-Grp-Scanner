# telegram-Grp-Scanner
Scan the telegram grp and alert on the required message over the mail

Step one: get the api keys and set it to the project

api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
phone = 'YOUR_PHONE_NUMBER'
# You need to get your own Telegram API ID and hash by registering an application on my.telegram.org.

Step two: set the email app password, to send emails

app_password = "your_app_password"
# this you need to get the App passwords, by following the below mentioned steps

Generating an App-Specific Password
1. Go to your Google Account Security Settings.
2. Under "Signing in to Google," select "App passwords."
3. Enter your Google account password if prompted.
4. Select "Mail" as the app and "Other" as the device.
5. Generate the password and use it in your script.

Step three: trigger the script using Python: python script_name.py

:Install this required lib:

pip install telethon
