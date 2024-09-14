import scrapy


class DarwinSpider(scrapy.Spider):
    name = "darwin"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        #Data Object With Attributes 
        books = response.css('article.product_pod')
    
        for book in books:
            yield {
                'title': book.css('h3 a::text').get(),
                'price' : book.css('.product_price .price_color::text').get()[1:],
                'link' : book.css('h3 a::attr(href)').get(),
                'rating': book.css('p::attr(class)').get().replace(" ","").split('g')[1]
            }
                
            #Handling Pagination 
            next_page = response.css('.next a::attr(href)').get()
            root_url = 'https://books.toscrape.com/'

            if next_page:
                if 'catalogue' in next_page:
                    next_page_url = root_url+next_page
                else:
                    next_page_url = root_url+'catalogue/'+next_page

                #Follow the links and response and repeat parse function 
                yield response.follow(next_page_url, callback=self.parse)
                
     
