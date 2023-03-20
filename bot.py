from selenium import  webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

class Instagram:
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path="/chromedriver.exe")
        self.driver.maximize_window()
        self.driver.get(url="https://www.instagram.com")
        self.is_logged_in = False
        self.is_in_user_profile = False
        self.on_followers = False

    def login_with_facebook(self, username: str, password: str) -> bool:
        """Will try to log in, if successful return true else false"""
        xpath = "/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/section/main/" \
                "article/div[2]/div[1]/div[2]/form/div/div[5]/button"
        try:
            # wait ten seconds for the login with facebook button to show and then click it
            WebDriverWait(self.driver, 10).until(
                ec.presence_of_element_located((By.XPATH, xpath))
            )
        finally:
            # when the login in with facebook button shows up just get hold of it
            login_with_facebook = self.driver.find_element(By.XPATH, xpath)
            # and click it
            login_with_facebook.click()

        # getting hold of the email input area
        email_input_area = self.driver.find_element(By.ID, "email")
        # input the username
        email_input_area.send_keys(username)
        # Getting hold of the password input area
        password_input_area = self.driver.find_element(By.ID, "pass")
        # # input the password
        password_input_area.send_keys(password)
        # getting hold of the login button
        login_button = self.driver.find_element(By.ID, "loginbutton")
        login_button.click()


    def go_to_user_url(self, url: str) -> None:
        """makes sure that the user is signed in or else throw an exception"""
        pass

    def go_to_followers(self) -> None:
        """requires the user to be signed in and with to be a user profile"""
        pass

