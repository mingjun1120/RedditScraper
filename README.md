## RedditScraper
Hi there 👋 This Reddit Scrapper is my first Selenium Python project that I have built.

## Functions
**This scrapper can help you to scrape the post data as follow:**
1. title
2. upvotes
3. date
4. username
5. user profile link
6. post link
7. number of comments
8. post content
9. post comments

## Usage
* User is required to create a `.env` file within this project folder after downloading or cloning
* Then type these 2 lines of code within the `.env` file
  1. `MYUSERNAME=**_Your_Reddit_Account_Username_**`
  2. `PASSWORD=**_Your_Reddit_Account_Password_**`

* Specify the subreddits you want to scrape at **line 169** in `scrap_reddit.py`. The list variable `SUBREDDIT` will store all subreddits specified by user
* Specify the sorting type you want at **line 172** in `scrap_reddit.py`. The variable `SORT` will store the type specified by user
  1. Sorting typed are set to _**hot**_, _**new**_, _**rising**_ or _**top**_
* Specify the timespan you want **line 176** in `scrap_reddit.py` but timespan is **only applicable** for the _**top** sorting type_
* **Finnaly**, run `scrap_reddit.py`
