from bs4 import BeautifulSoup
import urllib2
from time import time
import string

# a seemingly reasonable user agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'

MOVIE_ID_LOC = 'movie_ids.list'
TITLE_URL = 'http://www.imdb.com/title/%s/'
OUTPUT_LOC = 'movie_storylines.list'

movie_IDs = []
with open(MOVIE_ID_LOC, 'r') as f:
    for line in f:
        movie_IDs.append(line.rstrip())

start = time()
with open(OUTPUT_LOC, 'a') as f:
    for i, movie_ID in enumerate(movie_IDs):
        if (i + 1) < 2452:
            continue
        print '(%d/%d) %s' % (i + 1, len(movie_IDs), movie_ID)
        title_URL = TITLE_URL % movie_ID
        request = urllib2.Request(title_URL)
        request.add_header('User-Agent', USER_AGENT)
        opener = urllib2.build_opener()
        
        soup = BeautifulSoup(opener.open(request))
        
        try:
            description = soup.find('div', attrs = {'itemprop': 'description'})
            text = description.find('p').text.strip()
            written_loc = string.find(text, 'Written by')
            cleaned_text = text[:written_loc].strip().replace('\n', ' ').encode('latin1', 'ignore')
        except Exception as e:
            # if any sort of exception, there's probably no summary, so ignore
            cleaned_text = ''
            
        f.write('%s|%s\n' % (movie_ID, cleaned_text))
print 'Time elapsed: %f s' % (time() - start)
