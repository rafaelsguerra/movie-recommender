import json
import scrapy
from bs4 import BeautifulSoup

class MovieInfo(scrapy.Spider):
    name = "movie_info"
    allowed_domains = ["rottentomatoes.com"]

    def start_requests(self):
        urls = []
        
        with open("movie_links.txt", 'r') as file:
            for path in file:
                urls.append("https://www.rottentomatoes.com" + path)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        data = response.body
        soup = BeautifulSoup(data, 'html.parser')

        try:
            title = soup.find('rt-text', attrs={'context': 'heading'}).text
            
            try:
                consensus = soup.find(id='critics-consensus').p.text
            except AttributeError:
                consensus = None

            mediainfo = soup.find("section", attrs={'class': 'media-info'})

            synopsis = mediainfo.find(attrs={'data-qa': 'synopsis-value'}).text
            dl = mediainfo.dl

            def get_info(info):
                try:
                    return dl.find("rt-text", string=info).parent.find_next_sibling("dd").text.replace("\n", "")
                except AttributeError:
                    return None

            director = get_info("Director")
            producer = get_info("Producer")
            screenwriter = get_info("Screenwriter")
            distributor = get_info("Distributor")
            production_co = get_info("Production Co")
            rating = get_info("Rating")
            genre = get_info("Genre")
            original_language = get_info("Original Language")
            release_date_theaters = get_info("Release Date (Theaters)")
            rerelease_date_theaters = get_info("Rerelease Date (Theaters)")
            release_date_streaming = get_info("Release Date (Streaming)")
            box_office = get_info("Box Office (Gross USA)")
            runtime = get_info("Runtime")
            sound_mix = get_info("Sound Mix")
            aspect_ratio = get_info("Aspect Ratio")

            scores = soup.findAll('rt-text', attrs={"data-mediascorecardmanager": 'overlayOpen:click', 'context': 'label'})
            critics_score = scores[0].text
            audience_score = scores[1].text

            movie_info = {
                'title': title,
                'synopsis': synopsis,
                'critics_consensus': consensus,
                'critics_score': critics_score,
                'audience_score': audience_score,
                'director': director,
                'producer': producer,
                'screenwriter': screenwriter,
                'distributor': distributor,
                'production_co': production_co,
                'rating': rating,
                'genre': genre,
                'original_language': original_language,
                'release_date_theaters': release_date_theaters,
                'rerelease_date_theaters': rerelease_date_theaters,
                'release_date_streaming': release_date_streaming,
                'box_office': box_office,
                'runtime': runtime,
                'sound_mix': sound_mix,
                'aspect_ratio': aspect_ratio,
            }

            yield movie_info

        except:
            with open('errors.txt', 'a') as errors:
                errors.write(title + '\n')