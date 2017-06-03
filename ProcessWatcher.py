import Tools.MailTest
import time
from subprocess import Popen, PIPE


class ProcessWatcher(object):
    def __init__(self):
        self.__duration = 60 * 3  # 3min
        self.__uwsgi_die = False
        self.__celery_die = False
        pass

    def set_duration(self, duration):
        self.__duration = duration
        return self

    def should_end_running(self):
        return self.__uwsgi_die and self.__celery_die

    def run(self):
        while (True):
            plist = self.get_running_process_list()
            if plist:
                self.check_uwsgi(plist)
                self.check_celery(plist)
                if self.should_end_running():
                    break
                time.sleep(self.__duration)

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
            print(e)


if __name__ == '__main__':
    ProcessWatcher().run()
