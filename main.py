from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from lxml import etree, html
import sys

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
		#root = etree.fromstring(self.driver.page_source, etree.HTMLParser());
		#print("=====")
		#print(len(root.xpath("//div[@class='_5pcr userContentWrapper']")))
		#posts = self.driver.find_elements_by_css_selector("[class = "_1dwg _1w_m _q7o"]")
		posts = self.driver.find_elements_by_xpath("//*[@id='comment_js_jc']/div/div/div/div[2]/div/div/div[1]/div[1]/div/span")
		print(len(posts))
		'''
		for post in posts:
			resp=[]
			resp = post.find_elements_by_xpath("//span[@class='UFICommentActorAndBody']")
			print(len(resp))
			print("========")
		'''
if __name__ == '__main__':
	if len(sys.argv) <= 2:
		print("Not Enough Arguments: python main.py ACCOUNT PASSWD!")
		sys.exit()
	account, passwd = sys.argv[1], sys.argv[2]
	Manager = ClubManage(account, passwd)
	Manager.login()
	Manager.EnterClub(Club_Url)
	Manager.SearchPost()
	


		
	