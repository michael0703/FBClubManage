import math
import time
import csv

class UnionFile():
	
	def __init__(self, firstfilename, secondfilename):

		self.fstfd = open(firstfilename, 'r')
		self.scdfd = open(secondfilename, 'r')

		self.FirstCsvReader = csv.reader(self.fstfd)
		self.SecondCsvReader = csv.reader(self.scdfd)

		self.firstset = set()
		self.secondset = set()
		self.unionset = set()

	def InitSet(self):
		# put the csv file in the memory

		self.firstset = set([x[1] for x in self.FirstCsvReader])
		self.secondset = set([x[1] for x in self.SecondCsvReader])

	def Union(self):

		self.unionset = self.firstset & self.secondset

	def PrintSet(self):

		print(self.unionset)

if __name__ == '__main__':

	U = UnionFile('a.csv', 'b.csv')
	U.InitSet()
	U.Union()
	U.PrintSet()

		
		