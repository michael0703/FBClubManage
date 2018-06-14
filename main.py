from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from lxml import etree, html
import sys
import time

FB_Url = 'https://facebook.com'
Club_Url = 'https://www.facebook.com/groups/huberstudents/'

class  ClubManage():
	def __init__(self, account, passwd):
		self.account = account
		self.passwd = passwd
		self.driver = webdriver.Chrome()
	def login(self):
		self.driver.get(FB_Url)
		self.driver.find_element_by_name("email").send_keys(self.account)
		self.driver.find_element_by_name("pass").send_keys(self.passwd)
		self.driver.find_element_by_xpath("//label[@id='loginbutton']/input").click()
	def EnterClub(self, Url):
		self.driver.get(Url);
	def SearchPost(self):
		posts = self.driver.find_elements_by_xpath("//div[@class='_5pcr userContentWrapper']")
		#xpath = "//div[@class='_5pcr userContentWrapper']//span[@class='UFICommentActorAndBody']"
		time.sleep(2)
		print(len(posts), "======")
		for idx, post in enumerate(posts):
			if idx == 0:
				continue

			target = post.find_elements_by_xpath(".//div[@class='UFIlist']")
			time.sleep(2)
			print(len(target))
			if(len(target) >= 1):
				print(target[0])



if __name__ == '__main__':
	if len(sys.argv) <= 2:
		print("Not Enough Arguments: python main.py ACCOUNT PASSWD!")
		sys.exit()
	account, passwd = sys.argv[1], sys.argv[2]
	Manager = ClubManage(account, passwd)
	Manager.login()
	Manager.EnterClub(Club_Url)
	Manager.SearchPost()
	


		
	