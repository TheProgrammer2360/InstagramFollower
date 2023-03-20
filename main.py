from bot import Instagram
import time
import os


mybot = Instagram()
phone_number = os.environ["PHONENUMBER"]
password = os.environ["PASSWORD"]

time.sleep(3600)
