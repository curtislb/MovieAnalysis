from bs4 import BeautifulSoup
import urllib2
from time import time

# a seemingly reasonable user agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'

MOVIE_ID_LOC = 'movie_ids.list'
CAST_URL = 'http://www.imdb.com/title/%s/fullcredits'
OUTPUT_LOC = 'movie_casts.list'

movie_IDs = []
with open(MOVIE_ID_LOC, 'r') as f:
    for line in f:
        movie_IDs.append(line.rstrip())

start = time()
with open(OUTPUT_LOC, 'a') as f:
    for i, movie_ID in enumerate(movie_IDs):
        if (i + 1) < 8245:
            continue
        print '(%d/%d) %s' % (i + 1, len(movie_IDs), movie_ID)
        cast_URL = CAST_URL % movie_ID
        request = urllib2.Request(cast_URL)
        request.add_header('User-Agent', USER_AGENT)
        opener = urllib2.build_opener()
        
        soup = BeautifulSoup(opener.open(request))
        
        table = soup.find_all('td', attrs = {'class': 'itemprop'})
        for entry in table:
            actor_ID = entry.find('a')['href'].split('/')[2]
            actor_name = entry.text.strip().encode('latin1', 'ignore')
            f.write('%s,%s,%s\n' % (movie_ID, actor_ID, actor_name))
print 'Time elapsed: %f s' % (time() - start)
