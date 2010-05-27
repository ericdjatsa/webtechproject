from store_movie import *
from moovog.src.crawler.models import *
import imdb 

def test():
    i = imdb.IMDb()
    film = i.search_movie('avatar')[0]
    fichier = File.objects.all()[0]
    data = store_movie(film,fichier)
