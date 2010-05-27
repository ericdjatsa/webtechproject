Hi to all,this is a small guide to explain how to use the crawler module:

1)Create the web_tech database if you don't have it yet
$ mysql -u root -p
(you need the password you gave at the mysql installation)
>create database web_tech;
>grant all privileges on web_tech.* to 'web_tech_user'@'localhost' identified by 
'web_tech_user';

2) open a new console and move to the moovog diretory of your svn folder :
$ cd svn/moovog
edit the utils.py file and modify the line 11
DIRS=['/home/edy/Videos/Movies'] replace '/home/edy/Videos/Movies' with your local directory where you have some movie files with extension ".avi",".wmv",".divx" etc...
TIP: you can just create dummy movie files into a local directory(e.g: /home/<user>/Movies) using this command lines:
$cd  #in order to go to your home directory
$mkdir Movies
$cd Movies
$ echo -e "Avatar \n Avatar \n Avatar \n " >> Avatar.avi
$ echo -e "Titanic \n Titanic \n Titanic \n " >> Titanic.wmv
and so on with every movie title you have in mind

when you are done, change the DIRS variable in utils.py to be: DIRS=['/home/<user>/Movies']

3)Now launch syncdb
$python manage.py syncdb
this will create the tables associated to the models
to check if the tables have been created correctly go to the mysql console and type:
>show databases #this should show a list of existing databases where you also find the database "web_tech"
> use web_tech
>show tables from web_tech # this will list all tables in web_tech database,you should see a table named crawler_file
2)Now we will use the Crawler,into the moovog directory open a python shell:
$ cd svn/moovog
$ python manage.py shell
>>>from src.crawler.utils import *
>>> from src.crawler.models import *
>>> myC=Crawler() # create a Crawler object
>>> myC.crawl()
>>>myc.saveToDB()

To check if the files found where saved to the DB,go back to the mysql console and type:
>select * from crawler_file ; 
You should see records like in the following figure:
+----+----------------+-----------+------------------------------------------------+----------------------------------+
| id | filename       | extension | path                                           | hash_code                        |
+----+----------------+-----------+------------------------------------------------+----------------------------------+
|  1 | Madagascar.wmv | wmv       | /home/edy/Videos/Movies/Cartoon/Madagascar.wmv | 6776f939662afbb5c1319c1a89f0e84f | 
|  2 | Avatar.avi     | avi       | /home/edy/Videos/Movies/Action/Avatar.avi      | 9798b49dd5815877236821c05007b36d | 
|  3 | 24h.divx       | divx      | /home/edy/Videos/Movies/Action/24h.divx        | 2ecd3c59f5b45d256e1ded6441ff4577 | 
|  4 | IronMan.wmv    | wmv       | /home/edy/Videos/Movies/Action/IronMan.wmv     | 69f7ee71badd2eb8620c1c9047ad1168 | 
|  5 | Titanic.avi    | avi       | /home/edy/Videos/Movies/Romance/Titanic.avi    | 500196d994f7f07b1d834afe6506140f | 
|  6 | Marimar.divx   | divx      | /home/edy/Videos/Movies/Romance/Marimar.divx   | f46d3aefb5ac55c314ab0e8fdcc41d4a | 
+----+----------------+-----------+------------------------------------------------+----------------------------------+
6 rows in set (0.00 sec)

That's it you're done! Go and take a coffee :-)

Please report any error encountered so that I can update this how to and correct the module if necessary.
Happy Coding ;-)
Eric

