from selenium import  webdriver
from selenium.webdriver.common.by import By

class Instagram:
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path="/chromedriver.exe")
        self.driver.maximize_window()
        self.driver.get(url="https://www.instagram.com")
        self.is_logged_in = False
        self.is_in_user_profile = False
        self.username = ""
        self.password = ""
        self.on_followers = False

    def login_with_facebook(self, username: str, password: str) -> bool:
        """Will try to log in, if successful return true else false"""
        pass

    def go_to_user_url(self, url: str) -> None:
        """makes sure that the user is signed in or else throw an exception"""
        pass

    def go_to_followers(self) -> None:
        """requires the user to be signed in and with to be a user profile"""
        pass

