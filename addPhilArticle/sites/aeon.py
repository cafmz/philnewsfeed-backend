import secrets
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from check import check_new_article

def aeon_rss(url):
    print("\nConnecting to Aeon rss feed...")
    
    article_list = []
    
    try:
        r = urllib.request.urlopen(url).read().decode('utf-8')
        root = ET.fromstring(r)
        
        for child in root.find('channel').findall('item'):
            id = int(secrets.randbelow(2**64))
            name = "Aeon"
            title = child[0].text.replace("\xa0", "")
            link = child[1].text
            time = child[4].text
            
            dateFormatter = "%Y-%m-%dT%H:%M:%S.%fZ"
            dt = datetime.strptime(time, dateFormatter)
            published = dt.strftime("%Y-%m-%d")
            
            if check_new_article(link) is not None:
                article = {'id':id, 'name': name, 'title': title, 'link': link, 'published': published}
                article_list.append(article)
        
        print("Finished scraping Aeon rss feed!\n")
        return article_list
            
    except Exception as e:
        print("Aeon (rss feed) - The scraping job failed. See exception:\n", e)
