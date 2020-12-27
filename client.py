import requests
import json
import time
import random
import logging
from ua import USER_AGENT_LIST


def init_log():
    formatter = '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.WARNING, format=formatter)


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
    token = {
        'access_token': '',
        'userid': '',
        'type': 1,
        'segment': ''
    }

    def __init__(self):
        super().__init__()
        self.seat3 = self.index + '/web/seat3'
        self.auto = str(input('auto booking? (y/n) : '))
        logging.debug(self.auto)

    def _update_time(self):
        self.data['day'] = time.strftime("%Y-%m-%d", time.localtime())
        self.data['startTime'] = time.strftime("%H:%M", time.localtime())

    def set_token(self):
        with open('./data/token.json', 'r') as f:
            access = json.load(f)
        self.token['access_token'] = access['access_token']
        self.token['segment'] = self.data['segment']
        self.token['userid'] = access['userid']
        self.token['type'] = access['type']

    def login(self):
        self._update_time()

        prefix = self.index + "/api.php/login"
        logging.info("request GET from " + prefix)
        try:
            school_data = requests.get(
                prefix, headers=self.headers, params=self.data)
        except Exception as e:
            logging.error(e)
            return None
        if school_data.status_code == 200:
            login_data = school_data.content.decode('unicode_escape')
            logging.debug(login_data)

    def load_area(self):
        with open('./data/segment.json', 'r') as f:
            area = json.load(f)
        print("choose area:")
        idx = 1
        for x in area['obj']:
            print(idx, x['areaname'])
            idx += 1
        val = ''
        val = input('input index of area (1-8) : ')
        if val == '':
            val = 2
        else:
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
        try:
            school_data = requests.get(
                prefix, headers=self.headers, params=self.data)
        except ConnectionError as e:
            logging.error("check your connection")
            return None
        except Exception as e:
            logging.error(e)
            return None
        if school_data.status_code == 200:
            seats_data = school_data.content.decode('unicode_escape')
            logging.debug(seats_data)
        else:
            logging.error("load seat error code : " +
                          str(school_data.status_code))
            return None

        seats_data = json.loads(seats_data)
        if seats_data['status'] == 1:
            return seats_data['data']['list']
        else:
            logging.warning("there is no space to order")
            return None

    def filter_empty(self, seats):
        if seats == None:
            return []
        empty = []
        used = [2, 3, 6, 7]
        for x in seats:
            status = x['status']
            if status not in used:
                empty.append((x['name'], x['status_name'],
                              x['area_name'], x['id']))
                logging.info(str(x['status']))
        if len(empty) == 0:
            logging.info("there is no space to order")
        return empty

    def book(self, seats):
        if self.token['access_token'] == '':
            logging.warning("no access token at login.json")
            return 1

        if self.auto == 'y':
            print("auto booking seat ...")
            id = random.choice(range(len(seats))) + 1
        else:
            id = input('input index of seat : ')
        if id == '':
            logging.warning("you give up")
            return 1
        else:
            id = int(id) - 1
            print("booking ", seats[id][0], seats[id][1], seats[id][2])
        if id < 0 or id >= len(seats):
            logging.error("choose exceeded seat id")
            return 1
        ids = seats[id][3]
        prefix = self.index + "/api.php/spaces/" + str(ids) + "/book"
        logging.info("request POST from " + prefix)
        try:
            school_data = requests.post(
                prefix, headers=self.headers, data=self.token, params=self.data)
        except Exception as e:
            logging.error(e)
            return 1
        if school_data.status_code == 200:
            msg = school_data.content
            logging.debug(msg)
        else:
            logging.error("load seat error code : " + str(school_data.status_code))
            return 1
        
        msg = json.loads(msg)
        if msg['status'] == 1:
            logging.info(msg['msg'].decode('unicode_escape'))
            print("book success!!! ", msg['data']['list']['starttime'])
            return 0
        else:
            logging.info(msg['msg'])
            print(msg['msg'])
            return 1

    def show(self, seats):
        idx = 1
        for x in seats:
            print(idx, ":", x[0], x[1], x[2])
            idx += 1

    def check_repeat(self):
        empty_seats = []
        while len(empty_seats) == 0:
            seats = self.load_seat(area)
            empty_seats = self.filter_empty(seats)
            if len(empty_seats) == 0:
                time.sleep(5)
        return empty_seats

if __name__ == "__main__":
    init_log()
    c = Client()
    area = c.load_area()
    c.set_token()
    empty_seats = c.check_repeat()
    c.show(empty_seats)
    c.book(empty_seats)
