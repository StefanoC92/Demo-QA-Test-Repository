# vim test.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(autouse="True")
def driver_handler():

    options = Options()
    #Comment following 2 lines to Run with Chrome GUI
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    #Create instance of Chrome webdriver
    driver = webdriver.Chrome(options=options)
    #Run web application
    driver.get("https://www.tutorialspoint.com/selenium/practice/alerts.php")

    yield driver

    #close the web driver
    driver.quit

def test_title(driver_handler):
    title = driver_handler.title

    assert title == "Selenium Practice - Alerts"