import scrapy
from juart_scraper.items import ProductItem


class ProductParseSpider(scrapy.Spider):
    name = "product_parse"
    allowed_domains = ["juart.bg"]
    start_urls = ["https://juart.bg"]
    custom_settings = {
        'ITEM_PIPELINES': {
            "juart_scraper.pipelines.ConcatenateDescriptionPipeline": 100,
            "juart_scraper.pipelines.JsonWithEncodingPipeline": 300,
        }
    }

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
        item["title"] = response.css("h2.product_title::text").get().strip()
        item["id"] = response.css("span.sku::text").get().strip()
        item["price"] = response.css(".summary bdi::text").get().strip()
        item["description"] = response.xpath("//div[@id='tab-description']//p")
        item["tags"] = response.css(".summary span.tagged_as a::text").getall()
        yield item
