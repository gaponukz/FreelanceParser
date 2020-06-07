import requests
from bs4 import BeautifulSoup
import codecs

class Parse:
	def __init__(self, url: str):
		request = requests.get(url)
		html = BeautifulSoup(request.content, 'html.parser')
		href = lambda element: element['href']
		path_to_element = '.l-projectList > .j-order > header:nth-child(1) > a:nth-child(2)'

		self.urls = list(map(href, html.select(path_to_element)))

	def write_data(self):
		file = codecs.open("lastwork.txt", "w", "utf_8_sig" )

		for url in self.urls:
			file.write(f'{url}\n')
		file.close()

	def update_data(self, new):
		if not new != self.urls[0]:
			file = codecs.open( "lastwork.txt", "w", "utf_8_sig" )
			data.insert(0, post.last_url)
			file.write(data)
			file.close()

post = Parse('https://freelance.ua/orders/?page=1&st=2&clear=1')
print(post.urls)