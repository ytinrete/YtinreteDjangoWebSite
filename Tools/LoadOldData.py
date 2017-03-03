import json
from MessageBoard.models import Thread
import datetime
import MessageBoard.kittycode
import pytz


# python3 manage.py shell
# import Tools.LoadOldData
# Tools.LoadOldData.load_old()

def load_old():
    with open("data.txt", "r") as f:
        content = f.readlines()
        count = 0
        content = content[-20:]
        tz = pytz.timezone('Asia/Shanghai')
        for line in content:
            # print(line)
            obj = json.loads(line.rstrip('\n'))

            t = Thread()
            t.Author = obj['Author']
            index = obj['Content'].find('_imgUpload_')
            if index > 0:
                tmpContent = obj['Content'][0:index]
                tmpImg = obj['Content'][index + 11:]
            else:
                tmpContent = obj['Content']
                tmpImg = ''

            t.Content = tmpContent
            t.ContentEncode = MessageBoard.kittycode.encode(tmpContent)
            t.ImageUpload = tmpImg
            t.Timestamp = int(obj['Time'])
            t.TimeStr = datetime.datetime.fromtimestamp(int(t.Timestamp),
                                                        tz=tz).strftime('%Y-%m-%d %H:%M:%S')
            # t.Time = datetime.datetime.fromtimestamp(int(obj['Time']))
            t.save()
            count += 1

    print(count)


if __name__ == "__main__":
    load_old()
