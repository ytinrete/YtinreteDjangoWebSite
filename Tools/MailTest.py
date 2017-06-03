import YtinretePythonServer.configs
from email import encoders
from email.header import Header
from email.mime.multipart import MIMEMultipart, MIMEBase
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

import smtplib


def send_mail(subject, content):
    account = YtinretePythonServer.configs.MAIL_TASK_ACCOUNT
    passwd = YtinretePythonServer.configs.MAIL_TASK_PASSWD
    account_name = YtinretePythonServer.configs.MAIL_TASK_NAME
    to_name = YtinretePythonServer.configs.MAIL_TASK_TO_NAME
    to_addr = YtinretePythonServer.configs.MAIL_TASK_TO_ADDR

    msg = MIMEMultipart('alternative')
    msg["From"] = _format_addr(account_name + ('<%s>' % account))
    msg["To"] = _format_addr(to_name + ('<%s>' % to_addr))
    msg["Subject"] = Header(subject, 'utf-8').encode()

    # 普通文本,alternative才能看得到,否则文本和html只能选一个
    msg.attach(MIMEText(content, "plain", "utf-8"))

    server = smtplib.SMTP("smtp.mailgun.org", 25)
    server.starttls()  # ssl
    server.set_debuglevel(1)
    server.login(account, passwd)
    server.sendmail(account, [to_addr], msg.as_string())
    server.quit()


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


if __name__ == '__main__':
    send_mail('sub', "lalala")

    pass
