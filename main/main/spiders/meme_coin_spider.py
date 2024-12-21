from scrapy import Spider
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapy.selector import Selector
import time

DIRECTORY = "C:/Daniel Na/Meme Coin Scraper/main/main/spiders/addresses/"

class MemeCoinSpider(Spider):
    name = 'MemeCoin'

    def __init__(self, *args, **kwargs):
        super(MemeCoinSpider, self).__init__(*args, **kwargs)

        self.wallet_address = [kwargs.get('start_url')]
        self.url = "https://explorer.solana.com/address/" + self.wallet_address[0]
        self.file_name = DIRECTORY + self.wallet_address[0]

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
        time.sleep(10)  # Allow JavaScript to load
        sel = Selector(text=self.driver.page_source)
        temp = sel.xpath('//div[@class="d-flex align-items-center "]/span[@class="font-monospace"]/a/@href').get()
        temp = temp[4:]
        if temp is None:
            print("Couldnt get the data in time :( Im a naughty spider")
            return
        self.driver.quit()
        print(temp)
        
        file1 = open(self.file_name + ".txt", 'r+')
        transactions = file1.readlines()
        if len(transactions) == 0:
            file1.close()
            file1 = open(self.file_name + ".txt", 'a', encoding="utf-8")
            file1.write(temp + "\n")
        elif temp != transactions[-1].strip():
            file1.close()
            file1 = open(self.file_name + ".txt", 'a', encoding="utf-8")
            file1.write(temp + "\n")
        file1.close()

        yield {
            "text": temp
        }