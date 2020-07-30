import scrapy
import re
from congress_scraping.items import Senate


class SenateScraper(scrapy.Spider):
    name = 'senate_co'
    allowed_domains = ['senado.gov.co']
    start_urls = ['https://www.senado.gov.co/index.php/el-senado/senadores?lastletter=Todos#modazdirectory']

    def parse(self, response):
        links = response.css(
            '.modazdirectory__result.modazdirectory__layout-misc_on blockquote a::attr(href)'
            ).extract()
        print('""""""NUMBER OF LINKS FOUND""""""""', len(links))
        count_1 = 0
        count_2 = 0
        for senate_url in links:
            count_1 += 1
            if re.search('el-senado', senate_url):
                count_2 += 1
                yield response.follow(senate_url, callback=self.parse_details)
        
        print('""""""THIS IS COUNT_1""""""', count_1)
        print('""""""THIS IS COUNT_2""""""', count_2)

    def parse_details(self, response):
        item = Senate()

        name = response.css('h2, h3').css('::text').get()
        pic = response.css(
            'img.modazdirectory__image, .sppb-addon-content img'
            ).css('::attr(src)').get()
        
        party_op1, party_op2 = (
            response.css('tr:nth-child(3) td+ td p::text').get(),
            response.css('h2+ p, h2+ div *').re_first(r'(?<=\>)[\sA-zÀ-ú]+(?=\<)')
        )

        birth_date = response.css(
            'div.sppb-addon-content'
            ).re_first(r'\d+\s{0,2}?[dD][\s\w]+\s\d+')

        city_op1, city_op2 = (
            response.css('tr:nth-child(2) td+ td p::text').get(),
            response.css('div.sppb-addon-content').re_first(r'(?<=\d\,\s)[\s\w]+\,{1}[\s\w]+(?=\.|\<)')
        )
        
        com_pattern = r'primera|segunda|tercera|cuarta|quinta|sexta|s[eé]ptima'
        com_ = ''.join(response.css('.sppb-addon-content *').getall())
        com_const = re.findall(com_pattern, com_.lower())

        twitter = response.css(
            'div.sppb-addon-content'
            ).re_first(r'(?<!\w)@\w+')

        item['name'] = name
        item['picture'] = pic
        item['party'] = party_op2 if party_op1 is None else party_op1
        item['birth_date'] = birth_date
        item['city'] = city_op2 if city_op1 is None else city_op1
        item['com_const'] = com_const[0] if len(com_const) > 0 else None
        item['twitter'] = twitter

        yield item
