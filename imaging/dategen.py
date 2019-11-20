import datetime

year = 2019
month = 10
day = 18
hour = 17
minute = 0

now = datetime.datetime(year,month,day,hour,minute)
for i in range(6):
	now = now + datetime.timedelta(minutes=30)
	

	print(now.strftime("%Y%m%d%H%M"))
