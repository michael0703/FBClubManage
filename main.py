from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import time

FB_Url = 'https://facebook.com'
Club_Url = 'https://www.facebook.com/groups/1603769146534321/?sorting_setting=CHRONOLOGICAL'

class  ClubManage():
	def __init__(self, account, passwd):

		self.account = account
		self.passwd = passwd
		self.driver = webdriver.Chrome()
		
		#self.driver.set_window_size(1920,1080)
	def login(self):

		self.driver.get(FB_Url)
		self.driver.find_element_by_name("email").send_keys(self.account)
		self.driver.find_element_by_name("pass").send_keys(self.passwd)
		self.driver.find_element_by_xpath("//label[@id='loginbutton']/input").click()
	
	def EnterClub(self, Url):

		self.driver.get(Url);

	def LocateToTheLatest(self):

		flag = True
		while flag:
			posts = self.driver.find_elements_by_xpath("//div[@class='_5pcr userContentWrapper']")
			print(len(posts))
			time.sleep(1)
			for idx, post in enumerate(posts):
				if idx == 0:
					continue
				post_time = post.find_element_by_xpath(".//abbr[contains(@class,'_5ptz')]").get_attribute("title")
				if int(post_time.split()[0].split('-')[1]) != CurMonth:
					print("End of search!", post_time.split()[0].split('-')[1])
					flag = False
					break
			if flag:
				#roll down the page
				self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)") 
				print("Start to Roll the Page!")
				time.sleep(10)

	def SearchPost(self):
		
		# Use this func to first load all the CurMonth Post
		# Uncomment it when u need the whole result. OTHERWISE, COMMENT IT WHILE TESTING!
		#self.LocateToTheLatest()

		# Locate all the post in CurMonth
		posts = self.driver.find_elements_by_xpath("//div[@class='_5pcr userContentWrapper']")
		print(len(posts))
		time.sleep(2)
		
		# Traverse all the posts
		for idx, post in enumerate(posts):
			if idx == 0:
				continue
			
			# All the Post Information : timestamp, user, userlink, post-content
			post_time = post.find_element_by_xpath(".//abbr[contains(@class,'_5ptz')]").get_attribute("title")
			post_user = post.find_element_by_xpath(".//h5[contains(@class,'_14f3')]")
			post_userid = post.find_element_by_xpath(".//h5[contains(@class,'_14f3')]").find_element_by_xpath(".//a").get_attribute("href")
			#post_content = post.find_element_by_xpath(".//div[contains(@class, 'userContent')]").text
			print(post_userid, post_time)

			# Locate the Comments
			comments_box = post.find_elements_by_xpath(".//div[@class='_3b-9 _j6a']")
			if len(comments_box) == 0:
				continue
			comment_list = comments_box[0].find_elements_by_xpath(".//div[@role='article']")
			
			# Expand all the comments below
			roll_btn = comments_box[0].find_elements_by_xpath(".//a[@class='UFIPagerLink']")
			if len(roll_btn) > 0:
				ActionChains(self.driver).click(roll_btn[0]).perform()
				#print("success")
			time.sleep(3)				# important !! need to wait for the comment expand
			
			print("======")

			# Traverse all the comments
			for comment in comment_list:

				# All the Comment Information : user, userlink, comment-content, timestamp
				Comment_ActorandBody = comment.find_element_by_xpath(".//div[@class='UFIImageBlockContent _42ef']")
				Comment_Actor = Comment_ActorandBody.find_element_by_xpath(".//div[@class='UFICommentContent']").text.split()[0]
				Comment_ActorId = Comment_ActorandBody.find_element_by_xpath(".//a").get_attribute('href')
				
				# Use for debug. under shows the time of the "Comment" not the "Post"
				#Time_block = Comment_ActorandBody.find_element_by_xpath(".//div[@class='fsm fwn fcg UFICommentActions']")
				#Time_diff = Time_block.find_element_by_xpath(".//abbr[@class='UFISutroCommentTimestamp livetimestamp']").text

				print(Comment_Actor, Comment_ActorId)
			
			print("======")

if __name__ == '__main__':
	if len(sys.argv) <= 2:
		print("Not Enough Arguments: python main.py ACCOUNT PASSWD!")
		sys.exit()
	account, passwd = sys.argv[1], sys.argv[2]
	Manager = ClubManage(account, passwd)
	Manager.login()
	Manager.EnterClub(Club_Url)
	Manager.SearchPost()
	


		
	