'''
Created	on 2015-9-6

@author: opzoon
'''
import sys,os,time
import psutil
sys.path.append('..\public')
import LogConfig
import smtplib
import email.mime.multipart
import email.mime.text
import socket
Mylog=Mylog=LogConfig.Logger()
localIP = socket.gethostbyname(socket.gethostname())
flag=[]
def	getProcessInfo(proc):
	info={}
	try:
		info['cpu']=str(proc.cpu_percent(interval=2)) + "%"
		info['vms'] = proc.memory_info()[1] 
		info['name'] = proc.name()	
		info['pid']	= proc.pid	
	except psutil.NoSuchProcess:
		info['name'] = "Closed_Process"
		info['pid']	= 0
		info['vms']	= 0
		info['cpu']	= 0
	print(info['name'],info['pid'], info['vms']/2**20, info['cpu'])
	if float(info['cpu'][:2])==0.0:
		Mylog.logger.warn('%s_%s is Wrong,Memory:%s,CPU:%s'%(info['name'],info['pid'], info['vms']/2**20, info['cpu']))
		if info['pid'] not in flag:
			flag.append(info['pid'])
			content='''你好，IP:%(ip)s Name:%(name)s Pid:%(pid)s服务出现异常'''%{'ip':localIP,'name':info['name'],'pid':info['pid']}
			print(content)
			sendEmail(content)
	else:
		Mylog.logger.info('Name:%s,PID:%s,Memory:%s,CPU:%s'%(info['name'],info['pid'], info['vms']/2**20, info['cpu']))
def	getAllProcessInfo(p_name=None):	   
	instances =	[]
	all_processes =	list(psutil.process_iter())	
	if p_name is None:
		for	proc in	all_processes:
			getProcessInfo(proc)
	else:
		for	proc in	all_processes:
			try:
				if proc.name()==p_name:	
					getProcessInfo(proc)
			except psutil.NoSuchProcess:
				continue
				
	#print(instances)
	#return	instances
	
def sendEmail(content=''):
	msg=email.mime.multipart.MIMEMultipart()
	sendTo=["wangluqiang@opzoon.com",'wujingjing@opzoon.com','shijingnan@opzoon.com','zhangqunqun@opzoon.com','yangjunxiang@opzoon.com']
	#sendTo=['532525592@qq.com']
	msg['from']="opzoon_frs_test@126.com"
	msg['to']=','.join(sendTo)
	msg['subject']='警告'

	#content='''
	#	你好，比对服务出现异常！
	#'''

	txt=email.mime.text.MIMEText(content)
	msg.attach(txt)

	try:
		smtp=smtplib.SMTP()
		smtp.connect('smtp.126.com')
		smtp.login('opzoon_frs_test','pmbfzpanmiqjyias')
		smtp.sendmail('opzoon_frs_test@126.com',sendTo,msg.as_string())
		smtp.quit()
	except Exception as e:
		print(str(e))
		
if __name__	== "__main__":
	while 1:		
		getAllProcessInfo('EditPlus.exe')
		time.sleep(600)
