# 好好学习，天天占座

富强民主，文明和谐。

每隔 10 秒自动刷新出空闲座位。

## 使用方法

```sh
git clone git@github.com:Baileyswu/seats.git
cd seats
python3 -m venv seatenv
source seatenv/bin/activate
pip install requests
python client.py
```

## 查座成功界面

```
(seatenv) user@hosts Seats % python client.py
choose area:
1 一楼A区
2 一楼B区
3 一楼数字阅览室
4 一楼自习区
5 4A
6 4B
7 4C
input index of area (1-7) : 5
loading seat at 15:37:39
('002', '空闲', '中文文科图书借阅区4A(H-I)')
('023', '空闲', '中文文科图书借阅区4A(H-I)')
('034', '空闲', '中文文科图书借阅区4A(H-I)')
('042', '空闲', '中文文科图书借阅区4A(H-I)')
```