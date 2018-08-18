from selenium import webdriver
import sys
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
import time, itertools

class FacebookBot(object):
    """
    Facebook bot using with framework of selenium
    """     
    SCROLL_PAUSE_TIME = 3
    PAGE_PAUSE_TIME = 3
    CLICK_PAUSE_TIME = 2

    def __init__(self, email=str(), password=str(), driver = webdriver.Chrome()):
        self.email = email
        self.password = password
        self.driver = driver

        self.driver.get("https://m.facebook.com")
        email_field = self.driver.find_element_by_id("m_login_email") 
        email_field.send_keys(self.email)
        password_field = self.driver.find_element_by_id("m_login_password")
        password_field.send_keys(self.password, Keys.RETURN)
        print("successfully logged as %s" %(self.email))
        time.sleep(self.PAGE_PAUSE_TIME)

        try:
            self.driver.find_element_by_xpath("//button[@type='submit' and @value='OK']")           
        except NoSuchElementException:
            print("failed to login")
            self.driver.quit()

        self.driver.get("https://m.facebook.com/login/save-device/cancel/?flow=interstitial_nux&nux_source=regular_login")      
        time.sleep(self.PAGE_PAUSE_TIME)       
         

    def _check_exists_by_xpath(self, xpath):
        try:
            self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True


    def add_friends(self):
        """
        bot send friend request 
        """

        self.driver.get("https://m.facebook.com/friends/center/requests/?mff_nav=1") #navigate to friends page
        time.sleep(self.PAGE_PAUSE_TIME)
        
        # Scroll down to bottom
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(self.SCROLL_PAUSE_TIME)
        
        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        count = 0
        while True:
            friend_names = self.driver.find_elements_by_xpath("//*[starts-with(@data-autoid, 'autoid')]/a[string-length(text()) > 0]")
            friend_request_buttons = self.driver.find_elements_by_xpath("//button[@type='submit' and @value='Добавить в друзья']")
        
            friends_dict = dict(zip(friend_names, friend_request_buttons)) #merge two lists into a dictionary
        
            for friend_name, friend_request in friends_dict.items():
                if friend_name.text == "":
                    continue
        
                if self._check_exists_by_xpath("//form[@class='_55-k']/button"): #if exists modal form
                    button = self.driver.find_element_by_xpath("//form[@class='_55-k']/button")
                    button.click() #close modal form

                # Friend requests overflow
                #if self._check_exists_by_xpath("//a[@href='/friends/center/requests/outgoing/' and @role='button']"): 
                #    break
                try:
                    count += 1       
                    print( "%d -- %s" %(count, friend_name.text) )    
                    friend_request.click()                
                except ElementNotVisibleException:
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(self.SCROLL_PAUSE_TIME)
                    break

                time.sleep(self.CLICK_PAUSE_TIME)
                
        
            # Scroll down to bottom
            #self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/15);")
            
            # Wait to load page
            #time.sleep(self.SCROLL_PAUSE_TIME)
        
            # Calculate new scroll height and compare with last scroll height
            #new_height = self.driver.execute_script("return document.body.scrollHeight")
            #if new_height == last_height:
            #    break
            #last_height = new_height


    def remove_friend_requests(self, amount = 1000):
        self.driver.get("https://m.facebook.com/friends/center/requests/outgoing/")
        time.sleep(self.PAGE_PAUSE_TIME)

        # Scroll down to bottom
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")       
        time.sleep(self.SCROLL_PAUSE_TIME)
        
        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        count = 0

        while count < amount:
            friend_requests = self.driver.find_elements_by_xpath("//button[@type='submit' and @value='Отменить']")

            for friend_request in friend_requests:
                if friend_request.text == "":
                    continue

                count += 1
                friend_request.click()
                print("%d removed request" %(count))

            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")                     
            time.sleep(self.SCROLL_PAUSE_TIME)
        
            # Calculate new scroll height and compare with last scroll height
            #new_height = self.driver.execute_script("return document.body.scrollHeight")
            #if new_height == last_height:
            #    break
            #last_height = new_height



            