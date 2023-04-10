import praw
import sqlite3

class SubredditScraper:
    def __init__(self, subreddit_name):
        # Initialize PRAW with your Reddit API credentials
        self.reddit = praw.Reddit(
            client_id="your_client_id",
            client_secret="your_client_secret",
            username="your_username",
            password="your_password",
            user_agent="your_user_agent",
        )
        
        self.subreddit_name = subreddit_name
        
        # Connect to a SQLite database
        self.conn = sqlite3.connect("subreddit_data.db")
        self.c = self.conn.cursor()
        
        # Create a table to store the subreddit data
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS subreddit (
                id TEXT PRIMARY KEY,
                title TEXT,
                author TEXT,
                score INTEGER,
                num_comments INTEGER
            )
        """)

    def fetch_posts(self, limit=10):
        # Fetch the top posts from the subreddit
        subreddit = self.reddit.subreddit(self.subreddit_name)
        return subreddit.top(limit=limit)

    def save_to_database(self, posts):
        # Insert the post data into the database
        for post in posts:
            data = (post.id, post.title, post.author.name, post.score, post.num_comments)
            self.c.execute("INSERT OR IGNORE INTO subreddit VALUES (?, ?, ?, ?, ?)", data)
        
        # Commit the changes to the database
        self.conn.commit()

    def close_database(self):
        # Close the database connection
        self.conn.close()

if __name__ == "__main__":
    scraper = SubredditScraper("learnpython")  # Change this to the name of the subreddit you want to fetch data from
    posts = scraper.fetch_posts(limit=10)
    scraper.save_to_database(posts)
    scraper.close_database()