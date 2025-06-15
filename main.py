
from bs4 import BeautifulSoup
import requests
import time
import random
from dotenv import load_dotenv
import os
import smtplib
import pyfiglet

# Configuration
URL = "https://www.amazon.in/dp/B0CS6FPH6P"
target = 60000
load_dotenv()

# Email setup
from_email = "elayabarathiedison@gmail.com"
to_email = "sampgoogsamp@gmail.com"
password = os.getenv("GOOGLE_PASSWORD")

# Advanced headers
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
]

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Cache-Control": "max-age=0",
    "TE": "trailers"
}

print(pyfiglet.figlet_format("\n-- Amazon Price Tracker --\n\n"))

def get_price():
    try:
        # Initialize session
        session = requests.Session()
        headers["User-Agent"] = random.choice(user_agents)
        
        # Add random delay
        time.sleep(random.uniform(2, 5))
        
        # Make request
        response = session.get(URL, headers=headers, timeout=10)
        response.raise_for_status()

        # Check for blocking
        if any(x in response.text for x in ["api-services-support", "captcha", "robot check"]):
            raise Exception("Amazon blocking detected")

        # Parse response
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Try multiple price selectors
        selectors = [
            "span.a-price-whole",
            "span.a-offscreen",
            "span.priceToPay",
            "span.a-color-price"
        ]
        
        for selector in selectors:
            price_element = soup.select_one(selector)
            if price_element:
                price_text = price_element.get_text()
                price_text = price_text.replace('₹', '').replace(',', '').strip()
                if price_text:
                    return int(float(price_text))
        
        raise Exception("Price element not found")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def send_email(price):
    subject = "🚨 Price Alert!"
    body = f"⚠️ Time to grab the deal! Tic Tic Tic... ⏰\nCurrent Price: ₹{price}\nTarget Price: ₹{target}\nLink: {URL}"
    message = f"Subject: {subject}\n\n{body}"
    
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, message.encode('utf-8'))
        print("✅ Email sent successfully!")

# Main execution
if __name__ == "__main__":
    price = get_price()
    
    if price is not None:
        print(f"✅ Current Price: ₹{price}")
        print(f"✅ Target Price: ₹{target}")
        
        if price < target:
            print("🚨 Price dropped below target!")
            send_email(price)
        else:
            print(f"Price still above target (₹{target}) 🥲")
    else:
        print("Failed to retrieve price")