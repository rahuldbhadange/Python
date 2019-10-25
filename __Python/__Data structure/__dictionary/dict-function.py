data = dict(
    DATABASE='flaskr.db',
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
)
print(data)
for k, v in data.items():
    print(k, ":", v)
for k in data.keys():
    print(k)
for v in data.values():
    print(v)
