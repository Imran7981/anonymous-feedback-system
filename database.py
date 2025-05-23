import sqlite3
conn = sqlite3.connect('feedbacks.db')
conn.row_factory = sqlite3.Row
from datetime import datetime
from textblob import TextBlob

def init_db():
    conn = sqlite3.connect('feedbacks.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS feedbacks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            feedback TEXT NOT NULL,
            media TEXT,
            timestamp TEXT,
            sentiment TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_feedback(username, feedback, media, timestamp):
    # Sentiment analysis using TextBlob
    blob = TextBlob(feedback)
    polarity = blob.sentiment.polarity
    if polarity > 0:
        sentiment = "positive"
    elif polarity < 0:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    conn = sqlite3.connect('feedbacks.db')
    c = conn.cursor()
    c.execute('INSERT INTO feedbacks (username, feedback, media, timestamp, sentiment) VALUES (?, ?, ?, ?, ?)',
              (username, feedback, media, timestamp, sentiment))
    conn.commit()
    conn.close()

def get_feedback_count():
    conn = sqlite3.connect('feedbacks.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM feedbacks")
    count = c.fetchone()[0]
    conn.close()
    return count

def get_all_feedbacks():
    conn = sqlite3.connect('feedbacks.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT username, feedback, media, timestamp, sentiment, id FROM feedbacks")
    rows = c.fetchall()
    conn.close()
    return rows