import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains


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

        # waiting for 'Turn on Notifications' in order to confirm that I have logged in
        header_xpath = "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div" \
                       "/div[2]/div/div/div/div/div[2]/div/div/div[2]/span"
        not_now_button_xpath = "/html/body/div[2]/div/div/div[2]/div/div/div[1]" \
                               "/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]"
        # wait 10 seconds for the header to appear
        try:
            WebDriverWait(self.driver, 20).until(
                ec.presence_of_element_located((By.XPATH, header_xpath))
            )
        except TimeoutException:
            # when 10 seconds have passed but still not logged in
            return False
        else:
            # when the notification is up
            # find the not now button and click it
            not_now_button = self.driver.find_element(By.XPATH, not_now_button_xpath)
            not_now_button.click()
            # update the logged in status
            self.is_logged_in = True
            return True

    def go_to_user_url(self, url: str) -> None:
        """makes sure that the user is signed in or else throw an exception"""
        if not self.is_logged_in:
            raise InstagramException("Not Logged In")
        self.driver.get(url=url)
        self.is_in_user_profile = True

    def go_to_followers(self) -> None:
        """requires the user to be signed in and with to be a user profile"""
        # raise the exception when th user is not the profile
        if not self.is_in_user_profile:
            raise InstagramException("Not in a user profile")
        # when user in on the profile
        # wait maximum of 10 seconds for followers link to be available
        xpath = "/html/body/div[2]/div/div/div[1]/div/div/div" \
                "/div[1]/div[1]/div[2]/section/main/div/header/section/ul/li[2]/a"
        try:
            WebDriverWait(self.driver, 10).until(
                ec.presence_of_element_located((By.XPATH, xpath))
            )
        except TimeoutException:
            # when it is still not there, stop the program because it means that there is low internet
            raise InstagramSlowInternet("Your internet is slow, please try again")
        else:
            # When the followers link has been found
            followers_link = self.driver.find_element(By.XPATH, xpath)
            followers_link.click()
            self.on_followers = True
            self.is_in_user_profile = False

    def follow_everyone(self) -> None:
        """will follow everyone not followed"""
        if not self.on_followers:
            raise InstagramException("Not on followers page")
        actions = ActionChains(self.driver)
        # get all the buttons with follow text
        buttons_with_follow = [button for button in self.driver.find_elements(By.TAG_NAME, "button") if button.text ==
                               "Follow"]
        # scroll to the last one
        actions.move_to_element(buttons_with_follow[-1]).perform()
        prev_last = buttons_with_follow[-1]
        # repeating the process until we reach the last user
        continue_scrolling = True
        while continue_scrolling:
            buttons_with_follow = [button for button in self.driver.find_elements(By.TAG_NAME, "button") if
                                   button.text ==
                                   "Follow"]
            # scroll to the last one
            actions.move_to_element(buttons_with_follow[-1]).perform()
            # wait 5 seconds for the other elements to load
            time.sleep(2)
            # checking if we are on the last element
            if prev_last == buttons_with_follow[-1]:
                continue_scrolling = False
            else:
                # update the new last element
                prev_last = buttons_with_follow[-1]


class InstagramException(Exception):
    def __init__(self, message):
        super().__init__(message)


class InstagramSlowInternet(Exception):
    def __init__(self, message):
        super().__init__(message)
