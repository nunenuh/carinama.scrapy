import scrapy
import json

class PopMamaSpider(scrapy.Spider):
    name = 'popmama'
    protocol = "https://"
    base_url = 'www.popmama.com/baby-name/'
    
    def build_url(self):
        letter = 'abcdefghijklmnopqrstuvwxyz'
        male_url, female_url = [], []
        for let in letter:
            male = self.protocol + self.base_url + 'male/' + let
            female = self.protocol + self.base_url + 'female/' + let
            male_url.append(male)
            female_url.append(female)
            
        all_url = male_url + female_url
        return all_url
    
    def start_requests(self):
        for url in self.build_url():
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        url = response.url
        results = response.css('div.result-content > div.row > ol')
        print(url)
        for result in results:
            for res in result.css('div > li'):
                name = res.css('a::text').extract_first().strip()
                gender = url.split('/')[-2]
                
                yield {
                    "name": name,
                    "gender": gender,
                    "source": url
                }