from bot import Instagram
import time
import os


mybot = Instagram()
phone_number = os.environ["PHONENUMBER"]
password = os.environ["PASSWORD"]
print(f"phone number : {phone_number}\n password: {password}")
time.sleep(3600)
