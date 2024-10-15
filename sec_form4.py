from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from datetime import datetime
import smtplib
import pandas as pd
import numpy as np


nametext = []
TickerText = []
TotalQuantity = []
pricetext = []


# Get the current date

# Calculate the check-in date (2 days after the current date)


# Setup
driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))



# Navigate to the website
driver.get('http://openinsider.com/')


links = []
# Wait for the JavaScript to load
driver.implicitly_wait(2)



# Find the elements with the class 'boxprice'
prices = driver.find_elements(By.CSS_SELECTOR, '.background:#f1fff1')
print(prices)

# names = driver.find_elements(By.CSS_SELECTOR, '.title')
# names.pop(0)

print(len(names))


for price in prices:
    pricetext.append(price.text)

for name in names:
    nametext.append(name.text)


for name in nametext:
    links.append(f'https://www.satorealestate.com/vacation-rentals/rental/{name.replace(" ","-")}')

for link in links:
    print(link)
d = {'Names': nametext,'Prices': pricetext, 'Link': links}


df = pd.DataFrame(columns=[ 'Date', 'Ticker', 'Quantity','Investor','Title','Value','Plane Price'])

df['Date'] 
# Print the text of each element
print(df)



# Close the driver
driver.quit()
driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))





driver.implicitly_wait(2)

flightselector = driver.find_elements(By.CSS_SELECTOR, '.flight-selector')
for outer_div in flightselector:
    print((outer_div.find_element(By.CSS_SELECTOR, '.route-label')).text)
    if(  "Depart:" == (outer_div.find_element(By.CSS_SELECTOR, '.route-label').text)):
        departingflights = outer_div.find_elements(By.CSS_SELECTOR, '.btn-fare-wheel')



        for flight in departingflights:
            if (str(checkout_date).replace("-","/") == flight.find_element(By.CSS_SELECTOR, '.id').text):
                if((flight.find_element(By.CSS_SELECTOR, '.fare-price').text).find("Sold")):
                    departingflightstext.append(flight.find_element(By.CSS_SELECTOR, '.fare-price').text)

        print(departingflightstext)
df["Plane Price"] = min(departingflights)

df = df.assign(industry='yyy')

# Set up the SMTP server and log into your account
server = smtplib.SMTP('smtp.office365.com', 587)
server.starttls()
server.login("fishingtripfinder@outlook.com", "PWD!23")


sendingemail = "fishingtripfinder@outlook.com"

recievingemails = ["ezra.n.schwartz@gmail.com"]

dfstring = df.to_string(index=False)

# Create the message
msg = """\
Subject: Hello, here are the bookings avalible


"""+dfstring



server.sendmail(sendingemail, recievingemails, msg)

# Close the connection to the server
server.quit()