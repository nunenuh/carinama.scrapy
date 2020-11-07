import scrapy
import json

class MaknaaSpider(scrapy.Spider):
    name = 'makna'
    protocol = "https://"
    base_url = 'www.maknaa.com/arti-nama'
    
    def build_url(self):
        letter = 'abcdefghijklmnopqrstuvwxyz'
        # letter = 'ab'
        urls = []
        for let in letter:
            url = self.protocol + self.base_url + '?start=' + let + '&page=1'
            urls.append(url)
        return urls
    
    def start_requests(self):
        for url in self.build_url():
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        is_exist = response.css('table.striped.bordered.translations-table')
        is_exist = len(is_exist)>0
        
        if is_exist:
            results = response.css('table.striped.bordered.translations-table > tbody > tr')
            for tr_result in results:
                td_result = tr_result.css('td ::text').extract()
                td_data = []
                for text in td_result:
                    text = text.strip()
                    if len(text)>0:
                        td_data.append(text)
                yield {
                    'name': td_data[1],
                    'description': td_data[2],
                    'gender': td_data[3],
                    'language': td_data[4], 
                    'source': response.url
                }
                
            
            page_num = response.url.split('&')[-1]
            page_num = page_num.split('=')[-1]
            page_num = str(int(page_num) + 1)
            page_num = f'page={page_num}'
            next_page_url = response.url.split('&')[0] + '&' + page_num
            yield scrapy.Request(response.urljoin(next_page_url))
            
                
                
                
            # next_page_url = response.css("li.page-item > a[rel='next']::attr(href)").extract_first()
            # if next_page_url is not None:
            #     yield scrapy.Request(response.urljoin(next_page_url))


                