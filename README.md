# RedditScraper
Hi there 👋 This Reddit Scrapper is my first Selenium Python project that I have built.

# Functions
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

# How to use
1. User is required to create a `.env` file within this project folder after downloading or cloning
2. Then, just type these 2 lines of code inside the `.env` file you have just created
  1. MYUSERNAME=**Your_Reddit_Account_Username**
  2. PASSWORD=**Your_Reddit_Account_Password**

3. Specify the subreddits you want to scrape at **line 169** in `scrap_reddit.py`. The list variable `SUBREDDIT` will store all subreddits specified by user
4. Specify the sorting type you want at **line 172** in `scrap_reddit.py`. The variable `SORT` will store the type specified by user
   * Sorting types are set to _**hot**_, _**new**_, _**rising**_ or _**top**_
5. Specify the timespan you want **line 176** in `scrap_reddit.py` but timespan is **only applicable** for the _**top** sorting type_
   * Sorting timespan are set to _**hour**_, _**day**_, _**week**_, _**month**_, _**year**_, or _**all**_.
7. **Finnaly**, double check the code at **line 181**. Make sure that the link formed can be opened in browser and then run `scrap_reddit.py`

# Example
* In this project, I specified _UncleRoger_ and _badminton_ at **line 169** in `scrap_reddit.py`. E.g. **`SUBREDDIT = ['r/UncleRoger', 'r/badminton']`**.
* Sorting type that I used was **`SORT = 'top'`** at **line 172** in `scrap_reddit.py`.
* Since I use _**top**_ as my _**sorting type**_, so I can specify timespan for this program at **line 176**. E.g. **`TIME = 'month'`**. Otherwise, **no need to specify timespan**
* Finally, I try to open up the link that will formed at **line 181** in browser to check whether it can be browsed. If yes, run the program. Otherwise, double check the link.
