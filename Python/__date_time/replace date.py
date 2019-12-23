import datetime

d1 = datetime.datetime.now()
print('d1:', d1)

d2 = d1.replace(year=2009)
print('d2:', d2)
date = d1.date()
d3 = date.replace(day=1)
print(d3)

end_plus = (datetime.datetime.strptime(str(d3), '%Y-%m-%d') + datetime.timedelta(days=31)).strftime('%Y-%m-%d')
end_plus = end_plus + "T00:00:00+00:00"
print(end_plus)