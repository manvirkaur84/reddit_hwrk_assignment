
# Reddit Homework Assignment

## 📝 Assignment Overview  
This project connects to the Reddit API using PRAW to collect, clean, and export social media posts from subreddits related to **education**, **autism**, and **teachers**.  
It’s designed to simulate a real-world data pipeline — where we securely load Reddit API credentials, fetch “hot” and search keyword-based posts, clean them, 
and save everything into a structured CSV file for later analysis.  

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

## ⚙️ 1. Mount Drive and set up Git
```python from google.colab import drive drive.mount('/content/drive')
 %cd /content/drive/MyDrive/assignment_folder 
 !git config --global user.name "Manvir Kaur" 
 !git config --global user.email "manvir99@icloud.com" ```

## 2. Create requirements.txt
praw
pandas
requests
python-dotenv
(Colab already has google.colab, so you don’t need to install it.)

## 3. Create reddit_api.env
Store your Reddit credentials in:
/content/drive/MyDrive/assignment_folder/reddit_api.env

Example:
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=your_user_agent

## 3. Script
The main file is reddit_code.py.
It does all three tasks:
  * Fetches “hot” posts from 3 subreddits (education, teachers, autism)
  * Searches posts by keyword (ex: "behaviors")
  * Cleans, deduplicates, and exports to reddit_data.csv

## 🚀 4. How to Run
In Colab:

python
Copy code
%cd /content/drive/MyDrive/assignment_folder
!pip install -r requirements.txt
!python reddit_code.py

You’ll see output like:
⬇️  r/education: collecting HOT (limit=50) ...
🔎  r/teachers: searching 'homework' (limit=25) ...
📁 Saved 150 rows to reddit_data.csv
🎉 Done.

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

