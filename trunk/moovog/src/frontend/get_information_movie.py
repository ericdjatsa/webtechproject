#!/usr/bin/env python
"""
get_first_movie.py

Usage: get_first_movie "movie title"

Search for the given title and print the best matching result.
"""
import sys, threading

global table_done
table_done=[0,0,0,0,0]

class ThreadUpdate(threading.Thread):
    def __init__(self,movie,IMDB,number):
        threading.Thread.__init__(self)
        self.movie = movie
        self.IMDB = IMDB
        self.number=number
    def run(self):
        print '===========update started========='   
        self.IMDB.update(self.movie)
        table_done[self.number] = 1
        print '==========unpdate done==============='
        self._Thread__stop()


def get(title):

    #import the package imdb
    try:
        import imdb
    except ImportError:
        print 'You bad boy!  You need to install the IMDbPY package!'
        sys.exit(1)

    i = imdb.IMDb()

    in_encoding = sys.stdin.encoding or sys.getdefaultencoding()
    out_encoding = sys.stdout.encoding or sys.getdefaultencoding()

    title = unicode(title, in_encoding, 'replace')
    try:
        # Do the search, and get the results (a list of Movie objects).
        results = i.search_movie(title)
    except imdb.IMDbError, e:
        print "Probably you're not connected to Internet.  Complete error report:"
        print e
        sys.exit(3)

    if not results:
        print 'No matches for "%s", sorry.' % title.encode(out_encoding, 'replace')
        sys.exit(0)

    print '======================================'

    
    # This is a Movie instance.
    movies = results[:5]
    #print "////image///: "+movies[0]['cover']
    #print movies[0].get('nb_votes').__str__()
    #print type(movies[0].get('title'))
    #print type(movies[0].get('runtimes').__str__())
    #print type(movies[0].get('story').__str__())
    number = 0
    for k in movies:
        ThreadUpdate(movie = k,IMDB = i, number = number).start()
        number = number + 1
    
    while (table_done[0]*table_done[1]*table_done[2]*table_done[3]*table_done[4] == 0):
        pass


    return movies
