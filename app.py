from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import os
import re


class Fbclicker:

    counter = 0

    def __init__(self, email, password, group_name):
        self.email = email
        self.password = password
        self.group_name = group_name
        self.browser = None
        self.block_notification()

    def block_notification(self):
        ''' This functions block pop-up notifications on Chrome.'''
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        self.browser = webdriver.Chrome(options=chrome_options,
                                        executable_path="/path/to/chromedriver")

    def sign_in(self):
        ''' This function allows us to log into Facebook.com.'''
        self.browser.get('https://facebook.com')
        email_input = self.browser.find_element_by_name('email')
        password_input = self.browser.find_element_by_name('pass')
        email_input.send_keys(self.email)
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.ENTER)
        time.sleep(1)

    def scroll_page(self):
        ''' This function redirects us to group page and scrolls page to invite section. '''
        self.browser.get('https://facebook.com/groups/' + self.group_name)
        self.browser.execute_script('window.scrollTo(0,500)')

    def check_new_members(self):
        try:
            element = self.browser.find_element_by_class_name('_3ip6')
            num_of_members = re.findall('\d+', element.text)
            if int(num_of_members[0]) > 0:
                return True
            else:
                return False
        except NoSuchElementException as e:
            print('You have les than 30 new members this week.')

    def writte_post(self):
        if self.check_new_members() == True:
            buttons = self.browser.find_elements_by_css_selector('._42ft._4jy0._4jy3._517h._51sy.mls')
            [button.click() for button in buttons if button.text == 'Write Post']
            time.sleep(5)
            self.browser.execute_script('window.scrollTo(0,2000)')
            time.sleep(5)
            post_button = self.browser.find_elements_by_css_selector('._1mf7._4jy0._4jy3._4jy1._51sy.selected._42ft')
            post_button.click()

    def click_invite(self):
        ''' This function finds elements with 'INVITE' button and clicks on each. '''
        try:
            element = self.browser.find_element_by_xpath("//div[@class='_6a rfloat _ohf']")
            while element:
                Fbclicker.counter += 1
                element.click()
                time.sleep(2)
                element = self.browser.find_element_by_xpath("//div[@class='_6a rfloat _ohf']")
                time.sleep(2)
        except NoSuchElementException as e:
            print('You have no more people to invite. Try in 1 hour.')


    def close_browser(self):
        self.browser.close()

    def __exit__(self, exc_type, exc_value, traceback):
        self.closeBrowser()


def main():
    ''' The full process of inviting fans.'''
    fb_pass = os.environ.get('FB_PASS')
    fb_mail = os.environ.get('FB_@')

    a = Fbclicker('damiannklis@gmail.com'), str(fb_pass), '298296040793329')
    a.sign_in()
    a.scroll_page()
    a.writte_post()

    print("You've invited " + str(a.counter) + " people.")

    a.close_browser()

if __name__ == '__main__':
    main()