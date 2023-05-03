# scrapy shell
# fetch('https://www.w3schools.com/html/html_intro.as')
# response.css('#main h2').getall()
# response.css('#main h2::text').getall()
# /c/aaTCC/w3s
# scrapy crawl w3 -o(add) -O


import json
import scrapy
from bs4 import BeautifulSoup
from googletrans import Translator


class W3Spider(scrapy.Spider):
    name = "w3"
    start_urls = ["https://www.w3schools.com/html/html_intro.asp",
                  "https://www.w3schools.com/html/html_basic.asp",
                  "https://www.w3schools.com/html/html_elements.asp",
                  "https://www.w3schools.com/html/html_attributes.asp",
                  "https://www.w3schools.com/html/html_headings.asp",
                  "https://www.w3schools.com/html/html_paragraphs.asp",
                  "https://www.w3schools.com/html/html_styles.asp",
                  "https://www.w3schools.com/html/html_formatting.asp",
                  "https://www.w3schools.com/html/html_comments.asp",
                  "https://www.w3schools.com/html/html_css.asp",
                  "https://www.w3schools.com/html/html_links.asp",
                  "https://www.w3schools.com/html/html_images.asp",
                  "https://www.w3schools.com/html/html_images_background.asp",
                  "https://www.w3schools.com/html/html_page_title.asp",
                  "https://www.w3schools.com/html/html_tables.asp",
                  "https://www.w3schools.com/html/html_table_borders.asp",
                  "https://www.w3schools.com/html/html_table_sizes.asp",
                  "https://www.w3schools.com/html/html_table_headers.asp",
                  "https://www.w3schools.com/html/html_table_padding_spacing.asp",
                  "https://www.w3schools.com/html/html_table_colspan_rowspan.asp",
                  "https://www.w3schools.com/html/html_table_styling.asp",
                  "https://www.w3schools.com/html/html_table_colgroup.asp",
                  "https://www.w3schools.com/html/html_classes.asp",
                  "https://www.w3schools.com/html/html_id.asp"
                  ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        sections = []

        translator = Translator()

        for tag in soup.select('#main h2'):
            # traduz o título para o português
            translated_title = translator.translate(
                tag.text.strip(), dest='pt').text
            current_dict = {'title': translated_title, 'content': ''}
            next_tag = tag.find_next_sibling()
            while next_tag and next_tag.name != 'hr':
                current_dict['content'] += str(next_tag)
                next_tag = next_tag.find_next_sibling()
            # traduz o conteúdo para o português
            translated_content = translator.translate(
                current_dict['content'], dest='pt').text
            current_dict['content'] = translated_content

           

            sections.append(current_dict)

        yield {'sections': sections}

    def closed(self, reason):
        # cria um dicionário com a chave "sections"
        sections_list = []
        for item in self.crawler.stats.get('item_scraped_count', []):
            sections_list.extend(item['sections'])
        result_dict = {'sections': sections_list}

        # converte o dicionário para JSON
        result_json = json.dumps(result_dict)
        self.logger.info(result_json)
        yield json.loads(result_json)
