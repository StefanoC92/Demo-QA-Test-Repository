import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from visual_comparison.utils import ImageComparisonUtil

import time

@pytest.fixture
def chrome_webdriver():

    options = Options()
    #Comment following 2 lines to Run with Chrome GUI
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    yield driver

    driver.close()

def check_entry(webdriver, label_id: str, text_area_id: str, label_text: str, text_area_placeholder: str):
    #Check entry
    #Label
    lable_element = webdriver.find_element(By.ID, label_id)
    lable_element = WebDriverWait(webdriver, timeout=2).until(EC.visibility_of_element_located((By.ID, label_id)))
    assert label_text in lable_element.text
    #Data
    text_area_element = WebDriverWait(webdriver, timeout=2).until(EC.visibility_of_element_located((By.ID, text_area_id)))
    assert text_area_placeholder in text_area_element.get_attribute('placeholder')

    time.sleep(0.1)

def enter_text_value(webdriver, text_area_id: str, text_value: str):
    #Enter data
    text_area_element = WebDriverWait(webdriver, timeout=2).until(EC.visibility_of_element_located((By.ID, text_area_id)))
    text_area_element.send_keys(Keys.TAB)
    text_area_element.clear()
    text_area_element.send_keys(text_value)

    time.sleep(0.1)

def visual_comparison(webdriver, element_id: str):

    element = WebDriverWait(webdriver, timeout=5).until(EC.visibility_of_element_located((By.ID, element_id)))
    actual_image_path = "sources/actual_layouts/actual.png"
    actual_image_bytes = element.screenshot_as_png

    with open(actual_image_path, 'wb') as f:
        f.write(actual_image_bytes)
    
    expected_image_path = "sources/expected_layouts/expected.png"
    expected_image = ImageComparisonUtil.read_image(expected_image_path)
    actual_image = ImageComparisonUtil.read_image(actual_image_path)

    visual_comparison_result_path = "sources/visual_comparison_result/result.png"
    ImageComparisonUtil.compare_images(expected_image, actual_image, visual_comparison_result_path)

    match_result = ImageComparisonUtil.check_match(expected_image_path, actual_image_path)
    assert match_result

def test_text_box_title(chrome_webdriver):
    """
        - DQTP-TC-1: Test Case to test the rendering and functionality of the submission form.
    """

    #STEP 1:
    chrome_webdriver.get("https://demoqa.com/text-box")

    # #Check page title (By Tag Name)
    # heading1 = chrome_webdriver.find_element(By.TAG_NAME, 'h1')
    # assert "Text Box" in heading1.text

    #Check page title (By CSS Selector)
    heading1 = WebDriverWait(chrome_webdriver, timeout=2).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'h1.text-center')))
    assert "Text Box" in heading1.text

    #Test Data
    label_id_values = [
        "userName-label",
        "userEmail-label",
        "currentAddress-label",
        "permanentAddress-label",
    ]

    text_area_id_values = [
        "userName",
        "userEmail",
        "currentAddress",
        "permanentAddress"
    ]

    label_text_values = [
        "Full Name",
        "Email",
        "Current Address",
        "Permanent Address"
    ]

    text_area_placeholder_values = [
        "Full Name",
        "name@example.com",
        "Current Address",
        ""
    ]

    #Check Full Name entry
    for i in range(0, 4):

        check_entry(webdriver = chrome_webdriver, 
                    label_id = label_id_values[i], 
                    text_area_id= text_area_id_values[i], 
                    label_text= label_text_values[i], 
                    text_area_placeholder= text_area_placeholder_values[i])

    #STEP 2:
    text_values = [
        "Name Surname User 1",
        "name.surname@google.com",
        "Via delle Vie 12",
        "Via delle Vie 12"
    ]

    for i in range (0, 4):

        enter_text_value(webdriver = chrome_webdriver, 
                        text_area_id = text_area_id_values[i], 
                        text_value = text_values[i])
        
    #STEP 6: 
    submit_button = WebDriverWait(chrome_webdriver, timeout=5).until(EC.element_to_be_clickable((By.ID, 'submit')))
    submit_button.click()

    visual_comparison(chrome_webdriver, element_id= "output")
    




