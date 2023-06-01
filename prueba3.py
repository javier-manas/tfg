#gologin

# Import Dependencies
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

# Specify the path to the chromedriver executable
PATH = "C:/Users/Javie/.gologin/browser/orbita-browser-112/chrome.exe"

# Create a new instance of the Chrome web driver
driver = webdriver.Chrome(executable_path=None)

# Open the Twitter login page
driver.get("https://twitter.com/login")

# Wait for the page to load before continuing
sleep(3)

# Find the username input field using its XPATH and enter a username
username = driver.find_element(By.XPATH,"//input[@name='text']")
username.send_keys("@gmail.com")

# Find the 'Next' button using its XPATH and click it to move to the password field
next_button = driver.find_element(By.XPATH,"//span[contains(text(),'Next')]")
next_button.click()

# Wait for the next page to load before continuing
sleep(3)

# Find the password input field using its XPATH and enter a password
password = driver.find_element(By.XPATH,"//input[@name='password']")
password.send_keys('')

# Find the 'Log in' button using its XPATH and click it to log in
log_in = driver.find_element(By.XPATH,"//span[contains(text(),'Log in')]")
log_in.click()

subject="Lionel Messi"
# Wait for the page to load before continuing
sleep(3)

# Find the search box input field using its XPATH and enter the subject to search for
search_box = driver.find_element(By.XPATH,"//input[@data-testid='SearchBox_Search_Input']")
search_box.send_keys(subject)

# Simulate pressing the ENTER key to submit the search
search_box.send_keys(Keys.ENTER)

# Wait for the page to load before continuing
sleep(3)

# Find the 'People' filter button using its XPATH and click it to filter search results
people = driver.find_element(By.XPATH,"//span[contains(text(),'People')]")
people.click()

# Wait for the page to load before continuing
sleep(3)

# Find the first profile on the search results page using its XPATH and click it to visit the profile page
profile = driver.find_element(By.XPATH,'//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/section/div/div/div[1]/div/div/div/div/div[2]/div/div[1]/div/div[1]/a/div/div[1]/span/span[1]')
profile.click()

# initialize empty lists to store scraped data
UserTags=[]
TimeStamps=[]
Tweets=[]
Replys=[]
reTweets=[]
Likes=[]

# find all tweet articles on the page
articles = driver.find_elements(By.XPATH,"//article[@data-testid='tweet']")

# loop over the articles to extract data from each tweet
while True:
    for article in articles:
        # extract user handle
        UserTag = driver.find_element(By.XPATH,".//div[@data-testid='User-Name']").text
        UserTags.append(UserTag)

        # extract timestamp
        TimeStamp = driver.find_element(By.XPATH,".//time").get_attribute('datetime')
        TimeStamps.append(TimeStamp)

        # extract tweet text
        Tweet = driver.find_element(By.XPATH,".//div[@data-testid='tweetText']").text
        Tweets.append(Tweet)

        # extract number of replies
        Reply = driver.find_element(By.XPATH,".//div[@data-testid='reply']").text
        Replys.append(Reply)

        # extract number of retweets
        reTweet = driver.find_element(By.XPATH,".//div[@data-testid='retweet']").text
        reTweets.append(reTweet)

        # extract number of likes
        Like = driver.find_element(By.XPATH,".//div[@data-testid='like']").text
        Likes.append(Like)

        # scroll down to load more tweets
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
        sleep(3)

        # find all tweet articles again to check if there are more tweets to scrape
        articles = driver.find_elements(By.XPATH,"//article[@data-testid='tweet']")

        # remove duplicate tweets and check if enough unique tweets have been scraped
        Tweets2 = list(set(Tweets))
    if len(Tweets2) > 5:
        break # exit loop if enough unique tweets have been scraped


print("UserTags : "+UserTags[0])
print("TimeStamp : "+TimeStamps[0])
print("Tweet : "+Tweets[0])
print("Replys : "+Replys[0])
print("reTweets : "+reTweets[0])
print("Likes : "+Likes[0])