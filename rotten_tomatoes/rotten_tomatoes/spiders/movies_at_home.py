from pathlib import Path
import scrapy
import json
from urllib.parse import quote_plus

class MoviesAtHome(scrapy.Spider):
    name = "movies_at_home"
    allowed_domains = ["rottentomatoes.com"]
    start_urls = [f"https://www.rottentomatoes.com/napi/browse/{name}/sort:popular?page=1"]

    def parse(self, response):
        
        data = json.loads(response.body)
        yield from data['grid']['list']

        filename = f"{self.name}.txt"
        with open(filename, 'a') as json_file:
            for movie_data in data['grid']['list']:
                json.dump(movie_data, json_file)
                json_file.write('\n')
        
        page_id = data['pageInfo']['endCursor']
        next_page = "?after=" + quote_plus(str(page_id))

        print(page_id)
        
        if page_id is not None:
            next_page = response.urljoin(next_page)            
            yield scrapy.Request(next_page, callback=self.parse)