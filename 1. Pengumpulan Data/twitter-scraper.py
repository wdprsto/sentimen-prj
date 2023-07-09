# Necessary libraries are imported
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from time import sleep
import csv

# Twitter username, password, search keyword, and number of tweets to be scraped are assigned to variables
search_query = "prj lang:in since:2023-04-01 until:2023-07-31"
tweet_count = 9000
file_csv = "Crawl9k.csv"
twitter_user = "username"
twitter_pass = "password"

# Selenium webdriver is started and the login process is performed on Twitter
executable_path = "chromedriver.exe"
options = webdriver.ChromeOptions()
options.set_capability('unhandledPromptBehavior', 'dismiss')

driver = webdriver.Chrome(executable_path=executable_path, options=options)

wait = WebDriverWait(driver, 10)

def login():
    driver.get("https://twitter.com/login")

    username_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text']")))
    username_input.send_keys(twitter_user)
    next_button = driver.find_element(By.CSS_SELECTOR, "div[data-testid='apple_sign_in_button'] + div + div + div[role='button']")
    next_button.click()

    password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
    password_input.send_keys(twitter_pass)
    login_button = driver.find_element(By.CSS_SELECTOR, "div[data-testid='LoginForm_Footer_Container'] div[role='button']")
    login_button.click()

    # Navigates to Twitter search page and starts scraping tweets
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[data-testid='sidebarColumn']")))
    
# do login as user
login()

driver.get(f"https://twitter.com/search?q={search_query}&src=typed_query&f=live")
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "article[data-testid='tweet']")))

data = []
saved_data = []

with open(file_csv, "a", newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['username','full_text','lang','reply_count','quote_count','favorite_count','view_count','created_at','tweet_url'])

def get_tweets():
    html = driver.page_source
    beautifulSoupText = BeautifulSoup(html, "html.parser")
    for tag in beautifulSoupText.findAll('article'):
        try:
            tweet_url = tag.select('a[href*="/status/"]')[0]['href']
            tweet_id = tweet_url.split("/")[3]

            if tweet_id in saved_data:
                continue

            username = tag.find('a', string=lambda text: text and '@' in text).text
            created_at = tag.find('time', attrs={})['datetime'] #akses nilai dari atribut datetime
            full_text = tag.find('div', attrs={'data-testid':'tweetText'}).text
            reply_count = tag.find('span', attrs={'data-testid':'app-text-transition-container'}).text
            quote_count = tag.findAll('span', attrs={'data-testid':'app-text-transition-container'})[1].text
            favorite_count = tag.findAll('span', attrs={'data-testid':'app-text-transition-container'})[2].text
            view_count = tag.findAll('span', attrs={'data-testid':'app-text-transition-container'})[3].text
            lang = tag.find('div', attrs={'data-testid':'tweetText'})['lang']

            data.append((username,full_text,lang,reply_count,quote_count,favorite_count,view_count,created_at,tweet_url));
            saved_data.append(tweet_id)
        except: 
            continue

    with open(file_csv, "a", newline='', encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        # The for loop
        for username,full_text,lang,reply_count,quote_count,favorite_count,view_count,created_at,tweet_url in data:
            writer.writerow([username,full_text,lang,reply_count,quote_count,favorite_count,view_count,created_at,tweet_url])

        # if tweet_text is not None and search_query in tweet_text.text.lower():
        #     data.append(tweet_text.text.strip())

# Scrolls down the page to load more tweets
last_height = driver.execute_script("return document.body.scrollHeight")
while len(saved_data) < tweet_count:
    sleep(3)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[role='progressbar']")))
    wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div[role='progressbar']")))

    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

    sleep(3)
    get_tweets(); data = [] #kosongin lagi datanyaa
    print(len(saved_data))
