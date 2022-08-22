#coding=utf-8
import socket,os,sys,win32gui
from time import sleep
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import *

import colorama 
from colorama import Fore,Back,Style
colorama.init(autoreset=False)
os.system("title capt")

#请在此输入窗口名
w='任务管理器'

def local_ip():

	hostname = socket.gethostname()
	# 获取本机内网ip
	local_ip = ''.join(socket.gethostbyname_ex(hostname)[-1])

	return local_ip

app = QApplication(sys.argv)
screen = QApplication.primaryScreen()

path=sys.path[0]
os.chdir(path)

FailsafeMap=['None','未能找到程序']
print (Fore.YELLOW +'|'+'X'*len(os.getcwd()),'INFO','X'*len(os.getcwd()))
print(Fore.GREEN+'|','工作目录   -',os.getcwd())
print(Fore.GREEN+'|','本机内网ip -',local_ip())
print('\n')
def capture():
	hwnd = win32gui.FindWindow(None, w)#Handle of Window
	global Failsafe
	Failsafe=0
	if hwnd==0:
		Failsafe=1
	elif hwnd!=0:
		img = screen.grabWindow(hwnd,0,0).toImage()
		img.save("capt.jpg")
		file = open('capt.jpg', 'rb')
		global content
		content = file.read()
		file.close()

 
def main():
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)#创建一个服务器socket监听
	sock.bind((local_ip(),2333))
	sock.listen(5)#设置最大监听数
	while True:
		#sleep(0.2)
		conn,address = sock.accept()#接受浏览器请求
		request = conn.recv(1024)
		capture()
		if Failsafe!=0:
			print(Fore.BLUE+Back.WHITE+'\n>'+'a clinet from','-',Fore.BLUE+str(address[0]) +":"+ str(address[1]))
			print(Fore.RED+Back.WHITE+'! Failsafe -',FailsafeMap[Failsafe])
			conn.send(b'HTTP/1.1 200 Failsafe\r\n')
			conn.send(b'Content-Type: text/html; charset=utf-8\r\n\r\n')
			b1 = bytes(FailsafeMap[Failsafe],'UTF-8')
			b2=b'<p>'+b1+b'</>'
			conn.send(b2)
		else:
			try:
				conn.send(b'HTTP/1.1 200 OK\r\n')
				conn.send(b'Content-Type:image/jpg\r\n\r\n')
				conn.sendall(content)
				print(Fore.BLUE+Back.WHITE+'\n>'+'a clinet from','-',Fore.BLUE+str(address[0]) +":"+ str(address[1]))
				conn.close()
			except:
				conn.close()
		
while True:
	while True:
		main()