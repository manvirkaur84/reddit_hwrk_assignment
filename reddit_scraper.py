

from typing import List, Dict, Any
import os
import pandas as pd
import praw
from dotenv import dotenv_values


# Define the path to your .env file in Google Drive
# IMPORTANT: Update this path to the actual location of your reddit_api.env file in your Google Drive
env_file_path = '/content/drive/MyDrive/assignment_folder/reddit_api.env'

# Load environment variables from reddit_api.env file if it exists
if os.path.exists(env_file_path):
    config = dotenv_values(env_file_path)
    print(f"✅ Environment variables loaded from {env_file_path}!")
else:
    config = {}
    print(f"❌ Error: '{env_file_path}' not found. Environment variables not loaded.")
    print("Please ensure the 'reddit_api.env' file is in the specified Google Drive path.")

# Authenticate with Reddit using environment variables
reddit = praw.Reddit(
  client_id="cK1a0rTKjVUp7RSVKyX9Ug",
  client_secret="MvS-_Ms9GN2TIheI8i6VFafDIlO88A",
  user_agent="My Test App v1.0 by u/Fit-Offer-8414" # A unique description
)

print("✅ Reddit API authenticated successfully!")
print(f"Connected as: {reddit.user.me()}")


FIELDNAMES = [
    "title",
    "score",
    "upvote_ratio",
    "num_comments",
    "author",
    "subreddit",
    "url",
    "permalink",
    "created_utc",
    "is_self",
    "selftext",
    "flair",
    "domain",
    "search_query",
]

def _to_int(x):
    try:
        return int(x)
    except Exception:
        return None

def _row_from_post(post, subreddit_name: str, search_query: str | None) -> Dict[str, Any]:
    author = post.author.name if post.author else None
    text = post.selftext if isinstance(post.selftext, str) else None
    if text and len(text) > 500:
        text = text[:500] + "..."
    return {
        "title": getattr(post, "title", None),
        "score": getattr(post, "score", None),
        "upvote_ratio": getattr(post, "upvote_ratio", None),
        "num_comments": getattr(post, "num_comments", None),
        "author": author,
        "subreddit": subreddit_name,
        "url": getattr(post, "url", None),
        "permalink": ("https://reddit.com" + getattr(post, "permalink","")) if getattr(post,"permalink",None) else None,
        "created_utc": _to_int(getattr(post, "created_utc", None)),
        "is_self": getattr(post, "is_self", None),
        "selftext": text,
        "flair": getattr(post, "link_flair_text", None),
        "domain": getattr(post, "domain", None),
        "search_query": search_query if search_query else None,
    }

def fetch_hot_posts(subs, limit=50) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for sub in subs:
        print(f"⬇️  r/{sub}: collecting HOT (limit={limit}) ...")
        for post in reddit.subreddit(sub).hot(limit=limit):
            rows.append(_row_from_post(post, sub, search_query=None))
    return rows

def export_posts_to_csv(rows, out_path="reddit_data.csv"):
    if not rows:
        print("⚠️ No rows to export.")
        return
    df = pd.DataFrame(rows)
    df = df[[c for c in FIELDNAMES if c in df.columns]]
    df = df.drop_duplicates(subset="permalink", keep="first")
    df.to_csv(out_path, index=False)
    print(f"📁 Saved {len(df)} rows to {out_path}")

if __name__ == "__main__":
    SUBS = ["education", "teachers", "college"]
    posts = fetch_hot_posts(SUBS, limit=50)
    export_posts_to_csv(posts, out_path="/content/drive/MyDrive/assignment_folder/reddit_data.csv")
    print("🎉 Done.")
