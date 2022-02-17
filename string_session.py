from telethon.sessions import StringSession
from telethon.sync import TelegramClient

print("Telethon String Session Generator")
print(
    """Please go-to my.telegram.org
Login using your Telegram account
Click on API Development Tools
Create a new application, by entering the required details"""
)

APP_ID = int(input("Enter APP ID here: "))
API_HASH = input("Enter API HASH here: ")

with TelegramClient(StringSession(), APP_ID, API_HASH) as client:
    string = client.session.save()
    saved_messages_template = """<code>STRING_SESSION</code>: <code>{}</code>
<i>It is forbidden to pass this value to third parties</i>""".format(
        string
    )
    client.send_message("me", saved_messages_template, parse_mode="html")
    print("Check Your Telegram Saved Messages For String Session")
