import requests, json, time
from pyquery import PyQuery as pq


class Client(object):
    index = "seats.lib.ecnu.edu.cn/web/seat3?area=40&segment=1403094"
    

    def __init__(self):
        super().__init__()
        self.date = "2020-12-22"
        self.startTime = "13:00"
        self.endTime = "22:00"
        self.url = self._concate()
        print(self.url)


    def _concate(self):
        return "http://" + self.index + \
            "&=" + self.date + \
            "&=" + self.startTime + \
            "&=" + self.endTime

        # http://seats.lib.ecnu.edu.cn/web/seat3?area=40&segment=1403094&day=2020-12-23&startTime=11:57&endTime=22:00
        # http://seats.lib.ecnu.edu.cn/web/seat3?area=40&segment=1403094&day=2020-12-23&startTime=12:54&endTime=22:00
        # http://seats.lib.ecnu.edu.cn/web/seat3?area=8&segment=1377791&day=2020-12-23&startTime=12:55&endTime=21:55
    
    def get_html(self):
        self.date = time.strftime("%Y-%m-%d", time.localtime())
        self.startTime = time.strftime("%H:%M", time.localtime())
        self.url = self._concate() 
        # + "api.php/spaces_old"
        print(self.url)
        r = requests.get(self.url)
        if r.ok:
            return r.text
        return None
    
    def get_seats(self):
        html = self.get_html()
        doc = pq(html)
        lis = doc('li')
        

        return 0

    
c = Client()
c.get_seats()