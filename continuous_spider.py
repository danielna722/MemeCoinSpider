import time
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.signalmanager import dispatcher
from scrapy import signals
import smtplib
from threading import Thread
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


SPIDERS_DIRECTORY = "C:/Daniel Na/Meme Coin Scraper/main/main/spiders"

def sendMessage(to_phone, msg):
    message = msg + " is a money glitch?!?!?!"
    gmail_user = "ppehackathon@gmail.com" 
    gmail_app_password = "ytgxpkeabqkekofv" 
    sent_from = gmail_user 
    sent_to = [to_phone, to_phone] 
    sent_subject = "BUY ALERT" 
    email_text = """\nFrom: %s \nTo: %s \nSubject: %s %s """ % (sent_from, ", ".join(sent_to), sent_subject, message) 
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465) 
    server.ehlo() 
    server.login(gmail_user, gmail_app_password) 
    server.sendmail(sent_from, sent_to, email_text) 
    server.close()

def run_spider(wallet_address):
    command = ["scrapy", "crawl", "MemeCoin", "-a", f"start_url={wallet_address}", "-L", "ERROR"]
    process = subprocess.Popen(command, cwd=SPIDERS_DIRECTORY)
    process.wait()
    print("Done with run_spider")

#Given wallet address, check to see if the newest transaction matches the corresponding value in the map
# If different, return False. If same, return True
# Update the map if different
def same_address_transaction_map(wallet_address, address_transaction_map):
    file = open(SPIDERS_DIRECTORY + "/addresses/" + wallet_address + ".txt", "r+")
    transactions = file.readlines()
    file.close()
    
    latest_transaction = transactions[-1]
    print("LATEST TRANSACTION: ",  latest_transaction, " \nThe Transaction in the map: ", address_transaction_map[wallet_address])
    time.sleep(5)
    if address_transaction_map[wallet_address] is not None:
        if latest_transaction[0:10] == address_transaction_map[wallet_address][0:10]:
            print("The map is up to date (the transaction in the file is equal to map)")
            return True
        else:
            print("The map is NOT up to date (the transaction in the file is NOT equal to map)")
            address_transaction_map[wallet_address] = latest_transaction
            return False
    else:
        # map is not in sync with the file
        print("The map is NOT up to date (the transaction in the file is NOT equal to map)")
        address_transaction_map[wallet_address] = latest_transaction
        return False

def is_transaction_buy(transaction_signature, wallet_address):
    url = "https://explorer.solana.com/tx/" + transaction_signature
    driver = webdriver.Chrome()
    driver.get(url)
    text = ""

    try:
        # Wait for the element to load and have text
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[3]/div[7]/div[2]/table/tbody/tr[2]/td[2]/div[1]/span[2]/a'))
        )
        # Fetch and print the text
        text = element.text
        if not text:
            text = driver.execute_script("return arguments[0].textContent;", element)
        print(f"From Address: {text}")
    except Exception as e:
        print(f"Error: {e}")
        # Delete the transaction that threw error
        
    driver.quit()

    return text == wallet_address

def get_wallet_address_list():
    wallet_addresses = []
    file = open("wallet_addresses.txt", "r")
    for line in file:
        wallet_addresses.append(line.strip())
    return wallet_addresses

def run_spider_continuously(recipients):

    # Define which wallet addresses I want to follow
    

    wallet_addresses = get_wallet_address_list()
    

    name_number_map = {
        "Daniel" : "danielna722@gmail.com",
        "Matua" : "matp671@gmail.com",
        "Krish" : "krish.gopalani@gmail.com",
        "Owen" : "owenlchau0916@gmail.com"
    }

    address_transaction_map = {}

    # For each wallet address, check if a corresponding file containing its transaction history exists
    # If so, value in the map is set to the most recent
    # If not, value is set to None
    for wallet_address in wallet_addresses:
        try:
            file = open(SPIDERS_DIRECTORY+ "/addresses/" + wallet_address + ".txt", "r+")
            transactions = file.readlines()
            if len(transactions) > 0:
                address_transaction_map[wallet_address] = transactions[-1]
            else:
                address_transaction_map[wallet_address] = None
            file.close()
        except:
            file = open(SPIDERS_DIRECTORY+ "/addresses/" + wallet_address + ".txt", "w+")
            address_transaction_map[wallet_address] = None
            file.close()
        

    while True:
        try:
            wallet_addresses = get_wallet_address_list()
            for wallet_address in wallet_addresses:
                if wallet_address not in address_transaction_map.keys():
                    file = open(SPIDERS_DIRECTORY+ "/addresses/" + wallet_address + ".txt", "w+")
                    address_transaction_map[wallet_address] = None
                    file.close()

                run_spider(wallet_address)
                if not same_address_transaction_map(wallet_address, address_transaction_map):
                    transaction_signature = address_transaction_map[wallet_address]
                    if is_transaction_buy(transaction_signature, wallet_address):
                        print("About to send messages: ")
                        text_message = "Wallet Address: " + wallet_address + "\nTransaction Signature: " + transaction_signature
                        for r in recipients:
                            sendMessage(name_number_map[r], text_message)
                time.sleep(5)        
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    # wallet_addresses = input("Enter wallet address(es)-separate with space if needed: ").split(" ")
    recipients = input("Enter recipients (Daniel, Matua, Owen, Krish): ").split()
    run_spider_continuously(recipients)