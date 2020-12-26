import requests, json, time, random
import logging
from ua import USER_AGENT_LIST

logging.basicConfig(level=logging.INFO)

class Client(object):
    index = "http://seats.lib.ecnu.edu.cn"
    data = {
                'area': '40', 
                'segment': '1403094',
                'day': '2020-12-23',
                'startTime': '18:00',
                'endTime': '22:00',
            }
    headers = {
            'Host': 'seats.lib.ecnu.edu.cn',
            'Accept-Language': 'zh,zh-CN;q=0.9',
            'Referer': index,
            'X-Requested-With': 'XMLHttpRequest',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
        }

    def __init__(self):
        super().__init__()
        self.seat3 = self.index + '/web/seat3'

    def load_seat(self):
        print("loading seat at ", time.strftime("%H:%M:%S", time.localtime()))

        self.data['day'] = time.strftime("%Y-%m-%d", time.localtime())
        self.data['startTime'] = time.strftime("%H:%M", time.localtime())
        self.headers['user-agent'] = random.choice(USER_AGENT_LIST)

        prefix = self.index + "/api.php/spaces_old"
        logging.info("request GET from " + prefix)
        school_datas = requests.get(prefix, headers=self.headers, params=self.data)
        if school_datas.status_code == 200:
            seats_data = school_datas.content.decode('unicode_escape')
            logging.debug(seats_data)
        else:
            logging.error("load seat error code : ", school_datas.status_code)
            return None
        seats_data = json.loads(seats_data)
        if seats_data['status'] == 1:
            return seats_data['data']['list']
        else:
            logging.info("there is no space to order")
            return None
    
    def choose_empty(self, seats):
        empty = []
        used = [2, 6, 7]
        for x in seats: 
            status = x['status']
            if status not in used:
                empty.append((x['name'], x['status_name'], x['area_name'], x['status']))
        return empty
    
   
if __name__ == "__main__":
    c = Client()
    empty_seats = []
    while len(empty_seats) == 0:
        seats = c.load_seat()
        empty_seats = c.choose_empty(seats)
        if len(empty_seats) == 0 : time.sleep(15)
    print(empty_seats)
