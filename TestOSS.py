import os
import unittest
import configparser
import sys
from API import finish_cleanup_state
from appium import webdriver
from appium.options.ios import XCUITestOptions  # Added for modern Appium

config = configparser.ConfigParser()
config.read('config.properties')
#uid = config.get('variables', 'deviceID')
#operating_system = config.get('variables', 'os')
uid = os.getenv("deviceID")
operating_system = os.getenv("deviceOS")

class SampleTestCase(unittest.TestCase):

    def setUp(self):
        # 1. Handle the Android logic inside setUp or before the suite runs
        if operating_system == 'Android':
            finish_cleanup_state(uid, 'passed')
            self.skipTest("Android cleanup complete, skipping iOS UI test.")

        # 2. Modern iOS Options setup
        options = XCUITestOptions()
        options.platform_name = 'iOS'
        options.udid = uid
        options.bundle_id = 'com.apple.Preferences'
        options.auto_dismiss_alerts = True
        
        # 3. Add SeeTest specific capabilities
        options.load_capabilities({
            'testName': 'Webhook cleanup',
            'accessKey': config.get('seetest_authorization', 'access_key_cleanup'),
            'releaseDevice': False,
            'appiumVersion': '3.0.1'
        })
        
        url = config.get('seetest_urls', 'cloud_url') + config.get('seetest_urls', 'wd_hub')
        
        # 4. Use 'options' instead of 'desired_capabilities'
        self.driver = webdriver.Remote(command_executor=url, options=options)

    def test(self):
        # Your test logic here
        pass

    def tearDown(self):
        # Ensure driver exists before trying to quit
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()
        finish_cleanup_state(uid, 'passed')

if __name__ == '__main__':
    # Ensure the env is active when running this: python3 TestOSS.py
    runner = unittest.TextTestRunner()
    suite = unittest.TestLoader().loadTestsFromTestCase(SampleTestCase)
    runner.run(suite)