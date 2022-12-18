from turtle import title
from numpy import sign
from selenium.webdriver.common.by import By
from sqlalchemy import false, true
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

# Define Page Functions to be tested --> 

class BasePage(object):
    def __init__(self, driver):
        self.driver = driver

class GamePage(BasePage):

    def is_title_matches(self):
        return ("Word Sweeper" in self.driver.title)

    def login_button(self):
        login_button = self.driver.find_element(By.XPATH,'//*[@id="navbarSupportedContent"]/form/a[1]')
        self.driver.execute_script("arguments[0].click();", login_button)
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.url_contains("/login"))

    def signup_button(self):
        signup_button = self.driver.find_element(By.XPATH,'//*[@id="navbarSupportedContent"]/form/a[2]')
        self.driver.execute_script("arguments[0].click();", signup_button)
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.url_contains("/signup"))

    def click_grid(self):
        for i in range(0,25):
            grid = self.driver.find_element(By.ID, str(i))
            grid.click()
        time.sleep(1)
        count = self.driver.find_element(By.XPATH,'//*[@id="count"]').text
        return count[8:]
    
    def flag(self):
        action = ActionChains(self.driver)
        for i in range(0,25):
            grid = self.driver.find_element(By.ID, str(i))
            action.move_to_element(grid).perform()
            action.context_click().perform()
            if "🚩" not in grid.text:
                return false
        time.sleep(1)
        return true

    def wrong_answer(self):
        answer = self.driver.find_element(By.XPATH,'//*[@id="ansInput"]')
        answer.send_keys("xxxxx")
        submit = self.driver.find_element(By.XPATH,'//*[@id="button-addon2"]')
        self.driver.execute_script("arguments[0].click();", submit)
        count = self.driver.find_element(By.XPATH,'//*[@id="count"]').text
        return count[8:]

class LoginPage(BasePage):

    def admin_signin(self):
        username = self.driver.find_element(By.XPATH,'//*[@id="username"]')
        username.send_keys("admin")
        password = self.driver.find_element(By.XPATH,'//*[@id="password"]')
        password.send_keys("root1234")
        signin_but = self.driver.find_element(By.XPATH,'//*[@id="submit"]')
        self.driver.execute_script("arguments[0].click();", signin_but)
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.url_contains("/admin"))
