import requests, json, time
from pyquery import PyQuery as pq
from urllib.parse import urlencode
from ua import USER_AGENT_LIST
import random

class Client(object):
    index = "http://seats.lib.ecnu.edu.cn"

    def __init__(self):
        super().__init__()
        self.data = {
            'area': '40', 
            'segment': '1403094',
            'day': '2020-12-23',
            'startTime': '18:00',
            'endTime': '22:00',
        }
        self.url = self.index + '/web/seat3'

    def _concate(self, prefix, data):
       return prefix + '?' + urlencode(data)

        # http://seats.lib.ecnu.edu.cn/web/seat3?area=40&segment=1403094&day=2020-12-23&startTime=11:57&endTime=22:00
        # http://seats.lib.ecnu.edu.cn/web/seat3?area=40&segment=1403094&day=2020-12-23&startTime=12:54&endTime=22:00
        # http://seats.lib.ecnu.edu.cn/web/seat3?area=8&segment=1377791&day=2020-12-23&startTime=12:55&endTime=21:55
    
    def get_html(self):
        self.data['day'] = time.strftime("%Y-%m-%d", time.localtime())
        self.data['startTime'] = time.strftime("%H:%M", time.localtime())
        url = self._concate(self.url, self.data)
        r = requests.get(url)
        if r.ok:
            return r.text
        return None
    
    def load_seat(self):
        self.data['day'] = time.strftime("%Y-%m-%d", time.localtime())
        self.data['startTime'] = time.strftime("%H:%M", time.localtime())
        prefix = self.index + "/api.php/spaces_old"
        USER_AGENT = random.choice(USER_AGENT_LIST)
        headers = {'user-agent': USER_AGENT}
        url = self._concate(prefix, self.data)
        school_datas = requests.get(url, headers=headers)
        print(school_datas.content.decode('unicode_escape'))
        return school_datas
    
    def get_seats(self):
        html = self.get_html()
        doc = pq(html)
        lis = doc('li')
        

        return 0
   
if __name__ == "__main__":
    c = Client()
    c.load_seat()
    c.get_seats()
