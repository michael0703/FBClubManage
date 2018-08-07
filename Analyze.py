import math
import time
import csv

class UnionFile():
	
	def __init__(self, firstfilename, secondfilename, thirdfilename):

		self.fstfd = open(firstfilename, 'r')
		self.scdfd = open(secondfilename, 'r')
		self.trdfd = open(thirdfilename, 'r')
		self.analyzefd = open("analyze.csv", 'w')

		self.FirstCsvReader = csv.reader(self.fstfd)
		self.SecondCsvReader = csv.reader(self.scdfd)
		self.ThirdCsvReader = csv.reader(self.trdfd)
		self.Analyzewriter = csv.writer(self.analyzefd)

		self.firstset = set()
		self.secondset = set()
		self.thirdset = set()
		self.unionset = set()
		self.diffset = set()

	def InitSet(self):
		# put the csv file in the memory

		self.firstset = set([x[0] for x in self.FirstCsvReader if len(x) > 0] )
		self.secondset = set([x[0] for x in self.SecondCsvReader  if len(x) > 0])
		self.thirdset = set([x[0] for x in self.ThirdCsvReader  if len(x) > 0])
		

	def Union(self):

		self.unionset = self.firstset | self.secondset

	def Diff(self):

		self.diffset = self.thirdset - self.unionset

	def PrintSet(self):

		print(self.firstset)
		print(self.secondset)
		print(self.thirdset)
		print(self.diffset)
		print('==========')

	def WriteFile(self):

		for name in self.diffset:
			print(name)
			self.Analyzewriter.writerow([name, ''])



if __name__ == '__main__':

	U = UnionFile('Comment.csv', 'Likelist.csv', 'ClubMember.csv')
	U.InitSet()
	U.Union()
	U.Diff()
	U.PrintSet()
	U.WriteFile()

		
		