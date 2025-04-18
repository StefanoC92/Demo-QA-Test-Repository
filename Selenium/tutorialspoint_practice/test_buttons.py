# vim test.py
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(autouse=True)
def driver_handler():

    options = Options()
    #Comment following 2 lines to Run with Chrome GUI
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    #Create instance of Chrome webdriver
    driver = webdriver.Chrome(options=options)

    # implicit wait of 15 seconds
    driver.implicitly_wait(10)

    #Run web application
    driver.get("https://www.tutorialspoint.com/selenium/practice/buttons.php")

    yield driver

    #close the web driver
    driver.close()

def test_title(driver_handler):
    title = driver_handler.title

    assert title == "Selenium Practice - Buttons"

def test_clickme_btn(driver_handler):
    btn = driver_handler.find_element(by=By.CLASS_NAME, value="btn-primary")
    btn.click()

    txt = driver_handler.find_element(by=By.ID, value="welcomeDiv")
    WebDriverWait(driver_handler, timeout=5).until(EC.visibility_of_element_located((By.ID, "welcomeDiv")))

    assert txt.text == "You have done a dynamic click"

def test_doubleclick_btn(driver_handler):
    
    btn = driver_handler.find_element(by=By.CLASS_NAME, value="btn-success")

    action = ActionChains(driver_handler)
    action.double_click(on_element=btn).perform()
    action.reset_actions()

    txt = driver_handler.find_element(by=By.ID, value="doublec")
    WebDriverWait(driver_handler, timeout=5).until(EC.visibility_of_element_located((By.ID, "welcomeDiv")))

    assert txt.text == "You have Double clicked"



    
