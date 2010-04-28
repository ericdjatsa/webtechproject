#MovieCrawler, written by Eric Djatsa-Eurecom (3/06).
#
#About:
#
#Usage:
#
##################################Configuration Variables####################################################################################
BIT_DEPTH=2048 #depth to read to when check a file's md5 signature - used for excluding duplicates from the index, 2kb seems to work well
URL_BASES=['http://localhost/'] #url bases for the directories to be crawled,they are located on the NAS
#DIRS=['\\\\movies\\action\\','\\\\movies\\romance\\','\\\\acmecorp\\cartoons\\'] #directories to crawl
DIRS=['Movies/']
DIRS_BASES=['\\\\acmecorp\\action\\','\\\\acmecorp\\romance\\','\\\\acmecorp\\cartoons\\'] #web root of these directories 
CRAWL_EXT=['.avi','.mpeg','.divx','.wmv'] #file types to list
START_DIR=DIRS[0] #the directory where the 'master' url list is located - this list has hyperlinks to the other lists
OUT_FNAME='default.htm' #output filename
#############################################################################################################################################
import MySQLdb, time, os, os.path
from myCrawler.models import File
class crawler:
        #crawl a list of directories, creating a list of dictionary files which match acceptable file
        #extensions (CRAWL_EXT variable), dictionary keys are the file's md5 hash (computed to BIT_DEPTH
        #in the file), and the dictionary values are list of file objects for a given md5 value. 
	def __init__(self):
		print 'executing crawler.init()'
		self.start_time=time.time() #start time for progress and logging
        
	def crawl(self):
		#walk listed directories and then generate file 
		#objects (url, md5, path) for each acceptable file
		self.__walk()
		self.paths_unique=[]
		self.crawl_times=[]
		cnt_total=0; cnt=0

		#File.delete_all()
		
		for f_path in self.full_paths:
			paths_d={}                      #files - these dictonary files contain unique files to be indexed
			try:                        #catch various errors that may occur here - bad file names, files 
				f=File(filename=os.path.basename(f_path),path=f_path)
				f_ext=os.path.splitext(f.filename)[1]
				f.extension=f_ext
				print 'file:',f,'path:',f.path
				f_ext=os.path.splitext(f.filename)[1]
				f.genMD5(BIT_DEPTH)     #removed between the os.walk and this bit of execution, etc.
				if not paths_d.has_key(f.hash_code):
					print 'file info'
					print 'file extension:',f.extension
					#f.save()
					paths_d[f.hash_code]=[f.path]
				else:
					f_list=paths_d[f.hash_code]
					f_list.append(f)
					paths_d[f.hash_code]=f_list
			except:
				print 'Error processing', f_path
			self.paths_unique.append(paths_d)
		print 'paths unique',self.paths_unique
		#save results into DB
		
		
	def __walk(self):
		#walk the parent directories, saving a list of files to be indexed
		self.paths=[]
		self.full_paths=[]
		cnt=0
		for p in DIRS:
			print 'Scanning', p
			paths=[]
			found=0
			for dirpath, dirnames, filenames in os.walk(p):
				paths.extend([os.path.join(dirpath,p)])
				print 'filenames',filenames
				for i in filenames:
					if self.__ok_ext(i):
						found+=1
						#print len(paths), 'files found in', p+'.'
						self.paths.append(paths)
						self.full_paths.extend([os.path.join(dirpath,i)])
						tmp=len(paths)
						cnt+=tmp
			#print '%i files found in %s' %(tmp, p)
		print 'full paths',self.full_paths
		print 'A total of %i files were found in the %i directories scanned' %(found, len(DIRS))

	def __ok_ext(self,fname):
	#return TRUE for non-temporary files which meet one of the extensions to crawl
		f_ext=os.path.splitext(fname)[1] 
		if f_ext in CRAWL_EXT and fname[0]!='~':
			return True
		return False
	
