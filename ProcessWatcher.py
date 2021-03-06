import Tools.MailTest
import time
import datetime
from subprocess import Popen, PIPE


class ProcessWatcher(object):
    def __init__(self):
        self.__duration = 60 * 3  # 3min
        self.__uwsgi_die = False
        self.__celery_die = False
        self.__ss_die = False
        pass

    def set_duration(self, duration):
        self.__duration = duration
        return self

    def should_end_running(self):
        return self.__uwsgi_die and self.__celery_die

    def run(self):
        while (True):
            try:
                plist = self.get_running_process_list()
                if plist:
                    self.check_uwsgi(plist)
                    self.check_celery(plist)
                    self.check_ss(plist)
                    if self.should_end_running():
                        print("exit in peace 0v0~", flush=True)
                        break
                else:
                    print("Popen error, this might be the reason", flush=True)
                print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'), flush=True)
                time.sleep(self.__duration)
            except BaseException as e:
                print(e, flush=True)

    def check_uwsgi(self, plist):
        if self.__uwsgi_die == False:
            if self.check_process_exist(plist, 'uwsgi'):
                print('uwsgi alive!')
            else:
                Tools.MailTest.send_mail('uwsgi die!', 'QAQ!')
                print('uwsgi die!')
                self.__uwsgi_die = True

    def check_celery(self, plist):
        if self.__celery_die == False:
            if self.check_process_exist(plist, 'celery'):
                print('celery alive!')
            else:
                Tools.MailTest.send_mail('celery die!', 'QAQ!')
                print('celery die!')
                self.__celery_die = True

    def check_ss(self, plist):
        if self.__ss_die == False:
            if self.check_process_exist(plist, 'ssserver'):
                print('ssserver alive!')
            else:
                Tools.MailTest.send_mail('ssserver die!', 'QAQ!')
                print('ssserver die!')
                self.__ss_die = True

    def check_process_exist(self, plist, target):
        found = False
        for line in plist:
            if line.find(target) != -1:
                found = True
                break
        return found

    def get_running_process_list(self):
        try:
            process = Popen(['ps', 'aux'], stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()
            return str(stdout, encoding='utf-8').splitlines()
        except BaseException as e:
            print(e, flush=True)


if __name__ == '__main__':
    ProcessWatcher().run()
