from pandas.core import frame
from selenium import webdriver
from selenium.webdriver.common.keys import Keys # Give us access to things like Enter key & escape key so that we can type in the search bar and then hit enter and be able to see all the search results
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import*
from decouple import config
import time
import datetime
import pandas as pd
import re

PATH = "C:\Program Files (x86)\chromedriver.exe"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--disable-infobars")
prefs = {"profile.default_content_setting_values.notifications" : 1}
chrome_options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(PATH, options=chrome_options)

def user_login():
    '''
    LOGIN BUTTON: _3Wg53T10KuuPmyWOMWsY2F -> class
    USERNAME FIELD: loginUsername -> id , username -> name
    PASSWORD FIELD: loginPassword -> id , password -> name
    '''

    loginBtn = driver.find_element_by_link_text('Log In')
    loginBtn.click()

    # Switch to iframe as the login form is within iframe tag
    frame = driver.find_element_by_xpath('//iframe[contains(@class, "_25r3t_lrPF3M6zD2YkWvZU")]')
    driver.switch_to.frame(frame)

    # Enter username
    usernameField = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginUsername"]')))
    usernameField.send_keys(config('MYUSERNAME', cast=str))

    # Enter password
    passwordField = driver.find_element_by_name('password')
    passwordField.send_keys(config('PASSWORD', cast=str))

    # Click the login button
    driver.find_element_by_xpath("//button[contains(text(), 'Log In')]").click()

    time.sleep(11)

    # Switch back to the parent frame which is "contents"
    driver.switch_to.default_content()

def collect_subData(number, postlinkaddress, post_lst_details):
    # sourcery no-metrics

    print('{}. PROCESSING -> {}'.format(number, postlinkaddress))

    # Opens a new tab
    driver.execute_script("window.open();")

    # Switch to the newly opened tab
    driver.switch_to.window(driver.window_handles[1])

    # Navigate to new URL in new tab
    driver.get(postlinkaddress)

    time.sleep(6)

    # Switch to original tab
    driver.switch_to.window(driver.window_handles[0])

    # Close original tab
    driver.close()

    # Switch back to newly opened tab, which is now in position 0
    driver.switch_to.window(driver.window_handles[0])

    # Scrape user profile name
    userProfileName = driver.find_element_by_xpath('//a[contains(@class, "_2tbHP6ZydRpjI44J3syuqC") and contains(@class, "_23wugcdiaj44hdfugIAlnX") and contains(@class, "oQctV4n0yUb0uiHDdGnmE")]').text
    
    # Scrape user profile link
    userProfileLink = driver.find_element_by_xpath('//a[contains(@class, "_2tbHP6ZydRpjI44J3syuqC") and contains(@class, "_23wugcdiaj44hdfugIAlnX") and contains(@class, "oQctV4n0yUb0uiHDdGnmE")]').get_attribute('href')
    
    # Scrape upvotes
    upvotes = driver.find_element_by_xpath('//div[contains(@class, "_1rZYMD_4xY3gRcSS3p8ODO") and contains(@class, "_3a2ZHWaih05DgAOtvu6cIo")]').text
    
    # Scrape title
    title = driver.find_element_by_xpath('//h1[contains(@class, "_eYtD2XCVieq6emjKBH3m")]').text

    # Scrape date
    days = driver.find_element_by_xpath('//a[@class="_3jOxDPIQ0KaOWpzvSQo-1s" and @data-click-id="timestamp"]').text
    day = filter(str.isdigit, days)
    day = "".join(day)
    day = int(float(day))
    if 'day' in days:
        date = str(datetime.date.today() - datetime.timedelta(day))
    else:
        date = str(datetime.date.today())
    
    # Scrape number of comments
    num_com = "".join(filter(str.isdigit, driver.find_element_by_xpath('//span[contains(@class, "FHCV02u6Cp2zYL0fhQPsO")]').text))

    # Scrape post's contents
    count = 0
    post_content = None
    while post_content == None and count < 3:
        try:
            if count == 0:
                # Scrap image
                try:
                    post_content = driver.find_element_by_xpath('//img[contains(@class, "_2_tDEnGMLxpM6uOa2kaDB3") and contains(@class, "ImageBox-image")]').get_attribute('src')
                except NoSuchElementException:
                    try:
                        post_content = driver.find_element_by_xpath('//div[contains(@class, "_3Oa0THmZ3f5iZXAQ0hBJ0k")]/a').get_attribute('href')
                    except NoSuchElementException:
                        pass
            elif count == 1:
                # Scrap video
                    try:
                        post_content = driver.find_element_by_xpath('//video[@class="_1EQJpXY7ExS04odI1YBBlj" and contains(@preload, "auto")]/source').get_attribute('src')
                    except NoSuchElementException:
                        try:
                            post_content = driver.find_element_by_xpath('//iframe[contains(@class, "media-element") and contains(@class, "_3K6DCjWs2dQ93YYZDOHjib")]').get_attribute('src')
                        except NoSuchElementException:
                            pass
            else:
                # Scrap text
                innerHTML = driver.find_element_by_xpath('//div[contains(@class, "_3xX726aBn29LDbsDtzr_6E") and contains(@class, "_1Ap4F5maDtT1E1YuCiaO0r") and contains(@class, "D3IL3FD0RFy_mkKLPwL4")]/div[contains(@class, "_292iotee39Lmt0MkQZ2hPV") and contains(@class, "RichTextJSON-root")]').get_attribute('innerHTML')
                pattern = re.compile(r"(?=>([^<]+))", re.DOTALL)
                matches = pattern.finditer(innerHTML)
                post_content = [" ".join(match.group(1).split()) for match in matches]
        except NoSuchElementException:
            time.sleep(2)
        count += 1
    
    # Scrape post's comments
    comments = driver.find_elements_by_xpath(
        '//div[starts-with(@class, "P8SGAKMtRxNwlmLz1zdJu") and contains(@class, "Comment") and contains(@class, "t1_") and contains(@class, "HZ-cv9q391bm8s7qT54B3") and contains(@class, "_3jJ0c2FXVItDFjup-54-X2")]/div[contains(@class, "_3tw__eCCe7j-epNCKGXUKk") and contains(@class, "_3jJ0c2FXVItDFjup-54-X2")]/div[@class="_3cjCphgls6DH-irkVaA0GM"]/div[contains(@class, "_292iotee39Lmt0MkQZ2hPV") and contains(@class, "RichTextJSON-root")]'
    ) # or contains(@class, "_1z5rdmX8TDr6mqwNv7A70U")

    # Pattern that used to find texts between all the tags
    pattern = re.compile(r"(?=>([^<]+))", re.DOTALL)

    comment_list = [] # comment_list stores all comments of the post (Wrap up the tuple below)
    for comment in comments:
        each_ppl_com = comment.get_attribute('innerHTML')
        matches = pattern.finditer(each_ppl_com)
        each_ppl_com_content = tuple(" ".join(match.group(1).split()) for match in matches) # Each tuple represents a comment commented by a user
        comment_list.append(each_ppl_com_content) # This list stores all the comments from each tuple(Means each comment)

    post_info = {
        'Post_Link': postlinkaddress,
        'Username': userProfileName,
        'UserProfileLink': userProfileLink,
        'Upvotes': upvotes,
        'Title': title,
        'Date': date,
        'Num_Comments': num_com,
        'Post_Content': post_content,
        'Comments': comment_list
    }
    post_lst_details.append(post_info)
    print("    Done\n")
    time.sleep(5)


