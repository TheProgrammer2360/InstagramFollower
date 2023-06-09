import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException,StaleElementReferenceException
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
            raise InstagramException("The followers tab is not open")
        actions = ActionChains(self.driver)
        scrolled_into_list = list()
        xpath = "/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]" \
                "/section/main/div/header/section/div[1]/div[1]/div/div[1]/button"
        following_not_wanted = self.driver.find_element(By.XPATH, xpath)
        while True:
            # get all the buttons with following or follow text
            buttons = [button for button in self.driver.find_elements(By.TAG_NAME, "button") if (button.text == "Follow" or button.text == "Following") and button != following_not_wanted]
            if len(scrolled_into_list) != 0:
                # condition to stop the while loop when the list is not updating
                if buttons[-1] == scrolled_into_list[-1]:
                    break
            for button in buttons:
                if button not in scrolled_into_list:
                    try:
                        # move to the button
                        actions.move_to_element(button).perform()
                        # update that you have scrolled into the element
                        scrolled_into_list.append(button)
                        # if it is  follow button, click it
                        if button.text == "Follow":
                            try:
                                button.click()
                            except ElementClickInterceptedException:
                                pass
                            # wait 1 second so it acts like human
                            time.sleep(1)
                    except StaleElementReferenceException:
                        # suggested for you option also has follow but cannot be scrolled into
                        pass
            # wait 3 seconds for the new list to load
            time.sleep(2)


class InstagramException(Exception):
    def __init__(self, message):
        super().__init__(message)


class InstagramSlowInternet(Exception):
    def __init__(self, message):
        super().__init__(message)
