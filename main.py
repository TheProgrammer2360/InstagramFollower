from bot import Instagram
import time
import os

mybot = Instagram()
phone_number = os.environ["PHONENUMBER"]
password = os.environ["PASSWORD"]

value = mybot.login_with_facebook(password=password, username=phone_number)
print(value)
time.sleep(3600)
