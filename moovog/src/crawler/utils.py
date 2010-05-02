#MovieCrawler, written by Eric Djatsa-Eurecom (3/06).
#
#About:
#
#Usage:
#
###############################Configuration Variables#######################################################################
BIT_DEPTH=2048 #depth to read to when check a file's md5 signature - used for excluding duplicates from the index, 2kb seems to work well
URL_BASES=['http://localhost/'] #url bases for the directories to be crawled,they are located on the NAS
#DIRS=['\\\\movies\\action\\','\\\\movies\\romance\\','\\\\acmecorp\\cartoons\\'] #directories to crawl
DIRS=['/home/edy/Videos/Movies']
DIRS_BASES=['\\\\acmecorp\\action\\','\\\\acmecorp\\romance\\','\\\\acmecorp\\cartoons\\'] #web root of these directories 
CRAWL_EXT=['.avi','.mpeg','.divx','.wmv'] #file types to list
START_DIR=DIRS[0] #the directory where the 'master' url list is located - this list has hyperlinks to the other lists
#############################################################################################################################################
import MySQLdb, time, os, os.path
import django
from models import File
class Crawler:
        #crawl a list of directories, creating a list of dictionary files which match acceptable file
        #extensions (CRAWL_EXT variable), dictionary keys are the file's md5 hash (computed to BIT_DEPTH
        #in the file), and the dictionary values are list of file objects for a given md5 value. 
	def __init__(self):
		self.start_time=time.time() #start time for progress and logging

        def walk(self):
		#walk the parent directories, saving a list of files to be indexed
		self.paths=[]
		self.full_paths=[]
		cnt=0
		for p in DIRS:
			paths=[]
			found=0
			for dirpath, dirnames, filenames in os.walk(p):
				paths.extend([os.path.join(dirpath,p)])
				for f in filenames:
					if self.__ok_ext(f):
						found+=1
						self.full_paths.extend([os.path.join(dirpath,f)])

	def __ok_ext(self,fname):
	#return TRUE for non-temporary files which meet one of the extensions to crawl
		f_ext=os.path.splitext(fname)[1] 
		if f_ext in CRAWL_EXT and fname[0]!='~':
			return True
		return False

	def crawl(self):
		#walk listed directories and then generate file 
		#objects (url, md5, path) for each acceptable file
		self.walk()
		self.Files={} #dictionary : {key=file_hash,value=file}
		self.paths_unique=[] #this is a list [key=file_hash, value= file_path]
		#self.crawl_times=[]
		cnt_total=0; cnt=0
		
		for f_path in self.full_paths:
			paths_d={}                  #files - these dictonary files contain unique files to be indexed
			try:                        #catch various errors that may occur here - bad file names, files 
				f=File(filename=os.path.basename(f_path),path=f_path)
				f_ext=os.path.splitext(f.filename)[1]
				f.extension=f_ext[1:]
				
				f.genMD5(BIT_DEPTH)
				if not paths_d.has_key(f.hash_code):
					paths_d[f.hash_code]=[f.path]
				else:
					paths_d[f.hash_code].append(f.path)
			except:
				print 'Error processing', f_path
			self.Files[f.hash_code]=f
			self.paths_unique.append(paths_d)

	def saveToDB(self):
		print 'looping into files'
		for (k,f) in self.Files.items():
			#save results into DB
			f.save()
    
