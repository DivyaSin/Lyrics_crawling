import scrapy
from string import ascii_lowercase

class ArtistsSpider(scrapy.Spider):
	name = "artists"


	def parse_lyrics(self, response):
		print "CRAWLED", response.url
		lyrics = response.css("div.lyrics-body p.verse::text").extract()
		lyrics_str = ' '.join(lyrics)

		if lyrics_str != "":
			temp = response.url.split("/")[-1].strip(".html")

			filename = "crawled/" + temp

			with open(filename, 'wb') as f:
				f.write(lyrics_str)
			self.log('Saved file %s' % filename)

	def get_lyrics(self, response):
		next_pages = response.css('table.songs-table.compact a::attr(href)').extract()
		for page in next_pages:
			if page is None:
				continue
			yield scrapy.Request(url=page, callback=self.parse_lyrics)
	def parse(self, response):
		next_pages = response.css('table.songs-table a::attr(href)').extract()
		# print "LEVEL ONE NEXT PAGES", next_pages
		for page in next_pages:
			if page is None:
				continue
			yield scrapy.Request(url=page, callback=self.get_lyrics)

	def start_requests(self):
		base = "http://www.metrolyrics.com/artists-"
		urls = []
		# count = 0
		for c in ascii_lowercase:
			# if count == 1:
			# 	break
			# count += 1
			url = base + c + ".html"
			urls.append(url)
			for i in xrange(1, 30):
				url = base + c + "-" + str(i) +".html"
				urls.append(url)
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

