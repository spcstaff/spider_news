import urllib.request
import urllib.parse
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
import pprint
import time
import re

# baseURL = ["http://www.trbappcon.org/2017conf/PresentationDetails.aspx?abstractid={}".format(str(i)) for i in range(1, 400, 1)]

baseURL = "http://www.trbappcon.org/2017conf/PresentationDetails.aspx?abstractid="
baseURL2 = "http://www.trbappcon.org/2017conf/"
# web_data = requests.get(baseURL)
# soup = BeautifulSoup(web_data.text, 'lxml')
# pprint.pprint(soup)
links = []
FileName = []

# locations = soup.find_all("a", text="Presentation")
# for location in locations:
# link = baseURL2+str(location.get('href'))
# links.append(link)


def get_link_list():
    for i in range(0, 360, 1):
        url = baseURL + str(i);
        print(url)
        web_data = requests.get(url)
        time.sleep(1)
        soup = BeautifulSoup(web_data.text, 'lxml')
        locations = soup.find_all("a", text="Presentation")
        for location in locations:
            name = location.get('href').split('/')[1]
            link = baseURL2 + urllib.parse.quote(str(location.get('href')))
            links.append((link, name))
    pprint.pprint(links)


def get_contents(link):
        time.sleep(1)
        try:
            urllib.request.urlretrieve(link[0], "%s" % link[1])
        except Exception as e:
            print(e)


if __name__ == '__main__':
    get_link_list()
    pool = Pool();
    pool.map(get_contents, links)


# get_contents()
# get_link_list()

# get_contents()

# urllib.request.urlretrieve("https://www.trbappcon.org/2017conf/presentations/1_3C_Externals_TPAC.pptx", "abcd.pptx")

# urllib.parse.urlencode("3_Presentation for TRB Planning Applications Conference in May 2017.pptx")