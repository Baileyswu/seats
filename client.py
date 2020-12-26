import requests, json, time, random
import logging
from ua import USER_AGENT_LIST

def init_log():
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
    
    def _update_time(self):
        self.data['day'] = time.strftime("%Y-%m-%d", time.localtime())
        self.data['startTime'] = time.strftime("%H:%M", time.localtime())

    def load_area(self):
        with open('./data/segment.json', 'r') as f: 
            area = json.load(f)
        print("choose area:")
        idx = 1
        for x in area['obj']:
            print(idx, x['areaname'])
            idx += 1
        val = input('input index of area (1-7) :')
        val = int(val)
        return area['obj'][val-1]

    def load_seat(self, area):
        print("loading seat at", time.strftime("%H:%M:%S", time.localtime()))
        self._update_time()
        
        self.data['area'] = area['area']
        self.data['segment'] = area['segment']
        self.headers['user-agent'] = random.choice(USER_AGENT_LIST)

        prefix = self.index + "/api.php/spaces_old"
        logging.info("request GET from " + prefix)
        school_data = requests.get(prefix, headers=self.headers, params=self.data)
        if school_data.status_code == 200:
            seats_data = school_data.content.decode('unicode_escape')
            logging.debug(seats_data)
        else:
            logging.error("load seat error code : ", school_data.status_code)
            return None
        seats_data = json.loads(seats_data)
        if seats_data['status'] == 1:
            return seats_data['data']['list']
        else:
            logging.warning("there is no space to order")
            return None
    
    def choose_empty(self, seats):
        if seats == None: return []
        empty = []
        used = [2, 6, 7]
        for x in seats: 
            status = x['status']
            if status not in used:
                empty.append((x['name'], x['status_name'], x['area_name']))
                logging.debug(x['name'], x['status_name'], x['area_name'], x['status'])
        if len(empty) == 0:
            logging.info("there is no space to order")
        return empty
    
   
if __name__ == "__main__":
    init_log()
    c = Client()
    empty_seats = []
    area = c.load_area()
    
    while len(empty_seats) == 0:
        seats = c.load_seat(area)
        empty_seats = c.choose_empty(seats)
        if len(empty_seats) == 0 : time.sleep(15)

    for x in empty_seats:
        print(x)
