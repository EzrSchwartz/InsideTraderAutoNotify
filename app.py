from flask import Flask, render_template
from sec_form4 import get_latest_form4_data
from apscheduler.schedulers.background import BackgroundScheduler
import sqlite3

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = sqlite3.connect('form4_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS form4_entries
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  filing_date TEXT,
                  trade_date TEXT,
                  ticker TEXT,
                  company_name TEXT,
                  insider_name TEXT,
                  title TEXT,
                  trade_type TEXT,
                  price REAL,
                  quantity INTEGER,
                  owned INTEGER,
                  delta_own REAL,
                  value REAL)''')
    conn.commit()
    conn.close()

init_db()

# Function to update the database with new Form 4 entries
def update_form4_data():
    new_entries = get_latest_form4_data()
    conn = sqlite3.connect('form4_data.db')
    c = conn.cursor()
    for entry in new_entries:
        c.execute('''INSERT INTO form4_entries
                     (filing_date, trade_date, ticker, company_name, insider_name,
                      title, trade_type, price, quantity, owned, delta_own, value)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (entry['filing_date'], entry['trade_date'], entry['ticker'],
                   entry['company_name'], entry['insider_name'], entry['title'],
                   entry['trade_type'], entry['price'], entry['quantity'],
                   entry['owned'], entry['delta_own'], entry['value']))
    conn.commit()
    conn.close()

# Schedule the update function to run every hour
scheduler = BackgroundScheduler()
scheduler.add_job(func=update_form4_data, trigger="interval", hours=1)
scheduler.start()

@app.route('/')
def index():
    conn = sqlite3.connect('form4_data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM form4_entries ORDER BY filing_date DESC LIMIT 100')
    entries = c.fetchall()
    conn.close()
    return render_template('index.html', entries=entries)

if __name__ == '__main__':
    app.run(debug=True)
