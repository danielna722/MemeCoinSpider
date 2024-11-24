from scrapy import Spider
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapy.selector import Selector
import time

class MemeCoinSpider(Spider):
    name = 'MemeCoin'

    def __init__(self, *args, **kwargs):
        super(MemeCoinSpider, self).__init__(*args, **kwargs)

        self.wallet_address = [kwargs.get('start_url')]
        self.url = "https://explorer.solana.com/address/" + self.wallet_address[0]
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
        temp = sel.xpath('//div[@class="d-flex align-items-center "]/span[@class="font-monospace"]/a/text()').get()
        self.driver.quit()
        
        file1 = open(self.wallet_address[0] + ".txt", 'r+')
        transactions = file1.readlines()
        if len(transactions) == 0:
            file1.close()
            file1 = open(self.wallet_address[0] + ".txt", 'a')
            file1.write("\n" + temp)
        elif temp != transactions[-1]:
            file1.close()
            file1 = open(self.wallet_address[0] + ".txt", 'a')
            file1.write("\n" + temp)
        file1.close()

        yield {
            "text": temp
        }