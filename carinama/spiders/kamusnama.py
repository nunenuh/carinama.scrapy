import scrapy
import random

PROTOCOL = 'https'
DOMAIN = 'kamusnama.com'
SEARCH_URL = {
    'male': 'cari-nama-laki-laki',
    'female': 'cari-nama-perempuan',
    'front': 'rangkaian-nama-depan',
    'midle': 'rangkaian-nama-tengah',
    'last': 'rangkaian-nama-belakang'
}

def build_search_urls(abjad, gender, page_num):
    base_url = f'{PROTOCOL}://{DOMAIN}/{SEARCH_URL[gender]}'
    query = f'?cocok=nama%20depan&abjad={abjad}&page={page_num}'
    url = base_url + query
    return url


def build_search_rangkaian_urls(position, name, pnum=None):
    base_url = f'{PROTOCOL}://{DOMAIN}/{SEARCH_URL[position]}/'
    query = f'{name}'
    if pnum==None:
        query += f'?page=1'
    else:
        query += f'?page={pnum}' 
    url = base_url + query
    return url

def build_start_urls(gender):
    urls = []
    abjad = 'abcdefghijklmnopqrstuvwxyz'
    # abjad = abjad[22:]
    for letter in abjad:
        url = build_search_urls(letter, gender, "1")
        urls.append(url)
    return urls


class KamusNamaSpider(scrapy.Spider):
    name = 'kamus_nama'
    start_urls =  build_start_urls('male') + build_start_urls('female')
    name_position = 'front'
    abjad_min_page = 10
    rangkaian_min_page = 21
    
    
    
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def get_curr_gender_abjad_page(self, response):
        url_split = response.url.split('?')
        url_domain, url_query = url_split[0], url_split[-1]
          
        url_query = url_query.split('&')     
        abjad = url_query[1].split('=')[-1]
        pnum = url_query[-1].split('=')[-1]
        
        url_domain = url_domain.split('/')[-1]
        gender = url_domain.split('-')[-1]
        if gender=='laki':
            gender = "male"
        elif  gender=='perempuan':
            gender = "female"
        else:
            gender = "male"
        return gender, abjad, pnum
    
    def get_curr_name_rangkaian_page(self, response):
        url_split = response.url.split('/')
        url_query = url_split[-1]
        name = url_query.split("?")[0]
        return name
    
    def build_sampled_abjad_search_urls(self, response):
        results = response.css('nav.nav-pagination-wrapper.text-center > nav > ul.pagination *.page-link::text')
        results = results.extract()
        results = results[1:-1] #remove prev and next
        
        pages = []
        if results is not None and len(results) > 0:
            last_page_num = int(results[-1])
            pages = [i+1 for i in range(last_page_num)]
            if last_page_num > self.abjad_min_page:
                pages = random.sample(pages, k=self.abjad_min_page)
                
        curr_gender, curr_abjad, curr_page_num = self.get_curr_gender_abjad_page(response)

        urls = []
        for pnum in pages:
            url = build_search_urls(curr_abjad, curr_gender, str(pnum))
            urls.append(url)
            
        return urls
    
    def build_sampled_rangkaian_pagination_urls(self, response):
        urls = [response.url]
        results = response.css('nav.nav-pagination-wrapper.text-center > nav > ul.pagination *.page-link::text')
        if results is not None:
            results = results.extract()
            results = results[1:-1] #remove prev and next
            
            pages = []
            if results is not None and len(results) > 0:
                last_page_num = int(results[-1])
                pages = [i+1 for i in range(last_page_num)]
                if last_page_num > self.rangkaian_min_page:
                    pages = random.sample(pages, k=self.rangkaian_min_page)
            
            curr_name = self.get_curr_name_rangkaian_page(response)
            
            urls = []
            for pnum in pages:
                url = build_search_rangkaian_urls(self.name_position, curr_name, str(pnum))
                urls.append(url)
                
        return urls
        
    def parse(self, response):
        sampled_urls = self.build_sampled_abjad_search_urls(response)
        for url in sampled_urls:
            print(f'PARSE:\t Go To URL: {url}')
            yield scrapy.Request(url=url, callback=self.parse_abjad_page)
    
    def parse_abjad_page(self, response):
        results = response.css('div.columnsWrap.search-result-wrapper > article.columns1_3 > div.search-result-item ')
        
        for result in results:
            name = result.css('h4 > a::text').extract_first().strip()
            gender = result.css('p > strong::text').extract_first().upper()
            data =  { 'base_name': name, 'gender': gender,}
            
            rangkaian_url = build_search_rangkaian_urls(self.name_position, name)
            print(f'PARSE_ABJAD:\t Go To URL: {rangkaian_url}')
            yield scrapy.Request(url=rangkaian_url , callback=self.parse_rangkaian_url, cb_kwargs=dict(parse_data=data))
            
    def parse_rangkaian_url(self, response, parse_data):
        sampled_urls = self.build_sampled_rangkaian_pagination_urls(response)
        for url in sampled_urls:
            print(f'PARSE_RANGKAIAN:\t Go To URL: {url}')
            yield scrapy.Request(url=url, callback=self.parse_rangkaian_page, cb_kwargs=dict(parse_data=parse_data))
            
            
    def parse_rangkaian_page(self, response, parse_data):
        results = response.css('li.sc_list_item.icon-right-open-big *::text')
        for result in results:
            parse_data['name'] = result.extract()
            parse_data['source'] = response.url
            print(parse_data)
            yield parse_data