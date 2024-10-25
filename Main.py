
import os
import time
import requests
import pandas as pd
from datetime import datetime
import pickle

def get_recent_form4_filings():
    url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&CIK=&type=4&company=&dateb=&owner=include&start=0&count=100&output=atom"
    
    headers = {
        "User-Agent": "Ezra Schwartz ezra.n.schwartz@gmail.com"
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        
        from xml.etree import ElementTree as ET
        root = ET.fromstring(content)
        
        filings = []
        for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
            form_type = entry.find("{http://www.w3.org/2005/Atom}category").attrib['term']
            if form_type == "4":  # Only look for Form 4
                filing = {
                    'Title': entry.find("{http://www.w3.org/2005/Atom}title").text,
                    'Filing Date': entry.find("{http://www.w3.org/2005/Atom}updated").text,
                    'Link': entry.find("{http://www.w3.org/2005/Atom}link").attrib['href']
                }
                filings.append(filing)
        df = pd.DataFrame(filings)
        return df
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None

def load_sent_filings(file_name="sent_filings.pkl"):
    if os.path.exists(file_name):
        with open(file_name, 'rb') as f:
            return pickle.load(f)
    return pd.DataFrame()

def save_sent_filings(df, file_name="sent_filings.pkl"):
    with open(file_name, 'wb') as f:
        pickle.dump(df, f)

def get_new_filings():
    recent_filings = get_recent_form4_filings()
    sent_filings = load_sent_filings()

    if sent_filings.empty:
        return recent_filings

    new_filings = recent_filings[~recent_filings['Link'].isin(sent_filings['Link'])]

    return new_filings

def send_email(filings_df):
    df_string = filings_df.to_string()

    return requests.post(
        "https://api.mailgun.net/v3/sandbox55e96ef46e2a4db4bc76f56c750f6215.mailgun.org/messages",
        auth=("api", "c34419cfef8bf7082bf96d4ce9d4b2a6-784975b6-b954c6e4"), 
        data={
            "from": "Insider Filings <mailgun@sandbox55e96ef46e2a4db4bc76f56c750f6215.mailgun.org>", 
            "to": ["exoticjoe841@gmail.com"], 
            "subject": "NEW INSIDER BUYS!!!!!$$$",
            "text": f'INSIDER BUYS\n\n{df_string}'
        }
    )

def schedule_emails():
    while True:
        now = datetime.now()
        if now.hour >= 9 and now.hour < 17:
            new_filings = get_new_filings()

            if not new_filings.empty:
                response = send_email(new_filings)

                if response.status_code == 200:
                    print("Email sent successfully!")
                    save_sent_filings(new_filings)
                else:
                    print(f"Failed to send email: {response.status_code}, {response.text}")
            else:
                print("No new filings to report.")
        else:
            print("Outside business hours. Will resume at 9 AM.")

        time.sleep(600)

schedule_emails()


# def test_run():
#     new_filings = get_new_filings()

#     if not new_filings.empty:
#         response = send_email(new_filings)

#         if response.status_code == 200:
#             print("Test email sent successfully!")
#             save_sent_filings(new_filings)
#         else:
#             print(f"Failed to send email: {response.status_code}, {response.text}")
#     else:
#         print("No new filings to report in the test run.")

# test_run()