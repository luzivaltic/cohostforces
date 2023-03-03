import scrapy
from csv import DictWriter, writer
from cohostforces.items import ContestItem, UserItem

class CrawlingSpider(scrapy.Spider):
    name = "demo"
    allows_domain = 'https://codeforces.com'
    start_url = [
        'https://codeforces.com/ratings/page/2',
        'https://codeforces.com/ratings/page/3',
        'https://codeforces.com/ratings/page/4',
        'https://codeforces.com/ratings/page/5',
        'https://codeforces.com/ratings/page/6',
        'https://codeforces.com/ratings/page/7',
        'https://codeforces.com/ratings/page/8',
        'https://codeforces.com/ratings/page/9',
        'https://codeforces.com/ratings/page/10',
        'https://codeforces.com/ratings/page/11',
        'https://codeforces.com/ratings/page/12',
    ]

    def start_requests(self):
        for url in self.start_url:
            yield scrapy.Request(url=url, callback=self.access_user_info)

    def get_pageId(self, response):
        page_ids = response.xpath('//div[@id="pageContent"]/div/ul/li/span/a//@href').extract()
        for page_id_url in page_ids:
            url = self.allows_domain + page_id_url
            yield scrapy.Request(url=url, callback=self.access_user_info)

    def access_user_info(self, response):
        user_url_list = response.xpath('//div[@class="datatable ratingsDatatable"]/div[6]/table/tr/td[2]/a//@href').extract()
        for url in user_url_list:
            total_link = self.allows_domain + url
            yield scrapy.Request(url=total_link, callback=self.parse_user_info)

    def parse_user_info(self, response):
        users = UserItem()

        title = response.xpath('//div/div/div/div[2]/div/div[1]/span//text()').get()
        users['Title'] = title

        name = response.xpath('//div[@id="pageContent"]/div[2]/div[5]/div[2]/div/h1/a//text()').get()
        users['Name'] = name

        rating = response.xpath('//div[@id="pageContent"]/div[2]/div[5]/div[2]/ul/li[1]/span[1]//text()').get()
        users['Rating'] = rating

        max_rating = response.xpath('//div[@id="pageContent"]/div[2]/div[5]/div[2]/ul/li[1]/span[2]/span[2]//text()').get()
        users['Max_rating'] = max_rating

        ## Access user
        url = response.xpath('//div[@id="pageContent"]/div[1]/ul/li/a[text()="Contests"]//@href').get()
        contest_link = self.allows_domain + url

        print("+ " + contest_link)
        
        yield scrapy.Request(url=contest_link, callback=self.parse_contest_info)   

    def get_title(self, rating):
        if rating < 1200:
            return 'Newbie'
        elif rating < 1400:
            return 'Pupil'
        elif rating < 1600:
            return 'Specialist'
        elif rating < 1900:
            return 'Expert'
        elif rating < 2100:
            return 'Candidate Master'
        elif rating < 2300:
            return 'Master'
        elif rating < 2400:
            return 'International Master'
        elif rating < 2600:
            return 'Grandmaster'
        elif rating < 3000:
            return 'International Grandmaster'
        else:
            return 'Legendary Grandmaster'

    def parse_contest_info(self, response):
        string = str(response)
        string = string.replace('<200 https://codeforces.com/contests/with/', '')
        string = string.replace('>', '')
        username = string

        key_block = response.css('table.tablesorter.user-contests-table thead tr')
        table = {}
        table_keys = []
        table_values = []

        for key in key_block:
            table_keys = key.css('th').css('::text').extract()
        table_keys.append('Title')
        
        data_block = response.css('table.tablesorter.user-contests-table tbody tr')
        for data in data_block:
            values = data.css('td')[0:-1].css('::text').extract()
            columns_data = []
            for item in values:
                item = item.strip()
                if item != '':
                    columns_data.append(item)
            columns_data.append(self.get_title(int(columns_data[-1])))
            
            table_values.append(columns_data)
        

        with open('data/' + username + '.csv', 'w+') as f_object:
            dictwriter_object = writer(f_object)
            dictwriter_object.writerow(table_keys)
            for value in table_values:
                dictwriter_object.writerow(value)
    
        return table


