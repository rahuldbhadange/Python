import datetime

_d = "2019-06-04T06:27:35.000077+00:00"

# _datetime = datetime.datetime.now()     # 2019-06-05 13:26:49.615872
# datetime.timezone.
_datetime = datetime.datetime.now()     # 2019-06-05 07:58:27.569693
# _date = _d.isoformat     # 2019-06-05 07:58:27.569693
print(_datetime)

date = _datetime.date()
print(date)

time = _datetime.time()
print(time)


# new_date = date.fromisoformat("ddmmyyyy")
# new_date = date.isoformat()     # 2019-06-05
day = str(date.day)
print(day)

month = str(date.month)
print(month)
# print("fygh", month, "T00:00:00+00:00")

year = str(date.year)
print(year)

new_date = day + "." + month + "." + year
print(new_date)

# important: padding
new_date = str("{:0>2d}".format(_datetime.day)) + "." + str(_datetime.month) + "." + str(_datetime.year)
print(new_date)
# formatted_date = event.time.strftime("%d.%m.%Y")

formatted_date = _datetime.strftime("%d.%m.%Y")
print("formatted_date", formatted_date)

# 5	{:0>2d}	05	Pad number with zeros (left padding, width 2)

num = 10

print("{:0>2d}".format(num))
