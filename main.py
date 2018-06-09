from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains


FB_Url = 'https://facebook.com'

class  ClubManage():
	def __init__(self, account, passwd):
		self.account = account
		self.passwd = passwd

	def login(self):
		driver = webdriver.Chrome()
		driver.get(FB_Url)
		driver.find_element_by_name("email").send_keys(self.account)
		driver.find_element_by_name("pass").send_keys(self.passwd)
		driver.find_element_by_xpath("//label[@id='loginbutton']/input").click()

if __name__ == '__main__':
	print("xxxx")
	ClubManage('0972795235', 'xxxxxxxxxxx').login()
		


		
	