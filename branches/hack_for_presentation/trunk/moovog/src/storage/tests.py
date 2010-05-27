from store_movie import *
from moovog.src.crawler.models import *
from moovog import imdb 

def test():
    i = imdb.IMDb()
    film = i.search_movie('avatar')[0]
    i.update(film)
    fichier = File.objects.all()[0]
    data = Store_movie(film,fichier)
    data.start()
