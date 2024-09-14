import scrapy


class DarwinSpider(scrapy.Spider):
    name = "darwin"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        #Data Object With Attributes 
        books = response.css('article.product_pod')
        for book in books:
            #Drill into each book product page
            rel_url = response.css('h3 a::attr(href)').get()
            root_url = 'https://books.toscrape.com/'
            
            if 'catalogue/' in rel_url:
                book_url = root_url+rel_url
            else:
                book_url = root_url+'catalogue/'+rel_url

            #Follow, callback to new function that parses the book page
            yield response.follow('next_page_url', callback=self.parse_book_page)

            #Next Page Link
            next_page = response.css('li.next a ::attr(href)').get()

            if next_page:
                if 'catalogue' in next_page:
                    next_page_url = root_url+next_page
                else:
                    next_page_url = root_url+'catalogue/'+next_page

                #Follow the links and response and repeat parse function 
                yield response.follow(next_page_url, callback=self.parse)

        
                
    def parse_book_page(self, response):
        
        table_rows = response.css('table tr')

        yield {
            "url": response.url,
            "title": response.css('.product_main h1::text').get(),
            "category": response.xpath("//ul[@class='breadcrumb]/li[@class='active']/preceding-sibling::li[1]/a/text()").get(),
            "description": response.xpath("//div[@class='product_description']/following-sibling::p/text()").get()[:75],
            "price": response.xpath("//p[@class='price_color']/text()").get()[1],
            "upc": table_rows[0].css('td::text').get(),
            "type": table_rows[1].css('td::text').get(), 
            "stock": table_rows[5].css('td::text').get(),
            "reviews": table_rows[6].css('td::text').get(),
            "rating": response.css("p.star-rating::attr(class)").get().replace(" ", "").split('g')[1]
        }
       





                