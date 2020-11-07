import scrapy



class KamusNamaSpider(scrapy.Spider):
    name = 'kamusnama_v1'
    protocol = 'https://'
    base_url = 'kamusnama.com/'
    start_urls = [
        protocol + base_url + 'cari-nama-laki-laki?page=1',
        protocol + base_url + 'cari-nama-perempuan?page=1'
    ]
        
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        results = response.css('div.search-result-item')
        
        for result in results:
            name = result.css('h4 > a::text').extract_first()
            desc = result.css('p *::text').extract()
            desc = " ".join(desc)
            
            gender = result.css('p > strong::text').extract_first().upper()
            lang = None
            source = response.url
            # print(description)
            
            yield {
                'name': name,
                'desc': desc,
                'gender': gender,
                'language': lang,
                'url': source
            }
        
        next_page_url = response.css("li.page-item > a[rel='next']::attr(href)").extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))
            
    

class KamusNamaSpider(scrapy.Spider):
    name = 'kamusnama_v2'
    protocol = 'https://'
    base_url = 'kamusnama.com/'
    start_urls = [
        protocol + base_url + 'cari-nama-laki-laki?page=1',
        protocol + base_url + 'cari-nama-perempuan?page=1'
    ]
    
    search_detail = [
        'rangkaian-nama-depan',
        'rangkaian-nama-tengah',
        'rangkaian-nama-belakang'
    ]
    
    temp = []
    
    def build_start_detail_url(self, name):
        urls = []
        sub_name = []
        for sub in self.search_detail:
            sn = '_'.join(sub.split('-')[1:])
            sub_name.append(sn)
            
            url = self.protocol + self.base_url + sub + '/' + name + '?page=1'
            urls.append(url)
        return urls, sub_name
        
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        results = response.css('div.search-result-item')
        
        for result in results:
            name = result.css('h4 > a::text').extract_first().strip()
            desc = result.css('p *::text').extract()
            desc = " ".join(desc)
            gender = result.css('p > strong::text').extract_first().upper()
            source = response.url
            # print(description)
            
            data =  {
                'base_name': name,
                'desc': None,
                'gender': gender,
                'language': None,
                'base_url': source
            }
            
            detail_url, sub_name = self.build_start_detail_url(name)
            for dl_url, sn in zip(detail_url, sub_name):
                yield scrapy.Request(url=dl_url, callback=self.detail_parse,
                                     cb_kwargs=dict(parse_data=data, sub_name=sn))
        
        next_page_url = response.css("li.page-item > a[rel='next']::attr(href)").extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))
            
            
    def detail_parse(self, response, parse_data, sub_name):
        results = response.css('li.sc_list_item.icon-right-open-big *::text')
        for result in results:
            parse_data['name'] = result.extract()
            parse_data['position'] = sub_name
            parse_data['detail_url'] = response.url
            yield parse_data
        
        next_page_url = response.css("li.page-item > a[rel='next']::attr(href)").extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url), callback=self.detail_parse, 
                                 cb_kwargs=dict(parse_data=parse_data, sub_name=sub_name))