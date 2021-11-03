import scrapy


class ScrapeSpider(scrapy.Spider):
    name = "scrape"

    def start_requests(self):
        urls = [
            'https://www.dfs.ny.gov/reports_and_publications/press_releases'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for quote in response.css('tr.data-row'):
            url = "https://www.dfs.ny.gov" + quote.css('td.views-field.views-field-view-node a::attr(href)').get()

            d = {
                'date': quote.css('td.views-field.views-field-field-release-date-created::text').get().replace(" ", ""),
                'title': quote.css('td.views-field.views-field-view-node a::text').get(),
                'url': url
            }
            request = scrapy.Request(url=url,
                                     callback=self.parse2,
                                     cb_kwargs=d)
            yield request

    def parse2(self, response, date, title, url):
        print("hi" + response.url)
        h1 = response.css('div.page-body h1::text').getall() + response.css('div.page-body h1 strong::text').getall()
        h3 = response.css('div.page-body h3::text').getall() + response.css('div.page-body h3 em::text').getall() + response.css('div.page-body h3 em strong::text').getall()
        yield dict(
            date=date,
            title=title,
            url=url,
            content=" ".join(h1 + h3),
        )



