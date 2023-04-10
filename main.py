import praw
import sqlite3
import pandas as pd
import json
import xml.etree.ElementTree as ET

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

    def export_to_excel(self):
        # Retrieve the data from the database
        data = pd.read_sql_query("SELECT * FROM subreddit", self.conn)
        
        # Save the data to an Excel file
        data.to_excel("subreddit_data.xlsx", index=False)

    def export_to_json(self):
        # Retrieve the data from the database
        self.c.execute("SELECT * FROM subreddit")
        data = self.c.fetchall()
        
        # Convert the data to a list of dictionaries
        result = []
        for row in data:
            result.append({
                "id": row[0],
                "title": row[1],
                "author": row[2],
                "score": row[3],
                "num_comments": row[4]
            })
        
        # Save the data to a JSON file
        with open("subreddit_data.json", "w") as f:
            json.dump(result, f)

    def export_to_xml(self):
        # Retrieve the data from the database
        self.c.execute("SELECT * FROM subreddit")
        data = self.c.fetchall()
        
        # Create the XML tree and root element
        root = ET.Element("subreddit")
        
        # Add the data as child elements to the root element
        for row in data:
            post = ET.SubElement(root, "post")
            ET.SubElement(post, "id").text = row[0]
            ET.SubElement(post, "title").text = row[1]
            ET.SubElement(post, "author").text = row[2]
            ET.SubElement(post, "score").text = str(row[3])
            ET.SubElement(post, "num_comments").text = str(row[4])
        
        # Save the XML tree to a file
        tree = ET.ElementTree(root)
        tree.write("subreddit_data.xml", encoding="UTF-8", xml_declaration=True)

    def close_database(self):
        # Close the database connection
        self.conn.close()

if __name__ == "__main__":
    scraper = SubredditScraper("learnpython") 