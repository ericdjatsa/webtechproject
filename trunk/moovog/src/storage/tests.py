from store_movie import *
from moovog.src.crawler.models import *
from moovog import imdb 

def test(list_of_titles):
    for title in list_of_titles:
        i = imdb.IMDb()
        film = i.search_movie(title)[0]
        i.update(film)
        fichier = File.objects.all()[0]
        data = Store_movie(film,fichier)
        data.start()

class Thread_Test(threading.Thread):
    
    def __init__(self, name):
        threading.Thread.__init__(self, name = name)
    
    def run(self):
        j = 0
        for i in range(1,1000000): j+=i/2
        print i
        return i
    
def thread_test():
    print "currently active : %s" % str(threading.active_count())
    thread_1 = Thread_Test("thread_1")
    thread_1.start()
    print "current thread : %s" % str(thread_1.name)
    print "currently active : %s" % str(threading.active_count())
    thread_2 = Thread_Test("thread_2")
    thread_2.start()
    print "current thread : %s" % str(thread_2.name)
    print "currently active : %s" % str(threading.active_count())
    thread_3 = Thread_Test("thread_3")
    thread_3.start()
    print "current thread : %s" % str(thread_3.name)
    print "currently active : %s" % str(threading.active_count())
    while threading.active_count() > 1: pass
    print "counting DONE."
    
def drop_seeker_tables():
    # http://docs.djangoproject.com/en/dev/topics/db/sql/#executing-custom-sql-directly
    from django.db import connection, transaction
    cursor = connection.cursor()
    cursor.execute("DROP TABLE `seeker_actor_model`, `seeker_aka_model`, `seeker_aka_model_countries`, `seeker_award_category_model`, `seeker_award_matcher_model`, `seeker_award_model`, `seeker_character_model`, `seeker_country_model`, `seeker_director_model`, `seeker_genre_model`, `seeker_imdb_object_model`, `seeker_movie_model`, `seeker_movie_model_actors`, `seeker_movie_model_directors`, `seeker_movie_model_genres`, `seeker_movie_model_original_countries`, `seeker_movie_model_writers`, `seeker_release_date_model`, `seeker_release_date_model_countries`, `seeker_test_movie_model`, `seeker_writer_model`;")
    transaction.commit_unless_managed()
    