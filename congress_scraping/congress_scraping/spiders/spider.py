import scrapy
import re
from congress_scraping.items import CongressSenate


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
        item = CongressSenate()

        name_h2, name_h3 = (
            response.css('h2::text').get(),
            response.css('h3::text').get()
        )

        item['name'] = name_h3 if name_h2 is None else name_h2
        item['picture'] = response.css('img.modazdirectory__image::attr(src)').get()
        item['party'] = response.css('tr:nth-child(3) td+ td p::text').get()
        item['birth_date'] = response.css('tr:nth-child(1) td+ td p::text').get()
        item['city'] = response.css('tr:nth-child(2) td+ td p').css('::text').get()
        item['com_const'] = response.css('tr:nth-child(4) td+ td p').css('::text').get()
        item['twitter'] = response.css('div.sppb-addon-content').re_first(r'(?<!\w)@\w+')

        yield item
