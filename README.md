
# Reddit Homework Assignment

## 📝 Assignment Overview  
This project connects to the Reddit API using PRAW to collect, clean, and export social media posts from subreddits related to **education**, **autism**, and **teachers**.  
It’s designed to simulate a real-world data pipeline — where we securely load Reddit API credentials, fetch “hot” and keyword-based posts, clean them, and save everything into a structured CSV file for later analysis.  

---

## ⚙️ Before You Start  
Make sure you have:
- Internet access  
- A **Google Colab** account (the notebook runs there)  
- **Python 3.8+** (Colab’s default version works fine)  
- Your own Reddit API credentials:
  - Client ID  
  - Client Secret  
  - User Agent  

---

## 📦 1. Install Requirements  
Run this first in Google Colab:  
```python !pip install -r requirements.txt```

This installs all the required libraries listed in requirements.txt:

praw → connects to Reddit’s API
pandas → data cleaning and CSV export
python-dotenv → loads credentials securely from an env file
requests → handles Reddit’s API calls internally

Note: You won’t see google.colab listed in requirements.txt.
That’s because Colab already includes it by default, so there’s no need to install it with pip.
You can still import it in the notebook (from google.colab import drive) and it will work. It just doesn’t need to be installed like a normal package.

---

## 🔐 2. Create Your reddit_api.env File

We don’t hard-code secrets directly into the notebook.
Instead, we create a small env file that stores Reddit API credentials.

In a new Colab cell, run this command (and replace the placeholders with your info):

%%writefile /content/drive/MyDrive/assignment_folder/reddit_api.env
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here
REDDIT_USER_AGENT=your_user_agent_here


What’s inside:
REDDIT_CLIENT_ID → from your Reddit developer app
REDDIT_CLIENT_SECRET → secret key from Reddit
REDDIT_USER_AGENT → short name for your app, like: MyRedditApp/1.0 by u/yourUsername

This file should live in the same folder where you’re running the notebook so the code can read it.

---

### 💾 3. Mount Google Drive

Your reddit_api.env file and your final CSV both live in your Google Drive folder.
Run this cell at the top of the notebook:

from google.colab import drive
drive.mount('/content/drive')

Approve access. This lets the notebook read reddit_api.env and later write reddit_data.csv to Drive.

---

## 🚀 4. Execution

Now you’re ready to run the notebook: ManvirKaur_reddit_code.ipynb

Make sure you’re in the correct folder:

%cd /content/drive/MyDrive/assignment_folder

Run all cells in order.

The notebook will:
* Load Reddit credentials from reddit_api.env
* Connect to the Reddit API
* Pull “hot” posts from three subreddits:
    * education
    * autism
    * teachers
* Search posts by keyword (for example, “support”)
* Clean and deduplicate results
* Export everything to a CSV file called reddit_data.csv
* While it runs, you’ll see messages like:
    * Collected 50 posts from r/education
    * Done search for 'support' in r/autism
    * Saved 150 rows to reddit_data.csv

---

## 📊 5. `reddit_data.csv`

After the notebook runs, it creates a file named **`reddit_data.csv`** in your Google Drive folder.  
This file contains all collected and cleaned Reddit posts.  

Below is a description of each column included in the CSV:

| Column | Description | Data Type |
|---------|-------------|------------|
| `title` | The full title of the post. | String |
| `score` | The net score (upvotes - downvotes). | Integer |
| `upvote_ratio` | Ratio of upvotes to total votes (proxy for quality / approval). | Float |
| `num_comments` | Total number of comments. | Integer |
| `author` | Username of the post’s author. If deleted, may be `None`. | String |
| `subreddit` | Subreddit where the post came from. | String |
| `url` | External link URL (if it’s a link post). | String |
| `permalink` | Permanent Reddit link to the post itself. | String |
| `created_utc` | Unix timestamp of when the post was created (UTC). | Integer / String |
| `is_self` | `True` if text-only/self post, `False` if it links out. | Boolean |
| `selftext` | The body text of the post (truncated to 500 characters so rows don’t explode). | String |
| `flair` | Flair / tag / category label on the post. | String |
| `domain` | Domain of the linked content. | String |
| `search_query` | The keyword used to find this post during search. | String |

If any columns are missing data (for example, deleted authors or empty selftexts), the notebook fills them with `None` or `NaN.` 

