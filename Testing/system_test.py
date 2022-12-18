import unittest, os
from selenium import webdriver
from sqlalchemy import true
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import page
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


class TestWeb(unittest.TestCase):

    def setUp (self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install())) #have to have chrome installed
        self.driver.get("http://127.0.0.1:5000")

    def test_title(self): #correct site
        gamePage = page.GamePage(self.driver)
  
        assert gamePage.is_title_matches()

    def test_loginBut(self): #Open Login Page
        gamePage = page.GamePage(self.driver)
        gamePage.login_button()
        url = self.driver.current_url
        assert ("/login" in url)

    def test_signUpBut(self):
        gamePage = page.GamePage(self.driver)
        gamePage.signup_button()
        url = self.driver.current_url
        assert ("/signup" in url)

    def test_adminLog(self):
        gamePage = page.GamePage(self.driver)
        gamePage.login_button()
        loginPage = page.LoginPage(self.driver)
        loginPage.admin_signin()
        url = self.driver.current_url
        assert  ("/admin" in url)

    def test_graphClick(self): #left click
        gamePage = page.GamePage(self.driver)
        guessCount = int(gamePage.click_grid())
        assert guessCount != 0

    def test_flag(self):
        gamePage = page.GamePage(self.driver)
        assert  gamePage.flag()

    def test_submitWrong(self):
        gamePage = page.GamePage(self.driver)
        guessCount = int(gamePage.wrong_answer())
        assert guessCount == 1
    

    def tearDown(self):
        return self.driver.close()


if __name__ == '__main__':
    unittest.main()
    
