# -*- coding : utf-8 -*-

import pprint
from googleapiclient.discovery import build
from urllib.request import urlopen
from bs4 import BeautifulSoup
from newspaper import Article
from time import gmtime, strftime


def get_link():
    # call api to get json file, build service first, target the customsearch api
    service = build("customsearch", "v1",
                    developerKey='AIzaSyBZtIjpRfeKk_E-e1DUXCf8goEcTLxyvic')

    # call the customsearch api with formated query elements
    res = service.cse().list(
        q='casino river hotel',
        cx='014452005112961186943:btsgmzwssuw',
        dateRestrict='w[3]',
        fields='items(title, link, labels(displayName))'
    ).execute()

    #json_file = unquote(res)
    #res_dict = json.loads(res)

    #print(res['items'][0]['link'])

    return res['items']

get_link()

def get_text(link):

    # read html
    url = link
    html = urlopen(url).read()

    # build soup and get text
    soup = BeautifulSoup(html, 'lxml')
    for script in soup(["script", "style"]): # remove <script> and css
        script.extract()

    # get text
    text = soup.get_text()

    # break into lines and trim
    lines = (line.strip() for line in text.splitlines())

    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split(" "))

    text = ' '.join(chunk for chunk in chunks if chunk)

    print(text)
    return text

# get_text('http://www.timesunion.com/business/article/New-hotel-final-piece-in-Rivers-Casino-Resort-11253434.php')


def news_refine(url):
    # build article from url
    article = Article(url)

    # download article and parse
    article.download()

    article.parse()
    # print(article.publish_date)

    article.nlp()
    return article


# news_refine('http://www.timesunion.com/business/article/New-hotel-final-piece-in-Rivers-Casino-Resort-11253434.php')


def parse_results():

    items = get_link()

    returned_data = "title, link, date, author, keywords\n"

    for item in items:
        title = item['title']
        link = item['link']
        # display_name = item['displayName']
        article = news_refine(link)
        author = article.authors
        date = article.publish_date
        keywords = ' '.join(phrase for phrase in article.keywords)

        cleared = "%s, %s, %s, %s, %s, \n" % (title, link, date, author, keywords)
        returned_data += cleared
    pprint.pprint(returned_data)
    return returned_data

# parse_results()


def save_data():
    file_path = strftime("%Y%m%d%H%M%S", gmtime())
    output = open("data%s.csv" % file_path, "w+")
    output.write(parse_results())
    output.close()

save_data()