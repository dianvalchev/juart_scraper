import scrapy


class FormSpider(scrapy.Spider):
    name = 'product_search'
    start_urls = ['https://juart.bg/']

    def parse(self, response):

        # Form data
        form_data = {
            's': 'гоблен',  # Search query
        }

        yield scrapy.FormRequest.from_response(response, formdata=form_data, callback=self.parse_result_page)

    def parse_result_page(self, response):
        # Extract information from the result page
        product_titles = response.css('h2.entry-title ::text').getall()
        product_urls = response.css('h2.entry-title ::attr(href)').getall()

        for title, price in zip(product_titles, product_urls):
            yield {'product_title': title.strip(),
                   'product_url': price.strip(),
                   }

        # Extract the "Next" pagination link
        next_page_link = response.css('.pagination a.next.page-numbers::attr(href)').get()

        if next_page_link is not None:
            yield response.follow(next_page_link, callback=self.parse_result_page)
