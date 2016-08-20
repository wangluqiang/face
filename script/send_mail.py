#coding=utf-8
import smtplib,os,sys,time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
cur_path = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(cur_path+'\\..\\public')
import Config

#=============定义发送邮件==========
def send_mail(file_new):
    cfg = Config.Config()
    #发信邮箱
    mail_from= cfg.mail_from_info()
    #收信邮箱
    mail_to = cfg.mail_to_info()
    mail_to_user = ','.join(mail_to)
    #定义正文
    
    #添加附件
    msg = MIMEMultipart('related')
    #构造附件
    att = MIMEText(open("1.rar", 'rb').read(), 'utf-8')
    att["Content-Type"] = 'application/octet-stream'
    att["Content-Disposition"] = 'attachment; filename="1.rar"'
    msg.attach(att)
    
    #msg = MIMEText("hello", _subtype='text',_charset='utf-8')
    #定义标题
    msg['Subject']=u"自动化测试报告"
    #定义发送时间（不定义的可能有的邮件客户端会不显示发送时间）
    msg['date']=time.strftime('%a, %d %b %Y %H:%M:%S %z')
    #
    msg['From'] = "opzoon_frs_test@126.com"
    msg['to'] = "opzoon_frs_test@126.com"
    smtp=smtplib.SMTP()
    #连接 SMTP 服务器
    smtp.connect('smtp.126.com')
    #用户名密码
    smtp.login("opzoon_frs_test","pmbfzpanmiqjyias")
    smtp.sendmail("opzoon_frs_test@126.com","wujingjing@opzoon.com",msg.as_string())
    smtp.quit()
    print('email has send out !')
    
if __name__ == "__main__":
    send_mail("1.rar")
