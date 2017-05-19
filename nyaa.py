#VERSION: 1.01
#AUTHORS: Phuong Tran (phuongtm6994@gmail.com)
# LICENSING INFORMATION
from novaprinter import prettyPrinter
from helpers import retrieve_url, download_file
from bs4 import BeautifulSoup

# some other imports if necessary
class nyaa(object):
  url = 'https://sukebei.nyaa.si'
  name = 'Sukebei Nyaa' # spaces and special characters are allowed here
  # Which search categories are supported by this search engine and their corresponding id
  # Possible categories are ('all', 'movies', 'tv', 'music', 'games', 'anime', 'software', 'pictures', 'books')
  supported_categories = {'all': '0', 'movies': '6', 'tv': '4', 'music': '1', 'games': '2', 'anime': '7', 'software': '3'}

  def __init__(self):
    pass

  # DO NOT CHANGE the name and parameters of this function
  # This function will be the one called by nova2.py
  def search(self, what, cat='all'):
    # what is a string with the search tokens, already escaped (e.g. "Ubuntu+Linux")
    # cat is the name of a search category in ('all', 'movies', 'tv', 'music', 'games', 'anime', 'software', 'pictures', 'books')
    # q - query, f - filter, c - category
    base_url = 'https://sukebei.nyaa.si/?q=%s&f=0&c=0_0'
    response = retrieve_url(base_url % what)
    soup = BeautifulSoup(response, 'html.parser')
    table = soup.find('table')
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    for row in rows:
      tds = row.find_all('td')
      ref = tds[1].find('a').get('href')
      title = tds[1].find('a').text
      link = tds[2].find_all('a')[-1].get('href')
      _size = tds[3].text
      size = _size[:-3]
      unit = _size[-3:]
      # sizeInBytes = -1
      if unit == "GiB":
        sizeInBytes = float(size) * 1073741824
      elif unit == "MiB":
        sizeInBytes = float(size) * 1000000
      seeders = tds[5].text
      leechers = tds[6].text
      res = dict(link=link,
                 name=title,
                 size=str(sizeInBytes),
                 seeds=seeders,
                 leech=leechers,
                 engine_url=self.url,
                 desc_link=self.url + ref)
      prettyPrinter(res)
