# Whole-foods-and-Amazon-Fresh-delivery-slot-detector

Currently this script works for Amazon Fresh and Amazon Whole Foods and has been tested on Windows. I anticipate the code to run on other platforms as well. You'll need to change some of the config settings specific to the platform (eg: setting environment variables)

## Behavior
The script logs you in using the supplied credentials and once it reaches the page showing availability of slots, it keeps refreshing the page at random few seconds. If it detects a slot, it sends a text message AND also makes a call to a phone number of your choice to notify.

## Instructions
 
### How to run?
The default mode is WholeFoods. If you want to  use Amazon Fresh, invoke the script with parameter “af”.

**WholeFoods**: python amazon_slot_detector.py

**Amazon Fresh**: python amazon_slot_detector.py af


**IMPORTANT caveat**: At one step during loging, it will ask for OTP…after you enter the OTP (within 60 secs) **DO NOT click on 'Continue' button** . The code will do it for you. (or else the code breaks. Heck I didn’t want to invest on optimization when I didn’t have food at home). 


### Prerequisites:

Install Python 3.x
 
pip install -U selenium

pip install twilio
 
Download chrome webdriver as per your Chrome version from here: https://chromedriver.chromium.org/downloads.
Provide the path of the folder containing the driver in the System PATH variable. 
 
Create a Twilio account. It would be great if you could use my referral link: www.twilio.com/referral/ZAVEPt
 
Set **TWILIO_ACCOUNT_SID** and **TWILIO_AUTH_TOKEN** as system environment variables as per your Twilio credentials (Seen on Twilio's dashboard)
 
Read the top part of the code to set required parameters

 
**Note**: It would be a good idea if you could add items to your cart beforehand so that upon notification you can quickly checkout items.
 

