import easyocr
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime, timedelta
import pytz
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import os
# import sys

# saving console log as txt file
#############################################
# timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
# filename = f"log_{timestamp}.txt"
# sys.stdout = open(filename, "w", encoding='utf-8')
# sys.stderr = sys.stdout

TMS_URL = "https://tms25.nepsetms.com.np/"
UserName = "YOUR USERNAME HERE"
PassWord = "YOUR PASSWORD HERE"
OrderEntry_URL = "https://tms25.nepsetms.com.np/tms/me/memberclientorderentry"
Stock_Symbol = "NMIC"
buyingQuantity = "10"
buyingPrice = "BUYING PRICE"
preOpenPrice = "PRE-OPEN BUYING PRICE"  # if you want to place order at pre-open

ktm = pytz.timezone("Asia/Kathmandu")
est = pytz.timezone("America/Toronto")

now_est = datetime.now(est)

now_ktm = datetime.now(ktm)
target_ktm = now_ktm.replace(hour=10, minute=20, second=0, microsecond=0)

if now_ktm >= target_ktm:
    target_ktm += timedelta(days=1)

target_est = target_ktm.astimezone(est)

while True:
    if datetime.now(est) >= target_est:
        print("It is time to log in!")
        print(datetime.now(ktm))
        break
    time.sleep(1)

# pyautogui.hotkey('win', 'alt', 'r')

# Setup Selenium
driver = webdriver.Chrome()
driver.maximize_window()
driver.get(TMS_URL)
time.sleep(10)

# Fill in username/password (you replace this with actual values)
driver.find_element(By.XPATH, "//input[@placeholder='Client Code/ User Name']").send_keys(UserName)

# Find the CAPTCHA image

while True:
    driver.find_element(By.XPATH, "//input[@placeholder='Password']").send_keys(PassWord)
    captcha_img = driver.find_element(By.XPATH, "//img[@alt='Captcha']")
    captcha_img.screenshot("captcha.png")
    reader = easyocr.Reader(['en'])  # Load English model
    result = reader.readtext('captcha.png')
    # Print out the detected text
    for detection in result:
        print("Detected text:", detection[1])
        print(datetime.now(ktm))
    if result:
        captcha_text = result[0][1]
        print("CAPTCHA:", captcha_text)
        print(datetime.now(ktm))
        captcha_input = driver.find_element(By.ID, 'captchaEnter')  # replace with actual ID
        captcha_input.send_keys(captcha_text)
        login_button = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Login']")
        login_button.click()
        time.sleep(10)
        try:
            # Find the span inside an element with class 'ubadge__item'
            element = driver.find_element(By.CSS_SELECTOR, ".ubadge__item span")
            text = element.text
            print(f"Span text: {text}")
            print(datetime.now(ktm))
            # Check if the text matches expected login username or ID
            if text.strip() == UserName:  # Replace with expected value
                print("✅ Logged in as expected.")
                print(datetime.now(ktm))
                break
        except Exception as e:
            continue


# PRE OPEN SESSION

target_ktm = now_ktm.replace(hour=10, minute=29, second=59, microsecond=0)
target_est = target_ktm.astimezone(est)

while True:
    if datetime.now(est) >= target_est:
        print("It is time to place orders")
        print(datetime.now(ktm))
        break
    time.sleep(1)

driver = webdriver.Chrome()
driver.maximize_window()

driver.get(OrderEntry_URL)

time.sleep(5)

buy_toggle = driver.find_element(By.CSS_SELECTOR, "div.xtoggler-control label:nth-child(3)")
buy_toggle.click()

symbol_input = driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="symbol"]')
symbol_input.clear()
symbol_input.send_keys(Stock_Symbol)
time.sleep(1)
symbol_input.send_keys(Keys.ENTER)
time.sleep(1)

# try:
#     # Wait up to 10 seconds for the element to be present in the DOM
#     price_element = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.XPATH, "//label[normalize-space()='Open']/following-sibling::b"))
#     )
#     open_price = price_element.text
#     buyingPrice = str(math.floor(float(open_price) * 1.10 * 10) / 10)
#     print("Open=", open_price)
#     print("Buy=", buyingPrice)
#
# except Exception as e:
#     print("❌ Could not find the open price.")
#     print(e)

qty_input = driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="quantity"]')
qty_input.clear()
qty_input.send_keys(buyingQuantity)

time.sleep(1)

while True:
    try:
        price_input = driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="price"]')
        price_input.clear()
        price_input.send_keys(preOpenPrice)
        buy_button = driver.find_element(By.XPATH, "//button[@type='submit' and text()='BUY']")
        buy_button.click()
    except Exception as e1:
        print(e1)
        buy_time = datetime.now(ktm)
        print(f"hopefully bought at {buy_time}")
        break

# OPEN SESSION

target_ktm = now_ktm.replace(hour=10, minute=59, second=59, microsecond=0)
target_est = target_ktm.astimezone(est)

while True:
    if datetime.now(est) >= target_est:
        print("It is time to place orders")
        print(datetime.now(ktm))
        break
    time.sleep(1)

driver.get(OrderEntry_URL)

time.sleep(5)

buy_toggle = driver.find_element(By.CSS_SELECTOR, "div.xtoggler-control label:nth-child(3)")
buy_toggle.click()

symbol_input = driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="symbol"]')
symbol_input.clear()
symbol_input.send_keys(Stock_Symbol)
time.sleep(1)
symbol_input.send_keys(Keys.ENTER)
time.sleep(3)

# try:
#     # Wait up to 10 seconds for the element to be present in the DOM
#     price_element = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.XPATH, "//label[normalize-space()='Open']/following-sibling::b"))
#     )
#     open_price = price_element.text
#     buyingPrice = str(math.floor(float(open_price) * 1.10 * 10) / 10)
#     print("Open=", open_price)
#     print("Buy=", buyingPrice)
#
# except Exception as e:
#     print("❌ Could not find the open price.")
#     print(e)

qty_input = driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="quantity"]')
qty_input.clear()
qty_input.send_keys(buyingQuantity)

time.sleep(1)

while True:
    try:
        price_input = driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="price"]')
        price_input.clear()
        price_input.send_keys(buyingPrice)
        buy_button = driver.find_element(By.XPATH, "//button[@type='submit' and text()='BUY']")
        buy_button.click()
    except Exception as e1:
        print(e1)
        buy_time = datetime.now(ktm)
        print(f"hopefully bought at {buy_time}")
        exit()

