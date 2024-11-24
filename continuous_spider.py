import time
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.signalmanager import dispatcher
from scrapy import signals
import smtplib
from threading import Thread
import subprocess

def sendMessage(to_phone, msg):
    message = msg + " is a money glitch?!?!?!"
    gmail_user = "ppehackathon@gmail.com" 
    gmail_app_password = "ytgxpkeabqkekofv" 
    sent_from = gmail_user 
    sent_to = [to_phone, to_phone] 
    sent_subject = "PPE Violation Alert" 
    email_text = """\nFrom: %s \nTo: %s \nSubject: %s %s """ % (sent_from, ", ".join(sent_to), sent_subject, message) 
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465) 
    server.ehlo() 
    server.login(gmail_user, gmail_app_password) 
    server.sendmail(sent_from, sent_to, email_text) 
    server.close()

def run_spider(wallet_address):
    spider_directory = "C:/Daniel Na/Meme Coin Scraper/main/main/spiders"

    command = ["scrapy", "crawl", "MemeCoin", "-a", f"start_url={wallet_address}"]
    print(command)

    subprocess.run(command, cwd=spider_directory)

#Given wallet address, check to see if the newest transaction matches the corresponding value in the map
# If different, return False. If same, return True
# Update the map if different
def same_address_transaction_map(wallet_address, address_transaction_map):
    file = open("C:/Daniel Na/Meme Coin Scraper/main/main/spiders/" + wallet_address + ".txt", "r+")
    transactions = file.readlines()
    file.close()
    latest_transaction = transactions[-1]
    if latest_transaction == address_transaction_map[wallet_address]:
        return True
    else:
        # map is not in sync with the file
        address_transaction_map[wallet_address] = latest_transaction
        return False





def run_spider_continuously(wallet_addresses, recipients):

    # stores text result
    

    name_number_map = {
        "Daniel" : "danielna722@gmail.com",
        "Matua" : "matp671@gmail.com",
        "Krish" : "krish.gopalani@gmail.com",
        "Owen" : "owenlchau0916@gmail.com"
    }

    address_transaction_map = {}

    for wallet_address in wallet_addresses:
        try:
            file = open("C:/Daniel Na/Meme Coin Scraper/main/main/spiders/" + wallet_address + ".txt", "r+")
            transactions = file.readlines()
            if len(transactions) > 0:
                address_transaction_map[wallet_address] = transactions[-1]
            else:
                address_transaction_map[wallet_address] = None
            file.close()
        except:
            file = open("C:/Daniel Na/Meme Coin Scraper/main/main/spiders/" + wallet_address + ".txt", "w+")
            address_transaction_map[wallet_address] = None
            file.close()
        

    while True:
        try:
            for wallet_address in wallet_addresses:
                thread = Thread(target = run_spider, args=(wallet_address,))
                thread.start()
                thread.join()
                time.sleep(5)  # Adjust delay between spider runs if needed
                if not same_address_transaction_map(wallet_address, address_transaction_map):
                    for r in recipients:
                        sendMessage(name_number_map[r], wallet_address)

                
                
            
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    wallet_addresses = input("Enter wallet address(es)-separate with space if needed: ").split(" ")
    recipients = input("Enter recipients (Daniel, Matua, Owen, Krish): ").split()
    run_spider_continuously(wallet_addresses, recipients)
