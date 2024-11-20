
import time
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.signalmanager import dispatcher
from main.main.spiders.meme_coin_spider import MemeCoinSpider 
from scrapy import signals
import smtplib

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

def run_spider_continuously(wallet_address, recipients):
    process = CrawlerProcess(get_project_settings())  # Load Scrapy settings

    # stores text result
    

    name_number_map = {
        "Daniel" : "danielna722@gmail.com",
        "Matua" : "matp671@gmail.com",
        "Krish" : "krish.gopalani@gmail.com",
        "Owen" : "owenlchau0916@gmail.com"
    }


    def handle_item(item, response, spider):
        spider_results.append(item["text"])
        print(f"Extracted text: {item['text']}")  # Print the `text` variable

    # Connects the signal handler to Scrapy's item_scraped signal
    dispatcher.connect(handle_item, signal=signals.item_scraped)

    while True:
        try:
            print("Starting the Scrapy spider...")
            spider_results = []
            spider_results.clear()  # Clear results before the next run
            process.crawl(MemeCoinSpider)
            process.start(stop_after_crawl=True)  # Block until the spider finishes
            print("Spider finished. Results:")
            print(spider_results) 
            for r in recipients:
                sendMessage(name_number_map[r], "This works")
            break
            time.sleep(30)  # Adjust delay between spider runs if needed
            
        except KeyboardInterrupt:
            process.stop()
            break

if __name__ == "__main__":
    wallet_address = input("Enter wallet address(es)-separate with space if needed: ")
    recipients = input("Enter recipients (Daniel, Matua, Owen, Krish): ").split()
    run_spider_continuously(wallet_address, recipients)
