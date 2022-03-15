import threading

import requests
import os
import sys
import random
from requests import get
import socket
import time
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QSize
#importing Widgtes
from PyQt5.QtWidgets import *
#importing Engine Widgets
from PyQt5.QtWebEngineWidgets import *
#importing QtCore to use Qurl
from PyQt5.QtCore import *
#main window class (to create a window)-sub class of QMainWindow class

class Window(QMainWindow):
    #defining constructor function
    def __init__(self):
        #creating connnection with parent class constructor
        super().__init__()
        QMainWindow.__init__(self)
        self.setMinimumSize(QSize(300, 200))
        self.setWindowTitle("Website Cloner By Khaled Alshanbari")
        #---------------------adding browser-------------------
        self.browser = QWebEngineView()
        #setting url for browser, you can use any other url also
        self.browser.setUrl(QUrl('http://google.com'))
        #to display google search engine on our browser
        self.setCentralWidget(self.browser)
        #-------------------full screen mode------------------
        #to display browser in full screen mode, you may comment below line if you don't want to open your browser in full screen mode
        self.showMaximized()
        #----------------------navbar-------------------------
        #creating a navigation bar for the browser
        navbar = QToolBar()
        #adding created navbar
        self.addToolBar(navbar)
        #-----------------prev Button-----------------
        #creating prev button
        CloneBtn = QAction('Clone',self)
        #when triggered set connection
        CloneBtn.triggered.connect(self.clickMethod)
        # adding prev button to the navbar
        navbar.addAction(CloneBtn)
        # -----------------prev Button-----------------
        # creating prev button
        prevBtn = QAction('Prev', self)
        # when triggered set connection
        prevBtn.triggered.connect(self.browser.back)
        # adding prev button to the navbar
        navbar.addAction(prevBtn)
        #-----------------next Button---------------
        nextBtn = QAction('Next',self)
        nextBtn.triggered.connect(self.browser.forward)
        navbar.addAction(nextBtn)
        #-----------refresh Button--------------------
        refreshBtn = QAction('Refresh',self)
        refreshBtn.triggered.connect(self.browser.reload)
        navbar.addAction(refreshBtn)
        #-----------home button----------------------
        homeBtn = QAction('Home',self)
        #when triggered call home method
        homeBtn.triggered.connect(self.home)
        navbar.addAction(homeBtn)
        #---------------------search bar---------------------------------
        #to maintain a single line
        self.searchBar = QLineEdit()
        #when someone presses return(enter) call loadUrl method
        self.searchBar.returnPressed.connect(self.loadUrl)
        #adding created seach bar to navbar
        navbar.addWidget(self.searchBar)
        #if url in the searchBar is changed then call updateUrl method
        self.browser.urlChanged.connect(self.updateUrl)

    #method to navigate back to home page


    def clickMethod(self):
        self.close()

    def home(self):
        self.browser.setUrl(QUrl('http://google.com'))
    #method to load the required url
    def loadUrl(self):
        #fetching entered url from searchBar
        url = self.searchBar.text()
        #loading url
        self.browser.setUrl(QUrl(url))
    #method to update the url
    def updateUrl(self, url):
        #changing the content(text) of searchBar
        self.searchBar.setText(url.toString())
MyApp = QApplication(sys.argv)
#setting application name
QApplication.setApplicationName('Khaled Alshanbari')
#creating window
window = Window()
#executing created app
MyApp.exec_()
def Handler(c):
        # c.send('Server Online\n') # This is invalid HTTP header
        c.recv(1000)  # should receive request from client. (GET ....)
        c.send('HTTP/1.0 200 OK\n'.encode())
        c.send('Content-Type: text/html\n'.encode())
        c.send('\n'.encode())  # header and body should be separated by additional newline
        c.send(str(open(f'{desktop}/ClonedWebsite.html', 'r+').read()).encode())  # Use triple-quote string.
        c.close()
def get_Desktop():
    desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
    return desktop


try:
    desktop = get_Desktop()
    url = window.searchBar.text()
    if "https://" not in url:
        url = "https://"+url

    request = requests.get(url).text
    try:
        with open(f'{desktop}/ClonedWebsite.html','w+') as file:
            file.write(str(request))
            print("saved in : "+f'{desktop}/ClonedWebsite.html')
    except Exception as e:
        with open('ClonedWebsite.html','w+') as file:
            file.write(str(request))
            print("saved in : "+f'{os.getcwd()}ClonedWebsite.html')
except Exception as e:
    print(e)



s = socket.socket()# Create a socket object
ip = get('https://api.ipify.org').text
print("public IP : ",ip)
host = socket.getfqdn()
port = random.randint(9000,65000)
s.bind((host, port))        # Bind to the port

print ('Starting server on', host, port)
print ('The Web server URL for this would be http://%s:%d/' % (host, port))

s.listen(5)                 # Now wait for client connection.
all_threads = []
try:
    while True:
        print("Waiting for client")
        conn, addr = s.accept()
        print("Client:", addr)
        t = threading.Thread(target=Handler, args=(conn,))
        t.start()
        all_threads.append(t)
except KeyboardInterrupt:
    print("Stopped by Ctrl+C")
finally:
    if s:
        s.close()
    for t in all_threads:
        t.join()