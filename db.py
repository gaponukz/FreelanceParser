import sqlite3
import requests
import codecs
from bs4 import BeautifulSoup

class SQLiter:
	def __init__(self, db: str):
		self.connection = sqlite3.connect(db)
		self.cursor = self.connection.cursor()

	def get_users(self, status: bool = True):
		with self.connection:
			return self.cursor.execute("SELECT * FROM `Users` WHERE `status` = ?", (status,)).fetchall()

	def user_exists(self, user_id):
		with self.connection:
			result = self.cursor.execute("SELECT * FROM `Users` WHERE `user_id` = ?", (user_id,)).fetchall()
			return bool(len(result))

	def add_user(self, user_id, status = True):
		with self.connection:
			return self.cursor.execute("INSERT INTO `Users` (`user_id`, `status`) VALUES (?,?)", (user_id, status))

	def update_user(self, user_id, status):
		return self.cursor.execute("UPDATE `Users` SET `status` = ? WHERE `user_id` = ?", (status	, user_id))

	def close(self):
		self.connection.close()

class Parse:
	def __init__(self, url: str):
		request = requests.get(url)
		html = BeautifulSoup(request.content, 'html.parser')
		href = lambda element: element['href']
		path_to_element = '.l-projectList > .j-order > header:nth-child(1) > a:nth-child(2)'

		self.urls = list(map(href, html.select(path_to_element)))
		self.last_url = self.urls[0]

	def write_data(self):
		file = codecs.open("lastwork.txt", "w", "utf_8_sig" )

		for url in self.urls:
			file.write(f'{url}\n')
		file.close()

	def update_data(self, new):
		if not new != self.urls[0]:
			self.urls.append(new)