# coding:utf-8
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import time
import csv
import codecs
from datetime import date

Club_Url = 'https://www.facebook.com/groups/1603769146534321/?sorting_setting=CHRONOLOGICAL'
Club_MemberUrl = 'https://www.facebook.com/groups/huberstudents/members/'
driver_path = 'C:\Program Files (x86)\ChromeDriver\chromedriver.exe'

CurMonth = 6

class  ClubManage():
	def __init__(self, account, passwd):
		self.FB_Url = 'https://facebook.com'

		self.account = account
		self.passwd = passwd

		# Some default Chrome options
		chrome_options = webdriver.ChromeOptions()
		prefs = {"profile.default_content_setting_values.notifications" : 2}
		chrome_options.add_experimental_option("prefs",prefs)
		#chrome_options.add_argument('--headless')
		#chrome_options.add_argument('--disable-gpu')
		self.driver = webdriver.Chrome(driver_path, chrome_options=chrome_options)
		self.driver.set_window_size(1920,1080)

		# Create output files first
		self.postfd = open("Post.csv", "w")
		self.commentfd = open("Comment.csv", "w")
		self.likelistfd = open("Likelist.csv", "w")
		self.clubmemberfd = open('ClubMember.csv', 'w')

		self.postwriter = csv.writer(self.postfd)
		self.commentwriter = csv.writer(self.commentfd)
		self.likelistwriter = csv.writer(self.likelistfd)
		self.clubmemberwriter = csv.writer(self.clubmemberfd)

		# Add the Field
		self.postwriter.writerow(['UserName', 'UserId', 'PostTime'])
		self.commentwriter.writerow(['UserName', 'UserId', 'CommentTime'])
		self.likelistwriter.writerow(['UserName', 'UserId'])
		self.clubmemberwriter.writerow(['UserName', 'UserId', 'JoinDate'])

		# Kick out criteria
		self.kickday = 15

	def Login(self):

		# Login to FB
		self.driver.get(self.FB_Url)
		self.driver.find_element_by_name("email").send_keys(self.account)
		self.driver.find_element_by_name("pass").send_keys(self.passwd)
		self.driver.find_element_by_xpath("//label[@id='loginbutton']/input").click()


	def LocateToTheLatest(self):

		flag = True
		count = 15

		while flag:

			for i in range(count):
				self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)") 
				print("Start to Roll the Page!")
				time.sleep(4)

			count -= 3

			if count <= 3:
				count=3

			posts = self.driver.find_elements_by_xpath("//div[@class='_5pcr userContentWrapper']")
			print(len(posts))
			time.sleep(1)
			for idx, post in enumerate(posts):
				if idx == 0:
					continue
				post_time = post.find_element_by_xpath(".//abbr[contains(@class,'_5ptz')]").get_attribute("title")
				
				# It will GO WRONG when cross a year!!!!!!!!!!! Need to modify

				if int(post_time.split()[0].split('-')[1]) < CurMonth:
					print("End of search!", post_time.split()[0].split('-')[1])
					flag = False
					break
		self.driver.execute_script("window.scrollTo(0, 0)")
			
	def ParseId(self, data):

		# Parse the Id from href
		href = data[1].split('?')[1]
		if href[0] == 'i' and href[1] == 'd':
			data[1] = str(href.split('&')[0].split('=')[1])
		else:
			data[1] = str(data[1].split('?')[0].split('/')[-1])

	def WriteToFile(self, fd, data, Type):

		self.ParseId(data)
		encdata = [item.encode("cp950", "ignore").decode("cp950", "ignore") for item in data]
		if Type == 'Post':
			self.postwriter.writerow(encdata)
		elif Type == 'Comment':
			self.commentwriter.writerow(encdata)
		elif Type == 'Like':
			self.likelistwriter.writerow(encdata)
		elif Type == 'ClubMem':
			self.clubmemberwriter.writerow(encdata)
	
	def SearchPost(self, Url):
		self.driver.get(Url);
		
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
			print("======")
			print("Poster:")
			# All the Post Information : timestamp, user, userlink, post-content
			post_time = post.find_element_by_xpath(".//abbr[contains(@class,'_5ptz')]").get_attribute("title")
			post_user = post.find_element_by_xpath(".//h5[contains(@class,'_14f3')]")
			post_username =  post.find_element_by_xpath(".//h5[contains(@class,'_14f3')]").find_element_by_xpath(".//a").text
			post_userid = post.find_element_by_xpath(".//h5[contains(@class,'_14f3')]").find_element_by_xpath(".//a").get_attribute("href")
			#post_content = post.find_element_by_xpath(".//div[contains(@class, 'userContent')]").text
			print(post_username, post_time)

			self.WriteToFile(self.postfd, [post_username, post_userid, post_time], 'Post')

			#########################################
			# Locate the Like and Push the btn
