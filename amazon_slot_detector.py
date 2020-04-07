import os
import sys
import random
from twilio.rest import Client
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

###############################
# User specific info goes here 
###############################

AMAZON_EMAIL_ID='your email id'
AMAZON_PASSWORD=' your password '
FROM_NUMBER='+1425xxxxxxx'  ##Number generated through your Twilio account 
TO_NUMBER='+1562xxxxxxx'
# Download chrome webdriver as per your Chrome version from here: https://chromedriver.chromium.org/downloads
# Also, set TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN as system environment variables as per your Twilio credentials
DISABLE_COOKIE_LOGIN=True   #Let this be as is. Ping me if you want to know how to make it work with cookie login so you don't have to enter credentials 
###############################

DEFAULT_ERROR="Program ended abruptly. Please check."
browser=None
service_id="VUZHIFdob2xlIEZvb2Rz"  #default service id for WholeFoods

def sendMessage(slot_available=False, message="Test message"):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    message_client = client.messages.create(
                              body=message,
                              from_=FROM_NUMBER,
                              to=TO_NUMBER
                          )

    if slot_available==True and message != DEFAULT_ERROR:
        call_client = client.calls.create(
                            twiml='<Response><Say>You'+ message +'</Say></Response>',
                            from_=FROM_NUMBER,
                            to=TO_NUMBER
                        )

def check_availability(all_availabilities):
    try:
        available_bool=False
        for availability in all_availabilities:
            availability_innerHTML=availability.get_attribute('innerHTML').strip().lower()
            print(availability_innerHTML)
            if availability_innerHTML != "not available":
                available_bool=True
                sendMessage(slot_available=True,message="Slot available!!!")
                break;

        if available_bool==False:
            print("Slot DEFINITELY NOT available")
    except:
        sendMessage(slot_available=True,message="Exception reading slots. Slot POSSIBLY available")

def login(browser):
    login_email=browser.find_element_by_id('ap_email')
    login_email.send_keys(AMAZON_EMAIL_ID)
    sleep(2)
    browser.find_element_by_id('continue').click()
    sleep(2)
    browser.find_element_by_id('ap_password').send_keys(AMAZON_PASSWORD)
    sleep(6)
    browser.find_element_by_id('signInSubmit').click()


def try_cookie_login(mode="wf"):
    if DISABLE_COOKIE_LOGIN==True:
        return False
    print("Trying cookie login")
    global browser
    chrome_options=Options()
    chrome_options.add_argument("user-data-dir=C:\\Users\\temp\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
    try:
        browser=webdriver.Chrome(chrome_options=chrome_options)
        if mode=="af":
            print("Looking for slots on Amazon fresh...")
            browser.get("https://www.amazon.com/alm/storefront?almBrandId={}".format(service_id))
        else:
            print("Looking for slots on Whole foods...")
            browser.get("https://www.amazon.com/alm/storefront/ref=grocery_wholefoods?almBrandId={}".format(service_id))
        return True
    except:
        return False
        
def try_regular_login(mode="wf"):
    global browser
    browser=webdriver.Chrome()
    if mode=="af":
        print("Looking for slots on Amazon fresh...")
        browser.get("https://www.amazon.com/alm/storefront?almBrandId={}".format(service_id))
    else:
        print("Looking for slots on Whole foods...")
        browser.get("https://www.amazon.com/alm/storefront/ref=grocery_wholefoods?almBrandId={}".format(service_id))
    sleep(2)
    account_login_label=browser.find_element_by_id('nav-link-accountList')
    account_login_label.click()
    
    login(browser)
    
    verification_mode="otp"
    
    if verification_mode=="device":
        sleep(1)
        browser.find_element_by_css_selector("input[type='radio'][value='This verification mode shouldnt be required']").click()
        browser.find_element_by_id('continue').click()
    else:
        sleep(1)
        browser.find_element_by_css_selector("input[type='radio'][value='sms']").click()
        sleep(2)
        browser.find_element_by_id('continue').click()

        try:
            #waits for a minute for you to enter the OTP
            browser.find_element_by_name('code')
            print("You have 60 secs to enter OTP...")
            WebDriverWait(browser, 60).until(lambda browser: len(browser.find_element_by_name('code').get_attribute('value')) == 6)
            sleep(3)
            browser.find_element_by_css_selector("input[class='a-button-input']").submit()
        except:
            #sometimes if OTP is not working, you are asked to login instead
            login(browser)
    

def try_login(mode="wf"):
    if try_cookie_login(mode=mode)==False:
        print("cookie login failed...trying regular login")
        try_regular_login(mode=mode)
    browser.fullscreen_window()

#Default service is WholeFoods    
def main(mode="wf"):
    global service_id
    mode=mode.lower()
    if mode=="af":
        service_id="QW1hem9uIEZyZXNo"
    try_login(mode)
    wait_here=10
    print("Waiting for upto {} secs for UI elements to appear...".format(str(wait_here)))
    sleep(wait_here)
    try:
        print("Looking for a button to click ...")
        browser.find_element_by_class_name('nav-cart').click()
        #browser.find_element_by_class_name('ewc-button-input').submit()
        #Whole foods checkout
        #submit_button = WebDriverWait(browser, 25).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[class='ewc-button-input']")))
    except:     
        browser.find_element_by_id('nav-cart').click()
    
    sleep(3)
    try:
        browser.find_element_by_name("proceedToALMCheckout-{}".format(service_id)).click()  
        #browser.find_element_by_css_selector("input[class='a-button-input'][value='Proceed to checkout']").submit()
    except:
        browser.find_element_by_css_selector("input[class='a-button-input'][value='Proceed to checkout']").submit()
        
    sleep(4)
    browser.find_element_by_name('proceedToCheckout').click()
    if mode=="wf":
        #Whole foods will ask option for substitution
        sleep(2)
        #browser.find_element_by_css_selector("input[class='a-button-input']").submit()
        browser.find_element_by_xpath("//span[@class='a-button-inner']").click()
    refresh_intervals=[50,55,63,58,72,65]
    while True:
        check_availability(browser.find_elements_by_xpath("//div[@class='ufss-date-select-toggle-text-availability']"))
        refresh_interval=random.choice(refresh_intervals)
        print('Refreshing in {} secs...'.format(str(refresh_interval))) 
        sleep(refresh_interval)
        browser.refresh()
        sleep(5)


if __name__=="__main__":
    try:
        mode="wf"
        if len(sys.argv) == 1:
            print("No parameters supplied...Defaulting to WholeFoods...")
        else:
            mode=sys.argv[1]
            print("Supplied mode is {}".format(mode))
        main(mode)
    except:
        print("Something went wrong in the program. Please check")
        #You can uncomment below line if you want to be notified when the script fails
        #sendMessage(slot_available=True,message=DEFAULT_ERROR)
        raise