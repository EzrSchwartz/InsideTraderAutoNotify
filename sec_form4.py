import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

def get_latest_form4_data():
    # This is a placeholder function. In a real-world scenario, you would implement
    # logic to fetch the latest Form 4 filings from the SEC EDGAR database.
    # For demonstration purposes, we'll return some sample data.
    
    sample_data = [
        {
            'filing_date': '2024-10-11 21:52:05',
            'trade_date': '2024-10-09',
            'ticker': 'PEGY',
            'company_name': 'Pineapple Energy Inc.',
            'insider_name': 'Conroy Jeffrey J.',
            'title': '10%',
            'trade_type': 'P - Purchase',
            'price': 0.11,
            'quantity': 333921,
            'owned': 1860000,
            'delta_own': 22,
            'value': 36063
        },
        # Add more sample entries here
    ]
    
    return sample_data

def get_sec_form4_data(accession_number, cik):
    # This function remains the same as in the original code
    # ...

def parse_form4_xml(root):
    # This function remains the same as in the original code
    # ...
