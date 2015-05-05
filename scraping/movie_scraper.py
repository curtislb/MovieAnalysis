import json
import urllib2
import sys
from time import time

# a seemingly reasonable user agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'

# IMDb API URL
# thanks to this: https://ubuntuincident.wordpress.com/2012/02/12/get-imdb-ratings-without-any-scraping/
IMDB_API_URL = 'http://app.imdb.com/title/maindetails?tconst=%s'

# list of movie IDs (one per line)
MOVIE_IDS_FILE = 'movie_ids.list'

# output file
OUTPUT_JSON_FILE = 'movies.bigdata'

# load movie IDs
movie_IDs = []
with open(MOVIE_IDS_FILE, 'r') as f:
    for line in f:
        movie_IDs.append(line.rstrip())

# download movie info
start_time = time()
with open(OUTPUT_JSON_FILE, 'a') as f:
    for i, movie_ID in enumerate(movie_IDs):
        api_URL = IMDB_API_URL % movie_ID
        request = urllib2.Request(api_URL)
        request.add_header('User-Agent', USER_AGENT)
        opener = urllib2.build_opener()
        movie_data_json = json.load(opener.open(request))
        
        # print to screen
        print ('%d: %s (%s)' % ((i + 1), movie_data_json['data']['title'], movie_ID)).encode('latin1')
        
        movie_data_string = json.dumps(movie_data_json)
        f.write(movie_data_string)
        f.write(',')
print 'Time taken: %f s' % (time() - start_time)
