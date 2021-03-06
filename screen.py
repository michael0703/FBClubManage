# coding:utf-8
import sys
import signal
import threading
from queue import Queue
import tkinter as tk
from tkinter import ttk  
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import time
import pickle
import os.path

import crawl
import Analyze

# Club_Url = 'https://www.facebook.com/groups/1603769146534321/?sorting_setting=CHRONOLOGICAL'
# Club_MemberUrl = 'https://www.facebook.com/groups/huberstudents/members/'

CurMonth = 8

SAVE_FILE = "save.pkl"

class RedirectText(object):
  def __init__(self, text_ctrl):
    self.output = text_ctrl

  def write(self, string):
    self.output.insert(tk.END, string)
    self.output.see(tk.END)

  def flush(self):
    pass

class MainApplication():
  def __init__(self, master=None):
    master.title('FB社團神器')
    #master.resizable(0,0)

    self.isLogin = False
    self.Manager = None
    self.Analyzer = None

    self.account = ""
    self.passwd = ""
    self.club_Url = ""

    self.master = master
    self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
    self.createInputs()
    self.createTextfield()
    self.createButtons()
    self.master.lift()
    self.master.attributes("-topmost", True)

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

    if os.path.exists(SAVE_FILE):
      data = pickle.load(open(SAVE_FILE, "rb"))
      self.usernameInput.insert(tk.END, data["username"])
      self.passwordInput.insert(tk.END, data["password"])
      self.urlInput.insert(tk.END, data["url"])


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
    self.button1 = ttk.Button(self.master,text="爬社團成員名單", command=self.crawlClubListThread)
    self.button1.grid(row=2, sticky='we', padx=5)

    self.button2 = ttk.Button(self.master,text="爬Po文/回覆/按讚名單", command=self.crawlPostThread)
    self.button2.grid(row=3, sticky='we', padx=5)

    self.button3 = ttk.Button(self.master,text="爬潛水名單", command=self.crawlAnalyzeThread)
    self.button3.grid(row=4, sticky='we', padx=5, pady=(0,5))


  def printInfo(self):
    print(self.usernameInput.get())
    self.text.insert( tk.END, self.usernameInput.get() )


  def fbLogin(self):
    try:
      print("登入中，請稍待...\n")
      self.account, self.passwd = self.usernameInput.get(), self.passwordInput.get()
      self.club_Url = self.urlInput.get() # Club URL
      self.Manager = crawl.ClubManage(self.account, self.passwd)
      if not self.Manager.Login():
        print("登入失敗!請再輸入一次")
        return
      self.text.insert( tk.END, "Login!\n" )
      self.isLogin = True

      data = {
        "username": self.account,
        "password": self.passwd,
        "url": self.club_Url
      }
      pickle.dump(data, open(SAVE_FILE, "wb"))

    except KeyboardInterrupt:
      self.Manager.driver.quit()


  def crawlClubListThread(self):
    threading.Thread(target=self.crawlClubList).start()

  def crawlClubList(self):
    if not self.isLogin:
      self.fbLogin()

    club_MemberUrl = ""

    if self.club_Url[-1] == '/':
      club_MemberUrl = self.club_Url + "members/"
    else:
      club_MemberUrl = self.club_Url + "/members/"

    self.Manager.SearchClubList(club_MemberUrl)
    messagebox.showinfo("社團爬蟲完畢" , "社團名單爬蟲完畢! 名單檔案為 ClubMember.csv")


  def crawlPostThread(self):
    threading.Thread(target=self.crawlPost).start()

  def crawlPost(self):
    if not self.isLogin:
      self.fbLogin()

    club_Url_Recent = ""

    if self.club_Url[-1] == '/':
      club_Url_Recent = self.club_Url + "?sorting_setting=CHRONOLOGICAL/"
    else:
      club_Url_Recent = self.club_Url + "/?sorting_setting=CHRONOLOGICAL/"

    self.Manager.SearchPost(club_Url_Recent)
    messagebox.showinfo("社團爬蟲完畢" , "社團Po文爬蟲完畢! 名單檔案為 Post.csv, Comment.csv, Likelist.csv")


  def crawlAnalyzeThread(self):
    threading.Thread(target=self.crawlAnalyze).start()

  def crawlAnalyze(self):

    try:
      self.Analyzer = Analyze.UnionFile('Comment.csv', 'Likelist.csv', 'ClubMember.csv')
      self.Analyzer.InitSet()
      self.Analyzer.Union()
      self.Analyzer.Diff()
      self.Analyzer.PrintSet()
      self.Analyzer.WriteFile()
    except:
      try:
        tmpfile3fd = open('ClubMember.csv', 'r')
        tmpfile3fd.close()
      except:
        #print('缺少社團成員名單,開始爬社團成員')
        self.crawlClubList()

      try:
        tmpfile1fd = open('Comment.csv', 'r')
        tmpfile2fd = open('Likelist.csv', 'r')
        tmpfile1fd.close()
        tmpfile2fd.close()
      except:
        #print('缺少Post,開始爬留言按讚...')
        self.crawlPost()

      
      #print('重新開始分析潛水名單...')
      self.Analyzer = Analyze.UnionFile('Comment.csv', 'Likelist.csv', 'ClubMember.csv')
      self.Analyzer.InitSet()
      self.Analyzer.Union()
      self.Analyzer.Diff()
      self.Analyzer.PrintSet()
      self.Analyzer.WriteFile()


if __name__ =='__main__':
  window = tk.Tk()
  app = MainApplication(master=window)
  print('再執行以下功能前，請先輸入帳號密碼以及社團網址!!!')
  window.mainloop()