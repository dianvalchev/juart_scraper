import scrapy
from juart_scraper.items import ProductItem


class JuartSpider(scrapy.Spider):
    name = "juart"
    allowed_domains = ["juart.bg"]
    start_urls = ["https://juart.bg"]

    def parse(self, response):
        # Get all the categories' urls and put them in a variable.
        all_categories = response.css(".menu-center > ul.main-menu li a::attr(href)").getall()
        # Parse through all the categories, looking for products.
        for category_url in all_categories:
            yield scrapy.Request(category_url, callback=self.parse_category)

    def parse_category(self, response):
        # Get all products' urls on the page and put them in a variable
        all_products = response.css(".archive-products > ul.products li .product-loop-title::attr(href)").getall()
        # Parse through all the products, extracting the data
        for product_url in all_products:
            yield scrapy.Request(product_url, callback=self.parse_product)

    def parse_product(self, response):
        # Extract required data from each product
        item = ProductItem()
        item["title"] = response.css("h2.product_title::text").get()
        item["id"] = response.css("span.sku::text").get()
        item["price"] = response.css(".summary bdi::text").get()
        item["description"] = response.css(".woocommerce-tabs > .resp-tabs-container > .tab-content > p::text").getall()
        yield item

