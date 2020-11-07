import scrapy
import json

class PrenagenSpider(scrapy.Spider):
    name = 'prenagen'
    protocol = "https://"
    base_url = 'www.prenagen.com/id/'
    query_base_url = 'kumpulan-nama-bayi/cari?gender=semua&language=semua&page=1'
    start_urls = [protocol + base_url + query_base_url]

    def parse(self, response):
        results = response.css('div.babyname-item.row.font-color')
        for result in results:
            name = result.css('div.col-sm-2.babyname-name::text').extract_first()
            meaning = result.css('div.col-sm-5.babyname-arti::text').extract_first()
            gender = result.css('div.col-sm-2.babyname-gender > i').attrib['class']
            gender = gender.split(" ")[-1]
            gender = gender.split("-")[-1]
            if gender=="venus":
                gender = "PEREMPUAN"
            else:
                gender= "LAKI-LAKI"
            lang = result.css('div.col-sm-2.babyname-bahasa::text').extract_first()
            source = response.url
            
            yield {
                    'name': name,
                    'desc': meaning,
                    'gender': gender,
                    'language': lang,
                    'url': source
                }
                
        next_page_url = response.css("li.page-item > a[rel='next']::attr(href)").extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))