HTTPS = "https://www.reddit.com/"
SUBREDDIT = ["r/badminton", "r/UncleRoger"]

# Sorting type, set to 'hot', 'new', 'rising' or 'top'
SORT = "top"

# Sorting timespan, set to 'hour', 'day', 'week', 'month', 'year', or 'all'.
# Only has effect for the 'top' sorting types
TIME = "month"

# Get all posts
for sub in SUBREDDIT:
    # Iterate through every subreddit listed
    link = HTTPS + sub + "/" + SORT + "/?t=" + TIME # e.g. https://www.reddit.com/r/badminton/top/?t=month
    print(f'\nLink of the web page: {link}')

    if sub == SUBREDDIT[0]:
        driver.get(link)

        # Login
        user_login()

        # Scroll 3 times for more posts shown on the screen
        n_scrolls = 3
        while True:
            n_scrolls -= 1
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(7)
            if n_scrolls < 0:
                break

        '''
        Each post's class in <a></a> tags -> SQnoC3ObvgnGjWt90zD9Z _2INHSNB8V5eaWp4P0rY_mE
        posts = grabbed_posts.find_elements_by_xpath('//div[starts-with(@id, "t3_n")]')
        '''
        post_lst_details = []
        number = 1
        hrefs = driver.find_elements_by_xpath('//a[contains(@class, "SQnoC3ObvgnGjWt90zD9Z") and contains(@class, "_2INHSNB8V5eaWp4P0rY_mE")]')
        postLinks = [postLink.get_attribute('href') for postLink in hrefs]
        for postlinkaddress in postLinks:
            collect_subData(number, postlinkaddress, post_lst_details)
            number+=1

        # Save into a dataframe
        df = pd.DataFrame(post_lst_details)

        # Save the dataframe into a CSV file
        df.to_csv(sub.replace('r/', '') + '.csv', header=True, index=False)
 
        print(f'Total: {len(hrefs)} posts have crawled')
    
    else:
        # Opens a new tab
        driver.execute_script("window.open();")

        # Switch to the newly opened tab
        driver.switch_to.window(driver.window_handles[1])

        # Navigate to new URL in new tab
        driver.get(link)

        time.sleep(6)

        # Scroll 3 times for more posts shown on the screen
        n_scrolls = 3
        while True:
            n_scrolls -= 1
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(7)
            if n_scrolls < 0:
                break
        
        # Each post's class in <a></a> tags -> SQnoC3ObvgnGjWt90zD9Z _2INHSNB8V5eaWp4P0rY_mE
        post_lst_details = []
        number = 1
        hrefs = driver.find_elements_by_xpath('//a[contains(@class, "SQnoC3ObvgnGjWt90zD9Z") and contains(@class, "_2INHSNB8V5eaWp4P0rY_mE")]')
        postLinks = [postLink.get_attribute('href') for postLink in hrefs]
        for postlinkaddress in postLinks:
            collect_subData(number, postlinkaddress, post_lst_details)
            number+=1

        # Save into a dataframe
        df = pd.DataFrame(post_lst_details)

        # Save the dataframe into a CSV file
        df.to_csv(sub.replace('r/', '') + '.csv', header=True, index=False)
 
        print(f'Total: {len(hrefs)} posts have crawled')