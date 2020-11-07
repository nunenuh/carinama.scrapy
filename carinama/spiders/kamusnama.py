import scrapy


class KamusNamaLakiSpider(scrapy.Spider):
    name = 'kamus_nama_laki'
    protocol = 'https://'
    base_url = 'kamusnama.com/'
    start_urls = [
        protocol + base_url + 'cari-nama-laki-laki?page=1',
    ]
    
    search_detail = ['rangkaian-nama-depan',]
    
    
    def build_start_detail_url(self, name):
        sub = self.search_detail[0]
        url = self.protocol + self.base_url + sub + '/' + name + '?page=1'
        return url
        
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        results = response.css('div.search-result-item')
        
        for result in results:
            name = result.css('h4 > a::text').extract_first().strip()
            gender = result.css('p > strong::text').extract_first().upper()

            data =  {
                'base_name': name,
                'gender': gender,
            }
            
            detail_url = self.build_start_detail_url(name)
            yield scrapy.Request(url=detail_url, callback=self.detail_parse, cb_kwargs=dict(parse_data=data))
        
        next_page_url = response.css("li.page-item > a[rel='next']::attr(href)").extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))
            
            
    def detail_parse(self, response, parse_data):
        results = response.css('li.sc_list_item.icon-right-open-big *::text')
        for result in results:
            parse_data['name'] = result.extract()
            parse_data['source'] = response.url
            yield parse_data
            
            
class KamusNamaPerempuanSpider(scrapy.Spider):
    name = 'kamus_nama_perempuan'
    protocol = 'https://'
    base_url = 'kamusnama.com/'
    start_urls = [
        protocol + base_url + 'cari-nama-perempuan?page=1'
    ]
    
    search_detail = ['rangkaian-nama-depan',]
    
    
    def build_start_detail_url(self, name):
        sub = self.search_detail[0]
        url = self.protocol + self.base_url + sub + '/' + name + '?page=1'
        return url
        
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        results = response.css('div.search-result-item')
        
        for result in results:
            name = result.css('h4 > a::text').extract_first().strip()
            gender = result.css('p > strong::text').extract_first().upper()

            data =  {
                'base_name': name,
                'gender': gender,
            }
            
            detail_url = self.build_start_detail_url(name)
            yield scrapy.Request(url=detail_url, callback=self.detail_parse, cb_kwargs=dict(parse_data=data))
        
        next_page_url = response.css("li.page-item > a[rel='next']::attr(href)").extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))
            
            
    def detail_parse(self, response, parse_data):
        results = response.css('li.sc_list_item.icon-right-open-big *::text')
        for result in results:
            parse_data['name'] = result.extract()
            parse_data['source'] = response.url
            yield parse_data

# class KamusNamaSpider(scrapy.Spider):
#     name = 'kamusnama_v1'
#     protocol = 'https://'
#     base_url = 'kamusnama.com/'
#     start_urls = [
#         protocol + base_url + 'cari-nama-laki-laki?page=1',
#         protocol + base_url + 'cari-nama-perempuan?page=1'
#     ]
        
#     def start_requests(self):
#         for url in self.start_urls:
#             yield scrapy.Request(url=url, callback=self.parse)
    
#     def parse(self, response):
#         results = response.css('div.search-result-item')
        
#         for result in results:
#             name = result.css('h4 > a::text').extract_first()
#             desc = result.css('p *::text').extract()
#             desc = " ".join(desc)
            
#             gender = result.css('p > strong::text').extract_first().upper()
#             lang = None
#             source = response.url
#             # print(description)
            
#             yield {
#                 'name': name,
#                 'desc': desc,
#                 'gender': gender,
#                 'language': lang,
#                 'url': source
#             }
        
#         next_page_url = response.css("li.page-item > a[rel='next']::attr(href)").extract_first()
#         if next_page_url is not None:
#             yield scrapy.Request(response.urljoin(next_page_url))
            
    
