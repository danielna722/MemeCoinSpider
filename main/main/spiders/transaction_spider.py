from scrapy import Spider
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapy.selector import Selector
import time

class TransactionSpider(Spider):
    name = 'TransactionSpider'


    def __init__(self, *args, **kwargs):
        super(TransactionSpider, self).__init__(*args, **kwargs)

        self.transaction_signature = [kwargs.get('signature')]
        self.buyer_address = [kwargs.get('buyer_address')]
        self.url = "https://explorer.solana.com/tx/" + self.transaction_signature[0]

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)

        # address = input("Enter the wallet address")
        # self.url = "https://explorer.solana.com/address/" + address

    def start_requests(self):
        url = self.url
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.driver.get(response.url)
        time.sleep(5)  # Allow JavaScript to load
        sel = Selector(text=self.driver.page_source)
        print("Going to grab the data from TransactionSpider")
        temp = sel.xpath('//td[@class="text-lg-end"]/div[@class="d-flex d-lg-none align-items-center"]/span[@class="font-monospace"]/a/text()').get()
        print("Grabbed it: ", temp)
        self.driver.quit()

        answer = temp == self.buyer_address[0]
        
        file1 = open("isTransactionBuy.txt", 'w+', encoding="utf-8")
        if answer:
            file1.write("True")
        else:
            file1.write("False")
        file1.close()

        yield {
            "text": temp
        }

