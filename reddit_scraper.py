

!pip install -r requirements.txt

from typing import List, Dict, Any
import os
import pandas as pd
import praw
from dotenv import load_dotenv

# load secrets from reddit.env
load_dotenv("/content/drive/MyDrive/assignment_folder/reddit_api.env")

client_id = os.getenv("REDDIT_CLIENT_ID")
client_secret = os.getenv("REDDIT_CLIENT_SECRET")
user_agent = os.getenv("REDDIT_USER_AGENT")

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent,
)

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
