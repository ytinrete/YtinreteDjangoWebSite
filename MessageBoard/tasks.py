from __future__ import absolute_import
from celery import task
from .models import VisitInfo
from bs4 import BeautifulSoup
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

import smtplib
import YtinretePythonServer.configs

import urllib.request
import urllib.parse
import urllib.error


def common_request_maker(path):
    if path:
        req = urllib.request.Request(path)
        req.add_header('User-Agent',
                       'Mozilla/5.0 (Linux; Android 4.4.4; Samsung Galaxy S4 - 4.4.4 - API 19 - 1080x1920 Build/KTU84P) '
                       + 'AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/33.0.0.0 Mobile Safari/537.36')
        req.add_header('X-Requested-With', 'com.android.browser')
        return req
    else:
        return None


def post(req, data):
    try:
        response = urllib.request.urlopen(req, data, timeout=10)
    except urllib.error.HTTPError as e:
        print(e)
        return
    res_str = str(response.read(), 'utf-8')

    return res_str


def get(req):
    return post(req, None)


@task
def search_req(time_str):
    if time_str is None or time_str == '':
        return
    try:
        for v in VisitInfo.objects.raw('SELECT * FROM MessageBoard_visitinfo WHERE TimeStr = %s', [time_str]):
            if v.Addr and v.Location == '':
                location = get_location2(v.Addr)
                if location is None:
                    location = get_location1(v.Addr)

                if location:
                    v.Location = location
                    v.save()  # just find first
                    break

    except BaseException as e:
        print(e)


def get_location1(ip):
    try:
        html_str = get(common_request_maker('http://whatismyipaddress.com/ip/' + ip))
        html_tree = BeautifulSoup(html_str, 'lxml')
        for meta in html_tree.head.select('meta'):
            if meta.get('name') == 'description':
                return meta.get('content')

    except BaseException as e:
        print(e)


def get_location2(ip):
    try:
        html_str = get(common_request_maker('http://www.ip.cn/index.php?ip=' + ip))
        html_tree = BeautifulSoup(html_str, 'lxml')
        for meta in html_tree.find_all("div", class_='well'):
            return meta.text

    except BaseException as e:
        print(e)


@task
def send_new_thread_mail(author, content):
    account = YtinretePythonServer.configs.MAIL_TASK_ACCOUNT
    passwd = YtinretePythonServer.configs.MAIL_TASK_PASSWD
    account_name = YtinretePythonServer.configs.MAIL_TASK_NAME
    to_name = YtinretePythonServer.configs.MAIL_TASK_TO_NAME
    to_addr = YtinretePythonServer.configs.MAIL_TASK_TO_ADDR

    msg = MIMEMultipart('alternative')
    msg["From"] = _format_addr(account_name + ('<%s>' % account))
    msg["To"] = _format_addr(to_name + ('<%s>' % to_addr))
    msg["Subject"] = Header('New Post Thread From ' + author, 'utf-8').encode()

    # 普通文本,alternative才能看得到,否则文本和html只能选一个
    msg.attach(MIMEText(author + ':' + content, "plain", "utf-8"))

    server = smtplib.SMTP("smtp.mailgun.org", 25)
    server.starttls()  # ssl
    # server.set_debuglevel(1)
    server.login(account, passwd)
    server.sendmail(account, [to_addr], msg.as_string())
    server.quit()


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))
