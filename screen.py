# coding:utf-8
import sys
import signal
import threading
import tkinter as tk
from tkinter import ttk  
from tkinter.scrolledtext import ScrolledText
import time
import crawl
import Analyze

Club_Url = 'https://www.facebook.com/groups/1603769146534321/?sorting_setting=CHRONOLOGICAL'
Club_MemberUrl = 'https://www.facebook.com/groups/huberstudents/members/'

CurMonth = 6

class RedirectText(object):
  def __init__(self, text_ctrl):
    self.output = text_ctrl

  def write(self, string):
    self.output.insert(tk.END, string)

  def flush(self):
    pass

class MainApplication():
  def __init__(self, master=None):
    master.title('FB社團神器')
    #master.resizable(0,0)

    self.isLogin = False
    self.Manager = None
    self.Analyzer = None


    self.master = master
    self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
    self.createInputs()
    self.createTextfield()
    self.createButtons()

    self.refresh()


  def refresh(self):
    self.master.update()
    self.master.after(1000,self.refresh)


  def on_closing(self):
    if self.Manager:
      self.Manager.driver.quit()

    self.master.destroy()

    
  def createInputs(self):
    self.mainFrame = tk.Frame(self.master, pady=5, padx=3, bg="white")
    self.mainFrame.grid(row=0, sticky="nsew")

    self.usernameLabel  = ttk.Label(self.mainFrame, text="帳號", background="#fff")
    self.usernameLabel.grid(column=0, row=0, sticky='w')
    self.usernameInput = ttk.Entry(self.mainFrame)
    self.usernameInput.grid(column=1, row=0)

    self.passwordLabel  = ttk.Label(self.mainFrame, text="密碼", background="#fff")
    self.passwordLabel.grid(column=0, row=1, sticky='w')
    self.passwordInput = ttk.Entry(self.mainFrame, show='*')
    self.passwordInput.grid(column=1, row=1)

    self.urlLabel  = ttk.Label(self.mainFrame, text="社團網址", background="#fff")
    self.urlLabel.grid(column=0, row=2, sticky='w')
    self.urlInput = ttk.Entry(self.mainFrame)
    self.urlInput.grid(column=1, row=2)


  def createTextfield(self):
    # self.scrollbar = tk.Scrollbar(self.master)
    # self.scrollbar.grid(column=1, row=1, sticky='e', padx=5)

    # self.text = tk.Text(self.master,yscrollcommand=self.scrollbar.set)
    # self.text = tk.Text(self.master, height=5)
    self.text = tk.scrolledtext.ScrolledText(self.master, height=20)
    self.text.grid(column=0, row=1, sticky='w', padx=5)

    # redirect stdout to text field
    redir = RedirectText(self.text)
    sys.stdout = redir


  def createButtons(self):
    self.button1 = ttk.Button(self.master,text="爬社團成員名單", command=self.crawlClubList)
    self.button1.grid(row=2, sticky='we', padx=5)

    self.button2 = ttk.Button(self.master,text="爬Po文/回覆/按讚名單", command=self.crawlPost)
    self.button2.grid(row=3, sticky='we', padx=5)

    self.button3 = ttk.Button(self.master,text="爬潛水名單", command=self.crawlAnalyze)
    self.button3.grid(row=4, sticky='we', padx=5, pady=(0,5))


  def printInfo(self):
    print(self.usernameInput.get())
    self.text.insert( tk.END, self.usernameInput.get() )


  def fbLogin(self):
    try:
      account, passwd = self.usernameInput.get(), self.passwordInput.get()
      club_Url = self.urlInput.get() # Club URL
      self.Manager = crawl.ClubManage(account, passwd)
      self.Manager.Login()
      self.text.insert( tk.END, "Login!\n" )
      self.isLogin = True

    except KeyboardInterrupt:
      self.Manager.driver.quit()


  def crawlClubList(self):
    if not self.isLogin:
      self.fbLogin()  

    self.Manager.SearchClubList(Club_MemberUrl)


  def crawlPost(self):
    if not self.isLogin:
      print("登入中，請稍待...\n")
      #threading.Thread(target=self.fbLogin).start()
      self.fbLogin()
    self.Manager.SearchPost(Club_Url)

  def crawlAnalyze(self):

    self.Analyzer = Analyze.UnionFile('Comment.csv', 'Likelist.csv', 'ClubMember.csv')
    self.Analyzer.InitSet()
    self.Analyzer.Union()
    self.Analyzer.Diff()
    self.Analyzer.PrintSet()
    self.Analyzer.WriteFile()



if __name__ =='__main__':
  window = tk.Tk()
  app = MainApplication(master=window)
  window.mainloop()