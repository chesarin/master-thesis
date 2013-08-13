from interfaces.idistancemetric import IDistanceMetric
import zipfile
import os


class ZipMetric(IDistanceMetric):

	def distance(self,fp1,fp2):
		m1 = fp1.get_malware()
		m2 = fp2.get_malware()
		filename = 'combine-zip'
		with zipfile.ZipFile(filename,'w',zipfile.ZIP_DEFLATED) as czip:
			czip.write(m1.get_path())
			czip.write(m2.get_path())
		czip.close()
		finfo = os.stat(filename)
		distance = float(finfo.st_size) / ( m1.get_size() +
											m2.get_size())
		print str(finfo.st_size)
		print str(m1.get_size())
		print str(m2.get_size())
		os.remove(filename)
		return (distance*100)

	def distance2(self,fp1,fp2):
		m1 = fp1.get_malware()
		m2 = fp2.get_malware()
		filename1 = 'zip1'
		with zipfile.ZipFile(filename1,'w',zipfile.ZIP_DEFLATED) as zip1:
			zip1.write(m1.get_path())
		zip1.close()
		filename2 = 'zip2'
		with zipfile.ZipFile(filename2,'w',zipfile.ZIP_DEFLATED) as zip2:
			zip2.write(m1.get_path())
		zip2.close()
		cfilename = 'combine-zip'
		with zipfile.ZipFile(cfilename,'w',zipfile.ZIP_DEFLATED) as czip:
			czip.write(m1.get_path())
			czip.write(m2.get_path())
		czip.close()
		m1info = os.stat(filename1)
		m2info = os.stat(filename2)
		cfinfo = os.stat(cfilename)
		distance = float(cfinfo.st_size) / ( m1info.st_size +
											 m2info.st_size)
		print str(cfinfo.st_size)
		print str(m1info.st_size)
		print str(m2info.st_size)
		os.remove(filename1)
		os.remove(filename2)
		os.remove(cfilename)
		return (distance*100)

