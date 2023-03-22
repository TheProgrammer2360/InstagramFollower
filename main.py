from bot import Instagram
import time
import os

mybot = Instagram()
phone_number = os.environ["PHONENUMBER"]
password = os.environ["PASSWORD"]

value = mybot.login_with_facebook(password=password, username=phone_number)
mybot.go_to_user_url("https://www.instagram.com/kaymo_black/")
mybot.go_to_followers()
time.sleep(2)
mybot.follow_everyone()
time.sleep(3600)