#			try:			
			like_box = post.find_element_by_xpath(".//div[contains(@class,'_3399') and contains(@class,'_1f6t')]")
			like_btn = like_box.find_elements_by_xpath(".//a[@class='_2x4v']")
			ActionChains(self.driver).click(like_btn[0]).perform()
			#print("click the like expand button", like_btn[0])
			while len(self.driver.find_elements_by_xpath(".//li[@class='_5i_q']")) == 0:
				time.sleep(1)
			'''
			except:
				print("open like except")
				pass
			'''
			has_like_btn = True
			while has_like_btn:
				try:
					like_more_btn = self.driver.find_elements_by_xpath(".//a[contains(@class,'uiMorePagerPrimary')]")
					if len(like_more_btn) > 0:
						print("click the more like btn")
						ActionChains(self.driver).click(like_more_btn[0]).perform()
						time.sleep(3)
					else:
						has_like_btn = False
				except:
					has_like_btn = False

			time.sleep(1)
			like_list = self.driver.find_elements_by_xpath(".//li[@class='_5i_q']")
			print("Like Num:", len(like_list))

			# Traverse All the Like
			for like_block in like_list:
				like = like_block.find_element_by_xpath(".//div[@class='_6a _5j0c']")
				like_user = like.find_element_by_xpath(".//a").text
				like_id = like.find_element_by_xpath(".//a").get_attribute('href')
				print(like_user, like_id)

				self.WriteToFile(self.likelistfd, [like_user, like_id], 'Like')


			# End of Like search Need to click to close the list
			try:
				close_btn = self.driver.find_elements_by_xpath(".//a[contains(text(), '關閉')]")
				ActionChains(self.driver).click(close_btn[0]).perform()
				print("close the like")
			except:
				print("close like except")
				pass


			# Locate the Comments
			comments_box = post.find_elements_by_xpath(".//div[@class='_3b-9 _j6a']")
			if len(comments_box) == 0:
				print("no comments")
				continue
			
			#########################################
			# Expand all the comments below
			try:
				has_roll_btn = True
				while has_roll_btn:
					roll_btn = comments_box[0].find_elements_by_xpath(".//a[@class='UFIPagerLink']")
					if len(roll_btn) > 0:
						ActionChains(self.driver).click(roll_btn[0]).perform()
						time.sleep(3)
					else:
						has_roll_btn = False
			except:
				pass

			comment_expand = comments_box[0].find_elements_by_xpath(".//div[@class='UFIImageBlockContent _42ef _8u']")
			for comment_expand_btn in comment_expand:
				has_expand_btn = True
				while has_expand_btn:
					try:
						expand_btn = comment_expand_btn.find_elements_by_xpath(".//a[@class='UFIPagerLink']")
						expand_btn1 = comment_expand_btn.find_elements_by_xpath(".//span[contains(@class,'UFIReplySocialSentenceLinkText')]")
						if len(expand_btn) > 0:
							ActionChains(self.driver).click(expand_btn[0]).perform()
							print("press first kind button!")
							time.sleep(3)
						elif len(expand_btn1) > 0:
							ActionChains(self.driver).click(expand_btn1[0]).perform()
							print("press second kind button!")
							time.sleep(3)
						else:
							has_expand_btn = False
					except:
						has_expand_btn = False


			# Retrieve all the comments
			time.sleep(1)
			comment_list = comments_box[0].find_elements_by_xpath(".//div[@role='article']")

			print("Commentors: {}".format(str(len(comment_list))))

			# Traverse all the comments
			for comment in comment_list:

				# All the Comment Information : user, userlink, comment-content, timestamp
				Comment_ActorandBody = comment.find_element_by_xpath(".//div[@class='UFIImageBlockContent _42ef']")
				Comment_Actor = Comment_ActorandBody.find_element_by_xpath(".//div[@class='UFICommentContent']").find_element_by_xpath(".//a").text.split('\n')[0]
				Comment_ActorId = Comment_ActorandBody.find_element_by_xpath(".//a").get_attribute('href')
				Time_block = Comment_ActorandBody.find_element_by_xpath(".//div[@class='fsm fwn fcg UFICommentActions']")
				Comment_time = Time_block.find_element_by_xpath(".//abbr[@class='UFISutroCommentTimestamp livetimestamp']").get_attribute('title')

				self.WriteToFile(self.commentfd, [Comment_Actor, Comment_ActorId, Comment_time], 'Comment')
				print(Comment_Actor, Comment_ActorId)
			
			print("======")
	

	def isRecentAdd(self, AddDate, TodayDate):

		#print(int(AddDate), int(TodayDate))
		#print(TimeDiff)
		TimeDiff = int(TodayDate)-int(AddDate)
		TimeBound = self.kickday * 86400
		if TimeDiff <= TimeBound:
			return True
		else:
			return False




	def SearchClubList(self, Club_Url):
		
		self.driver.get(Club_Url)

		# Let the member sort by date

		option_btn = self.driver.find_element_by_xpath(".//div[@class='_6a _6b rfloat _ohf']").find_element_by_xpath(".//a")
		ActionChains(self.driver).click(option_btn).perform()
		option_btn1 = self.driver.find_element_by_xpath(".//div[@class='_54ng']").find_element_by_xpath(".//span[contains(text(), '加入日期')]")
		ActionChains(self.driver).click(option_btn1).perform()

		time.sleep(3)
		print("Done first Part")

		# let the program works better

		NowProcess = 0
		LastProcess = 0
		
		# notice when can we stop
		
		last_height = self.driver.execute_script("return document.body.scrollHeight")
		new_height = -1

		# One time Process a page and then Scorll 

		while True:

			member_block = self.driver.find_element_by_xpath(".//div[@id='groupsMemberSection_all_members']")
			member_list = member_block.find_elements_by_xpath(".//div[@class='clearfix _60rh _gse']")
			NowProcess = len(member_list)
			print(LastProcess, NowProcess)

			for midx in range(NowProcess-LastProcess):
				member_info_block = member_list[LastProcess+midx].find_element_by_xpath(".//div[@class='clearfix _8u _42ef']")
				member_name_info = member_info_block.find_element_by_xpath(".//div[@class='_60ri fsl fwb fcb']")
				member_name = member_name_info.text
				try:
					member_id = member_list[LastProcess+midx].find_element_by_xpath(".//a[@class='_60rg _8o _8r lfloat _ohe']").get_attribute('href')
				except:
					member_id = "xxxxxxx?Doesn't_Have_url"

				try:
					member_time = member_info_block.find_element_by_xpath(".//div[@class='_60rj']/abbr").get_attribute('title')
					member_utime = member_info_block.find_element_by_xpath(".//div[@class='_60rj']/abbr").get_attribute('data-utime')
					member_time = member_time.split()[0].split('年')[0] +'-'+ member_time.split()[0].split('年')[1].split('月')[0] +'-'+ member_time.split()[0].split('月')[1].split('日')[0]
				except:
					member_utime = time.time()
					member_time = str(date.today())
				#print(member_name, member_time, member_id)
				if not self.isRecentAdd(member_utime, time.time()):
					print(member_name, member_time)
					self.WriteToFile(self.clubmemberfd, [member_name, member_id, member_time], 'ClubMem')
				
				
			LastProcess = len(member_list)

			self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
			time.sleep(3)

			new_height = self.driver.execute_script("return document.body.scrollHeight")
			if new_height == last_height:
				print("end!")
				break
			last_height = new_height

if __name__ == '__main__':
	if len(sys.argv) <= 2:
		print("Not Enough Arguments: python main.py ACCOUNT PASSWD!")
		sys.exit()
	account, passwd = sys.argv[1], sys.argv[2]
	Manager = ClubManage(account, passwd)
	Manager.Login()

	#Manager.SearchPost(Club_Url)

	Manager.SearchClubList(Club_MemberUrl)

	


		
	