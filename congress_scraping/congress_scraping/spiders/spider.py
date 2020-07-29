import scrapy
import re
from congress_scraping.items import Senate


class SenateScraper(scrapy.Spider):
    name = 'senate_co'
    allowed_domains = ['senado.gov.co']
    start_urls = ['https://www.senado.gov.co/index.php/el-senado/senadores?lastletter=Todos#modazdirectory']

    def parse(self, response):
        links = response.css('blockquote a::attr(href)').extract()
        for senate_url in links:
            if re.search('el-senado', senate_url):
                yield response.follow(senate_url, callback=self.parse_details)

    def parse_details(self, response):
        item = Senate()
        
        name_op1, name_op2 = (
            response.css('h2::text').get(),
            response.css('h3::text').get()
        )

        pic_op1, pic_op2 = (
            response.css('img.modazdirectory__image::attr(src)').get(),
            response.css('.sppb-addon-content img::attr(src)').get()
        )

        party_op1, party_op2 = (
            response.css('tr:nth-child(3) td+ td p::text').get(),
            response.css('strong a::text').get()
        )

        item['name'] = name_op2 if name_op1 is None else name_op1
        item['picture'] = pic_op2 if pic_op1 is None else pic_op1
        item['party'] = party_op2 if party_op1 is None else party_op1
        # item['birth_date'] = response.css('tr:nth-child(1) td+ td p::text').get()
        item['birth_date'] = response.css('div.sppb-addon-content').re_first(r'\d+\s{0,2}?[dD][\s\w]+\s\d+')
        item['city'] = response.css('tr:nth-child(2) td+ td p::text').get()
        item['com_const'] = response.css('tr:nth-child(4) td+ td p::text').get()
        item['twitter'] = response.css('div.sppb-addon-content').re_first(r'(?<!\w)@\w+')

        yield item
