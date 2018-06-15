from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
		time.sleep(2)
		for idx, post in enumerate(posts):
			if idx == 0:
				continue
			comments_box = post.find_elements_by_xpath(".//div[@class='_3b-9 _j6a']")
			if len(comments_box) == 0:
				continue
			roll_btn = comments_box[0].find_elements_by_xpath(".//a[@class='UFIPagerLink']")
			if len(roll_btn) > 0:
				ActionChains(self.driver).click(roll_btn[0]).perform()
				print("success")
			time.sleep(3)				# important !! need to wait for the comment expand
			comment_list = comments_box[0].find_elements_by_xpath(".//div[@role='article']")
			print(len(comment_list))




if __name__ == '__main__':
	if len(sys.argv) <= 2:
		print("Not Enough Arguments: python main.py ACCOUNT PASSWD!")
		sys.exit()
	account, passwd = sys.argv[1], sys.argv[2]
	Manager = ClubManage(account, passwd)
	Manager.login()
	Manager.EnterClub(Club_Url)
	Manager.SearchPost()
	


		
	