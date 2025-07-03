import os
import unittest
import configparser
import sys


from API import finish_cleanup_state

from appium import webdriver
from selenium.webdriver import DesiredCapabilities

status = 'failed'

# Properties sent from SeeTest Cloud that we can use in Script
uid = os.getenv("deviceID")
operating_system = os.getenv("deviceOS")

# Pre-defining the iPhone capabilities as script is designed for iOS only for now
capabilities = DesiredCapabilities.IPHONE

# config.properties reader
config = configparser.ConfigParser()
config.read('config.properties')


class SampleTestCase(unittest.TestCase):
    print('SampleTestCase started')
    # Android currently not supported. If Device is Android, exit the script before it starts
    if operating_system == 'Android':
        print('Python Script (logger) - operating_system is android, not yet supported: %s' % operating_system)
        # Marking the test as passed, otherwise cloud device will remain in 'Cleanup Failed' mode
        status = 'passed'
        # Marking the test as passed, and finishes up the cleanup session
        finish_cleanup_state(uid, status)
        # Exiting script
        sys.exit()

    # if iOS - Do nothing, continue test as usual
    elif operating_system == 'iOS':
        print('Python Script (logger) - operating_system is ios, continuing: %s' % operating_system)
        
        try:
            capabilities['testName'] = 'Webhook cleanup'
            capabilities['accessKey'] = '%s' % config.get('seetest_authorization', 'access_key_admin')
            capabilities['udid'] = '%s' % uid
            capabilities['platformName'] = 'iOS'
            capabilities['autoDismissAlerts'] = True  # This helps to handle unexpected native pop-ups
            capabilities['releaseDevice'] = False
            capabilities['generateReport'] = False  # Disable report creation, will help to reduce execution time
            capabilities['bundleId'] = 'com.apple.Preferences'
        except Exception as e:
            print('SampleTestCase error occurred: %s' % e)


    def setUp(self):
        print('SampleTestCase setUp started')
        self.driver = webdriver.Remote(desired_capabilities=capabilities,
                                       command_executor=config.get('seetest_urls', 'cloud_url') + config.get(
                                           'seetest_urls', 'wd_hub'))

    def test(self):
       print('SampleTestCase test started')


    def tearDown(self):
        # Marking the test as passed, otherwise cloud device will remain in 'Cleanup Failed' mode
        status = 'passed'
        # Ending the device reservation session
        self.driver.quit()
        # Marking the test as passed, and finishes up the cleanup session
        finish_cleanup_state(uid, status)

# Helps run the test using unittest framework
runner = unittest.TextTestRunner()
suite = unittest.TestLoader().loadTestsFromTestCase(SampleTestCase)
